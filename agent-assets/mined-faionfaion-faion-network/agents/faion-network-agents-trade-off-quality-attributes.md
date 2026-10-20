# Quality-Attribute Trade-off Analysis

## Summary

**One-sentence:** ATAM-style trade-off analysis between competing quality attributes (perf, security, cost, maintainability, availability): scenario-pair conflicts, sensitivity points, and resolution rules.

**One-paragraph:** ATAM-style trade-off analysis between competing quality attributes (perf, security, cost, maintainability, availability): scenario-pair conflicts, sensitivity points, and resolution rules. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Architecture decision affecting > 2 quality attributes with documented conflict.
- Post-incident analysis where SLO miss is rooted in an unstated QA trade-off.
- ATAM-style review prepared for an external audit or buyer.
- Output produces `report` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Architecture decision affecting > 2 quality attributes with documented conflict.
- Post-incident analysis where SLO miss is rooted in an unstated QA trade-off.
- ATAM-style review prepared for an external audit or buyer.

## Skip If (ANY kills it)

- Single-attribute decision (e.g. perf only) — use that attribute's spec instead.
- Pre-revenue prototype where QA constraints are not yet contractual.
- Tradeoff already documented in a current report — review on cadence only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| QA scenarios per attribute | table | team / SRE / sec |
| SLO numbers per attribute | table | SRE |
| Architecture diagram | C4 L2 minimum | architect |
| Stakeholder list with attribute ownership | table | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[quality-attributes]] | QA scenarios are the input to this analysis. |
| [[trade-off-decision-methods]] | ATAM may be the chosen method here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-scenario-pairs` | sonnet | Pair conflicting scenarios across attributes. |
| `locate-sensitivity-points` | opus | Detect architectural elements where small change moves multiple attributes. |
| `define-resolution-rules` | sonnet | Author quantified resolution rules per conflict. |
| `publish-report` | haiku | Compose ATAM-style report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tradeoff-report.md.j2` | ATAM-style report skeleton. |
| `templates/tradeoff-report.md` | ATAM-style report skeleton. Generated from `templates/tradeoff-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/scenario-pairs.json` | Scenario-pair payload. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-quality-attributes.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[quality-attributes]]
- [[trade-off-decision-methods]]
- [[performance-architecture]]
- [[security-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (scenarios, SLOs, diagram, stakeholders)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
