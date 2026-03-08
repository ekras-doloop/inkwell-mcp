# Inkwell MCP — X Thread

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

## Post 5 (before/after — attach both images)

Here's what Inkwell actually does. Same data: NASA GISS global temperature anomaly, 1880-2024. Public dataset anyone can pull.

BEFORE: Rainbow gradient bars. Gridlines. A title that describes the axes ("Global Temperature Anomaly Over Time") instead of stating a finding. Unnecessary legend. Y-axis extends to -1 and +2 when the data lives between -0.3 and +1.3. Inkwell verdict: SUBSTANCE_FAIL. The title doesn't state a finding — review stops there. Doesn't even get to style.

AFTER: "Global warming accelerated after 2000: anomaly tripled from +0.40 to +1.29C." Title IS the finding. Subtitle names NASA GISS, the baseline, the sample. One color. Direct labels on the endpoints. A baseline reference line. An annotation marking where acceleration begins. Range frames. Inkwell verdict: 16/16.

The data didn't change. The finding didn't change. What changed is that the chart now communicates instead of decorates.

Data source: data.giss.nasa.gov/gistemp/
Generate these yourself: github.com/ekras-doloop/inkwell-mcp/tree/main/examples

---

## Post 6 (the architectural fix)

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

## Post 7 (why this works)

Three things make this converge where v1 didn't:

First, separation of concerns. The substance reviewer literally cannot comment on fonts. The style reviewer literally cannot suggest a different chart type. They have different system prompts with explicit "do NOT comment on X" instructions. A font complaint can never veto valid data again.

Second, finite scoring. When you get "14/16, C6 scored 1 because your y-axis extends to 50 but your data maxes at 45" — that's actionable. You know exactly what to fix. You know how close you are. Compare that to "REJECTED: the chart doesn't fully embody Tufte's principles." Finite beats infinite.

Third, anti-hallucination. The style prompt says: "Score ONLY what you can see in the image. If you cannot clearly identify the font, score C4 based on whether the title states a finding. Do NOT guess the font family. If you see no gridlines, do not claim there are gridlines." This single instruction eliminated the phantom violations.

---

## Post 8 (the HITL gate)

The most important design decision isn't in either prompt. It's the escape hatch.

After 3 style-only rejections on the same chart (substance passes each time), Inkwell stops reviewing. It returns: "HITL ESCALATION. This chart has been rejected 3 times on style alone. The automated reviewer may be looping. Show the chart to a human."

This is the thing most LLM review systems are missing. You need a termination condition that isn't "the LLM finally approves." Because sometimes the LLM won't. Sometimes it's caught in a local minimum of its own aesthetic preferences. The right answer is to escalate, not to loop.

I think every adversarial LLM system needs a HITL gate. Code review bots. Writing critics. Design reviewers. If you're building one without an escape hatch, you're building an infinite loop with extra steps.

---

## Post 9 (the results)

With Inkwell v2, all 18 charts were approved within 1-3 rounds each. Average style score: 15.4/16. Three charts needed substance fixes — title math that didn't match the data (said "drops to 4" but the endpoint was 9.4). Those were legitimate catches. Zero infinite loops. Zero hallucinated violations.

Compare: v1 took 12 rounds on a single chart and never converged. Same charts, same data, same visual style. The only difference was the review architecture.

---

## Post 10 (what it is)

Inkwell is an MCP server. One Python file, ~300 lines. Works with Claude Code and Claude Desktop. You point it at a chart image, give it context about what the chart shows, and it runs the two-pass review.

Four tools:
- review_chart — the main two-pass review
- review_history — see all rounds for a chart
- reset_history — clear after a major redesign
- chart_spec — ask what charts your paper needs

pip install mcp anthropic, add to your .mcp.json, restart your client, done.

github.com/ekras-doloop/inkwell-mcp

---

## Post 11 (the deeper lesson)

John Snow didn't need a legend on his cholera map. He didn't need gridlines, gradient fills, or a 3D perspective view. He needed bars on streets and a pump in the middle. The data pointed at the pump, and a civilization changed its mind about how disease spreads.

Tufte turned that instinct into principles. Card and Mackinlay built it into interactive systems. Duarte showed that data presentations follow narrative arcs. Reynolds proved that restraint is the hardest and most important design skill.

What I learned building Inkwell is that these principles apply to the review process itself, not just the artifact being reviewed. A review system that loops forever disrespects the maker's time — Reynolds would strip it to its essence. A review system that tangles substance with style disrespects the hierarchy of concerns — Duarte would say the story has no structure. A review system that hallucinates violations disrespects the truth of the image in front of it — Tufte would call it a lie.

Snow's map worked because he let the data point at the pump and got out of the way. That's all Inkwell does: remove the noise, score what matters, and get out of the way. 300 lines of Python, four tools, two prompts. But the pattern generalizes. Any time you're building an LLM that judges creative work, you need finite scoring, separated concerns, and a door to the human.

The data should point at the pump. Everything else is chartjunk.
