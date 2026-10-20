# Schema Version Pinning

## Summary

**One-sentence:** Produces a schema-evolution spec pinning JSON-schema versions per agent + migration policy + breaking-change protocol so deployed agents survive schema drift.

**One-paragraph:** Tool-use and structured-output schemas drift over time. Agents deployed against v1 schemas crash silently when v2 ships. This methodology emits a versioning spec: schemas carry semver, agents pin against minor versions, migration tools convert recorded calls forward.

**Ефективно для:** team whose deployed agents start emitting validation errors after a routine schema 'cleanup'.

## Applies If (ALL must hold)

- Multiple agents share a tool-use schema.
- Schema changes more than once per quarter.
- Production deploys not redeployed in lockstep.

## Skip If (ANY kills it)

- Single-tenant agent, schema co-deployed.
- Schema frozen indefinitely.
- Prototype with no production runs.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `schemas/` | directory of versioned JSON schemas | repo |
| `agent-deploys.yaml` | list of {agent, pinned_version} | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-semver-in-schema; r2-pin-minor; r3-breaking-change-protocol; r4-recorded-call-migration; r5-version-in-tool-call. | ~900 |
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
| `templates/schema-version-pinning-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/schema-version-pinning-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/schema-version-pinning-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-schema-version-pinning.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
