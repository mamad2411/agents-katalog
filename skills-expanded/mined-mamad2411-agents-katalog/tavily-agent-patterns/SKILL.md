---
name: tavily-agent-patterns
description: Agent workflows on Tavily - RAG grounding, citation handling with scores and URLs, freshness control for news and finance, and credit budgeting. Use when wiring Tavily into retrieval, fact-checking, or monitoring flows.
---

# Tavily Agent Patterns

## RAG grounding recipe

1. Search with `search_depth: "advanced"`, `chunks_per_source: 3`,
   `max_results: 5`: you get pre-chunked, relevance-ranked snippets
   instead of whole pages.
2. Filter by `score` (drop results below ~0.5; tune per domain).
3. Only if a top result needs full context, follow up with
   `POST /extract` on that single URL with `format: "markdown"` and a
   `query` to keep just the relevant chunks.
4. Feed chunks to the model with their `url` attached; never merge chunks
   from different sources into one anonymous blob.

Anti-pattern: `include_raw_content: true` on 20 results. That is a token
flood and buries the model; chunking exists to prevent it.

## Citation handling

- Every claim in generated output should map to a `results[].url`; carry
  `title` and `url` through your pipeline, render `favicon` if the UI
  shows sources.
- `score` orders sources within a claim; cite the highest-scoring source
  first.
- Treat `include_answer` as a draft summary, not a citable source: it has
  no single URL behind it. When citations matter, synthesize from
  `results` yourself.
- On `news` topic, results carry publish dates; surface the date next to
  each citation so stale sources are visible.

## Freshness control

- Breaking or recent events: `topic: "news"` + `time_range: "day"` or
  `"week"`.
- Market questions: `topic: "finance"`.
- Precise windows (post-mortems, "what was known by X"):
  `start_date`/`end_date` in YYYY-MM-DD.
- Evergreen questions: no time filter; forcing recency on stable topics
  surfaces low-quality churn instead of canonical sources.
- Verification loop: when the model asserts something time-sensitive from
  memory, re-check with a `week`-scoped search before presenting it.

## Trust scoping

- Pin high-stakes queries with `include_domains` (official docs, vendor
  sites, .gov); run an unrestricted second pass to catch what the allowlist
  missed.
- Maintain an `exclude_domains` list for known content farms.
- `auto_parameters: true` is good for open-ended user queries; hand-tuned
  parameters win inside fixed pipelines.

## Credit budgeting

- Credits: `basic`/`fast`/`ultra-fast` search 1, `advanced` search 2;
  extraction 1 per 5 URLs basic, 2 per 5 advanced; crawl 1 per 10 pages,
  2 with `instructions`.
- Tight agent loops: `ultra-fast` or `fast` depth, `max_results: 3`,
  no raw content.
- Research passes: `advanced` + chunks, still usually cheaper than one
  unbounded crawl.
- Crawl only with `limit`, `max_depth`, and `allow_external: false` set;
  watch `usage.credits` on every response and stop on `429` with backoff
  rather than retrying hot.
