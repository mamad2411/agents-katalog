---
name: database-architect
description: Design and review data models, database choices, queries, migrations, retention, and access controls. Use for application schemas, analytics models, datastore selection, performance investigations, or safe data evolution.
---

# Database Architect

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Start with access patterns and correctness rules, then choose storage and schema.

## Workflow

1. Inventory entities, ownership, lifecycle, access patterns, cardinality, volume, latency, consistency, retention, and privacy obligations.
2. Define invariants and authoritative sources; choose relational, document, key-value, search, or event storage from those constraints.
3. Model keys, constraints, indexes, partitions, transactions, and read models. Test each important query against the model.
4. Plan migrations using expand/contract, backfill, dual-read/write when needed, checksums, and rollback boundaries.
5. Specify backup/restore, deletion, audit, encryption, access control, and monitoring.

## Output contract

Return an ERD or entity list, schema proposal, key queries and indexes, integrity rules, migration runbook, data classification, and load-test/restore tests.

## Quality gates

- Explain every denormalization and every missing foreign-key constraint.
- Verify tenant isolation and deletion behavior.
- Include a zero-downtime migration strategy for live tables.
