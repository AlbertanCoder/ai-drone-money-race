"""Build the one-screen front page: one chart, three numbers, five moments.

This is the page the site opens on. It deliberately has no controls, no
client-side JavaScript and no dependencies - the SVG is generated here in
Python and written as plain markup.

The long version (chapters, use cases, Alberta, careers, quiz, full table)
still exists; build_dashboard.py produces it as full.html.
"""
import math
import pathlib

import chart_data as cd

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "index.html"

# --- geometry ---------------------------------------------------------------
W, H = 1200, 560
L, R, T, B = 80, 118, 56, 54
PW, PH = W - L - R, H - T - B
X0, X1 = 1997.0, 2107.0
Y0, Y1 = 0.03, 30000.0

C = {"ai": "#2563eb", "dr": "#d97706", "aid": "#7c3aed",
     "hist": "#1e293b", "proj": "#b45309", "line": "#e2e8f0", "shade": "#fff7ed"}
TXT = {"ai": "#2563eb", "dr": "#b45309", "aid": "#7c3aed"}   # text-safe variants

SERIES = [("ai", "AI", cd.AI), ("dr", "Drones", cd.DRONES), ("aid", "AI Drones", cd.AI_DRONES)]


def xp(year):
    return L + (year - X0) / (X1 - X0) * PW


def yp(v):
    v = max(v, Y0)
    f = (math.log10(v) - math.log10(Y0)) / (math.log10(Y1) - math.log10(Y0))
    return T + PH - f * PH


def val_at(k, year):
    """Series value at any year, log-interpolated along the drawn segment."""
    vals = {"ai": cd.AI, "dr": cd.DRONES, "aid": cd.AI_DRONES}[k]
    yrs = list(cd.YEARS)
    for i in range(1, len(yrs)):
        if yrs[i] >= year:
            t = (year - yrs[i - 1]) / (yrs[i] - yrs[i - 1])
            return math.exp(math.log(vals[i - 1])
                            + t * (math.log(vals[i]) - math.log(vals[i - 1])))
    return float(vals[-1])


def money(v):
    if v >= 1000:
        return f"${v / 1000:.1f}T"
    if v >= 10:
        return f"${v:.0f}B"
    if v >= 1:
        return f"${v:g}B"
    if v >= 0.01:
        return f"${v * 1000:.0f}M"
    return f"${v * 1000:.1f}M"


def axis_money(v):
    if v >= 1000:
        return f"${v / 1000:g}T"
    if v >= 1:
        return f"${v:g}B"
    return f"${v * 1000:g}M"


def poly(vals, start, end):
    pts = [f"{xp(cd.YEARS[i]):.1f},{yp(vals[i]):.1f}" for i in range(start, end + 1)]
    return "M" + " L".join(pts)


def band_poly(k):
    lo, hi = cd.BAND[k]
    i0 = cd.LAST_REAL_IDX
    up = [(xp(cd.YEARS[i]), yp(hi[i])) for i in range(i0, len(cd.YEARS))]
    dn = [(xp(cd.YEARS[i]), yp(lo[i])) for i in range(len(cd.YEARS) - 1, i0 - 1, -1)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in up + dn)
    return f'<polygon points="{pts}" fill="{C[k]}" opacity=".13"/>'


def note(year, value, dx, dy, anchor, lines, k, bold=False):
    """A dot on a real data point plus a short label with a white halo."""
    x, y = xp(year), yp(value)
    cls = "nlab b" if bold else "nlab"
    spans = "".join(
        f'<tspan x="{x + dx:.1f}" dy="{0 if i == 0 else 15}">{ln}</tspan>'
        for i, ln in enumerate(lines)
    )
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#fff" '
            f'stroke="{C[k]}" stroke-width="2"/>'
            f'<text class="{cls}" x="{x + dx:.1f}" y="{y + dy:.1f}" fill="{TXT[k]}" '
            f'text-anchor="{anchor}">{spans}</text>')


