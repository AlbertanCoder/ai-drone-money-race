# The Money Race — AI vs Drones vs AI Drones

An interactive, dependency-free view of global annual investment in artificial
intelligence, conventional drones, and autonomous ("AI") drones from 2000 to
2100, with the events behind the curve, real-world applications, Alberta's
scene, and how to get into the field.

**Live:** https://albertancoder.github.io/ai-drone-money-race/

## Honesty statement

- **2000–2025 is an estimate, not sourced statistics.** No public series tracks
  these three categories back to 2000. The values are order-of-magnitude
  estimates, shown on the chart as `ESTIMATED (not sourced)` with a solid line.
- **2025–2100 is a scenario, not a forecast.** The projected segment is drawn
  dashed and dot-free, with a shaded band that widens from zero at 2025 to
  ±60% by 2100. That band is an *illustrative spread*, not a confidence
  interval, and it is derived from the base curve rather than statistically
  fitted.
- The three series are treated as **disjoint** buckets (AI excludes drones;
  Drones excludes AI-enabled), so they can be stacked.

## Layout

| Path | Role |
|---|---|
| `chart_data.py` | Single source of truth for the model and all narrative content |
| `dashboard_template.html` | The page itself, including the hand-rolled SVG chart |
| `build_dashboard.py` | Injects the model as JSON and writes `ai_drone_dashboard.html` |
| `verify_dashboard.py` | Asserts structure, boundaries, dates and the uncertainty band |
| `ai_drone_growth.py` | Static PNG poster, sharing the same model |
| `index.html` | Generated copy of `ai_drone_dashboard.html`, served by GitHub Pages |

`index.html` is a build artifact. Do not edit it — edit the template and rebuild.

## Rebuild

```bash
python build_dashboard.py     # template + model  ->  ai_drone_dashboard.html
python verify_dashboard.py    # asserts; also writes _check.js for syntax checking
node --check _check.js        # validates the generated script block
cp ai_drone_dashboard.html index.html
```

Requires Python 3 with `numpy`, and Node only for the syntax check.
