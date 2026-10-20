# Data Modeling

## Summary

**One-sentence:** Build any persistent schema in three sequential passes: conceptual (entities/relationships) → logical (attributes, keys, 3NF, tech-agnostic) → physical (tables, types, indexes, engine-specific).

**One-paragraph:** Data modeling is a three-pass discipline: conceptual (business terms only), logical (attributes + cardinality + 3NF, still tech-agnostic), physical (engine-specific types, indexes, partitions). Output is a schema spec at each level + migration plan, blocking the common failure of jumping straight to DDL.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Designing a new schema OR migrating > 5 tables.
- Workload has cross-entity queries with > 3 joins, OR data growth > 100M rows in 12 months.
- Domain experts available for the conceptual pass.

## Skip If (ANY kills it)

- Tiny app with < 5 tables and < 100K rows; build straight to DDL.
- ORM-generated schema with no analytics or hot-path query.
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain glossary | spreadsheet/markdown | domain expert |
| Top 10 queries by frequency | list with SLO | tech lead |
| Chosen DB engine | name + version | database-selection output |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/database-selection` | Provides the engine the physical pass targets. |
| `solo/dev/software-architect/arch-pattern-ddd` | Conceptual pass shares aggregates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for the 3-pass spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: glossary → conceptual → logical → physical → indexes → migration | ~900 |
| `content/05-examples.xml` | medium | Worked example: 3-pass schema for an Ordering bounded context | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-conceptual` | sonnet | Per-aggregate entity-relationship synthesis. |
| `design-indexes` | sonnet | Per-query index plan. |
| `audit-cross-team` | opus | Spot inconsistent term usage across teams. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema-3-pass.md.j2` | Three-pass schema spec: conceptual + logical + physical. |
| `templates/schema-3-pass.md` | Three-pass schema spec: conceptual + logical + physical. Generated from `templates/schema-3-pass.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pg-standard-table.sql` | PostgreSQL standard 3NF table skeleton with PK + audit columns + indexes. |
| `templates/pg-junction-table.sql` | PostgreSQL many-to-many junction table with composite PK + FK cascade rules. |
| `templates/mongo-schema.js` | MongoDB collection schema with `$jsonSchema` validator + indexes. |
| `templates/cassandra-table.cql` | Cassandra/ScyllaDB wide-row table: one-table-per-query + partition + clustering keys. |
| `templates/data-vault-hub.sql` | Data Vault 2.0 hub table skeleton with business-key + load-date + record-source. |
| `templates/scd-type2.sql` | Slowly-Changing-Dimension Type 2 table with effective_from/effective_to + current flag. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-data-modeling.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[database-selection]]
- [[arch-pattern-ddd]]
- [[caching-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
