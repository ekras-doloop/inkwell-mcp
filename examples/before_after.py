#!/usr/bin/env python3
"""
Before/After demo for Inkwell MCP.
Uses public data: global average temperature anomaly (NASA GISS).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

# ── Public data: NASA GISS global temperature anomaly (°C vs 1951-1980 baseline)
# Source: https://data.giss.nasa.gov/gistemp/
# Selected decades for clarity
years = [1880, 1900, 1920, 1940, 1960, 1980, 2000, 2010, 2020, 2024]
anomaly = [-0.16, -0.08, -0.27, 0.12, 0.03, 0.26, 0.40, 0.72, 1.02, 1.29]


# ═══════════════════════════════════════════════════════════════════════════
# BEFORE: Every common mistake
# ═══════════════════════════════════════════════════════════════════════════

def before():
    fig, ax = plt.subplots(figsize=(8, 5))

    # 3D-looking bars with gradient colors (chartjunk)
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.9, len(years)))
    bars = ax.bar(range(len(years)), anomaly, color=colors, edgecolor="black",
                  linewidth=0.8, width=0.7)

    # Gridlines everywhere
    ax.grid(True, alpha=0.4, linestyle="--")
    ax.set_axisbelow(True)

    # Generic title that describes axes, not finding
    ax.set_title("Global Temperature Anomaly Over Time (°C)",
                 fontsize=14, fontweight="bold", fontfamily="sans-serif")

    # Rotated labels (hard to read)
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, rotation=45, ha="right", fontfamily="sans-serif")
    ax.set_ylabel("Temperature Anomaly (°C)", fontfamily="sans-serif", fontsize=11)

    # Unnecessary legend
    ax.legend(["Anomaly (°C)"], loc="upper left", frameon=True, fontsize=10)

    # Y-axis from -1 to 2 (way beyond data range)
    ax.set_ylim(-1, 2)

    # Decorative border
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color("black")

    # "BEFORE" watermark
    fig.text(0.5, 0.5, "BEFORE", fontsize=72, color="red", alpha=0.12,
             ha="center", va="center", fontweight="bold", rotation=30)

    # Source and repo
    fig.text(0.5, -0.02, "Data: data.giss.nasa.gov/gistemp/  |  github.com/ekras-doloop/inkwell-mcp",
             fontsize=8, color="gray", ha="center", fontfamily="sans-serif")

    plt.tight_layout()
    fig.savefig(OUT / "before.png", dpi=180, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ✓ before.png")


# ═══════════════════════════════════════════════════════════════════════════
# AFTER: Inkwell-approved
# ═══════════════════════════════════════════════════════════════════════════

# Tufte palette
INK = "#2c3e50"
ACCENT = "#c0392b"
MUTED = "#95a5a6"
LIGHT = "#bdc3c7"

def after():
    fig, ax = plt.subplots(figsize=(8, 4))

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Georgia", "Times", "DejaVu Serif"],
        "axes.grid": False,
    })

    # Simple line — the data IS the story
    ax.plot(years, anomaly, "o-", color=ACCENT, linewidth=1.5, markersize=5,
            zorder=3)

    # Direct labeling on key points
    ax.text(years[0], anomaly[0] - 0.08, f"{anomaly[0]:+.2f}°C",
            fontsize=8, color=MUTED, ha="center", va="top", fontfamily="serif")
    ax.text(years[-1], anomaly[-1] + 0.06, f"{anomaly[-1]:+.2f}°C",
            fontsize=9, color=ACCENT, ha="center", va="bottom",
            fontweight="bold", fontfamily="serif")

    # Zero baseline — meaningful reference
    ax.axhline(0, color=LIGHT, linewidth=0.5, zorder=1)
    ax.text(1882, 0.04, "1951–1980 baseline", fontsize=7.5, color=LIGHT,
            fontfamily="serif")

    # Mark the acceleration — annotation below and right of the 2000 data point
    ax.annotate("acceleration\nbegins", xy=(2000, 0.40),
                xytext=(1988, -0.10), fontsize=7.5, color=MUTED,
                fontfamily="serif", style="italic", ha="center",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

    # Range frame — axes span data only
    ax.set_xlim(1875, 2028)
    y_min, y_max = min(anomaly) - 0.1, max(anomaly) + 0.15
    ax.set_ylim(y_min, y_max)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_bounds(y_min, y_max)
    ax.spines["bottom"].set_bounds(1880, 2024)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.4)
        ax.spines[spine].set_color(MUTED)

    ax.tick_params(axis="both", length=2, width=0.3, colors=MUTED, labelsize=9)
    ax.set_xticks([1880, 1920, 1960, 2000, 2024])

    # Title states the finding; subtitle states the data
    ax.set_title("Global warming accelerated after 2000: anomaly tripled from +0.40 to +1.29°C",
                 fontsize=11, fontweight="bold", fontfamily="serif", color=INK,
                 loc="left", pad=20)
    ax.text(0, 1.01, "NASA GISS global mean temperature anomaly vs 1951–1980 baseline, 10 sampled years (1880–2024).",
            transform=ax.transAxes, fontsize=8.5, color=MUTED, fontfamily="serif",
            va="bottom")

    # "AFTER" watermark
    fig.text(0.5, 0.5, "AFTER", fontsize=72, color="#27ae60", alpha=0.08,
             ha="center", va="center", fontweight="bold", rotation=30)

    # Source and repo
    fig.text(0.5, -0.02, "Data: data.giss.nasa.gov/gistemp/  |  github.com/ekras-doloop/inkwell-mcp",
             fontsize=8, color=MUTED, ha="center", fontfamily="serif")

    plt.tight_layout()
    fig.savefig(OUT / "after.png", dpi=180, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ✓ after.png")


def supergraphic():
    """Side-by-side BEFORE | AFTER in one image."""
    fig = plt.figure(figsize=(18, 8))

    # ── Supergraphic title ────────────────────────────────────────────
    fig.text(0.5, 0.97, "Same data. Same story. Better chart.",
             fontsize=20, fontweight="bold", ha="center", va="top",
             color=INK, fontfamily="serif")
    fig.text(0.5, 0.935, "Inkwell MCP — adversarial chart review for better data-ink ratio",
             fontsize=12, ha="center", va="top",
             color=MUTED, fontfamily="serif")

    # ── LEFT: BEFORE ──────────────────────────────────────────────────
    ax1 = fig.add_axes([0.04, 0.12, 0.43, 0.72])

    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.9, len(years)))
    ax1.bar(range(len(years)), anomaly, color=colors, edgecolor="black",
            linewidth=0.8, width=0.7)
    ax1.grid(True, alpha=0.4, linestyle="--")
    ax1.set_axisbelow(True)
    ax1.set_title("Global Temperature Anomaly Over Time (°C)",
                   fontsize=11, fontweight="bold", fontfamily="sans-serif")
    ax1.set_xticks(range(len(years)))
    ax1.set_xticklabels(years, rotation=45, ha="right", fontfamily="sans-serif", fontsize=8)
    ax1.set_ylabel("Temperature Anomaly (°C)", fontfamily="sans-serif", fontsize=9)
    ax1.legend(["Anomaly (°C)"], loc="upper left", frameon=True, fontsize=8)
    ax1.set_ylim(-1, 2)
    for spine in ax1.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color("black")

    # BEFORE label + verdict
    ax1.text(0.5, -0.22, "BEFORE", transform=ax1.transAxes,
             fontsize=16, fontweight="bold", color="#c0392b", ha="center",
             fontfamily="serif")
    ax1.text(0.5, -0.30, "Inkwell verdict: SUBSTANCE_FAIL (S3: title doesn't state a finding)",
             transform=ax1.transAxes, fontsize=8, color=MUTED, ha="center",
             fontfamily="serif", style="italic")

    # ── RIGHT: AFTER ──────────────────────────────────────────────────
    ax2 = fig.add_axes([0.54, 0.12, 0.43, 0.72])

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Georgia", "Times", "DejaVu Serif"],
        "axes.grid": False,
    })

    ax2.plot(years, anomaly, "o-", color=ACCENT, linewidth=1.5, markersize=5,
             zorder=3)

    ax2.text(years[0], anomaly[0] - 0.08, f"{anomaly[0]:+.2f}°C",
             fontsize=9, color=MUTED, ha="center", va="top", fontfamily="serif")
    ax2.text(years[-1], anomaly[-1] + 0.06, f"{anomaly[-1]:+.2f}°C",
             fontsize=10, color=ACCENT, ha="center", va="bottom",
             fontweight="bold", fontfamily="serif")

    ax2.axhline(0, color=LIGHT, linewidth=0.5, zorder=1)
    ax2.text(1882, 0.04, "1951–1980 baseline", fontsize=8, color=LIGHT,
             fontfamily="serif")

    ax2.annotate("acceleration\nbegins", xy=(2000, 0.40),
                 xytext=(1988, -0.10), fontsize=8, color=MUTED,
                 fontfamily="serif", style="italic", ha="center",
                 arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))

    ax2.set_xlim(1875, 2028)
    y_min, y_max = min(anomaly) - 0.1, max(anomaly) + 0.15
    ax2.set_ylim(y_min, y_max)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_bounds(y_min, y_max)
    ax2.spines["bottom"].set_bounds(1880, 2024)
    for spine in ["left", "bottom"]:
        ax2.spines[spine].set_linewidth(0.4)
        ax2.spines[spine].set_color(MUTED)
    ax2.tick_params(axis="both", length=2, width=0.3, colors=MUTED, labelsize=9)
    ax2.set_xticks([1880, 1920, 1960, 2000, 2024])

    ax2.set_title("Warming accelerated after 2000: anomaly tripled from +0.40 to +1.29°C",
                   fontsize=10, fontweight="bold", fontfamily="serif", color=INK,
                   loc="left", pad=16)
    ax2.text(0, 1.01, "NASA GISS temperature anomaly vs 1951–1980 baseline, 10 sampled years (1880–2024).",
             transform=ax2.transAxes, fontsize=7.5, color=MUTED, fontfamily="serif",
             va="bottom")

    # AFTER label + verdict
    ax2.text(0.5, -0.22, "AFTER", transform=ax2.transAxes,
             fontsize=16, fontweight="bold", color="#27ae60", ha="center",
             fontfamily="serif")
    ax2.text(0.5, -0.30, "Inkwell verdict: APPROVED — 16/16",
             transform=ax2.transAxes, fontsize=8, color=MUTED, ha="center",
             fontfamily="serif", style="italic")

    # ── Divider ───────────────────────────────────────────────────────
    fig.patches.append(plt.Rectangle((0.498, 0.08), 0.004, 0.82,
                       transform=fig.transFigure, facecolor=LIGHT, edgecolor="none"))

    # ── Footer ────────────────────────────────────────────────────────
    fig.text(0.5, 0.01,
             "Data: data.giss.nasa.gov/gistemp/  |  github.com/ekras-doloop/inkwell-mcp",
             fontsize=9, color=MUTED, ha="center", fontfamily="serif")

    fig.savefig(OUT / "supergraphic.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ✓ supergraphic.png")


if __name__ == "__main__":
    print("Generating before/after demo...")
    before()
    after()
    supergraphic()
    print(f"\nOutput: {OUT}")
