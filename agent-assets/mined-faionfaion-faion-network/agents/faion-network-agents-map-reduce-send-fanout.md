# Map Reduce Send Fanout

## Summary

**One-sentence:** Designs a map-reduce fan-out (Send / ParallelAgent / asyncio.gather) with concurrency cap, idempotency, and atomic super-step semantics, emitting a fanout-spec.

**One-paragraph:** Dynamic fan-out over a list lets you map per-item LLM work, but rate-limit cliffs hit fast and a single branch failure fails the whole super-step atomically — so non-idempotent work double-applies on retry. This methodology turns a fan-out profile (item count, per-item work, mutates_shared_state) into a deterministic fanout-spec: framework, concurrency cap, reducer, idempotency guarantee.

**Ефективно для:** solopreneur parallelising LLM work over a list (e.g. summarise 100 docs) without nuking the budget.

## Applies If (ALL must hold)

- Same work applied to a list of items.
- Per-item work is LLM/HTTP-bound, not CPU.
- Items are independent — no shared mutable state.
- ≥1 fan-out primitive available (Send, ParallelAgent, asyncio.gather).
- Result merge is well-defined (concat, sum, dict-merge).

## Skip If (ANY kills it)

- Single item — no fan-out needed.
- Items share mutable state — use a queue + workers, not fan-out.
- Per-item work is non-idempotent (e.g., billing) — fan-out retries double-charge.
- Item count <3 — overhead exceeds benefit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `fanout-profile.yaml` | item_count, per_item_work_kind, mutates_shared_state, idempotent, framework | author |
| `Per-item function` | Python async or sync | code |
| `Reducer` | function or annotated type | code |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[max-turns-circuit-breaker]] | Pair with turn cap. |
| [[manifest-then-fetch]] | Per-item outputs may be large. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rule r1 for concurrency cap (≤20), idempotency, atomic super-step, reducer choice, plus the three tree-branch rules (r-advanced, r-default-high, r-default-low) fixing cap, waves and shared-sink handling per tier. | ~1100 |
| `content/02-output-contract.xml` | essential | fanout-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | No cap, non-idempotent branch, hidden shared state, partial-success swallowed. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step design procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/fanout-profile.yaml` | Input. |
| `templates/fanout-spec.md.j2` | Output. |
| `templates/fanout-spec.md` | Output. Generated from `templates/fanout-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/fanout.py` | Working Send / gather wrapper. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-map-reduce-send-fanout.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-workflows]]
- [[max-turns-circuit-breaker]]
- [[manifest-then-fetch]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on mutates_shared_state (true → reject fan-out, recommend queue+workers), then on idempotent (false → reject or wrap in idempotency-key store), then on framework (langgraph → Send; adk → ParallelAgent; plain → asyncio.gather + Semaphore). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
