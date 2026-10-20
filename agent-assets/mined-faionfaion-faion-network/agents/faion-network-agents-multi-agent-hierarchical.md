# Hierarchical Manager-Worker Multi-Agent Pattern

## Summary

**One-sentence:** Generates a manager-worker multi-agent runner where one opus-class manager produces a typed JSON assignment plan, dispatches each subtask to a stateless worker, and synthesizes results into a final structured output.

**One-paragraph:** The manager is the only agent that holds the overall task context. It produces a `Plan` (typed JSON: assignments[] of `{worker_name, subtask, deps[]}`), the orchestrator dispatches subtasks to stateless workers respecting `deps[]`, gathers results, and feeds them back to the manager for synthesis. Workers never talk to each other — all communication routes through the manager. Cycle detection runs at plan-time; partial-failure policy is declared upfront (`abort`, `degrade`, `retry`).

**Ефективно для:** інженера, який ділить велике завдання на ролі — менеджер бачить ціле, воркери виконують свою частину; найбільш audit-friendly з multi-agent патернів.

## Applies If (ALL must hold)

- Task decomposes into ≥2 specialist subtasks (researcher / coder / reviewer, etc.).
- Worker roles are non-overlapping AND workers can be stateless (no shared memory needed).
- Manager can produce a structured assignment plan — task shape is knowable from the brief.
- Auditability matters — each subtask + result row goes into the trace.
- Latency budget tolerates 2 extra round-trips (manager plan + synthesis) on top of worker calls.

## Skip If (ANY kills it)

- Task fits in a single context window — manager overhead is wasted.
- Workers need shared mutable state — switch to `collaborative` (blackboard) instead.
- Latency under 5 s — plan + dispatch + synthesis adds ~3 round-trips minimum.
- Free-form dynamic exploration needed — switch to `conversational`.
- Workers' roles overlap significantly — `multi-agent-basics` will flag overlap during spec validation.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Validated multi-agent spec | YAML with `pattern: hierarchical` | `multi-agent-basics` |
| Worker roster + system prompts | list of `{name, role, model, system_prompt}` | spec |
| Top-level task statement | string | spec.task |
| Partial-failure policy | one of `abort`, `degrade`, `retry` | ops handbook |
| Per-agent budgets | int per worker | spec.agents |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/multi-agent-basics` | Upstream spec. |
| `geek/ai/ai-agents/schema-version-pinning` | Plan + result envelope carry `schema_version`. |
| `geek/ai/ai-agents/role-specialized-models` | Manager on opus, workers on sonnet/haiku per cognitive role. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: typed Plan schema, stateless workers, plan-time cycle check, declared failure policy, per-worker timeout | ~750 |
| `content/02-output-contract.xml` | essential | JSON Schema for `Plan` + `WorkerResult` + final `Synthesis` envelope; valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: cycles in plan, workers talking to workers, manager-also-worker, missing failure policy, no per-worker timeout | ~700 |
| `content/04-procedure.xml` | medium | 6-step build: validate spec → manager plans → cycle check → dispatch → gather → synthesize | ~800 |
| `content/06-decision-tree.xml` | essential | Pick hierarchical vs sequential vs collaborative vs conversational based on plan-knowability + audit need | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Manager plan + synthesis | opus | Decomposition + cross-result synthesis are the strongest reasoning steps. |
| Worker execution | sonnet | Reliable focused execution within a single role. |
| Trivial workers (classify / format) | haiku | Cost-saver per role-specialized-models. |
| Cycle-check on plan | code (no LLM) | Plan-time graph check; deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hierarchical_runner.py` | Synchronous manager-worker runner: typed JSON plan with one repair attempt, Kahn cycle check, per-worker timeout, abort/degrade/retry policy, Synthesis envelope with trace. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-basics]] — upstream spec.
- [[multi-agent-design-patterns]] — selects this pattern.
- [[multi-agent-production-bus]] — ships hierarchical via async message bus.
- [[role-specialized-models]] — manager=opus, workers=sonnet/haiku.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether hierarchical is the right pattern: pick it when the task is decomposable into non-overlapping roles with stateless workers AND audit matters. Pick sequential when the chain is linear and no manager judgement is needed; pick collaborative when workers need shared mutable state; pick conversational when the plan is unknowable upfront. Run it before scaffolding.
