# Inkwell MCP — X Thread

## Posting guide

13 posts. Attach images as noted. All images are in `examples/`.

| Post | Image to attach |
|------|----------------|
| 1 | (none) |
| 2 | (none) |
| 3 | (none) |
| 4 | (none) |
| 5 | `supergraphic.png` |
| 6 | `poor_richards_chartjunk.png` |
| 7 | `review_cycle.png` |
| 8 | `poor_richards_cycle.png` |
| 9 | (none) |
| 10 | (none) |
| 11 | (none) |
| 12 | (none) |
| 13 | (none) |

---

## Post 1 (personal hook)

In 1854, John Snow drew a map. He plotted cholera deaths as tiny bars stacked along the streets of Soho, and the pattern pointed straight at the Broad Street water pump. One visualization overturned the entire miasma theory of disease. I rave about Steven Johnson's "The Ghost Map" to my students every chance I get because it's the proof case: a single, honest chart can change what an entire civilization believes.

That map is where my obsession starts. Tufte's "The Visual Display of Quantitative Information" gave it a theory — data-ink ratio, chartjunk, the idea that every pixel must earn its place. Card and Mackinlay at Xerox PARC showed these principles could live inside interactive systems, that visualization wasn't just a publication artifact but a thinking tool. Nancy Duarte added the narrative layer — a presentation is a story with a shape, every slide either advances the argument or wastes the audience's time. Garr Reynolds pushed it further with Presentation Zen: restraint as design philosophy, signal-to-noise as the governing metric, the Japanese aesthetic of ma applied to information.

I've carried this religion for years. If your chart needs a paragraph of explanation, your chart has failed. If your data has been decorated, it's been obscured. Snow didn't add drop shadows to his cholera bars. He didn't need a legend. The data pointed at the pump.

So when I started generating research charts with AI, I wanted an AI reviewer that shared this religion. What I got instead was a disaster. And fixing that disaster became its own small contribution to the field.

github.com/ekras-doloop/inkwell-mcp

---

## Post 2 (the project)

Some context. I'm building a research project called Pneumae — AI reconstruction of historical thinkers as phone-based mentors. The work produced 11 papers with 18 data visualizations: corpus archaeology, rhetorical analysis, voice synthesis metrics. Real data from real corpora. Every chart needed to meet the standard I'd internalized from Snow, Tufte, Duarte, Reynolds, Card: title states the finding, subtitle names the data, direct labeling, no legends, serif type, range frames, muted palette, every mark earns its ink.

I wrote a matplotlib generator that produced all 18 charts. Then I needed a reviewer.

---

## Post 3 (the naive attempt)

The obvious move: give an LLM with vision a chart image and say "review this like Tufte would." So I built an MCP server — a tool that Claude Code can call — powered by Claude Sonnet's vision capabilities. The system prompt said: "Be brutal. Reject anything that doesn't meet Tufte's principles. You almost never approve."

This is the prompt engineering equivalent of telling a junior designer "be critical" with no rubric, no scoring, no finish line. It went exactly as badly as that analogy suggests.

---

## Post 4 (the failure mode)

Chart 1 went through 12 rounds of review. Twelve. The reviewer would reject for font concerns, I'd fix the font, it would reject for color, I'd fix the color, it would reject for the font again — the font it had just approved. It hallucinated "sans-serif" on a chart rendered in Georgia. It claimed "gridlines" on a chart with axes.grid set to False.

The core failure: substance and style were tangled in a single prompt. A real data integrity issue ("your title says doubles but the data shows 2.3x") was weighted the same as "I think your subtitle could be lighter gray." A font quibble could veto a chart whose data was perfect.

And because there was no scoring — just APPROVE or REJECT — there was no convergence. The reviewer had infinite room to find new complaints. It was an adversarial system with no termination condition. Snow didn't need 12 rounds of peer review on his cholera map. The data pointed at the pump. Duarte would call this a presentation with no resolution beat. Reynolds would call it noise without signal. Tufte would call it chartjunk in the review process itself.

---

## Post 5 (NASA before/after — attach `supergraphic.png`)

