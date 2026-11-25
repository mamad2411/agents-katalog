---
name: context-budget-audit
description: "Audit the seven claimants on an LLM call's context window, set a working ceiling, and cut in the right order. Use when prompts grow, agents drift, or token bills surprise you."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [context-engineering, tokens, cost, build]
    related_skills: [prompt-suite-versioning, agent-loop-safety]
    program_weeks: [6]
---

# Context Budget Audit

## 1 · Purpose

Make the context window a managed budget, allocated, measured, and alerted, instead
of an invisible resource that fails silently when it runs out.

## 2 · When to use

- Designing any new LLM call or agent step.
- When an agent "forgets" instructions it was given earlier (the classic symptom).
- When token cost or latency climbs without a quality gain.

## 3 · Inputs

- The model's advertised context limit (from its card or API docs).
- One real captured request (log, trace, or print of the assembled messages).
- The actual tokenizer for the model, or `tiktoken`/the provider's usage field.

## 4 · Procedure

1. Set the **working ceiling**: 80% of the advertised limit. The last 20% is
   headroom you never plan against, models degrade near the wall.
2. Measure, do not estimate, the seven claimants with the real tokenizer:
   system instructions, tool schemas, durable memory, conversation history,
   retrieved evidence, scratchpad/plan state, and the reservation for the model's
   own output.
3. Write the budget table: claimant × tokens × percent of ceiling. Total must be
   under 100% with output space reserved as a real line item.
4. Order the material: stable content first (cache-friendly), background in the
   middle, decisive evidence last, next to the instruction it decides.
5. Set the compaction policy for anything that grows: summarize older turns, keep
   decisions and commitments, drop scaffolding. Tier every claimant as pinned,
   compressible, or disposable.
6. Add the runtime guard: log `ctx=used/ceiling` on every call; alert above 90%.
7. When over budget, cut in this order, disposable history first, then
   compressible memory, then retrieved evidence (retrieve less, rerank harder).
   Never cut the output reservation or the decisive evidence last-mile.
8. Re-measure after the cut and record both budgets in the design note.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "The window is huge; budgeting is premature." | Huge windows still fail silently, "lost in the middle" does not throw an error. |
| "I'll estimate tokens by eye." | Four characters per token is a folk average, wrong per model and per language. Tokenize for real. |
| "Compaction loses information." | Unbounded growth loses the instruction the agent stops honoring. Compaction chooses what to keep. |
| "The API will error if we're over." | Some APIs truncate silently. The 90% alert is the only honest signal. |

## 6 · Red flags

- Nobody can say how many tokens the system prompt costs.
- History grows unbounded between two log lines.
- Retrieved chunks are appended, never re-ranked or trimmed.
- The output reservation is zero, the model's answer gets whatever is left.

## 7 · Verify

- A budget table exists with measured (not estimated) token counts for all seven
  claimants, totaling under the working ceiling.
- The runtime log shows `ctx=used/ceiling` per call.
- A compaction or tiering policy is named for every growing claimant.

## 8 · ZoroLogistics example

Week 6's extraction call against an 8,000-token working ceiling: system+schema 78,
document ~123, history 0 (single-shot), output reservation 1,500. The audit catches
the real risk early, a later version that threaded documents through a shared
session pushed history to 4,000 and silently dropped the null rule. The `ctx=` log
line is what made the regression visible in minutes instead of at the weekly review.

---
© 2026 Zorost Intelligence LLC · zorost.com
