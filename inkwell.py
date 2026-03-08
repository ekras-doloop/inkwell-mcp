#!/usr/bin/env python3
"""
Inkwell MCP — adversarial chart review for better data-ink ratio.

Two-pass review system:
  Pass 1 (SUBSTANCE): Does the chart show real data? Is the form right?
    Does the title match the data? Binary pass/fail on 4 criteria. Fails fast.
  Pass 2 (STYLE): 8 criteria scored 0-2 each. Total /16.
    >=12 = PASS, 8-11 = NEEDS_WORK, <8 = FAIL.

HITL gate: After 3 style-only rejections on the same chart, escalates to
  human review instead of looping forever.

Setup:
    pip install mcp anthropic

    Add to .mcp.json (Claude Code) or claude_desktop_config.json (Claude Desktop):
    {
        "mcpServers": {
            "inkwell": {
                "command": "python3",
                "args": ["/path/to/inkwell.py"],
                "env": { "ANTHROPIC_API_KEY": "sk-ant-..." }
            }
        }
    }
"""

import base64
import hashlib
import os
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "inkwell",
    instructions=(
        "Adversarial chart reviewer. Helps you improve your data-ink ratio "
        "and communicate more with your charts. Two-pass review: substance "
        "(data integrity) then style (Tufte principles). Escalates to human "
        "after 3 style-only rejections to prevent infinite loops."
    ),
)

# ── Configuration ─────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
REVIEW_MODEL = os.environ.get("INKWELL_MODEL", "claude-sonnet-4-20250514")

# Bedrock fallback (optional)
BEDROCK_REGION = os.environ.get("AWS_REGION", "us-east-1")
BEDROCK_MODEL = os.environ.get(
    "INKWELL_BEDROCK_MODEL", "us.anthropic.claude-sonnet-4-20250514-v1:0"
)

# ── Review history for HITL escalation ────────────────────────────────────
# Key: chart_id (hash of filename), Value: list of review results
_review_history: dict[str, list[dict]] = {}
HITL_THRESHOLD = int(os.environ.get("INKWELL_HITL_THRESHOLD", "3"))


# ── System prompts ────────────────────────────────────────────────────────

SUBSTANCE_SYSTEM = """You are a data visualization reviewer. Your ONLY job is to check four substance criteria. You are NOT reviewing style, fonts, colors, or layout.

Check these four things and NOTHING ELSE:

S1. REAL DATA — Does the chart show actual data (measurements, counts, corpus statistics, computed metrics)? Engineering specifications and design parameters also count as real data if labeled as such. Conceptual illustrations with invented numbers fail.

S2. RIGHT FORM — Is this visualization type appropriate for the data and finding? (e.g., don't use a pie chart for time series.) Be practical: if the form communicates the finding, it passes. Do NOT suggest alternative forms — just assess whether this one works.

S3. VISIBLE ARGUMENT — Can a reader see the main finding within 5 seconds? The title should state the finding. The visual should confirm it.

S4. DATA INTEGRITY — Are labels, values, and units consistent? Does the title's claim match what the chart actually shows? (e.g., title says "doubles" but data shows 2.3x = FAIL.)

Respond in EXACTLY this format:
S1: PASS or FAIL — one sentence why
S2: PASS or FAIL — one sentence why
S3: PASS or FAIL — one sentence why
S4: PASS or FAIL — one sentence why
VERDICT: SUBSTANCE_PASS or SUBSTANCE_FAIL

If ANY criterion fails, VERDICT is SUBSTANCE_FAIL.
Do NOT comment on style, fonts, colors, gridlines, or layout. Those are not your job."""

