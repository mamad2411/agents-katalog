---
name: dsn-research-synthesis
version: 1.0.0
description: Turn raw user-research data into themes, evidence-backed insights, and prioritized recommendations - without inventing findings the data does not support.
author: matrixx0070
tags: [design, research, synthesis, insights, ux, affinity]
capabilities: []
---

# Research Synthesis

## When to use
Use this after interviews, usability sessions, surveys, or support-ticket dumps, when you have a pile of observations and need to know what they mean and what to do. Turns scattered notes into decisions the team can act on.

**Not for:** planning or running the study (use dsn-user-research), quantitative significance testing on large survey samples, or writing insights you *wish* the data showed — synthesis is bounded by evidence.

## Method
1. **Collect the raw signal.** Pull discrete observations — quotes, behaviors, errors, workarounds — each tagged with its source participant. Keep them atomic: one observation per note.
2. **Cluster bottom-up.** Group by affinity into themes. Let groupings emerge; do not force notes into a theme you hoped to find.
3. **Elevate to insights.** Per theme, write an insight: what users need or struggle with and why. An insight explains a pattern; it is not a restated observation.
4. **Weight the evidence.** State how many participants and which sources back each insight. *Decision:* backed by 1 participant → label "anecdote / hypothesis", not "finding"; 3+ across sources → a finding you can act on.
5. **Flag contradictions and gaps.** Note where participants disagreed and what remains unanswered.
6. **Recommend.** Convert insights into prioritized, actionable recommendations tied to evidence — never one the data cannot back.

## Example
Six of eight participants abandoned at the payment step; four said the CVV field was "hidden". **Theme:** payment friction. **Insight (6/8):** users lose confidence when required fields are visually de-emphasized. **Recommendation (high):** promote CVV to a first-class field — addresses the drop-off. A lone participant wanting Apple Pay is logged as a **hypothesis**, not a finding.

## Pitfalls
- Top-down clustering: sorting notes into pre-decided buckets confirms bias instead of finding truth.
- Restating an observation and calling it an insight — an insight must explain *why*.
- Reporting frequency vaguely ("many users") instead of X/N with sources.
- Recommending a solution the evidence does not reach, or skipping contradictions that complicate the story.

## Output format
```
# Research Synthesis: <study> (n=<participants>)
**Top findings:** insight — supported by X/N — representative quote
**Themes:** theme — observations behind it
**Contradictions / open questions:** ...
**Recommendations (prioritized):** action — insight it addresses — confidence
```
Every insight cites its evidence; anything speculative is labeled a hypothesis, not a finding.
