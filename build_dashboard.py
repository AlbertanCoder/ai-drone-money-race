"""
Build the self-contained interactive dashboard.

Reads the shared model in chart_data.py, injects it as JSON into
dashboard_template.html, and writes a single dependency-free HTML file
(no Plotly, no CDN, works offline).
"""
import json
import pathlib

import chart_data as cd

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "dashboard_template.html"
OUTPUT = HERE / "ai_drone_dashboard.html"
MARKER = "/*__PAYLOAD_JSON__*/"

payload = {
    "data": {
        "years": [int(y) for y in cd.YEARS],
        "ai": [round(float(v), 4) for v in cd.AI],
        "dr": [round(float(v), 4) for v in cd.DRONES],
        "aid": [round(float(v), 4) for v in cd.AI_DRONES],
        "historicalEnd": int(cd.HISTORICAL_END),
        "lastRealIdx": int(cd.LAST_REAL_IDX),
        "band": {
            k: {
                "lo": [round(float(v), 4) for v in cd.BAND[k][0]],
                "hi": [round(float(v), 4) for v in cd.BAND[k][1]],
            }
            for k in ("ai", "dr", "aid")
        },
    },
    "events": [
        [int(yr), bool(proj), head, det]
        for (yr, proj, head, det) in cd.EVENTS
    ],
    "eras": cd.ERAS,
    "usecases": cd.USECASES,
    "careers": cd.CAREERS,
    "starters": cd.STARTERS,
    "quiz": [
        {"q": q, "options": opts, "answer": ans, "explain": ex}
        for (q, opts, ans, ex) in cd.QUIZ
    ],
    "alberta": {
        "data": {
            "years": [int(y) for y in cd.YEARS],
            "ai": [round(float(v), 5) for v in cd.ALBERTA["ai"]],
            "dr": [round(float(v), 5) for v in cd.ALBERTA["dr"]],
            "aid": [round(float(v), 5) for v in cd.ALBERTA["aid"]],
            "historicalEnd": int(cd.ALBERTA["historical_end"]),
            "lastRealIdx": int(cd.ALBERTA["last_real_idx"]),
            "y0log": cd.ALBERTA["y0log"],
            "y1log": cd.ALBERTA["y1log"],
            "y1lin": cd.ALBERTA["y1lin"],
            "yticksLog": cd.ALBERTA["yticks_log"],
            "yticksLin": cd.ALBERTA["yticks_lin"],
        },
        "events": [
            [int(yr), bool(proj), head, det]
            for (yr, proj, head, det) in cd.ALBERTA["events"]
        ],
        "cards": [
            {"emoji": e, "name": n, "where": w, "when": t, "blurb": b, "so": s}
            for (e, n, w, t, b, s) in cd.ALBERTA["cards"]
        ],
        "careers": [{"org": o, "what": w} for (o, w) in cd.ALBERTA["careers"]],
    },
}

# Sanity checks so a bad model fails loudly rather than silently rendering junk.
n = len(payload["data"]["years"])
for key in ("ai", "dr", "aid"):
    assert len(payload["data"][key]) == n, f"{key} length mismatch"
assert all(v > 0 for v in payload["data"]["aid"]), "log scale needs positive values"

blob = json.dumps(payload, separators=(",", ":"))
assert "</script" not in blob.lower(), "payload would break out of the script tag"

html = TEMPLATE.read_text(encoding="utf-8")
if MARKER not in html:
    raise SystemExit(f"marker {MARKER} not found in {TEMPLATE.name}")

html = html.replace(MARKER, blob)
OUTPUT.write_text(html, encoding="utf-8")

kb = OUTPUT.stat().st_size / 1024
print(f"saved -> {OUTPUT}")
print(f"        {kb:,.0f} KB  |  {n} data points  |  {len(payload['events'])} events")