STYLE_SYSTEM = """You are scoring a chart's visual style against 8 criteria. The chart has ALREADY passed substance review — do not re-evaluate whether the data is real or the visualization type is correct.

Score each criterion 0, 1, or 2:
  0 = clear violation
  1 = acceptable but improvable
  2 = good

THE 8 CRITERIA:
C1. DATA-INK RATIO — Every mark shows data or helps read data. No decorative elements.
C2. DIRECT LABELING — Data points labeled directly, no legend required. Key values annotated.
C3. COLOR RESTRAINT — Maximum two colors carrying meaning. Muted palette.
C4. TYPOGRAPHY — Title states finding (bold). Subtitle describes data (lighter). Clean type hierarchy.
C5. WHITE SPACE — Chart is not cramped. Labels don't overlap. Breathing room.
C6. RANGE FRAMES — Axes span only the data range, not arbitrary round numbers.
C7. ANNOTATIONS — Text annotations carry meaning (ratios, key values), not decoration.
C8. CONTEXT — Subtitle identifies whose data, what was measured, and sample size.

IMPORTANT RULES:
- Score ONLY what you can see in the image. Do not hallucinate violations.
- If you cannot clearly identify the font, score C4 based on whether title states finding and subtitle describes data. Do NOT guess the font family.
- If you see no gridlines, do not claim there are gridlines.
- A score of 1 is acceptable. Not everything needs to be 2.

Respond in EXACTLY this format:
C1: [0/1/2] — one sentence
C2: [0/1/2] — one sentence
C3: [0/1/2] — one sentence
C4: [0/1/2] — one sentence
C5: [0/1/2] — one sentence
C6: [0/1/2] — one sentence
C7: [0/1/2] — one sentence
C8: [0/1/2] — one sentence
TOTAL: [X]/16
VERDICT: STYLE_PASS (if >= 12) or STYLE_NEEDS_WORK (if 8-11) or STYLE_FAIL (if < 8)

Do NOT suggest alternative visualization types. That was decided in substance review."""


def _call_claude(system: str, content: list, max_tokens: int = 1500) -> str:
    """Call Claude via Anthropic API (preferred) or Bedrock fallback."""
    if ANTHROPIC_API_KEY:
        import anthropic

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=REVIEW_MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": content}],
        )
        return response.content[0].text
    else:
        import boto3

        client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
        resp = client.invoke_model(
            modelId=BEDROCK_MODEL,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "system": system,
                    "messages": [{"role": "user", "content": content}],
                }
            ),
        )
        result = json.loads(resp["body"].read())
        return result["content"][0]["text"]


def _build_image_content(image_path: str) -> list:
    """Build the image content block for Claude vision."""
    content = []
    img_path = Path(image_path)
    if img_path.exists() and img_path.suffix.lower() in (".png", ".jpg", ".jpeg"):
        img_bytes = img_path.read_bytes()
        media_type = (
            "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"
        )
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64.b64encode(img_bytes).decode(),
                },
            }
        )
    return content


def _chart_id(image_path: str) -> str:
    """Stable ID for a chart filename (not content — so resubmissions track)."""
    return hashlib.md5(Path(image_path).name.encode()).hexdigest()[:12]


def _check_hitl(chart_id: str) -> str | None:
    """Check if this chart should be escalated to human review."""
    history = _review_history.get(chart_id, [])
    style_rejections = [
        r
        for r in history
        if r.get("substance") == "PASS"
        and r.get("style_verdict") in ("STYLE_NEEDS_WORK", "STYLE_FAIL")
    ]
    if len(style_rejections) >= HITL_THRESHOLD:
        scores = [r.get("style_score", "?") for r in style_rejections]
        return (
            f"HITL ESCALATION: This chart has been rejected {len(style_rejections)} "
            f"times on style alone (substance passes every time). "
            f"Style scores across rounds: {scores}. "
            f"The automated reviewer may be looping. "
            f"Show the chart to a human and ask: "
            f"'Does this chart communicate its finding clearly? "
            f"Any label overlaps or readability issues?'"
        )
    return None