Here's what Inkwell actually does. Same data: NASA GISS global temperature anomaly, 1880-2024. Public dataset anyone can pull.

BEFORE: Rainbow gradient bars. Gridlines. A title that describes the axes ("Global Temperature Anomaly Over Time") instead of stating a finding. Unnecessary legend. Y-axis extends to -1 and +2 when the data lives between -0.3 and +1.3. Inkwell verdict: SUBSTANCE_FAIL. The title doesn't state a finding — review stops there. Doesn't even get to style.

AFTER: "Global warming accelerated after 2000: anomaly tripled from +0.40 to +1.29C." Title IS the finding. Subtitle names NASA GISS, the baseline, the sample. One color. Direct labels on the endpoints. A baseline reference line. An annotation marking where acceleration begins. Range frames. Inkwell verdict: 16/16.

The data didn't change. The finding didn't change. What changed is that the chart now communicates instead of decorates.

Data source: data.giss.nasa.gov/gistemp/
Generate these yourself: github.com/ekras-doloop/inkwell-mcp/tree/main/examples

---

## Post 6 (Franklin before/after — attach `poor_richards_chartjunk.png`)

Poor Richard's Chartjunk. Same idea, different century.

Benjamin Franklin tracked his 13 virtues in a weekly grid — one of history's first self-quantification systems. He recorded every violation and admitted Order was his chronic failure: "I was surprised to find myself so much fuller of faults than I had imagined."

BEFORE: An exploded pie chart with 13 pastel slices. You can't compare any two values. You can't see that Order is 3x the median. The title says "Distribution (%)" — distribution of what? Compared to what? Inkwell verdict: SUBSTANCE_FAIL. Pie hides rank order. No finding visible.

AFTER: Sorted horizontal bars. Order jumps out at 18, red. Industry and Humility in dark ink. Everything else in muted gray. A dashed median line at 6 shows the "3x" claim visually. Title: "Order was Franklin's worst vice — 18 violations per course, 3x his median." Inkwell verdict: APPROVED, 16/16.

Data source: "The Autobiography of Benjamin Franklin" (1791), Part Two.

---

## Post 7 (NASA review cycle — attach `review_cycle.png`)

But how does Inkwell get you from BEFORE to AFTER? Here's the actual feedback loop, three rounds on the NASA temperature data:

ROUND 1: The bad chart goes in. Inkwell runs substance check. S3 FAIL: "Title describes axes, not finding. No argument visible." Review stops. Style is skipped. You know exactly what to fix: rewrite the title as a finding.

ROUND 2: Title fixed. Now Inkwell passes substance and runs style. Score: 9/16 — STYLE_NEEDS_WORK. C1: 0 — gridlines add no data. C3: 0 — 10 colors, need max 2. C2: 0 — legend instead of direct labels. Three specific things to fix. Not "it doesn't feel right." Three things.

ROUND 3: Gridlines gone. One color. Direct labels. Range frames. Score: 16/16 — APPROVED. Three rounds. Done.

This is what finite scoring buys you: convergence. You know where you stand at every step.

---

## Post 8 (Franklin review cycle — attach `poor_richards_cycle.png`)

Same convergence, different data. Franklin's 13 virtues through three rounds:

ROUND 1: Exploded pie chart. SUBSTANCE_FAIL. S2: "Pie chart hides rank order." S3: "No finding visible in 5 seconds." Fix: switch to bars, write the finding into the title.

ROUND 2: Vertical bars, unsorted, rainbow colors, gridlines. STYLE_NEEDS_WORK, 8/16. C1: 0 — gridlines. C3: 0 — 13 colors. C5: 0 — rotated labels, cramped. Fix: sort by value, go horizontal, 2 colors, add median line.

ROUND 3: Sorted horizontal bars. Order in red at 18. Median line at 6. APPROVED, 16/16.

Two different datasets, two different starting points, same pattern: substance first, style second, 3 rounds to done. The feedback is specific enough to act on and finite enough to converge.

---

## Post 9 (the architectural fix)

The fix wasn't prompt engineering. It was architecture. I split the review into two completely separate passes with separate system prompts, separate API calls, and separate verdicts.

