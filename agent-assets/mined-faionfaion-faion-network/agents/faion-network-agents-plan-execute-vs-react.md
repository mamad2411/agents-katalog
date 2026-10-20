# Plan-Execute vs ReAct

## Summary

**One-sentence:** Produces an agent-loop-spec selecting Plan-Execute, ReAct, or Hybrid (top-level plan + per-step ReAct) based on horizon, adaptability, and audit requirements.

**One-paragraph:** Plan-Execute front-loads reasoning into an auditable plan but cannot adapt; ReAct adapts step-by-step but produces no auditable trace. Hybrid (top-level plan + per-step ReAct) is what Claude Code, LangGraph supervisor+workers, and the deep-agents pattern all converge on. This methodology emits a deterministic spec picking the loop type per drivers, plus the max_turns and replan policy.

**Ефективно для:** team running multi-step agents whose runs either wander (pure ReAct on long horizons) or fail at step 2 (pure Plan-Execute on exploratory goals).

## Applies If (ALL must hold)

- Designing an agent loop for a new task.
- Diagnosing existing loops that wander or lock in early.
- Choosing between LangGraph plan-execute, ReAct, or supervisor+workers.
- Horizon-bounded budget per run is required.

## Skip If (ANY kills it)

- Single-tool one-shot call — no loop needed.
- Pure RAG retrieval without iteration.
- Throwaway script with no audit requirement.
- Goal fits in a single LLM turn.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `task-spec.yaml` | {goal, known_substeps, horizon, audit_required, adaptability_needed} | operator |
| `max_turns_budget` | integer | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[max-turns-circuit-breaker]] | ReAct loops MUST cap turns. |
| [[subagent-as-context-firewall]] | Hybrid spawns sub-loops as subagents. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: plan when predictable, react when exploratory, hybrid long-horizon, max-turns mandatory, separate plan from execute, slim state doc. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agent-loop spec. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: pure ReAct on 30-step goal, blind plan-execute, no max_turns, plan-inside-execution, fat state. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: parse task → compute drivers → walk tree → set max_turns → emit spec. | ~700 |
| `content/05-examples.xml` | recommended | One worked Plan-Execute + one ReAct + one Hybrid spec. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks plan-execute / react / hybrid from drivers. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_task_spec` | haiku | Mechanical YAML→typed dict. |
| `classify_drivers` | sonnet | Subjective: is the task truly predictable? |
| `audit_for_loop_drift` | opus | Catching infinite loops in existing traces. |
| `emit_loop_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/agent-loop-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/agent-loop-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/agent-loop-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum task spec (predictable, 5-step). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-plan-execute-vs-react.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[subagent-as-context-firewall]]
- [[max-turns-circuit-breaker]]
- [[multi-agent-production-bus]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `adaptability_needed` (true → ReAct), then on `horizon > 10 AND mixed_predictability` (true → Hybrid), default Plan-Execute. Each leaf cites a rule id.
