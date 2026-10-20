# Role-Specialized Models

## Summary

**One-sentence:** Produces a model-routing spec assigning each agent role (planner/coder/critic/summarizer) to the best-fit model rather than using one frontier model for everything.

**One-paragraph:** Using opus for every agent role is wasteful; using haiku for every role is reckless. Role-specialised routing maps each role to its best-fit model (planner=opus, coder=sonnet, summarizer=haiku, etc.) based on the role's competence floor and cost profile. This methodology emits a spec.

**Ефективно для:** team running multi-role agents whose monthly bill is dominated by opus calls on roles where sonnet would suffice.

## Applies If (ALL must hold)

- Multi-role agent with >= 3 distinct roles.
- Cost optimization required.
- Quality benchmarks exist per role.

## Skip If (ANY kills it)

- Single-role agent.
- Quality constraints make routing risky.
- All roles are top-tier (e.g., reasoning-heavy).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `role-inventory.yaml` | list of {role, competence_floor, expected_call_volume} | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-competence-floor; r2-no-frontier-default; r3-per-role-eval; r4-drift-recheck; r5-fallback-to-stronger. | ~900 |
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
| `templates/role-specialized-models-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/role-specialized-models-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/role-specialized-models-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-role-specialized-models.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
