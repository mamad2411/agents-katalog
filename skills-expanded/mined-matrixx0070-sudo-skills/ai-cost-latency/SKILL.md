---
name: ai-cost-latency
version: 1.0.0
description: Optimize an LLM app for cost and latency via model routing, caching, batching, and token budgets without losing quality.
author: matrixx0070
tags: [cost, latency, caching, routing, tokens]
---

## When to use

Use this when an LLM feature works but is too slow or too expensive at real volume, and you need to cut cost/latency while holding quality on a measured eval set.

**Not for:** a feature that is not yet correct (fix quality first, see `ai-eval-harness`), or picking whether to fine-tune (see `ai-fine-tune-plan`).

## Method

1. Measure before cutting: log per-request input tokens, output tokens, cost, and p50/p95 latency. Optimize the biggest driver, not the loudest complaint.
2. Trim tokens: shorten the prompt, cap `max_tokens`, drop dead few-shot examples, and compress retrieved context to the top few passages.
3. Cache aggressively. Decision point: stable prefix (system prompt, tools, long context) → prompt caching; identical repeated requests → exact-response cache; near-duplicate queries → semantic cache with a similarity threshold.
4. Route by difficulty: send easy cases to a small/fast model, hard cases to the large one, using a cheap classifier or a confidence check. Decision point: if the router misroutes hard cases, raise the escalation threshold.
5. Batch and parallelize: group offline work into batch API calls; fan out independent sub-tasks concurrently to cut wall-clock latency.
6. Stream tokens to the user to cut PERCEIVED latency even when total time is unchanged.
7. Re-run the eval set after each change. A cheaper pipeline that drops quality below the gate is not a win.

## Example

Chat feature: $0.011/req, p95 2.9s. Profiling shows a 1,800-token static system prompt resent every call and all traffic on the large model.

```
1. prompt-cache the system prefix      -> input tokens billed drop ~70%
2. route: classify simple FAQs -> small model (~60% of traffic)
3. stream output
```

Result: $0.004/req, p95 1.4s, eval pass-rate unchanged (91% → 90%, within gate). Routing verified: 0 hard cases misrouted on the holdout.

## Pitfalls

- **Optimizing before measuring.** Guessing the bottleneck. Profile tokens and latency first.
- **Caching volatile output.** Serving a stale answer for a time-sensitive or personalized query. Scope caches by what is actually stable.
- **Router quality blindness.** Cheaper model silently tanks hard cases. Re-run the eval after routing, every time.
- **Chasing total when perceived matters.** Ignoring streaming. For interactive UIs, time-to-first-token often beats total time.

## Output format

```
# Cost/Latency Plan: <feature>
BASELINE: $/req=<x> | in/out tokens=<x/y> | p50/p95=<a/b>
TOKEN TRIM: <changes>
CACHING: prefix | exact | semantic(threshold=<t>)
ROUTING: easy->small | hard->large | escalation=<rule>
BATCH/CONCURRENCY: <what>
STREAMING: yes/no
RESULT: $/req=<x'> | p95=<b'> | eval delta=<within gate?>
```
