# Reasoning-First Architectures

## Summary

**One-sentence:** Produces an agent-architecture spec selecting ReAct, Tree-of-Thought, Reflexion, or Planning-Loop based on task complexity, branching needs, and budget.

**One-paragraph:** Agents that act without thinking produce hallucinated tool calls and brittle plans. Reasoning-first architectures (ReAct, ToT, Reflexion, Planning Loop) explicitly separate thinking from acting. This methodology picks the right one per drivers: complexity, branching, replan budget.

**Ефективно для:** team running agents that act too fast and fail at branching tasks; their traces show no thinking step.

## Applies If (ALL must hold)

- Designing a new agent for complex multi-step tasks.
- Existing agents fail on branching or recovery from errors.
- Reasoning models (o1, claude-extended-thinking) are available.

## Skip If (ANY kills it)

- Simple lookup or single-tool tasks.
- Latency-critical with <100ms budget.
- Closed deterministic workflows.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `task-profile.yaml` | {complexity, branching, error_recovery_needed, budget_per_run} | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-thought-before-action; r2-tot-when-branching; r3-reflexion-when-recovery; r4-planning-loop-long-horizon; r5-budget-cap. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with detector + repair. | ~700 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure. | ~600 |
| `content/05-examples.xml` | recommended | Worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision branches mapped to rule ids. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_input` | haiku | Mechanical. |
| `classify_drivers` | sonnet | Subjective tradeoffs. |
| `audit_output` | opus | Cross-cutting subtleties. |
| `emit_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/reasoning-first-architectures-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/reasoning-first-architectures-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/reasoning-first-architectures-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-reasoning-first-architectures.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
