---
name: funnel-map
description: Maps the funnel as it actually is, stage by stage with real numbers, names the conversion question each step must answer, finds the leak that costs the most money, and designs one fix sized to test in two weeks. Use when traffic exists but revenue disappoints, or nobody can say where buyers actually drop.
argument-hint: "[funnel steps + any numbers you have per stage]"
---

# Funnel Map — find the leak before touching anything

Funnels rarely fail everywhere at once; they fail at one stage while everyone argues about a different one. The map is the argument-ender: every step from first touch to money, the real number at each, the question the buyer is silently asking there — and the discipline to fix the leak that costs the most, not the one that is most visible.

## Inputs
- The funnel steps as they exist today, and any numbers per stage: $ARGUMENTS
- From `marketing-brief.md` if present: **Channels & funnel** (current stages and numbers), the offer (the thing being converted to), and the objections (they predict where buyers stall).

## Do this
1. Draw the funnel as it IS, not as designed — every real step from first touch to money, plus renewal or repeat if it applies. Attach the actual number at each step. Where a number does not exist, write UNKNOWN — never an estimate dressed as data.
2. For each stage, write the conversion question the buyer is silently asking there — "is this for me?", "do I believe this?", "what does it cost me to find out?", "is it safe to say yes now?" — and name the asset currently answering it. A stage whose question has no asset is a leak by design.
3. Find the leak that matters. For each drop-off, weigh drop size × volume reaching it × value per person — a 5-point leak at the proposal stage can cost more than a 30-point leak at the top. Benchmark against your own history first, category norms second.
4. Diagnose before designing. The usual suspects, in order:
   - The promise upstream does not survive to this stage (message mismatch).
   - The stage's question has no answer (missing proof, missing clarity).
   - The ask outruns the trust built so far (a step too steep).
5. Design ONE fix, sized to test inside two weeks, with the single number that will prove or kill it. Inside Claude Code, the funnel-strategist agent can pressure-test the diagnosis and the fix.
6. If key numbers came up UNKNOWN, the first fix is measurement — instrument the missing stages before spending anything on optimisation.
7. Update **Channels & funnel** in `marketing-brief.md` with the mapped stages and the numbers as of today.

## Output
The funnel map as a table — stage, number (or UNKNOWN), the buyer's question, the asset answering it, status — followed by the leak with the costing behind it, the one fix with its test and success number, and the measurement gaps.

## Rules
- UNKNOWN beats invented. A map with honest gaps drives better decisions than one padded with guesses.
- One leak at a time. Funnels compound — fixing the biggest leak changes every number downstream, so re-map before fixing the next.
- Check message match before mechanics. Most "page problems" are broken promises from the ad or post before it.
- The buyer's question at each stage decides the asset, not the other way round.
- Fixes are sized to learn in two weeks. Big-bang rebuilds hide which change did the work.
