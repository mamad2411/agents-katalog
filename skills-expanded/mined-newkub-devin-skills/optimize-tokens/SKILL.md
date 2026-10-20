---
name: follow-lib-openai-optimize tokens
description: Reduce token usage and cost — prompt sizing, caching, model selection
argument-hint: "[scope]"
related:
  - follow-lib-openai
  - report-before-after
---

## Goal

Reduce token usage and cost of OpenAI API calls — prompt sizing, context trimming, caching, model selection, and usage tracking

## Scope

Use when optimizing cost/latency of existing OpenAI usage — covers baseline usage, prompt/context reduction, model routing, and verification (must measure before and after)

## Execute

### 1. Baseline Usage

> Goal: capture the token/cost baseline before optimizing

1. Log the `usage` field from every response (`prompt_tokens`, `completion_tokens`, `total_tokens`) — if not logged yet → add it first to have a baseline
2. Identify the most expensive calls — model × tokens × frequency are the real cost drivers; run `/deep-optimize`
3. Compute cost from the current pricing of the models in use — see `https://openai.com/api/pricing` (never guess prices)

### 2. Reduce Prompt And Context Size

> Goal: cut unnecessary tokens from inputs

1. Trim system prompts — keep only instructions that actually change the output
2. Reduce context: summarize history instead of sending the full conversation, retrieve only relevant chunks (RAG) instead of whole documents
3. Use `max_completion_tokens` to cap output — prevents runaway generations
4. Structured output via `zodResponseFormat` — output is shorter and more schema-conformant than free-form text

### 3. Cache And Reuse

> Goal: reduce repeated input tokens

1. Use prompt caching — put the static prefix (system prompt, shared context) before dynamic parts to get cache hits (see the official docs for cache requirements)
2. Cache responses app-side — identical requests need not be re-called
3. Batch API for non-real-time work — cheaper than sync calls (see the official docs)

### 4. Route Models

> Goal: use a model just good enough for the job

1. Simple tasks (classification, extraction, short answers) → use the mini/nano tier instead of the flagship
2. Route by complexity — flagship only for heavy reasoning work
3. Test quality after downgrading — cost savings must not degrade output beyond what is acceptable

### 5. Verify And Compare

> Goal: measure after the change vs the baseline

1. Compare `usage` tokens and cost before/after with `/report-before-after`
2. Check output quality has not degraded — run existing evals/tests if present
3. If there is no improvement or a quality regression → revert that point and report

## Rules

- Always log `usage` — never optimize without consumption data
- Change one point at a time — keep prompt trim vs caching vs model routing effects separable
- Preserve output quality — set an acceptance threshold clearly before downgrading a model
- Never guess prices/limits — always check the official pricing and model docs
- Use `/follow-lib-openai` for the API reference

## Expected Outcome

- Token usage and cost reduced vs the baseline with real numbers
- Model routing uses the tier suited to each task
- Output quality not degraded beyond the threshold
- Usage logging complete for continuous monitoring