@mcp.tool()
def review_chart(
    image_path: str,
    context: str,
    code: str = "",
) -> str:
    """Two-pass chart review: substance first, then style. HITL escalation after repeated style rejections.

    Args:
        image_path: Absolute path to the chart image (PNG or JPEG).
        context: What the chart shows — paper title, finding, data source. The more context you give, the better the review.
        code: Optional matplotlib/plotting code that generated the chart. Helps the reviewer check data integrity.

    Returns:
        Structured review with pass/fail on substance (S1-S4), scores on style (C1-C8, total /16), or HITL escalation if the reviewer is looping.
    """
    chart_id = _chart_id(image_path)
    chart_name = Path(image_path).name

    # ── HITL check ────────────────────────────────────────────────
    hitl_msg = _check_hitl(chart_id)
    if hitl_msg:
        return hitl_msg

    # ── Build image content ───────────────────────────────────────
    image_content = _build_image_content(image_path)
    if not image_content:
        return f"ERROR: Could not read image at {image_path}"

    prompt_text = f"Review this chart.\n\nContext: {context}"
    if code:
        prompt_text += f"\n\nPlotting code:\n```python\n{code}\n```"

    # ── PASS 1: SUBSTANCE ─────────────────────────────────────────
    substance_content = image_content + [{"type": "text", "text": prompt_text}]
    substance_result = _call_claude(SUBSTANCE_SYSTEM, substance_content, max_tokens=800)

    substance_pass = "SUBSTANCE_PASS" in substance_result

    if not substance_pass:
        _review_history.setdefault(chart_id, []).append(
            {
                "substance": "FAIL",
                "result": substance_result,
            }
        )
        review_count = len(_review_history[chart_id])
        return (
            f"REJECTED — SUBSTANCE FAILURE (review #{review_count} of {chart_name})\n\n"
            f"{substance_result}\n\n"
            f"Fix the substance issues before resubmitting. Style review is skipped."
        )

    # ── PASS 2: STYLE ─────────────────────────────────────────────
    style_content = image_content + [{"type": "text", "text": prompt_text}]
    style_result = _call_claude(STYLE_SYSTEM, style_content, max_tokens=1000)

    # Parse score from result
    style_score = None
    style_verdict = "UNKNOWN"
    for line in style_result.splitlines():
        if line.startswith("TOTAL:"):
            try:
                style_score = int(line.split("/")[0].split(":")[1].strip())
            except (ValueError, IndexError):
                pass
        if line.startswith("VERDICT:"):
            style_verdict = line.split(":")[1].strip()

    # Record
    _review_history.setdefault(chart_id, []).append(
        {
            "substance": "PASS",
            "style_score": style_score,
            "style_verdict": style_verdict,
            "result": style_result,
        }
    )
    review_count = len(_review_history[chart_id])

    # Build response
    if style_verdict == "STYLE_PASS":
        header = f"APPROVED (review #{review_count} of {chart_name})"
    elif style_verdict == "STYLE_NEEDS_WORK":
        remaining = HITL_THRESHOLD - len(
            [
                r
                for r in _review_history[chart_id]
                if r.get("substance") == "PASS"
                and r.get("style_verdict") in ("STYLE_NEEDS_WORK", "STYLE_FAIL")
            ]
        )
        header = (
            f"STYLE_NEEDS_WORK (review #{review_count} of {chart_name}, "
            f"score {style_score}/16, "
            f"{remaining} more rejection(s) before HITL escalation)"
        )
    else:
        header = f"STYLE_FAIL (review #{review_count} of {chart_name}, score {style_score}/16)"

    return (
        f"{header}\n\n"
        f"── Substance ──\n{substance_result}\n\n"
        f"── Style ──\n{style_result}"
    )


@mcp.tool()
def review_history(image_path: str) -> str:
    """Get the review history for a chart (all rounds).

    Args:
        image_path: Absolute path to the chart image.

    Returns:
        Summary of all review rounds for this chart, showing substance pass/fail and style scores.
    """
    chart_id = _chart_id(image_path)
    history = _review_history.get(chart_id, [])
    if not history:
        return f"No review history for {Path(image_path).name}"

    lines = [f"Review history for {Path(image_path).name} ({len(history)} rounds):"]
    for i, r in enumerate(history, 1):
        sub = r.get("substance", "?")
        score = r.get("style_score", "n/a")
        verdict = r.get("style_verdict", "n/a")
        lines.append(f"  Round {i}: substance={sub}, style={score}/16 ({verdict})")
    return "\n".join(lines)


@mcp.tool()
def reset_history(image_path: str) -> str:
    """Reset review history for a chart (e.g., after major redesign).

    Args:
        image_path: Absolute path to the chart image.

    Returns:
        Confirmation of how many rounds were cleared.
    """
    chart_id = _chart_id(image_path)
    old_count = len(_review_history.get(chart_id, []))
    _review_history[chart_id] = []
    return f"Reset history for {Path(image_path).name} (was {old_count} rounds)"


@mcp.tool()
def chart_spec(
    paper_text: str,
    paper_title: str = "",
) -> str:
    """Ask Inkwell to specify what charts a paper or report needs.

    Args:
        paper_text: The paper/report content (can be truncated to ~8000 chars).
        paper_title: Optional title for reference.

    Returns:
        Chart specifications with data requirements, recommended forms, and what to omit.
    """
    spec_prompt = f"""Read this text and specify 2-4 charts that would strengthen its argument.

For each chart:
- THE ONE THING it must communicate
- The data (EXACT numbers from the text — quote the source line)
- The form (chart type) and WHY this form suits the data
- What to OMIT (decorative elements, unnecessary axes, legends)
- Title (states the finding, not the axes)
- Subtitle (describes the data source, what was measured, sample size)
- If the text has no quantitative data for a chart, say so — do NOT invent.

{f"Title: {paper_title}" if paper_title else ""}

Text:
{paper_text[:8000]}"""

    content = [{"type": "text", "text": spec_prompt}]
    return _call_claude(SUBSTANCE_SYSTEM, content, max_tokens=3000)


if __name__ == "__main__":
    mcp.run()
