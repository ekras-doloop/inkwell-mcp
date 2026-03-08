#!/usr/bin/env python3
"""
Poor Richard's Review Cycle — 3-round strip showing Inkwell convergence
on Franklin's 13 virtues data.

Round 1: Exploded pie chart → SUBSTANCE_FAIL (S2: pie hides rank order)
Round 2: Unsorted vertical bars with rainbow → STYLE_NEEDS_WORK 8/16
Round 3: Sorted horizontal bars, 2 colors, direct labels → APPROVED 16/16
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────
virtues = [
    "Temperance", "Silence", "Order", "Resolution", "Frugality",
    "Industry", "Sincerity", "Justice", "Moderation", "Cleanliness",
    "Tranquility", "Chastity", "Humility",
]
violations = [3, 5, 18, 7, 4, 12, 6, 2, 8, 3, 9, 4, 11]

# Sorted for Round 3
order = np.argsort(violations)[::-1]
v_sorted = [virtues[i] for i in order]
c_sorted = [violations[i] for i in order]

# Tufte palette
INK = "#2c3e50"
ACCENT = "#c0392b"
MUTED = "#95a5a6"
LIGHT = "#bdc3c7"
GREEN = "#27ae60"
RED = "#c0392b"
AMBER = "#e67e22"


def review_cycle():
    fig = plt.figure(figsize=(22, 9))

    # ── Main title ────────────────────────────────────────────────────
    fig.text(0.5, 0.97, "Poor Richard's Review Cycle: 3 Rounds to a Better Chart",
             fontsize=22, fontweight="bold", ha="center", va="top",
             color=INK, fontfamily="serif")
    fig.text(0.5, 0.935,
             "Franklin's 13 virtues, same data. Substance first, then style. Converges in 1–3 rounds.",
             fontsize=12, ha="center", va="top",
             color=MUTED, fontfamily="serif")

    panel_w = 0.26
    panel_h = 0.58
    panel_y = 0.18
    gap = 0.055
    x_starts = [0.03, 0.03 + panel_w + gap, 0.03 + 2 * (panel_w + gap)]

    # ══════════════════════════════════════════════════════════════════
    # ROUND 1: Exploded pie — SUBSTANCE_FAIL
    # ══════════════════════════════════════════════════════════════════
    ax1 = fig.add_axes([x_starts[0], panel_y, panel_w, panel_h])

    colors_bad = plt.cm.Set3(np.linspace(0, 1, 13))
    explode = [0.04] * 13
    explode[2] = 0.14

    ax1.pie(violations, labels=virtues, autopct="%1.0f%%",
            colors=colors_bad, explode=explode, startangle=90,
            textprops={"fontsize": 5.5, "fontfamily": "sans-serif"},
            pctdistance=0.78)
    for t in ax1.texts:
        if "%" in t.get_text():
            t.set_fontsize(4.5)

    ax1.set_title("Franklin's Virtue Violations\nDistribution (%)",
                   fontsize=9, fontweight="bold", fontfamily="sans-serif", pad=6)

    # Round label
    fig.text(x_starts[0] + panel_w / 2, panel_y + panel_h + 0.06,
             "ROUND 1", fontsize=14, fontweight="bold", color=RED,
             ha="center", fontfamily="serif")

    # Verdict
    fig.text(x_starts[0] + panel_w / 2, panel_y - 0.02,
             "SUBSTANCE_FAIL", fontsize=11, fontweight="bold",
             color="white", ha="center", fontfamily="serif",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=RED, alpha=0.9))

    # Feedback
    fig.text(x_starts[0] + panel_w / 2, panel_y - 0.065,
             'S2 FAIL: "Pie chart hides rank order."\nS3 FAIL: "No finding visible in 5 seconds."',
             fontsize=7.5, color=MUTED, ha="center", fontfamily="serif",
             style="italic", linespacing=1.3)

    # Fix label
    arrow_x = x_starts[0] + panel_w + gap / 2
    fig.text(arrow_x, panel_y + panel_h / 2 + 0.03,
             "FIX", fontsize=10, fontweight="bold", color=INK,
             ha="center", fontfamily="serif")
    fig.text(arrow_x, panel_y + panel_h / 2 - 0.02,
             "Switch to bars.\nTitle = finding.",
             fontsize=7.5, color=MUTED, ha="center", fontfamily="serif",
             linespacing=1.3)

    # ══════════════════════════════════════════════════════════════════
    # ROUND 2: Unsorted vertical bars, rainbow — STYLE_NEEDS_WORK
    # ══════════════════════════════════════════════════════════════════
    ax2 = fig.add_axes([x_starts[1], panel_y, panel_w, panel_h])

    # Vertical bars, unsorted (Franklin's original order), rainbow
    ax2.bar(range(13), violations, color=colors_bad, edgecolor="black",
            linewidth=0.5, width=0.7)
    ax2.grid(True, alpha=0.3, linestyle="--")
    ax2.set_axisbelow(True)
    ax2.set_title("Order was Franklin's worst vice\n— 18 violations per course",
                   fontsize=8.5, fontweight="bold", fontfamily="sans-serif", pad=6)
    ax2.set_xticks(range(13))
    ax2.set_xticklabels([v[:4] for v in virtues], rotation=45, ha="right",
                         fontsize=5.5, fontfamily="sans-serif")
    ax2.set_ylabel("Violations", fontfamily="sans-serif", fontsize=7)
    ax2.legend(["Violations per course"], loc="upper right", frameon=True, fontsize=5.5)
    ax2.set_ylim(0, 25)
    for spine in ax2.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color("black")

    # Round label
    fig.text(x_starts[1] + panel_w / 2, panel_y + panel_h + 0.06,
             "ROUND 2", fontsize=14, fontweight="bold", color=AMBER,
             ha="center", fontfamily="serif")

    # Verdict
    fig.text(x_starts[1] + panel_w / 2, panel_y - 0.02,
             "STYLE_NEEDS_WORK  8/16", fontsize=10, fontweight="bold",
             color="white", ha="center", fontfamily="serif",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=AMBER, alpha=0.9))

    # Feedback
    fig.text(x_starts[1] + panel_w / 2, panel_y - 0.065,
             'C1: 0 — gridlines add no data\nC3: 0 — 13 colors, need max 2\nC5: 0 — rotated labels, cramped',
             fontsize=7.5, color=MUTED, ha="center", fontfamily="serif",
             style="italic", linespacing=1.3)

    # Fix label
    arrow_x2 = x_starts[1] + panel_w + gap / 2
    fig.text(arrow_x2, panel_y + panel_h / 2 + 0.03,
             "FIX", fontsize=10, fontweight="bold", color=INK,
             ha="center", fontfamily="serif")
    fig.text(arrow_x2, panel_y + panel_h / 2 - 0.02,
             "Sort by value.\nHorizontal bars.\n2 colors. Direct\nlabels. Median line.",
             fontsize=7, color=MUTED, ha="center", fontfamily="serif",
             linespacing=1.3)

    # ══════════════════════════════════════════════════════════════════
    # ROUND 3: Sorted horizontal bars — APPROVED
    # ══════════════════════════════════════════════════════════════════
    ax3 = fig.add_axes([x_starts[2], panel_y, panel_w, panel_h])

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Georgia", "Times", "DejaVu Serif"],
        "axes.grid": False,
    })

    y_pos = range(len(virtues))
    bar_colors = [ACCENT if v_sorted[i] == "Order" else
                  INK if c_sorted[i] >= 10 else MUTED
                  for i in range(len(virtues))]

    ax3.barh(y_pos, c_sorted, color=bar_colors, edgecolor="none", height=0.6)

    for i, (v, c) in enumerate(zip(v_sorted, c_sorted)):
        ax3.text(c + 0.3, i, str(c), fontsize=8, va="center",
                 color=bar_colors[i], fontweight="bold" if c >= 10 else "normal",
                 fontfamily="serif")

    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(v_sorted, fontsize=7.5, fontfamily="serif")
    ax3.invert_yaxis()
    ax3.set_xlabel("Violations per 13-week course", fontsize=7.5,
                   fontfamily="serif", color=MUTED)

    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_visible(False)
    ax3.spines["bottom"].set_bounds(0, 18)
    ax3.spines["bottom"].set_linewidth(0.4)
    ax3.spines["bottom"].set_color(MUTED)
    ax3.tick_params(axis="y", length=0)
    ax3.tick_params(axis="x", length=2, width=0.3, colors=MUTED, labelsize=7)
    ax3.set_xlim(0, 21)

    # Median line
    median_v = int(np.median(c_sorted))
    ax3.axvline(median_v, color=LIGHT, linewidth=0.6, linestyle="--", zorder=0)
    ax3.text(median_v + 0.3, 12.2, f"median = {median_v}", fontsize=6.5,
             color=LIGHT, fontfamily="serif", style="italic")

    ax3.set_title("Order was Franklin's worst vice\n— 18 violations per course, 3x his median",
                   fontsize=9, fontweight="bold", fontfamily="serif", color=INK,
                   loc="left", pad=12)
    ax3.text(0, 1.01,
             "Franklin, Autobiography (1791). 13 virtues, ~4 courses/year.",
             transform=ax3.transAxes, fontsize=7, color=MUTED, fontfamily="serif",
             va="bottom")

    # Round label
    fig.text(x_starts[2] + panel_w / 2, panel_y + panel_h + 0.06,
             "ROUND 3", fontsize=14, fontweight="bold", color=GREEN,
             ha="center", fontfamily="serif")

    # Verdict
    fig.text(x_starts[2] + panel_w / 2, panel_y - 0.02,
             "APPROVED  16/16", fontsize=11, fontweight="bold",
             color="white", ha="center", fontfamily="serif",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=GREEN, alpha=0.9))

    # ── Arrows between panels ─────────────────────────────────────────
    for i in range(2):
        x_from = x_starts[i] + panel_w + 0.003
        x_to = x_starts[i + 1] - 0.003
        mid_y = panel_y + panel_h / 2
        arrow = FancyArrowPatch(
            (x_from, mid_y), (x_to, mid_y),
            transform=fig.transFigure,
            arrowstyle="->,head_width=6,head_length=4",
            color=LIGHT, linewidth=1.5, mutation_scale=1,
        )
        fig.patches.append(arrow)

    # ── Footer ────────────────────────────────────────────────────────
    fig.text(0.5, 0.01,
             'Data: "The Autobiography of Benjamin Franklin" (1791), Part Two  |  github.com/ekras-doloop/inkwell-mcp',
             fontsize=9, color=MUTED, ha="center", fontfamily="serif")

    fig.savefig(OUT / "poor_richards_cycle.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ✓ poor_richards_cycle.png")


if __name__ == "__main__":
    print("Generating Poor Richard's review cycle...")
    review_cycle()
    print(f"\nOutput: {OUT}")
