# Schema Field Order

## Summary

**One-sentence:** Produces a structured-output schema-ordering spec placing reasoning fields BEFORE final answer fields so the model thinks-then-answers within the JSON itself.

**One-paragraph:** When the LLM emits JSON with the final answer field first, it has to commit before reasoning. Reordering so reasoning/scratchpad/analysis fields come BEFORE the answer field forces the model to think first. Quality improves substantially without prompt changes.

**Ефективно для:** team using JSON-schema-constrained outputs whose answer quality plateaus despite better prompts.

## Applies If (ALL must hold)

- Using JSON-schema-constrained outputs (OpenAI strict / Anthropic tool_use).
- Answer quality matters more than latency.
- Schema can be modified.

## Skip If (ANY kills it)

- Free-form completions.
- Latency-critical (reasoning fields add tokens).
- Schema fixed by external contract.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `schema-fields.yaml` | list of {field, role: reasoning|intermediate|answer} | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-reasoning-first; r2-named-reasoning-field; r3-no-final-answer-shortcuts; r4-strict-required; r5-emit-token-cost. | ~900 |
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
| `templates/schema-field-order-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/schema-field-order-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/schema-field-order-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-schema-field-order.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
