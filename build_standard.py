"""Build the standard view: the chart plus the context a newcomer needs.

Three numbers, one chart, three acts, six uses, three Alberta facts. Static
SVG generated in Python; no client JavaScript, no controls.

Reuses the geometry, palette and chart from build_simple so the two pages can
never drift apart.
"""
import pathlib

import build_simple as bs
import chart_data as cd

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "index.html"

# --- three acts -------------------------------------------------------------
ACTS = [
    ("2000&ndash;2015", "Foundations", "ai",
     "AI was a research line item and drones were military or hobby hardware. "
     "Then AlexNet won ImageNet in 2012 and the field stopped assuming it had hit a wall."),
    ("2016&ndash;2025", "The inflection", "ai",
     "Transformers, then ChatGPT, turned models into products. Drones became both a consumer "
     "commodity and the defining weapon of a European war. AI spend alone goes "
     "$120B &rarr; $410B in these ten years."),
    ("2026&ndash;2100", "Autonomy", "aid",
     "The scenario: AI drones outspend conventional ones in 2027, conventional drones fade to a "
     "niche, and AI growth slows to a plateau rather than compounding forever."),
]

# --- six uses ---------------------------------------------------------------
USES = [
    ("Delivery", "ai",
     "Amazon Prime Air, DoorDash &times; Wing and Walmart &times; Wing fly groceries and takeaway "
     "to the door in about 30 minutes."),
    ("Health", "aid",
     "Zipline has parachuted blood and vaccines into clinics in Rwanda since 2016; Matternet moves "
     "lab samples between Swiss hospitals."),
    ("Farming", "dr",
     "Spraying and crop-scouting drones cover huge acreage with less chemical. Low margins plus "
     "big fields is exactly where the economics work."),
    ("Defence", "aid",
     "Cheap FPV reconnaissance drones became the most consequential weapon of a modern war, and "
     "budgets everywhere were replanned around that."),
    ("Industry", "dr",
     "Bridges, turbines and pipelines inspected without scaffolding or rope access. The unglamorous, "
     "profitable core of the industry."),
    ("On the ground", "ai",
     "Waymo robotaxis run the same perception-and-decide stack that flies a drone. The skills "
     "transfer between them."),
]

# --- three Alberta facts ----------------------------------------------------
ALBERTA = [
    ("Amii, Edmonton", "2002",
     "One of Canada&rsquo;s three national AI institutes, founded as the Alberta Ingenuity Centre "
     "for Machine Learning. Richard Sutton&rsquo;s reinforcement-learning group made Edmonton a "
     "serious AI city long before AI was a household word."),
    ("Foremost UAS Test Range", "2015",
     "Over 700 square nautical miles of restricted prairie airspace, used for beyond-visual-line-of-"
     "sight testing. Alberta&rsquo;s biggest physical asset in civilian drone work."),
    ("Meta data centre, Sturgeon County", "2026",
     "More than C$13 billion for a 1&nbsp;GW campus, Meta&rsquo;s first in Canada. The pitch is "
     "simple: cheap, reliable power and land for AI compute."),
]


def build_acts():
    return '<div class="acts">' + "".join(
        f'<div class="act" style="--c:{bs.C[k]}">'
        f'<div class="yr">{yr}</div><div class="nm">{name}</div>'
        f'<p>{text}</p></div>'
        for yr, name, k, text in ACTS) + "</div>"


def build_uses():
    return '<ul class="uses">' + "".join(
        f'<li style="--c:{bs.C[k]}"><b>{name}</b><span>{text}</span></li>'
        for name, k, text in USES) + "</ul>"


def build_alberta():
    return '<ul class="uses">' + "".join(
        f'<li style="--c:{bs.C["aid"]}"><b>{name}<em>{yr}</em></b><span>{text}</span></li>'
        for name, yr, text in ALBERTA) + "</ul>"


EXTRA_CSS = """
  h2.sect{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);
    margin:36px 0 12px;font-weight:800}
  .acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
  .act{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--c);
       border-radius:12px;padding:15px 17px}
  .act .yr{font-size:11.5px;font-weight:800;letter-spacing:.08em;color:var(--mute)}
  .act .nm{font-size:17px;font-weight:800;margin:3px 0 6px;letter-spacing:-.01em}
  .act p{margin:0;font-size:14px;line-height:1.5;color:#334155}
  ul.uses{list-style:none;margin:0;padding:0;background:var(--card);border:1px solid var(--line);
          border-radius:14px;overflow:hidden}
  ul.uses li{display:grid;gap:2px;padding:13px 18px;border-top:1px solid var(--line);
             border-left:4px solid #cbd5e1}
  ul.uses li:first-child{border-top:0}
  ul.uses b{font-size:14.5px;display:flex;gap:10px;align-items:baseline}
  ul.uses b em{font-style:normal;font-weight:700;font-size:11.5px;color:var(--mute)}
  ul.uses span{font-size:13.5px;line-height:1.5;color:var(--mute)}
  footer .links{display:flex;flex-direction:column;gap:6px;align-items:flex-start}
  footer .links a{white-space:normal}
  @media(max-width:900px){.acts{grid-template-columns:1fr}}
"""


BODY = """<body>
<div class="wrap">
  <span class="eyebrow">Illustrative model &middot; not a forecast</span>
  <h1>The Money Race: <span class="a">AI</span> vs <span class="b">Drones</span> vs <span class="c">AI Drones</span></h1>
  <p class="lede">Global annual investment, 2000&nbsp;&rarr;&nbsp;2100. AI compounds toward
     $10.9T a year. Conventional drones peak at $75B in 2045, then lose the field to autonomy,
     which overtakes them in 2027.</p>

  %STATS%

  <figure>
    <div class="key">
      <span style="--c:#2563eb">AI</span>
      <span style="--c:#d97706">Conventional drones</span>
      <span style="--c:#7c3aed">AI drones</span>
    </div>
    %SVG%
    <figcaption>Log scale &mdash; equal vertical distance means the same multiple, not the same
      dollar amount. Solid lines with dots are estimates; dashed lines and the shaded band are a
      scenario, not a forecast.</figcaption>
  </figure>

  <h2 class="sect">The story in three acts</h2>
  %ACTS%

  <h2 class="sect">Where the money actually goes today</h2>
  %USES%

  <h2 class="sect">Alberta, briefly</h2>
  %ALBERTA%

  <footer>
    <span>2000&ndash;2025 are order-of-magnitude estimates, not sourced statistics &mdash; no
      public series tracks these three categories that far back. 2025&ndash;2100 is a scenario;
      the shaded band is an illustrative spread, not a confidence interval. The three categories
      are disjoint, so they can be stacked.</span>
    <span class="links">
      <a href="full.html">Full breakdown &mdash; chapters, 13 use cases, careers, quiz, data &rarr;</a>
      <a href="simple.html">Just the chart &rarr;</a>
    </span>
  </footer>
</div>
</body>
</html>
"""


def main():
    html = bs.PAGE_HEAD.replace("</style>", EXTRA_CSS + "\n</style>") + BODY
    html = (html.replace("%STATS%", bs.build_stats())
                .replace("%SVG%", bs.build_svg())
                .replace("%ACTS%", build_acts())
                .replace("%USES%", build_uses())
                .replace("%ALBERTA%", build_alberta()))
    OUT.write_text(html, encoding="utf-8")
    print(f"saved -> {OUT.name}")
    print(f"        {OUT.stat().st_size / 1024:,.0f} KB  |  zero JavaScript  |  "
          f"{len(html.split())} words")


if __name__ == "__main__":
    main()