def cross(year_index):
    """Log-space interpolation of where AI drones overtake conventional drones."""
    i = year_index
    a0, a1 = cd.AI_DRONES[i - 1], cd.AI_DRONES[i]
    b0, b1 = cd.DRONES[i - 1], cd.DRONES[i]
    t = (math.log(b0) - math.log(a0)) / (
        (math.log(a1) - math.log(a0)) - (math.log(b1) - math.log(b0)))
    year = cd.YEARS[i - 1] + (cd.YEARS[i] - cd.YEARS[i - 1]) * t
    val = math.exp(math.log(a0) + t * (math.log(a1) - math.log(a0)))
    return year, val


def build_svg():
    i0 = cd.LAST_REAL_IDX
    last = len(cd.YEARS) - 1
    o = []

    # scenario backdrop
    o.append(f'<rect x="{xp(cd.HISTORICAL_END):.1f}" y="{T}" '
             f'width="{L + PW - xp(cd.HISTORICAL_END):.1f}" height="{PH}" fill="{C["shade"]}"/>')

    # y gridlines + labels
    for v in (0.1, 1, 10, 100, 1000, 10000):
        y = yp(v)
        o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L + PW}" y2="{y:.1f}" '
                 f'stroke="{C["line"]}" stroke-width="1"/>')
        o.append(f'<text class="tick" x="{L - 12}" y="{y + 4:.1f}" '
                 f'text-anchor="end">{axis_money(v)}</text>')

    # x labels
    for year in range(2000, 2101, 20):
        o.append(f'<text class="tick" x="{xp(year):.1f}" y="{T + PH + 26}" '
                 f'text-anchor="middle">{year}</text>')

    # uncertainty fans sit behind their lines
    for k, _n, _v in SERIES:
        o.append(band_poly(k))

    # solid + dots to 2025, dashed after
    for k, _n, vals in SERIES:
        o.append(f'<path d="{poly(vals, 0, i0)}" fill="none" stroke="{C[k]}" '
                 f'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
        o.append(f'<path d="{poly(vals, i0, last)}" fill="none" stroke="{C[k]}" '
                 f'stroke-width="2.4" stroke-dasharray="7 5" stroke-linejoin="round"/>')
        for i in range(0, i0 + 1):
            o.append(f'<circle cx="{xp(cd.YEARS[i]):.1f}" cy="{yp(vals[i]):.1f}" r="3.6" '
                     f'fill="{C[k]}" stroke="#fff" stroke-width="1.3"/>')

    # end labels
    for k, _n, vals in SERIES:
        o.append(f'<text class="endval" x="{L + PW + 12}" y="{yp(vals[last]) + 5:.1f}" '
                 f'fill="{TXT[k]}">{money(vals[last])}</text>')

    # No in-chart labels. The five moments below the chart carry the narrative,
    # and every label that tried to live here collided with another series or
    # another label. The chart's job is the shape, not the commentary.
    pass

    # frame + captions
    o.append(f'<line x1="{L}" y1="{T + PH}" x2="{L + PW}" y2="{T + PH}" stroke="#cbd5e1"/>')
    o.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T + PH}" stroke="#cbd5e1"/>')
    o.append(f'<text class="cap" x="{L + 4}" y="{T - 16}">ESTIMATED, NOT SOURCED</text>')
    o.append(f'<text class="cap" x="{xp(cd.HISTORICAL_END) + 12:.1f}" y="{T - 16}">SCENARIO</text>')
    o.append(f'<text class="tick" x="{L + PW}" y="{T + PH + 46}" text-anchor="end">'
             f'solid + dots = estimate \u00b7 dashed + shading = scenario</text>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Line chart of global annual investment in AI, conventional drones '
            f'and AI drones from 2000 to 2100">' + "".join(o) + "</svg>")