Pass 1 — SUBSTANCE. Four binary checks:
S1: Is this real data or invented numbers?
S2: Is this the right chart type for this data?
S3: Can you see the finding in 5 seconds?
S4: Does the title's claim match what the chart shows?

Any failure = immediate rejection. No style commentary. Fix the data first. Snow's map would pass all four in seconds: real death counts, spatial form fits spatial data, the cluster is visible instantly, the title matches the pattern.

Pass 2 — STYLE. Eight criteria, scored 0-2 each:
C1: Data-ink ratio
C2: Direct labeling
C3: Color restraint (max 2 meaningful colors)
C4: Typography (title = finding, subtitle = data)
C5: White space
C6: Range frames
C7: Meaningful annotations
C8: Context (whose data, sample size)

Total out of 16. >= 12 passes. 8-11 needs work. < 8 fails. A number, not a vibe.

---

## Post 10 (why this works)

Three things make this converge where v1 didn't:

First, separation of concerns. The substance reviewer literally cannot comment on fonts. The style reviewer literally cannot suggest a different chart type. They have different system prompts with explicit "do NOT comment on X" instructions. A font complaint can never veto valid data again.

Second, finite scoring. When you get "14/16, C6 scored 1 because your y-axis extends to 50 but your data maxes at 45" — that's actionable. You know exactly what to fix. You know how close you are. Compare that to "REJECTED: the chart doesn't fully embody Tufte's principles." Finite beats infinite.

Third, anti-hallucination. The style prompt says: "Score ONLY what you can see in the image. If you cannot clearly identify the font, score C4 based on whether the title states a finding. Do NOT guess the font family. If you see no gridlines, do not claim there are gridlines." This single instruction eliminated the phantom violations.

---

## Post 11 (the HITL gate)

The most important design decision isn't in either prompt. It's the escape hatch.

After 3 style-only rejections on the same chart (substance passes each time), Inkwell stops reviewing. It returns: "HITL ESCALATION. This chart has been rejected 3 times on style alone. The automated reviewer may be looping. Show the chart to a human."

This is the thing most LLM review systems are missing. You need a termination condition that isn't "the LLM finally approves." Because sometimes the LLM won't. Sometimes it's caught in a local minimum of its own aesthetic preferences. The right answer is to escalate, not to loop.

I think every adversarial LLM system needs a HITL gate. Code review bots. Writing critics. Design reviewers. If you're building one without an escape hatch, you're building an infinite loop with extra steps.

---

## Post 12 (what it is)

Inkwell is an MCP server. One Python file, ~300 lines. Works with Claude Code and Claude Desktop. You point it at a chart image, give it context about what the chart shows, and it runs the two-pass review.

Four tools:
- review_chart — the main two-pass review
- review_history — see all rounds for a chart
- reset_history — clear after a major redesign
- chart_spec — ask what charts your paper needs

pip install mcp anthropic, add to your .mcp.json, restart your client, done.

github.com/ekras-doloop/inkwell-mcp

---

## Post 13 (the deeper lesson)

John Snow didn't need a legend on his cholera map. He didn't need gridlines, gradient fills, or a 3D perspective view. He needed bars on streets and a pump in the middle. The data pointed at the pump, and a civilization changed its mind about how disease spreads.

Tufte turned that instinct into principles. Card and Mackinlay built it into interactive systems. Duarte showed that data presentations follow narrative arcs. Reynolds proved that restraint is the hardest and most important design skill.

What I learned building Inkwell is that these principles apply to the review process itself, not just the artifact being reviewed. A review system that loops forever disrespects the maker's time — Reynolds would strip it to its essence. A review system that tangles substance with style disrespects the hierarchy of concerns — Duarte would say the story has no structure. A review system that hallucinates violations disrespects the truth of the image in front of it — Tufte would call it a lie.

Snow's map worked because he let the data point at the pump and got out of the way. That's all Inkwell does: remove the noise, score what matters, and get out of the way. 300 lines of Python, four tools, two prompts. But the pattern generalizes. Any time you're building an LLM that judges creative work, you need finite scoring, separated concerns, and a door to the human.

The data should point at the pump. Everything else is chartjunk.
