---
name: llm-cost-and-latency
description: Finds where an app wastes LLM tokens and time, then cuts both with prompt caching, smaller models, batching and streaming.
---

# LLM cost and latency

Measure before changing anything. Optimizing the wrong call wastes a week.

## Steps

1. Find every model call site. For each, record the model, input tokens, output tokens, calls per day and whether a user is waiting. Use existing logs or add a temporary counter.
2. Rank call sites by daily cost and by user-facing latency. Work only on the top three.
3. Cache stable prefixes: put system prompt, tool definitions and reference documents first and user input last, then enable the provider's prompt caching. Check the cache hit field in responses to confirm it works.
4. Route by difficulty: classification, extraction and formatting usually run fine on a small model. Prove it on at least 50 real examples before switching.
5. Batch anything nobody is waiting for (nightly summaries, backfills) through the provider's batch API at a discount.
6. Cut tokens: trim retrieved context to what the question needs, drop chat history beyond a rolling window plus a summary, and set a tight max output.
7. For latency, stream tokens, run independent calls in parallel, and avoid chained calls that could be one.
8. Cache whole responses for identical inputs when answers do not need to be fresh.

## Rules

- Never switch models without a before and after quality check.
- Keep a kill switch to roll back.

## Report

A table of call sites with cost and latency before and after, the change made to each, and the quality check result.
