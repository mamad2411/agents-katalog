---
name: es-search-strategy
version: 1.0.0
description: Turn a fuzzy natural-language question into ranked per-source searches, resolving ambiguity before any query runs.
author: matrixx0070
tags: [enterprise-search, query-planning, decomposition, ranking, ambiguity]
capabilities: []
---

# Enterprise Search Strategy

## When to use
Reach for this before a broad or fuzzy search, when a single query string would miss the answer — the question bundles several sub-questions, spans multiple source types, or is ambiguous about who, when, or where. You produce the plan; es-search executes it.

**Not for:** a crisp single-source lookup where the query is obvious (go straight to es-search); merging results after the search (es-knowledge-synthesis); or deciding which connectors exist at all (es-source-management).

## Method
1. **Restate the ask** in one precise sentence. *Decision:* if a word is ambiguous — a name, a codename, "the doc" — list every plausible reading before proceeding.
2. **Resolve ambiguity.** Pick the most probable reading and label it an assumption. *Decision:* ask the user back only when the readings would send you to entirely different sources; otherwise proceed on the assumption.
3. **Decompose** into atomic sub-questions, each answerable from one artifact type.
4. **Map each sub-question to a source** and give the reason: chat for decisions and discussion, email for external threads, storage for finished docs, trackers for status and ownership.
5. **Craft the actual query** per source — keyword operators for structured sources, natural phrasing for semantic ones — and set a time window on each.
6. **Rank the plan** by likelihood of carrying the answer, so the highest-yield search runs first and can short-circuit the rest.

## Example
Ask: "Did we ever agree on the new onboarding SLA, and is it built yet?" You restate, then split into two atomics: (a) "Was an onboarding SLA decided?" → chat + email, semantic "onboarding SLA decision", last 90d; (b) "Is the SLA work shipped?" → tracker, keyword `label:onboarding SLA state:done`, last 30d. You rank (a) first — no decision means (b) is moot.

## Pitfalls
- Firing the search before resolving a name/codename ambiguity, then returning confident results for the wrong entity.
- Bundling two artifact types into one sub-question, forcing a query that fits neither source well.
- Reusing one query string across keyword and semantic sources.
- Omitting time windows, so stale artifacts dominate the ranking.

## Output format
```
Interpreted question: <one line>  (Assumption: <reading chosen>)

Sub-questions:
1. <atomic>
2. <atomic>

Search plan:
| # | Source | Query / filters | Window | Why |
|---|--------|-----------------|--------|-----|

Priority order: <ranked sub-# list> — top pick because <one line>
Open ambiguities: <only those that change which sources to hit>
```
