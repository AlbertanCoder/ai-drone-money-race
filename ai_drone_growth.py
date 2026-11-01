"""
Projected global investment: AI vs Drones vs AI-Enabled Drones, 2000-2100.

X axis = time (5-year points). Y axis = annual money invested, USD billions (log).
Historical events (2000-2026) are real. Everything after is an illustrative
projection and is shaded / flagged with an asterisk.
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter, FixedLocator

from chart_data import AI, AI_DRONES, DRONES, EVENTS, HISTORICAL_END, YEARS

# ---------------------------------------------------------------------------
# Palette / theme
# ---------------------------------------------------------------------------
C_AI, C_DR, C_AID = "#2563eb", "#f59e0b", "#dc2626"
C_HIST, C_PROJ = "#1e293b", "#b45309"
C_INK, C_MUTE = "#0f172a", "#64748b"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#cbd5e1",
    "text.color": C_INK,
    "axes.labelcolor": C_INK,
    "xtick.color": C_MUTE,
    "ytick.color": C_MUTE,
})


FIG_W, FIG_H = 21.0, 14.0
fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")
gs = GridSpec(2, 2, figure=fig,
              width_ratios=[3.5, 1.02], height_ratios=[1.0, 0.30],
              left=0.048, right=0.985, top=0.838, bottom=0.058,
              wspace=0.10, hspace=0.26)

ax = fig.add_subplot(gs[0, 0])       # main timeline
axc = fig.add_subplot(gs[1, 0])      # composition bars
axe = fig.add_subplot(gs[:, 1])      # key-moments panel
axe.axis("off")

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
fig.text(0.048, 0.958, "THE MONEY RACE:  AI  vs  DRONES  vs  AI DRONES",
         fontsize=28, fontweight="bold", color=C_INK, ha="left", va="center")
fig.text(0.048, 0.918,
         "Projected global annual investment, 2000\u20132100  \u00b7  USD billions, "
         "logarithmic scale  \u00b7  5-year intervals  \u00b7  18 key moments",
         fontsize=12.5, color=C_MUTE, ha="left", va="center")

# ---------------------------------------------------------------------------
# Main chart
# ---------------------------------------------------------------------------
ax.axvspan(HISTORICAL_END, 2100, color="#fff7ed", zorder=0)
ax.axvline(HISTORICAL_END, color=C_PROJ, lw=1.4, ls=(0, (5, 3)),
           alpha=0.75, zorder=2)

series = [
    (AI, C_AI, "AI   (excluding drones)", 2.6),
    (DRONES, C_DR, "Drones   (conventional / remote-piloted)", 2.6),
    (AI_DRONES, C_AID, "AI Drones   (autonomous intelligence)", 3.6),
]
for vals, col, label, lw in series:
    ax.plot(YEARS, vals, color=col, lw=lw, label=label, zorder=4,
            solid_capstyle="round")
    ax.plot(YEARS, vals, color=col, marker="o", ms=6.2, mec="white",
            mew=1.2, ls="none", zorder=5)

ax.set_yscale("log")
ax.set_ylim(0.035, 30000)
ax.set_xlim(1997, 2107)


def money(y, _pos=None):
    if y >= 1000:
        return f"${y / 1000:,.0f}T"
    if y >= 1:
        return f"${y:,.0f}B"
    return f"${y:,.1f}B"


def money1(y):
    """Compact money label that keeps one decimal for trillions."""
    if y >= 1000:
        return f"${y / 1000:,.1f}T"
    if y >= 1:
        return f"${y:,.0f}B"
    return f"${y:,.2f}B"


ax.yaxis.set_major_locator(FixedLocator([0.1, 1, 10, 100, 1000, 10000]))
ax.yaxis.set_major_formatter(FuncFormatter(money))
ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, p: ""))
ax.set_xlabel("TIME   \u00b7   Year", fontsize=13.5, fontweight="bold",
              labelpad=30, color=C_INK)
ax.set_ylabel("MONEY INVESTED   \u00b7   USD (log scale)", fontsize=13.5,
              fontweight="bold", labelpad=11, color=C_INK)

ax.set_xticks(np.arange(2000, 2101, 10))
ax.set_xticks(np.arange(2000, 2101, 5), minor=True)
ax.grid(True, which="major", color="#cbd5e1", lw=0.85, alpha=0.55, zorder=1)
ax.grid(True, which="minor", axis="y", color="#e2e8f0", lw=0.6, ls=":",
        alpha=0.7, zorder=1)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#cbd5e1")
ax.spines["bottom"].set_color("#cbd5e1")
ax.tick_params(axis="both", labelsize=11.5, length=0)
ax.tick_params(axis="x", which="minor", length=3, color="#cbd5e1")

# --- zone labels (below the axis, clear of the plot body)
xax = ax.get_xaxis_transform()
ax.text(2001, -0.105, "HISTORICAL  2000\u20132025", transform=xax, fontsize=11.5,
        fontweight="bold", color=C_HIST, alpha=0.7, ha="left", va="center")
ax.text(2100, -0.105, "PROJECTED  2026\u20132100  \u00b7  MODELLED", transform=xax,
        fontsize=11.5, fontweight="bold", color=C_PROJ, alpha=0.9,
        ha="right", va="center")

# --- end-of-line value labels
for vals, col, label, lw in series:
    ax.annotate(money1(vals[-1]), xy=(2100, vals[-1]), xytext=(2102.5, vals[-1]),
                fontsize=11.5, fontweight="bold", color=col,
                va="center", ha="left", zorder=6)

# --- numbered event markers along a top rail
# Rows are assigned greedily so markers never sit closer than MIN_GAP years apart.
rail = ax.get_xaxis_transform()
ROW_Y = [1.022, 1.066, 1.110]
MIN_GAP = 2.2
row_last, row_of = [-1e9] * len(ROW_Y), []
for yr, _p, _h, _d in EVENTS:
    for r, last in enumerate(row_last):
        if yr - last >= MIN_GAP:
            row_of.append(r)
            row_last[r] = yr
            break
    else:
        row_of.append(len(ROW_Y) - 1)

for i, (yr, proj, head, det) in enumerate(EVENTS):
    y_frac = ROW_Y[row_of[i]]
    col = C_PROJ if proj else C_HIST
    ax.plot([yr], [y_frac], marker="o", ms=12.2, transform=rail,
            mfc=col, mec="white", mew=1.3, clip_on=False, zorder=8)
    ax.text(yr, y_frac, str(i + 1), transform=rail, fontsize=7.4,
            fontweight="bold", color="white", ha="center", va="center",
            zorder=9, clip_on=False)
    ax.plot([yr, yr], [0.0, ROW_Y[0] - 0.011], transform=rail,
            color=("#d6a06a" if proj else "#94a3b8"),
            lw=0.75, ls=":", alpha=0.55, clip_on=False, zorder=1)

# ---------------------------------------------------------------------------
# Crossover callout: AI Drones overtake conventional Drones
# ---------------------------------------------------------------------------
i0 = list(YEARS).index(2025)
la, lb = np.log(AI_DRONES[i0]), np.log(AI_DRONES[i0 + 1])
da, db = np.log(DRONES[i0]), np.log(DRONES[i0 + 1])
t = (da - la) / ((lb - la) - (db - da))
x_x = 2025 + 5 * t
y_x = np.exp(la + t * (lb - la))

ax.plot([x_x], [y_x], marker="X", ms=15, color=C_AID, mec="white", mew=1.8,
        zorder=10)
ax.annotate(
    f"AI DRONES OVERTAKE\nCONVENTIONAL DRONES\n\u2248 {x_x:.0f}",
    xy=(x_x, y_x), xytext=(2040, 6),
    fontsize=11.6, fontweight="bold", color=C_AID, ha="left", va="center",
    arrowprops=dict(arrowstyle="-|>", color=C_AID, lw=1.9,
                    connectionstyle="arc3,rad=0.10", shrinkA=3, shrinkB=7),
    zorder=11)

# --- inflection callouts
ax.annotate("Generative AI\ninflection", xy=(2022, 410), xytext=(2003.5, 5200),
            fontsize=11, color=C_HIST, ha="left", va="center", style="italic",
            arrowprops=dict(arrowstyle="-|>", color="#94a3b8", lw=1.1,
                            shrinkA=4, shrinkB=6,
                            connectionstyle="arc3,rad=0.0"))
ax.annotate("Autonomy becomes the\ndefault operating mode",
            xy=(2040, 380), xytext=(2056, 165),
            fontsize=11, color=C_PROJ, ha="left", va="center", style="italic",
            arrowprops=dict(arrowstyle="-|>", color=C_PROJ, lw=1.1, alpha=0.9,
                            shrinkA=4, shrinkB=6,
                            connectionstyle="arc3,rad=0.0"))

# --- growth badge
cagr = lambda a, b: ((b / a) ** (1 / 25) - 1) * 100
badge = (f"2000 \u2192 2025 CAGR\n"
         f"AI        {cagr(AI[0], AI[5]):5.1f}%\n"
         f"Drones    {cagr(DRONES[0], DRONES[5]):5.1f}%\n"
         f"AI Drones {cagr(AI_DRONES[0], AI_DRONES[5]):5.1f}%")
ax.text(0.014, 0.028, badge, transform=ax.transAxes, fontsize=10.2,
        family="DejaVu Sans Mono", color=C_INK, ha="left", va="bottom",
        bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="#e2e8f0", lw=1.2),
        zorder=12)

leg = ax.legend(loc="lower right", bbox_to_anchor=(0.997, 0.012), fontsize=11.8,
                frameon=True, framealpha=0.96, edgecolor="#e2e8f0",
                borderpad=0.8, labelspacing=0.6)
leg.get_frame().set_linewidth(1.2)
for txt in leg.get_texts():
    txt.set_color(C_INK)


# ---------------------------------------------------------------------------
# Composition panel: share of total spend
# ---------------------------------------------------------------------------
PICK = [2000, 2025, 2050, 2075, 2100]
idx = [list(YEARS).index(y) for y in PICK]
a, d, ad = AI[idx], DRONES[idx], AI_DRONES[idx]
tot = a + d + ad
pa, pdr, pad = a / tot * 100, d / tot * 100, ad / tot * 100

ypos = np.arange(len(PICK))[::-1]
axc.barh(ypos, pa, height=0.58, color=C_AI)
axc.barh(ypos, pdr, left=pa, height=0.58, color=C_DR)
axc.barh(ypos, pad, left=pa + pdr, height=0.58, color=C_AID)

for i, yy in enumerate(ypos):
    for val, left in ((pa[i], 0), (pdr[i], pa[i]), (pad[i], pa[i] + pdr[i])):
        if val > 5.5:
            axc.text(left + val / 2, yy, f"{val:.0f}%", ha="center",
                     va="center", fontsize=10.5, fontweight="bold",
                     color="white")
    axc.text(102, yy, money1(tot[i]), ha="left", va="center",
             fontsize=10.5, fontweight="bold", color=C_MUTE)

axc.set_yticks(ypos)
axc.set_yticklabels([str(y) for y in PICK], fontsize=11.5, fontweight="bold")
axc.set_xlim(0, 118)
axc.set_ylim(-0.75, len(PICK) - 0.25)
axc.set_xticks([0, 25, 50, 75, 100])
axc.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=10)
axc.set_title("SHARE OF TOTAL SPEND   \u00b7   who owns the purse",
              fontsize=12.5, fontweight="bold", color=C_INK, loc="left", pad=9)
for s in ("top", "right", "left"):
    axc.spines[s].set_visible(False)
axc.spines["bottom"].set_color("#cbd5e1")
axc.tick_params(length=0)
axc.grid(True, axis="x", color="#e2e8f0", lw=0.8, ls=":", alpha=0.85)
axc.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Key moments panel
# ---------------------------------------------------------------------------
axe.text(0.0, 1.005, "KEY MOMENTS", fontsize=15.5, fontweight="bold",
         color=C_INK, transform=axe.transAxes, ha="left", va="top")
axe.text(0.0, 0.972, "Numbers match the timeline markers.",
         fontsize=10, color=C_MUTE, transform=axe.transAxes,
         ha="left", va="top")

hist = [f"{i + 1:02d}  \u00b7  {yr}   {head}\n            {det}"
        for i, (yr, p, head, det) in enumerate(EVENTS) if not p]
proj = [f"{i + 1:02d}* \u00b7  {yr}   {head}\n            {det}"
        for i, (yr, p, head, det) in enumerate(EVENTS) if p]

t_hist = axe.text(0.0, 0.930, "\n".join(hist), fontsize=9.4, color=C_HIST,
                  transform=axe.transAxes, ha="left", va="top",
                  linespacing=1.58, family="DejaVu Sans")

fig.canvas.draw()
_bb = t_hist.get_window_extent(fig.canvas.get_renderer())
_bb = _bb.transformed(axe.transAxes.inverted())
y_after = _bb.y0 - 0.026

axe.text(0.0, y_after, "*  PROJECTED MILESTONES   (2026 onward \u2014 speculative)",
         fontsize=9.8, fontweight="bold", color=C_PROJ,
         transform=axe.transAxes, ha="left", va="top")
t_proj = axe.text(0.0, y_after - 0.030, "\n".join(proj), fontsize=9.4,
                  color=C_PROJ, transform=axe.transAxes, ha="left", va="top",
                  linespacing=1.58, family="DejaVu Sans")

fig.canvas.draw()
_bb2 = t_proj.get_window_extent(fig.canvas.get_renderer())
_bb2 = _bb2.transformed(axe.transAxes.inverted())
y_take = _bb2.y0 - 0.045

axe.plot([0.0, 1.0], [y_take + 0.012] * 2, transform=axe.transAxes,
         color="#e2e8f0", lw=1.2, clip_on=False)
axe.text(0.0, y_take, "THE SHAPE OF IT", fontsize=11, fontweight="bold",
         color=C_INK, transform=axe.transAxes, ha="left", va="top")

take = (
    "\u25aa  AI is the base layer \u2014 by far the biggest pool in\n"
    "    absolute dollars, and it sets the ceiling before\n"
    "    flattening once the build-out matures.\n\n"
    "\u25aa  Conventional drones peak in absolute spend around\n"
    "    2045, then get displaced rather than shrink gently.\n\n"
    "\u25aa  AI Drones is the only line that stays on a growth\n"
    "    curve the entire century: ~$50M in 2000 to\n"
    "    ~$2.9T by 2100 \u2014 a 57,000x move."
)
axe.text(0.0, y_take - 0.028, take, fontsize=9.4, color=C_INK,
         transform=axe.transAxes, ha="left", va="top", linespacing=1.55,
         family="DejaVu Sans")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
fig.text(0.048, 0.017,
         "NOTE:  No public series tracks these categories back to 2000 \u2014 the 2000\u20132025 "
         "points are illustrative, not sourced; 2026\u20132100 is a projection, not a forecast. "
         "Categories are disjoint (AI excludes drones; Drones excludes AI-enabled).",
         fontsize=9.4, color=C_MUTE, ha="left", va="center", style="italic")

out = r"C:\Users\SHADHUNTER\charts\ai_drone_growth_2000_2100.png"
fig.savefig(out, dpi=150, facecolor="white")
print(f"saved -> {out}")

# ---------------------------------------------------------------------------
# Companion CSV so the numbers are reusable in a spreadsheet
# ---------------------------------------------------------------------------
import csv

csv_path = r"C:\Users\SHADHUNTER\charts\ai_drone_growth_2000_2100.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["year", "basis", "ai_bn_usd", "drones_bn_usd",
                "ai_drones_bn_usd", "total_bn_usd",
                "ai_share_pct", "drones_share_pct", "ai_drones_share_pct"])
    for i, yr in enumerate(YEARS):
        t = AI[i] + DRONES[i] + AI_DRONES[i]
        w.writerow([
            int(yr),
            "historical" if yr <= HISTORICAL_END else "projected",
            f"{AI[i]:.2f}", f"{DRONES[i]:.2f}", f"{AI_DRONES[i]:.2f}",
            f"{t:.2f}",
            f"{AI[i] / t * 100:.1f}",
            f"{DRONES[i] / t * 100:.1f}",
            f"{AI_DRONES[i] / t * 100:.1f}",
        ])
print(f"saved -> {csv_path}")

