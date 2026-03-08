#!/usr/bin/env python3
"""
Review Cycle — 3-round strip showing Inkwell's progressive feedback loop.

Same data (NASA GISS), three rounds:
  Round 1: SUBSTANCE_FAIL — title describes axes, not finding
  Round 2: STYLE_NEEDS_WORK 9/16 — title fixed, still has chartjunk
  Round 3: APPROVED 16/16 — clean, communicates

Shows how the two-pass system converges in 3 rounds.
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
years = [1880, 1900, 1920, 1940, 1960, 1980, 2000, 2010, 2020, 2024]
anomaly = [-0.16, -0.08, -0.27, 0.12, 0.03, 0.26, 0.40, 0.72, 1.02, 1.29]

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
    fig.text(0.5, 0.97, "How Inkwell Reviews: 3 Rounds to a Better Chart",
             fontsize=22, fontweight="bold", ha="center", va="top",
             color=INK, fontfamily="serif")
    fig.text(0.5, 0.935,
             "Same data, progressive feedback. Substance first, then style. Converges in 1-3 rounds.",
             fontsize=12, ha="center", va="top",
             color=MUTED, fontfamily="serif")

    panel_w = 0.26
    panel_h = 0.58
    panel_y = 0.18
    gap = 0.055
    x_starts = [0.03, 0.03 + panel_w + gap, 0.03 + 2 * (panel_w + gap)]

    # ══════════════════════════════════════════════════════════════════
    # ROUND 1: The bad chart — SUBSTANCE_FAIL
    # ══════════════════════════════════════════════════════════════════
    ax1 = fig.add_axes([x_starts[0], panel_y, panel_w, panel_h])

    colors_bad = plt.cm.RdYlGn_r(np.linspace(0.2, 0.9, len(years)))
    ax1.bar(range(len(years)), anomaly, color=colors_bad, edgecolor="black",
            linewidth=0.6, width=0.7)
    ax1.grid(True, alpha=0.4, linestyle="--")
    ax1.set_axisbelow(True)
    ax1.set_title("Global Temperature Anomaly\nOver Time (°C)",
                   fontsize=9, fontweight="bold", fontfamily="sans-serif", pad=6)
    ax1.set_xticks(range(len(years)))
    ax1.set_xticklabels(years, rotation=45, ha="right", fontsize=6.5,
                         fontfamily="sans-serif")
    ax1.set_ylabel("Anomaly (°C)", fontfamily="sans-serif", fontsize=7)
    ax1.legend(["Anomaly (°C)"], loc="upper left", frameon=True, fontsize=6)
    ax1.set_ylim(-1, 2)
    for spine in ax1.spines.values():
        spine.set_linewidth(1.2)
        spine.set_color("black")

    # Round label
    fig.text(x_starts[0] + panel_w / 2, panel_y + panel_h + 0.06,
             "ROUND 1", fontsize=14, fontweight="bold", color=RED,
             ha="center", fontfamily="serif")

    # Verdict box
    fig.text(x_starts[0] + panel_w / 2, panel_y - 0.02,
             "SUBSTANCE_FAIL", fontsize=11, fontweight="bold",
             color="white", ha="center", fontfamily="serif",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=RED, alpha=0.9))

    # Feedback
    fig.text(x_starts[0] + panel_w / 2, panel_y - 0.065,
             'S3 FAIL: "Title describes axes,\nnot finding. No argument visible."',
             fontsize=8, color=MUTED, ha="center", fontfamily="serif",
             style="italic", linespacing=1.3)

    # Fix arrow label
    arrow_x = x_starts[0] + panel_w + gap / 2
    fig.text(arrow_x, panel_y + panel_h / 2 + 0.03,
             "FIX", fontsize=10, fontweight="bold", color=INK,
             ha="center", fontfamily="serif")
    fig.text(arrow_x, panel_y + panel_h / 2 - 0.02,
             "Rewrite title\nas finding",
             fontsize=7.5, color=MUTED, ha="center", fontfamily="serif",
             linespacing=1.3)

    # ══════════════════════════════════════════════════════════════════
    # ROUND 2: Title fixed, still has chartjunk — STYLE_NEEDS_WORK
    # ══════════════════════════════════════════════════════════════════
    ax2 = fig.add_axes([x_starts[1], panel_y, panel_w, panel_h])

    # Same bad style but with a finding-based title
    ax2.bar(range(len(years)), anomaly, color=colors_bad, edgecolor="black",
            linewidth=0.6, width=0.7)
    ax2.grid(True, alpha=0.4, linestyle="--")
    ax2.set_axisbelow(True)
    ax2.set_title("Warming accelerated after 2000:\nanomaly tripled to +1.29°C",
                   fontsize=8.5, fontweight="bold", fontfamily="sans-serif", pad=6)
    ax2.set_xticks(range(len(years)))
    ax2.set_xticklabels(years, rotation=45, ha="right", fontsize=6.5,
                         fontfamily="sans-serif")
    ax2.set_ylabel("Anomaly (°C)", fontfamily="sans-serif", fontsize=7)
    ax2.legend(["Anomaly (°C)"], loc="upper left", frameon=True, fontsize=6)
    ax2.set_ylim(-1, 2)
    for spine in ax2.spines.values():
        spine.set_linewidth(1.2)
        spine.set_color("black")

    # Round label
    fig.text(x_starts[1] + panel_w / 2, panel_y + panel_h + 0.06,
             "ROUND 2", fontsize=14, fontweight="bold", color=AMBER,
             ha="center", fontfamily="serif")

    # Verdict box
    fig.text(x_starts[1] + panel_w / 2, panel_y - 0.02,
             "STYLE_NEEDS_WORK  9/16", fontsize=10, fontweight="bold",
             color="white", ha="center", fontfamily="serif",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=AMBER, alpha=0.9))

    # Feedback
    fig.text(x_starts[1] + panel_w / 2, panel_y - 0.065,
             'C1: 0 — gridlines add no data\nC3: 0 — 10 colors, need max 2\nC2: 0 — legend, not direct labels',
             fontsize=7.5, color=MUTED, ha="center", fontfamily="serif",
             style="italic", linespacing=1.3)

    # Fix arrow label
    arrow_x2 = x_starts[1] + panel_w + gap / 2
    fig.text(arrow_x2, panel_y + panel_h / 2 + 0.03,
             "FIX", fontsize=10, fontweight="bold", color=INK,
             ha="center", fontfamily="serif")
    fig.text(arrow_x2, panel_y + panel_h / 2 - 0.02,
             "Remove grid,\n1 color, direct\nlabels, range frame",
             fontsize=7.5, color=MUTED, ha="center", fontfamily="serif",
             linespacing=1.3)

    # ══════════════════════════════════════════════════════════════════
    # ROUND 3: Clean — APPROVED
    # ══════════════════════════════════════════════════════════════════
    ax3 = fig.add_axes([x_starts[2], panel_y, panel_w, panel_h])

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Georgia", "Times", "DejaVu Serif"],
        "axes.grid": False,
    })

    ax3.plot(years, anomaly, "o-", color=ACCENT, linewidth=1.5, markersize=4.5,
             zorder=3)

    ax3.text(years[0], anomaly[0] - 0.07, f"{anomaly[0]:+.2f}°C",
             fontsize=7, color=MUTED, ha="center", va="top", fontfamily="serif")
    ax3.text(years[-1], anomaly[-1] + 0.05, f"{anomaly[-1]:+.2f}°C",
             fontsize=8, color=ACCENT, ha="center", va="bottom",
             fontweight="bold", fontfamily="serif")

    ax3.axhline(0, color=LIGHT, linewidth=0.5, zorder=1)
    ax3.text(1882, 0.04, "baseline", fontsize=6.5, color=LIGHT,
             fontfamily="serif")

    ax3.annotate("acceleration\nbegins", xy=(2000, 0.40),
                 xytext=(2000, 0.12), fontsize=7, color=MUTED,
                 fontfamily="serif", style="italic", ha="center",
                 arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.7))

    ax3.set_xlim(1875, 2028)
    y_min, y_max = min(anomaly) - 0.1, max(anomaly) + 0.15
    ax3.set_ylim(y_min, y_max)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_bounds(y_min, y_max)
    ax3.spines["bottom"].set_bounds(1880, 2024)
    for spine in ["left", "bottom"]:
        ax3.spines[spine].set_linewidth(0.4)
        ax3.spines[spine].set_color(MUTED)
    ax3.tick_params(axis="both", length=2, width=0.3, colors=MUTED, labelsize=7.5)
    ax3.set_xticks([1880, 1920, 1960, 2000, 2024])

    ax3.set_title("Warming accelerated after 2000:\nanomaly tripled from +0.40 to +1.29°C",
                   fontsize=9, fontweight="bold", fontfamily="serif", color=INK,
                   loc="left", pad=12)
    ax3.text(0, 1.01,
             "NASA GISS, anomaly vs 1951–1980 baseline, 10 years.",
             transform=ax3.transAxes, fontsize=7, color=MUTED, fontfamily="serif",
             va="bottom")

    # Round label
    fig.text(x_starts[2] + panel_w / 2, panel_y + panel_h + 0.06,
             "ROUND 3", fontsize=14, fontweight="bold", color=GREEN,
             ha="center", fontfamily="serif")

    # Verdict box
    fig.text(x_starts[2] + panel_w / 2, panel_y - 0.02,
             "APPROVED  16/16", fontsize=11, fontweight="bold",
             color="white", ha="center", fontfamily="serif",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=GREEN, alpha=0.9))

    # ── Progress bar at bottom ────────────────────────────────────────
    bar_y = 0.10
    for i, (label, color, score) in enumerate([
        ("Substance\nFAIL", RED, "—"),
        ("Style\n9/16", AMBER, "||||||||||......"),
        ("Style\n16/16", GREEN, "||||||||||||||||"),
    ]):
        cx = x_starts[i] + panel_w / 2
        fig.text(cx, bar_y, score, fontsize=7, color=color, ha="center",
                 fontfamily="monospace", fontweight="bold")

    # ── Arrows between panels ─────────────────────────────────────────
    for i in range(2):
        x_from = x_starts[i] + panel_w + 0.003
        x_to = x_starts[i + 1] - 0.003
        mid_y = panel_y + panel_h / 2
        arrow = FancyArrowPatch(
            (x_from, mid_y), (x_to, mid_y),
            transform=fig.transFigure,
            arrowstyle="->,head_width=6,head_length=4",
            color=LIGHT, linewidth=1.5,
            mutation_scale=1,
        )
        fig.patches.append(arrow)

    # ── Footer ────────────────────────────────────────────────────────
    fig.text(0.5, 0.01,
             'Data: data.giss.nasa.gov/gistemp/  |  github.com/ekras-doloop/inkwell-mcp',
             fontsize=9, color=MUTED, ha="center", fontfamily="serif")

    fig.savefig(OUT / "review_cycle.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ✓ review_cycle.png")


if __name__ == "__main__":
    print("Generating review cycle strip...")
    review_cycle()
    print(f"\nOutput: {OUT}")
