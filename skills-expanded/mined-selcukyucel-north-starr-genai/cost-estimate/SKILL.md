---
name: cost-estimate
description: Estimate token costs for a proposed AI automation or change. Projects per-request and monthly costs at 1x, 10x, 100x scale with model comparison. Use before building or when the complexity gate detects cost impact (Q4=Yes).
---

# Cost Estimate — Token Cost Projection

## Purpose

Before building or changing an AI automation, estimate the token costs so teams can make informed decisions about model selection, caching strategy, and budget allocation. This prevents cost surprises at scale — a prompt that costs $0.01 per request becomes $1,000/month at 100K requests.

The complexity gate triggers this automatically when Q4 = Yes (cost impact detected).

## Input

The user provides a description of the AI automation or change. Can be:
- A new pipeline being designed
- A prompt change (e.g., adding few-shot examples)
- A model swap (e.g., upgrading from Haiku to Sonnet)
- A RAG configuration change (e.g., increasing top-k from 5 to 10)

## Workflow

### Step 1: Identify Token Sources

Map all sources of tokens in the pipeline:

**First, identify each distinct model/API call in the pipeline.** Many pipelines have multiple calls (e.g., classification call + extraction call + validation call, or embedding call + retrieval + generation). List each one as a separate component:

```
Pipeline components:
  1. <component name> — <model> — <purpose> (e.g., "Classification — Claude Haiku — categorize ticket")
  2. <component name> — <model> — <purpose> (e.g., "Extraction — Claude Sonnet — extract fields")
  3. <component name> — <model/API> — <purpose> (e.g., "Embedding — text-embedding-3-small — embed query")
```

Then, for **each component**, map its token sources:
1. **System prompt** — fixed tokens sent with every request
2. **User input** — variable tokens from user-provided content
3. **RAG context** — retrieved documents/chunks added to the prompt
4. **Tool definitions** — function/tool schemas if using tool use
5. **Conversation history** — if multi-turn, prior messages in context
6. **Output** — expected response length

For each source, estimate:
- **Fixed vs variable** — does this change per request?
- **Token count** — estimate or measure (use tokenizer if available)
- **Cacheable?** — can this be cached across requests? (e.g., system prompts, tool definitions)

### Step 2: Estimate Token Counts

For each token source:

```
Token Breakdown:
  System prompt:        ~[N] tokens (fixed, cacheable)
  User input:           ~[N] tokens average (variable)
  RAG context:          ~[N] tokens ([K] chunks × [N] tokens/chunk)
  Tool definitions:     ~[N] tokens (fixed, cacheable)
  Conversation history: ~[N] tokens average (variable, multi-turn only)
  ─────────────────────────────
  Total input:          ~[N] tokens/request
  Expected output:      ~[N] tokens/request
```

If exact counts aren't available, estimate conservatively (round up). Note assumptions.

### Step 3: Calculate Costs Per Model

Calculate per-request cost for relevant models. Use current published pricing:

| Model | Input $/1M | Output $/1M | Cache $/1M | Input Cost | Output Cost | Cache Savings | Total/Request |
|-------|-----------|-------------|-----------|------------|-------------|---------------|---------------|
| Claude Opus 4.6 | $15.00 | $75.00 | $1.88 | $[N] | $[N] | -$[N] | $[N] |
| Claude Sonnet 4.6 | $3.00 | $15.00 | $0.38 | $[N] | $[N] | -$[N] | $[N] |
| Claude Haiku 4.5 | $0.80 | $4.00 | $0.08 | $[N] | $[N] | -$[N] | $[N] |
| GPT-4o | $2.50 | $10.00 | — | $[N] | $[N] | — | $[N] |
| GPT-4o-mini | $0.15 | $0.60 | — | $[N] | $[N] | — | $[N] |

Notes:
- Use the models relevant to the project (check `CLAUDE.md` or model configs in the codebase)
- Cache savings apply only to cacheable tokens (system prompt, tool definitions)
- Pricing changes — note the date of the estimate

### Step 4: Project Monthly Costs

Scale the per-request cost to monthly projections:

