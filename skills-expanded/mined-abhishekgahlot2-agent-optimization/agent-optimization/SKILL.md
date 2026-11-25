---
name: agent-optimization
description: Use when optimizing, reviewing, or debugging LLM agents for latency, cost, reliability, delivery quality, benchmark integrity, prompt bloat, retry loops, tool-call waste, fast paths, or eval regressions. Apply the Agent Optimization Prompt: measure honestly, use real traces, exhaust deterministic levers before model/prompt tweaks, and verify on the real serving path.
---

# Agent Optimization

Use this skill when the user wants to improve an LLM agent without reward-hacking the metric.

## Core Rule

Never optimize the number. Optimize the thing the number measures.

If a metric improves and user-visible delivery does not, say so.

## Workflow

1. Establish the baseline:
   - metric
   - harness
   - sample size
   - trace source
   - model/provider/version if relevant
   - delivery and correctness gates

2. Inspect real traces or failures before proposing fixes.

3. Decompose the budget:
   - model generation and deliberation
   - turns and round trips
   - tool/database/service time
   - fixed overhead
   - retries and failed attempts

4. Rank deterministic levers before prompt/model changes:
   - caching
   - merged round trips
   - parallel tool calls
   - schema/semantic layers
   - typed intents
   - compilers/generators
   - validators
   - server-side budgets

5. Check unsupported asks:
   - If the action space cannot express the answer, require fallback, partial output with a note, or honest refusal.
   - Never accept silence as a valid degradation mode.

6. Verify on the real serving path.

7. Report:
   - measured before/after
   - method
   - gates passed
   - residual classes
   - behavior changes
   - rollout risk

## Reference Prompt

When a full copy-paste prompt is useful, read:

- `references/agent-optimization-prompt.md`

When a compact review gate is enough, read:

- `references/agent-optimization-checklist.md`

## Output Shape

Prefer this structure:

```markdown
## Verdict

PASS / FAIL / NEEDS DATA

## Evidence

- Baseline:
- Candidate:
- Harness:
- Data:
- Gates:

## Bottleneck

What actually dominates the budget.

## Fix Priority

1. Deterministic fix first
2. Next deterministic fix
3. Prompt/model change only if model-bound

## Verification Plan

How to prove the change without weakening gates.

## Risks

What may regress, what was not tested, and what telemetry must watch.
```
