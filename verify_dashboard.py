"""Extract the payload JSON and the main script from the built dashboard so
they can be validated independently (JSON parse + node --check)."""
import json
import pathlib
import re

here = pathlib.Path(__file__).resolve().parent
html = (here / "ai_drone_dashboard.html").read_text(encoding="utf-8")

payloads = re.findall(
    r'<script type="application/json" id="payload-src">(.*?)</script>',
    html, re.S)
assert len(payloads) == 1, f"expected 1 payload block, found {len(payloads)}"
raw = payloads[0]
(here / "_payload.json").write_text(raw, encoding="utf-8")

data = json.loads(raw)          # raises if invalid
blocks = re.findall(r"<script>(.*?)</script>", html, re.S)
assert blocks, "no executable script block found"
js = blocks[-1]
(here / "_check.js").write_text(js, encoding="utf-8")

n = len(data["data"]["years"])
assert len(data["data"]["ai"]) == n
assert len(data["data"]["dr"]) == n
assert len(data["data"]["aid"]) == n

# --- factual-integrity checks on the event timeline -------------------------
ev = data["events"]
assert ev[0][0] == 2001, "first armed Predator strike was 7 Oct 2001"
assert ev[0][1] is False, "the 2001 strike is historical, not projected"

last_year = data["data"]["years"][data["data"]["lastRealIdx"]]
for yr, proj, head, _d in ev:
    if proj:
        assert yr >= 2026, f"projected event {yr} '{head}' is inside the historical window"
    else:
        assert yr <= last_year, f"'{head}' ({yr}) is past the last real data point ({last_year})"

hist = sum(1 for e in ev if not e[1])
print(f"events   OK  {len(ev)} total  ({hist} historical / {len(ev) - hist} projected)")

# --- uncertainty fan ---------------------------------------------------------
# The fan is an illustrative spread, not a confidence interval, so the only
# things worth asserting are structural: it must bracket the base line, start
# at zero width on the last real data point, widen monotonically, and never
# push a value to zero (the chart has a log mode).
band = data["data"]["band"]
i0 = data["data"]["lastRealIdx"]
for k in ("ai", "dr", "aid"):
    lo, hi, base = band[k]["lo"], band[k]["hi"], data["data"][k]
    assert len(lo) == n and len(hi) == n, f"{k} band length mismatch"
    assert all(v > 0 for v in lo), f"{k} band floor must stay positive for the log scale"
    assert all(l <= b <= h for l, b, h in zip(lo, base, hi)), \
        f"{k} band does not bracket the base line"
    assert abs(hi[i0] - base[i0]) < 1e-6 and abs(lo[i0] - base[i0]) < 1e-6, \
        f"{k} band must be zero-width at the last real data point"
    rel = [(h - l) / (2.0 * b) for l, b, h in zip(lo, base, hi)]
    assert all(v <= 1e-9 for v in rel[:i0 + 1]), \
        f"{k} band must be zero-width across the historical segment"
    assert all(a <= b + 1e-9 for a, b in zip(rel, rel[1:])), \
        f"{k} relative spread must widen monotonically (absolute width can shrink " \
        f"for a declining series, which is why this checks the ratio)"

assert data["data"]["years"][i0] == data["data"]["historicalEnd"], \
    "the fact/projection boundary must land on a real data year"
print(f"band     OK  zero-width at {data['data']['years'][i0]}, "
      f"+/-{band['ai']['hi'][-1] / data['data']['ai'][-1] - 1:.0%} by {data['data']['years'][-1]}")
print(f"boundary OK  historicalEnd {data['data']['historicalEnd']} is a real data vertex")
print(f"boundary OK  last real data point = {last_year}; no historical event after it")

# --- Alberta view ------------------------------------------------------------
ab = data["alberta"]
ad, ae = ab["data"], ab["events"]
assert len(ad["ai"]) == n and len(ad["dr"]) == n and len(ad["aid"]) == n, "Alberta length mismatch"
assert all(v > 0 for v in ad["aid"]), "Alberta log scale needs positive values"
assert ad["y0log"] < min(ad["aid"]), "Alberta Y domain floor is above the smallest value"
assert ad["y1log"] > max(ad["ai"]), "Alberta Y domain ceiling is below the largest value"

last_ab = ad["years"][ad["lastRealIdx"]]
boundary = ad["historicalEnd"]
for yr, proj, head, _d in ae:
    if proj:
        assert yr >= boundary, f"Alberta projected event {yr} '{head}' is before the boundary"
    else:
        # A fact can be dated inside the boundary year (2026) even though the
        # 5-year data grid stops at 2025 - e.g. the Meta announcement of Jul 2026.
        assert yr <= boundary, f"Alberta '{head}' ({yr}) is past the historical boundary ({boundary})"

# Dates verified against primary sources this session.
dates = {yr: head for yr, _p, head, _d in ae}
assert 2002 in dates and "Amii" in dates[2002]
assert 2015 in dates and "Foremost" in dates[2015]
assert 2018 in dates and "BVLOS" in dates[2018]
assert 2026 in dates and "Meta" in dates[2026]

ab_hist = sum(1 for e in ae if not e[1])
print(f"alberta  OK  {len(ae)} events ({ab_hist} historical / {len(ae) - ab_hist} projected), "
      f"{len(ab['cards'])} cards, {len(ab['careers'])} career rows")
print(f"alberta  OK  Y domain {ad['y0log']} - {ad['y1log']} covers "
      f"{min(ad['aid'])} - {max(ad['ai'])}")

print(f"payload  OK  {len(raw):,} chars")
print(f"years    OK  {n} points  {data['data']['years'][0]}-{data['data']['years'][-1]}")
print(f"events   OK  {len(data['events'])}")
print(f"js       {len(js):,} chars extracted to _check.js")
print(f"marker   {'LEFT IN FILE - BUILD FAILED' if '__PAYLOAD_JSON__' in html else 'resolved'}")
