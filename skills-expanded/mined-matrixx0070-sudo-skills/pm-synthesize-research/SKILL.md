---
name: pm-synthesize-research
version: 1.0.0
description: Turn raw qualitative input — interviews, surveys, tickets, sales notes — into ranked, evidence-backed themes with source counts, quotes, and confidence-rated implications.
author: matrixx0070
tags: [product, research, synthesis, discovery, insights, themes]
capabilities: []
---

# Synthesize Research

## When to use
Use this when you have raw qualitative input, interview notes, survey responses, support tickets, sales call notes, and need to turn it into ranked themes with evidence, not a pile of quotes.

**Not for:** designing the study or interview guide, statistical analysis of quantitative survey data, or generating new ideas from scratch (use pm-brainstorming). If you have not decided what question the research informs, define that first, synthesis without a question produces trivia.

## Method
1. Confirm the question: what decision does this research inform?
2. Code the raw data: tag each observation with the underlying need, pain, or behavior. Keep observations atomic and traceable to source.
3. Cluster codes into themes. A theme is a recurring pattern across sources, not one loud voice. Count distinct supporting sources per theme.
4. Rank themes by frequency x severity x strategic relevance. **Decision point:** if a "theme" has one source, it is an anecdote, mark it tentative or drop it.
5. Attach evidence: 1-2 verbatim quotes per theme plus counts. **Decision point:** if the sample is skewed (e.g., only churned users), flag the bias explicitly.
6. Translate to implications: what to build, fix, or investigate, with a confidence level.

## Example
Question: "Why do trials not convert?" Coding 18 interviews + 40 tickets surfaces theme "setup is confusing" (11 sources, high severity). Quote: "I gave up before importing my data." Contrast: "missing integrations" appeared but only 2 sources, marked tentative. Implication: prioritize guided setup (high confidence); investigate integration demand further (low confidence, thin sample).

## Pitfalls
- Inflating one vivid quote into a "theme" without counting sources.
- Ignoring sample bias, generalizing from only churned or only power users.
- Cherry-picking quotes that confirm a prior instead of representing the cluster.
- Stopping at themes without translating them into decisions and confidence.

## Output format
```
# Research Synthesis: [question] — [date]
Sources: [type + counts], sample notes.

## Ranked themes
1. [theme statement] — support: N sources — severity: H/M/L
   - "quote 1"
   - "quote 2"

## Surprising findings / contradictions
- ...

## Implications
- [action] — confidence: H/M/L

## Gaps
- What the data cannot answer; what to research next.
Low-sample findings marked tentative.
```