| Scale | Requests/month | Cost/month (no cache) | Cost/month (with cache) |
|-------|---------------|----------------------|------------------------|
| 1x (current) | [N] | $[N] | $[N] |
| 10x (growth) | [N] | $[N] | $[N] |
| 100x (scale) | [N] | $[N] | $[N] |

If the user hasn't specified expected volume, ask. If unknown, use reasonable estimates and note the assumption.

### Step 4b: Calculate Cost Delta (for changes to existing pipelines)

If this estimate is for a **change** to an existing pipeline (not a new build), calculate the marginal cost impact:

1. Read the existing cost baseline from `.plans/BASELINE-<name>.md` or `.plans/COST-<name>.md`
2. If no prior cost data exists, estimate the current cost using the same method as Steps 1-4
3. Present the delta:

```
Cost Delta: <change description>
───────────────────────────────

                    Current         Proposed        Delta
Per request         $<N>            $<N>            +/- $<N> (+/- N%)
Monthly (1x)        $<N>            $<N>            +/- $<N> (+/- N%)
Monthly (10x)       $<N>            $<N>            +/- $<N> (+/- N%)

What changed:
  + Added: <new cost source> (+$<N>/request)
  - Removed: <removed cost source> (-$<N>/request)
  ~ Changed: <modified cost source> ($<old> → $<new>)
```

This tells the user the **marginal cost of their change**, not just the total. "Adding re-ranking costs +$0.002/request (+$60/mo at current volume)" is more useful than "$460/mo total."

### Step 5: Evaluate Optimization Opportunities

Identify ways to reduce costs:

1. **Prompt caching** — cacheable portion × cache pricing vs standard pricing
2. **Model tiering** — use cheaper model for simple tasks, expensive model for complex ones
3. **Batching** — aggregate requests for batch API (typically 50% discount)
4. **Response length control** — set max_tokens to limit output
5. **RAG optimization** — reduce chunk count, improve relevance to reduce context
6. **Conversation truncation** — limit history length in multi-turn conversations
7. **Result caching** — cache identical queries (e.g., FAQ responses)

For each applicable optimization, estimate the savings.

### Step 6: Present Output

```
## Cost Estimate: <automation description>

**Date:** <date>
**Model:** <recommended model>
**Volume assumption:** <requests/month>

### Token Breakdown

| Source | Tokens | Type | Cacheable |
|--------|--------|------|-----------|
| System prompt | [N] | fixed | yes |
| User input | [N] avg | variable | no |
| RAG context | [N] | variable | no |
| Tool definitions | [N] | fixed | yes |
| Output | [N] | variable | no |
| **Total** | **[N] in / [N] out** | | |

### Cost Per Request

| Model | $/request | Quality | Recommendation |
|-------|----------|---------|----------------|
| [model] | $[N] | [quality note] | [recommended / alternative / too expensive] |

### Monthly Projection

| Scale | Requests/mo | Cost/mo | With Caching |
|-------|------------|---------|-------------|
| 1x | [N] | $[N] | $[N] |
| 10x | [N] | $[N] | $[N] |
| 100x | [N] | $[N] | $[N] |

### Optimization Opportunities

1. [optimization]: saves ~[N]% ($[N]/mo at current volume)

### Recommendation

[Which model to use, whether the cost is within budget, what optimizations to apply]
```

### Step 7: Persist (optional)

For complex estimates or when comparing multiple approaches, write to `.plans/COST-<name>.md` using the format above. For quick estimates, presenting inline is sufficient.

## Notes

- Token counts are estimates — actual usage varies by input. Use conservative (high) estimates for budgeting.
- Model pricing changes frequently — always note the date of the estimate
- Caching savings assume the model provider supports prompt caching (Claude does, OpenAI does for some models)
- Batch API pricing is typically 50% of real-time pricing but has latency trade-offs
- This skill estimates direct API costs only — infrastructure costs (compute, storage, network) are separate
- For pipelines with multiple model calls (e.g., RAG + generation + validation), estimate each call separately and sum
- If the estimate exceeds the project budget, flag it prominently and suggest alternatives
