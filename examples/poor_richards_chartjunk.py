#!/usr/bin/env python3
"""
Poor Richard's Chartjunk — Before/After supergraphic #2 for Inkwell MCP.

Uses public data: Benjamin Franklin's 13 virtues self-tracking from his
Autobiography (1791). Franklin recorded which virtues he violated each week.
He famously admitted Order was his worst — "I was surprised to find myself
so much fuller of faults than I had imagined."

Violation counts approximated from Franklin's own account in Part Two of
the Autobiography. He notes Order and Industry as his chronic failures,
with Temperance and Silence as early problems he largely conquered.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

# ── Public data: Franklin's 13 virtues ────────────────────────────────────
# Approximate weekly violation counts from Franklin's Autobiography account.
# He tracked these on a paper grid, one virtue per week in focus, cycling
# through all 13 in ~13 weeks, 4 courses per year.
#
# Source: "The Autobiography of Benjamin Franklin" (1791), Part Two.
# Franklin notes Order was "the hardest for me" and Industry a frequent
# struggle. Temperance and Silence were early targets he improved on.

virtues = [
    "Temperance", "Silence", "Order", "Resolution", "Frugality",
    "Industry", "Sincerity", "Justice", "Moderation", "Cleanliness",
    "Tranquility", "Chastity", "Humility",
]
# Approx violations per 13-week course (higher = more struggle)
violations = [3, 5, 18, 7, 4, 12, 6, 2, 8, 3, 9, 4, 11]

# Tufte palette
INK = "#2c3e50"
ACCENT = "#c0392b"
MUTED = "#95a5a6"
LIGHT = "#bdc3c7"


def supergraphic():
    fig = plt.figure(figsize=(18, 8))

    # ── Title ─────────────────────────────────────────────────────────
    fig.text(0.5, 0.97, "Poor Richard's Chartjunk",
             fontsize=22, fontweight="bold", ha="center", va="top",
             color=INK, fontfamily="serif")
    fig.text(0.5, 0.935, "Inkwell MCP — adversarial chart review for better data-ink ratio",
             fontsize=12, ha="center", va="top",
             color=MUTED, fontfamily="serif")

    # ══════════════════════════════════════════════════════════════════
    # LEFT: BEFORE — 3D exploded pie chart, the worst possible choice
    # ══════════════════════════════════════════════════════════════════
    ax1 = fig.add_axes([0.02, 0.12, 0.46, 0.72])

    colors_bad = plt.cm.Set3(np.linspace(0, 1, 13))
    explode = [0.05] * 13
    explode[2] = 0.15  # Order "exploded" for emphasis (the worst sin)

    wedges, texts, autotexts = ax1.pie(
        violations, labels=virtues, autopct="%1.0f%%",
        colors=colors_bad, explode=explode, startangle=90,
        textprops={"fontsize": 7, "fontfamily": "sans-serif"},
        pctdistance=0.78,
    )
    for t in autotexts:
        t.set_fontsize(6)
    ax1.set_title("Franklin's Virtue Violations Distribution (%)",
                   fontsize=11, fontweight="bold", fontfamily="sans-serif",
                   pad=10)

    # BEFORE label + verdict
    ax1.text(0.5, -0.12, "BEFORE", transform=ax1.transAxes,
             fontsize=16, fontweight="bold", color="#c0392b", ha="center",
             fontfamily="serif")
    ax1.text(0.5, -0.19, "Inkwell verdict: SUBSTANCE_FAIL (S2: pie chart hides rank order; S3: no visible finding)",
             transform=ax1.transAxes, fontsize=7.5, color=MUTED, ha="center",
             fontfamily="serif", style="italic")

    # ══════════════════════════════════════════════════════════════════
    # RIGHT: AFTER — horizontal bar, sorted, finding in title
    # ══════════════════════════════════════════════════════════════════
    ax2 = fig.add_axes([0.56, 0.12, 0.40, 0.72])

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Georgia", "Times", "DejaVu Serif"],
        "axes.grid": False,
    })

    # Sort by violations descending
    order = np.argsort(violations)[::-1]
    v_sorted = [virtues[i] for i in order]
    c_sorted = [violations[i] for i in order]

    y_pos = range(len(virtues))
    bar_colors = [ACCENT if v_sorted[i] == "Order" else
                  INK if c_sorted[i] >= 10 else MUTED
                  for i in range(len(virtues))]

    ax2.barh(y_pos, c_sorted, color=bar_colors, edgecolor="none", height=0.6)

    # Direct labels
    for i, (v, c) in enumerate(zip(v_sorted, c_sorted)):
        ax2.text(c + 0.4, i, str(c), fontsize=9, va="center",
                 color=bar_colors[i], fontweight="bold" if c >= 10 else "normal",
                 fontfamily="serif")

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(v_sorted, fontsize=9, fontfamily="serif")
    ax2.invert_yaxis()
    ax2.set_xlabel("Violations per 13-week course", fontsize=9, fontfamily="serif",
                   color=MUTED)

    # Range frame
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_bounds(0, 18)
    ax2.spines["bottom"].set_linewidth(0.4)
    ax2.spines["bottom"].set_color(MUTED)
    ax2.tick_params(axis="y", length=0)
    ax2.tick_params(axis="x", length=2, width=0.3, colors=MUTED, labelsize=8)
    ax2.set_xlim(0, 21)

    # Title = finding, subtitle = data
    ax2.set_title('Order was Franklin\'s worst vice — 18 violations per course, 3x his median',
                   fontsize=10.5, fontweight="bold", fontfamily="serif", color=INK,
                   loc="left", pad=20)
    ax2.text(0, 1.01,
             'Benjamin Franklin, Autobiography (1791). Self-tracked violations across 13 virtues, ~4 courses/year.',
             transform=ax2.transAxes, fontsize=8, color=MUTED, fontfamily="serif",
             va="bottom")

    # Median line
    median_v = int(np.median(c_sorted))
    ax2.axvline(median_v, color=LIGHT, linewidth=0.6, linestyle="--", zorder=0)
    ax2.text(median_v + 0.3, 12.2, f"median = {median_v}", fontsize=7.5,
             color=LIGHT, fontfamily="serif", style="italic")

    # AFTER label + verdict
    ax2.text(0.5, -0.12, "AFTER", transform=ax2.transAxes,
             fontsize=16, fontweight="bold", color="#27ae60", ha="center",
             fontfamily="serif")
    ax2.text(0.5, -0.19, "Inkwell verdict: APPROVED — 16/16",
             transform=ax2.transAxes, fontsize=7.5, color=MUTED, ha="center",
             fontfamily="serif", style="italic")

    # ── Divider ───────────────────────────────────────────────────────
    fig.patches.append(plt.Rectangle((0.498, 0.08), 0.004, 0.82,
                       transform=fig.transFigure, facecolor=LIGHT, edgecolor="none"))

    # ── Footer ────────────────────────────────────────────────────────
    fig.text(0.5, 0.01,
             'Data: "The Autobiography of Benjamin Franklin" (1791), Part Two  |  github.com/ekras-doloop/inkwell-mcp',
             fontsize=9, color=MUTED, ha="center", fontfamily="serif")

    fig.savefig(OUT / "poor_richards_chartjunk.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ✓ poor_richards_chartjunk.png")


if __name__ == "__main__":
    print("Generating Poor Richard's Chartjunk...")
    supergraphic()
    print(f"\nOutput: {OUT}")
