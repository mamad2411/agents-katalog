# Data Analysis — Requirements Discovery and Quality Assessment

## Summary

**One-sentence:** BA-grade data analysis pipeline (purpose → elements → model → quality → rules) producing a data dictionary, six-dimension quality assessment, and validation/derivation/default/constraint/uniqueness rule set linked to requirements.

**One-paragraph:** Data Analysis in the BA context identifies what data the business needs, how it is structured, where it comes from and goes, its quality characteristics, and the rules governing it. The process runs five steps: identify data needs, define data elements, create a data model (conceptual → logical → physical), analyze data quality across six dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), and define data rules (validation, derivation, default, constraint, uniqueness). Output is a data dictionary and data requirements document linked to the specification.

**Ефективно для:**

- BA discovery, де треба перетворити vague stakeholder ask на quantified requirement з даними.
- Прод-готових data dictionary та data quality assessment перед спецою фічі.
- Reconciliation двох конфліктних звітів — читаємо обидва визначення, потім запускаємо третій query.
- Hand-off контракту з data team замість невизначеного Slack ping.

## Applies If (ALL must hold)

- Pre-spec discovery: profiling existing tables to convert a vague stakeholder assertion into a quantified requirement.
- Sizing a candidate feature: counts to confirm population, frequency, business value before backlog entry.
- Reconciling conflicting stakeholder data reports by reading both definitions and running a third query.
- Generating evidence packs for steering committees with sourced numbers and definition footnotes.
- Hand-off contract with the data team: drafting a data-request.md instead of an open-ended Slack ask.

## Skip If (ANY kills it)

- Statistical inference / A/B testing — analytics-engineer territory; BA stops at descriptive statistics and basic segmentation.
- Production data pipeline authoring — promotion to dbt models requires engineering review.
- Direct write access to source systems — BA queries are read-only.
- Heavily regulated PII without a DPIA — require synthetic/redacted environments.
- Replacing a certified source-of-truth metric with an ad-hoc calculation — reference it, never recompute.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Business question | Markdown / ticket | stakeholder |
| Source system catalog | JSON / Markdown | data platform |
| Read-only DB credentials | env | infra |
| Certified metric registry | YAML | analytics-engineering |
| Sample volume / cycle / cost data | CSV / JSON | system logs |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/elicitation-techniques` | Source the business question before any query. |
| `pro/ba/business-analyst/glossary-management-living-doc` | Anchor every data element to a canonical glossary term. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sql-stub-drafting` | haiku | Mechanical SELECT/COUNT skeletons. |
| `quality-dimension-scoring` | sonnet | Light judgement on 6 dimensions. |
| `data-rule-extraction` | sonnet | Reads ER + spec, emits validation/derivation rules. |
| `metric-reconciliation` | opus | Deep cross-source dispute reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-dictionary.md.j2` | One row per data element: name, type, source, owner, quality, scope. |
| `templates/data-dictionary.md` | One row per data element: name, type, source, owner, quality, scope. Generated from `templates/data-dictionary.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/data-quality-assessment.md.j2` | Six-dimension scoreboard with thresholds. |
| `templates/data-quality-assessment.md` | Six-dimension scoreboard with thresholds. Generated from `templates/data-quality-assessment.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/data-requirements.md.j2` | BR-linked data requirements: source, transformation, target. |
| `templates/data-requirements.md` | BR-linked data requirements: source, transformation, target. Generated from `templates/data-requirements.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable data dictionary. |
| `templates/_smoke-test.md` | Minimum viable data dictionary. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-data-analysis.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[data-driven-requirements]]
- [[glossary-management-living-doc]]
- [[requirements-documentation]]
- [[interface-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
