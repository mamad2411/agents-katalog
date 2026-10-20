# Data Analysis

## Summary

**One-sentence:** Identify, define, and document data needs before system development — data dictionary, conceptual/logical model, quality dimensions, and business rules as a versioned contract.

**One-paragraph:** Pre-development discovery for data entities: harvest sources, build a normalized data dictionary, derive conceptual and logical models, assess data quality on six dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), and surface business rules. Output is a `spec` artefact: data_dictionary, ERD, and quality_baseline. Becomes the contract developers, architects, and integration teams build against.

**Ефективно для:**

- Pre-database design коли немає shared data dictionary.
- ETL / integration layer між двома+ системами.
- Pre-migration scope assessment.
- Data-quality baseline для GDPR / HIPAA compliance.

## Applies If (ALL must hold)

- Starting database or integration design and no shared data dictionary exists.
- Reports from different systems show conflicting figures for the same metric.
- Building ETL/integration layer between two or more systems.
- Compliance requires documented data ownership and classification.

## Skip If (ANY kills it)

- Exploratory analytics spike where the data model will be thrown away.
- Event-streaming architectures with schema-on-read by design.
- Frontend-only features with no new data persistence.
- Authoritative data dictionary already exists and is current — extend, do not duplicate.
- Tiny CRUD apps with fewer than 10 entities — ceremony costs more than it saves.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-system inventory | YAML / Markdown table | architecture team |
| Sample data exports | CSV / Parquet | data engineering |
| Compliance classification rubric | doc | DPO / legal |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[interface-analysis]] | Sibling that maps the integration surface this data lives behind |
| [[ba-planning]] | Upstream plan that scopes data-analysis effort + governance |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: every field typed + sourced, six DQ dimensions scored, business rules as predicates, owner per entity, version pinned | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: free-text type, anonymous owner, missing DQ baseline, single-system bias | 850 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example: customer entity across CRM + billing | 700 |
| `content/06-decision-tree.xml` | essential | Routing on system count + DQ baseline status | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `field_normalization` | haiku | Mechanical mapping CSV header → field row. |
| `model_derivation` | sonnet | Conceptual → logical → physical with constraints. |
| `dq_assessment` | opus | Multi-dimensional quality scoring with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-dictionary.md.j2` | Markdown skeleton with field/source/type/owner/DQ columns |
| `templates/data-dictionary.md` | Markdown skeleton with field/source/type/owner/DQ columns Generated from `templates/data-dictionary.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable data-dictionary fixture |

| `templates/data-quality-assessment.md.j2` | DQ baseline skeleton scoring six dimensions per entity |
| `templates/data-quality-assessment.md` | DQ baseline skeleton scoring six dimensions per entity Generated from `templates/data-quality-assessment.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/data-requirements.md.j2` | data requirements skeleton (per-feature entity + field shortlist) |
| `templates/data-requirements.md` | data requirements skeleton (per-feature entity + field shortlist) Generated from `templates/data-requirements.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[interface-analysis]]
- [[business-process-analysis]]
- [[ba-planning]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (source-system count, DQ baseline presence, compliance flag) to the right rule. Use when in doubt whether the dictionary is ready to hand off to developers.
