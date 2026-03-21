# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Inkwell MCP is a single-file MCP server (`inkwell.py`) that provides adversarial chart review via Claude's vision API. It enforces Tufte-style data visualization principles through a two-pass architecture: substance check (binary pass/fail on 4 criteria) then style scoring (8 criteria, each 0-2, total /16). A HITL gate escalates to human review after 3 style-only rejections to prevent infinite nitpick loops.

## Running

```bash
# Install dependencies
pip install mcp anthropic

# Run as MCP server (stdio transport)
python3 inkwell.py

# Generate example before/after images
python3 examples/before_after.py
```

No test suite, no linter, no build step. The project is a single Python module.

## Architecture

**Single file**: `inkwell.py` contains everything — MCP tool definitions, system prompts, Claude API calls, review history, and HITL logic.

**Key flow** (`review_chart`):
1. Check HITL gate (has this chart been style-rejected >= threshold times?)
2. Build base64 image content for Claude vision
3. Pass 1: Call Claude with `SUBSTANCE_SYSTEM` prompt — binary S1-S4 check. If fail, stop.
4. Pass 2: Call Claude with `STYLE_SYSTEM` prompt — scored C1-C8. Parse score/verdict from response text.
5. Record result in `_review_history` (in-memory dict, keyed by MD5 of filename).

**API layer** (`_call_claude`): Anthropic SDK primary, Bedrock fallback if no `ANTHROPIC_API_KEY`.

**Four MCP tools**: `review_chart`, `review_history`, `reset_history`, `chart_spec`.

## Design Decisions

- Review history is keyed by **filename hash**, not content hash — so resubmitting a regenerated chart with the same filename tracks across rounds.
- `chart_spec` reuses `SUBSTANCE_SYSTEM` as its system prompt (it's asking about data, not style).
- The style/substance prompts contain explicit anti-hallucination instructions ("Score ONLY what you can see").
- HITL threshold is configurable via `INKWELL_HITL_THRESHOLD` env var (default 3).
