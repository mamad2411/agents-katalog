---
name: es-knowledge-synthesis
version: 1.0.0
description: Merge overlapping, partial, and conflicting cross-source hits into one deduplicated answer with per-claim attribution and confidence.
author: matrixx0070
tags: [enterprise-search, synthesis, attribution, deduplication, confidence, conflict]
capabilities: []
---

# Enterprise Search Knowledge Synthesis

## When to use
Reach for this after a cross-source search returns overlapping, partial, or conflicting hits and the user needs an answer, not a link dump. You turn scattered snippets from chat, email, storage, and trackers into one sourced narrative with every claim traceable.

**Not for:** planning the search (es-search-strategy); running the fan-out (es-search); or a single unambiguous hit that needs no reconciliation — just quote it with its source.

## Method
1. **Cluster by claim.** Group hits around the distinct facts they assert, not by which source they came from.
2. **Deduplicate.** Collapse restatements of the same fact into one claim, but keep every distinct source pointer so nothing loses provenance.
3. **Reconcile conflicts.** *Decision:* when sources disagree, prefer the most recent and most authoritative — but surface the disagreement explicitly rather than silently picking a winner.
4. **Attribute every claim** to its source(s): who, where, when. *Decision:* if a statement has no source, it does not enter the answer — flag it as a gap instead.
5. **Rate confidence per claim:** High (multiple independent recent sources agree), Medium (single credible source), Low (stale, indirect, or contested).
6. **Fill or flag gaps.** State what the sources do not cover instead of interpolating, and point to where the missing piece likely lives.

## Example
Three hits on "current API rate limit": a wiki page (6 months old) says 100/min, a Slack thread (last week) from the platform lead says "we raised it to 300/min," a ticket (last week) marked done reads "bump rate limit to 300." You cluster into one claim "rate limit = 300/min," mark it High (two recent independent sources), note the wiki's 100/min as a stale conflict that was superseded, and flag that the wiki page needs updating.

## Pitfalls
- Averaging or silently choosing between conflicting numbers instead of showing both and the reason one wins.
- Dropping a source pointer during dedupe, so a claim becomes unverifiable.
- Rating confidence High off a single source, or Low purely because a source is old when it is uncontested.
- Filling a coverage gap with a plausible guess rather than naming it as unknown.

## Output format
```
Answer: <2-5 sentences of the settled facts>

Supporting claims:
- <claim> — [source, author, YYYY-MM-DD] — High|Medium|Low
- ...

Conflicts:
- <topic>: <side A> vs <side B> → preferred <X> because <reason>

Confidence overall: <High|Medium|Low> — <driver>
Gaps / next lookups: <what's unknown> → check <where>
```