def build_stats():
    i0, last = cd.LAST_REAL_IDX, len(cd.YEARS) - 1
    peak = float(cd.DRONES.max())
    peak_yr = cd.YEARS[cd.DRONES.tolist().index(peak)]
    rows = [
        ("ai", "AI", cd.AI[i0], cd.AI[last], f"by {cd.YEARS[last]}"),
        ("dr", "Drones", cd.DRONES[i0], peak,
         f"peak in {peak_yr} \u00b7 then {money(cd.DRONES[last])} by {cd.YEARS[last]}"),
        ("aid", "AI Drones", cd.AI_DRONES[i0], cd.AI_DRONES[last], f"by {cd.YEARS[last]}"),
    ]
    return '<div class="stats">' + "".join(
        f'<div class="stat" style="--c:{C[k]}">'
        f'<div class="k">{name}</div>'
        f'<div class="now">{money(now)} in {cd.YEARS[i0]}</div>'
        f'<div class="v">{money(end)}</div>'
        f'<div class="n">{sub}</div></div>'
        for k, name, now, end, sub in rows) + "</div>"


MOMENTS = [
    ("2012", "AlexNet wins ImageNet", "Deep learning starts beating everything else.", "ai"),
    ("2022", "ChatGPT launches", "AI becomes a product, not a paper.", "ai"),
    ("2023", "NVIDIA crosses $1T", "The market prices the compute.", "ai"),
    ("2025", "AI capex supercycle", "Hyperscaler spend at record levels.", "dr"),
    ("2027", "Autonomy overtakes", "AI drones outspend conventional drones.", "aid"),
]


def build_moments():
    return "".join(
        f'<li style="--c:{C[k]}"><b>{yr}</b><span class="t">{t}</span>'
        f'<span class="d">{d}</span></li>'
        for yr, t, d, k in MOMENTS)


PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Money Race &mdash; AI vs Drones vs AI Drones, 2000&ndash;2100</title>
<meta name="description" content="One chart of global annual investment in AI, conventional drones and AI drones from 2000 to 2100. Estimates to 2025, scenario after.">
<style>
  :root{--ink:#0f172a;--mute:#475569;--line:#e2e8f0;--bg:#f1f5f9;--card:#fff;
        --ai:#2563eb;--dr:#d97706;--aid:#7c3aed;--proj:#b45309}
  *,*::before,*::after{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-size:16px;line-height:1.55;
       font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       -webkit-font-smoothing:antialiased}
  .wrap{max-width:1180px;margin:0 auto;padding:44px 24px 56px}
  .eyebrow{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.16em;
           text-transform:uppercase;color:var(--proj);background:#fff7ed;
           border:1px solid #fed7aa;border-radius:999px;padding:5px 13px}
  h1{font-size:clamp(26px,3.4vw,42px);line-height:1.1;letter-spacing:-.022em;
     margin:16px 0 10px;font-weight:800}
  h1 .a{color:var(--ai)} h1 .b{color:var(--proj)} h1 .c{color:var(--aid)}
  .lede{font-size:17px;max-width:68ch;color:var(--mute);margin:0}
  .stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:26px 0 18px}
  .stat{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--c);
        border-radius:12px;padding:14px 16px}
  .stat .k{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
  .stat .now{font-size:12px;font-weight:700;color:var(--mute);margin-top:6px;
             font-variant-numeric:tabular-nums}
  .stat .v{font-size:27px;font-weight:800;letter-spacing:-.025em;font-variant-numeric:tabular-nums}
  .stat .n{font-size:12px;color:var(--mute);font-variant-numeric:tabular-nums}
  figure{background:var(--card);border:1px solid var(--line);border-radius:14px;
         margin:0;padding:18px 18px 10px}
  svg{display:block;width:100%;height:auto}
  svg .tick{font-size:12px;fill:var(--mute);font-variant-numeric:tabular-nums}
  svg .cap{font-size:10.5px;font-weight:800;letter-spacing:.12em;fill:var(--proj)}
  svg .endval{font-size:14px;font-weight:800;font-variant-numeric:tabular-nums}
  svg .nlab{font-size:14px;font-weight:600;stroke:#fff;stroke-width:4;paint-order:stroke}
  svg .nlab.b{font-weight:800}
  .key{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;font-weight:700;
       color:var(--mute);margin:0 2px 10px}
  .key span{display:inline-flex;align-items:center;gap:7px}
  .key span::before{content:"";width:10px;height:10px;border-radius:3px;background:var(--c)}
  figcaption{font-size:13px;color:var(--mute);margin:8px 2px 4px}
  h2{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);
     margin:34px 0 10px;font-weight:800}
  ol.moments{list-style:none;margin:0;padding:0;background:var(--card);border:1px solid var(--line);
             border-radius:14px;overflow:hidden}
  ol.moments li{display:grid;grid-template-columns:70px 1fr;gap:2px 14px;padding:12px 18px;
                border-top:1px solid var(--line);border-left:4px solid var(--c)}
  ol.moments li:first-child{border-top:0}
  ol.moments b{grid-row:span 2;font-size:15px;font-variant-numeric:tabular-nums}
  ol.moments .t{font-weight:800}
  ol.moments .d{font-size:13.5px;color:var(--mute)}
  footer{margin-top:28px;font-size:13px;color:var(--mute);display:flex;gap:14px;
         justify-content:space-between;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:16px}
  footer span{max-width:62ch}
  a{color:#2563eb;font-weight:700;text-decoration:none;white-space:nowrap}
  a:hover{text-decoration:underline}
  :focus-visible{outline:3px solid #2563eb;outline-offset:2px;border-radius:4px}
  @media(max-width:640px){
    .stats{grid-template-columns:1fr}
    .wrap{padding:28px 16px 40px}
    svg .nlab{font-size:17px} svg .tick{font-size:14px} svg .endval{font-size:16px}
    svg .cap{font-size:12px}
  }
  @media print{
    body{background:#fff}
    .wrap{padding:0;max-width:none}
    ol.moments,figure{break-inside:avoid}
    a{color:inherit}
  }
</style>
</head>
"""


PAGE_BODY = """<body>
<div class="wrap">
  <span class="eyebrow">Illustrative model &middot; not a forecast</span>
  <h1>The Money Race: <span class="a">AI</span> vs <span class="b">Drones</span> vs <span class="c">AI Drones</span></h1>
  <p class="lede">Global annual investment, 2000&nbsp;&rarr;&nbsp;2100. AI compounds toward
     $10.9T a year. Conventional drones peak at $75B in 2045, then lose the field to autonomy.</p>

  %STATS%

  <figure>
    <div class="key">
      <span style="--c:#2563eb">AI</span>
      <span style="--c:#d97706">Conventional drones</span>
      <span style="--c:#7c3aed">AI drones</span>
    </div>
    %SVG%
    <figcaption>Log scale &mdash; equal vertical distance means the same multiple, not the same
      dollar amount. The two lower lines cross in 2027. Solid lines with dots are estimates;
      dashed lines and the shaded band are a scenario, not a forecast.</figcaption>
  </figure>

  <h2>Five moments that moved the curve</h2>
  <ol class="moments">%MOMENTS%</ol>

  <footer>
    <span>2000&ndash;2025 are order-of-magnitude estimates, not sourced statistics.
      2025&ndash;2100 is a scenario; the shaded band is an illustrative spread, not a
      confidence interval.</span>
    <a href="full.html">Chapters, use cases, Alberta, careers &rarr;</a>
  </footer>
</div>
</body>
</html>
"""


def main():
    html = (PAGE_HEAD + PAGE_BODY)
    html = (html.replace("%STATS%", build_stats())
                .replace("%SVG%", build_svg())
                .replace("%MOMENTS%", build_moments()))
    OUT.write_text(html, encoding="utf-8")
    print(f"saved -> {OUT.name}")
    print(f"        {OUT.stat().st_size / 1024:,.0f} KB  |  zero JavaScript  |  "
          f"{len(MOMENTS)} moments  |  {len(html.split())} words")


if __name__ == "__main__":
    main()




