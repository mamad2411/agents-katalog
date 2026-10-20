# Generator-Critic Loop with Hard Cap and Delta Exit

## Summary

**One-sentence:** Wraps generation in a Generator-Critic-Generator loop with a hard cap of 3 iterations, exits on critic veto, score plateau, or cap, and uses a cheap model for rubric criticism — capturing 70-95% of the achievable quality lift at a fraction of unbounded reflection cost.

**One-paragraph:** Wrap generation in a Generator → Critic → Generator loop with a hard cap of 3 iterations. Exit on critic veto, plateau (delta &lt; epsilon for two consecutive iterations), or cap. Use cheap models for rubric criticism (style, format, completeness) and same-tier models only for correctness criticism. Unbounded reflection is the most common cost trap in production agent stacks; bounding by three independent stop conditions covers correctness, efficiency, and safety.

**Ефективно для:** codegen-агентів, копірайтингу, структурованої екстракції з рубриками — будь-яких сценаріїв, де є чіткий критерій якості і модель може себе виправити.

## Applies If (ALL must hold)

- Codegen agents that compile/lint/test their own output before returning.
- Copywriting / summarisation with a clear rubric (length, voice, audience).
- Structured extraction where a critic verifies fields and citations.
- Self-correcting RAG where the critic checks the answer against retrieved chunks.

## Skip If (ANY kills it)

- Latency-critical paths (chat visible to users) — the second pass doubles wall time.
- Tool-calling agents where ground truth comes from the tool, not a critic.
- Trivial outputs that consistently pass on iteration 1 — kill the loop.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Generator prompt | Pydantic-bound system prompt | Application code |
| Critic rubric | Structured rubric text | Domain analyst |
| Epsilon (plateau threshold) | Float | Eval-driven config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `embedded-scratchpad-field` | Critic output is a scratchpad + score + should_continue triple. |
| `confidence-thresholded-cascade` | Cheap critic + strong generator is the dual of cheap generator + strong critic. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: three-exit-conditions, no-same-model, structured-should_continue, cap-at-3, cheap-rubric | ~1000 |
| `content/02-output-contract.xml` | essential | Critic output schema + loop trace schema | ~900 |
| `content/03-failure-modes.xml` | essential | Unbounded loops, same-prior generator/critic, threshold-from-score | ~800 |
| `content/06-decision-tree.xml` | essential | Pick rubric vs correctness critic vs split | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generator | sonnet or opus | Task-appropriate strong model |
| Rubric critic | haiku | Constrained classification, no reasoning depth needed |
| Correctness critic | same tier as generator | Catching wrong answers needs the capacity that produces them |

## Templates

| File | Purpose |
|------|---------|
| `templates/critic_schema.py` | Pydantic schema for the critic output (score, should_continue, feedback) |
| `templates/loop.py` | Reference loop with hard cap, delta exit, structured critic |
| `templates/_smoke-test.json` | Minimum valid critic output for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-generator-critic-bounded-loop.py` | Validates a critic output JSON against the schema | After every critic call |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedded-scratchpad-field]]
- [[confidence-thresholded-cascade]]
- [[idempotent-write-tools]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether quality lift on iteration 2 exceeds 2% on the eval. The tree then routes to rubric-only critic (cheap), correctness critic (same tier), or split mixed-critic (cheap rubric first, strong correctness only if rubric passes).
