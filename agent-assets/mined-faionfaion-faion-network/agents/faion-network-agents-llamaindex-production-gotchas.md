# Llamaindex Production Gotchas

## Summary

**One-sentence:** Hardens a LlamaIndex deployment (async loop, retriever concurrency, ReActAgent error handling, eval cost, callbacks) and emits a hardening-record.

**One-paragraph:** LlamaIndex has several non-obvious production failure modes: SubQuestionQueryEngine.query() blocks async loops, QueryFusionRetriever opens unbounded concurrent LLM calls, ReActAgent does not auto-recover from tool errors, and evaluation methods consume significant tokens. This methodology turns a deployment profile into a deterministic hardening-record patching each gotcha.

**Ефективно для:** solopreneur whose LlamaIndex bot worked in dev and now leaks money in prod.

## Applies If (ALL must hold)

- Using LlamaIndex in production (or about to).
- App is async (FastAPI / asyncio).
- ≥1 of the known gotchas is in your stack (sub-question engine, fusion retriever, ReAct, eval).
- Cost or latency budget is bounded.
- Observability is wired (or about to be).

## Skip If (ANY kills it)

- Notebook / not in production.
- Custom non-LlamaIndex stack — gotchas don't apply.
- App is fully sync (no async event loop to block).
- No tools, no eval — narrower hardening sufficies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `deployment-profile.yaml` | async, components_used (subq|fusion|react|eval), cost_cap_per_turn_usd, observability_target | author |
| `App entrypoint` | Python module | code |
| `Callback handler stub` | for tracing | config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Foundations. |
| [[llamaindex-agents-eval]] | Eval cost rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for async usage, concurrency caps, agent error catch, eval sampling, callbacks. | ~1400 |
| `content/02-output-contract.xml` | essential | hardening-record schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Blocked event loop, unbounded fusion, swallowed tool error, eval cost spiral. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step hardening procedure. | ~800 |
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
| `templates/deployment-profile.yaml` | Input. |
| `templates/hardening-record.md.j2` | Output. |
| `templates/hardening-record.md` | Output. Generated from `templates/hardening-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/patches.py` | Working async + concurrency + error patches. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-production-gotchas.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-hybrid-retrieval]]
- [[llamaindex-agents-eval]]
- [[langchain-production-patterns]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on async (true → require aquery + non-blocking patches), then on components_used (subq → wrap; fusion → cap; react → try/except), then on cost cap. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
