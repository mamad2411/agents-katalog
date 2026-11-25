---
name: sql-modeller
description: Design normalised relational schemas with the right keys, constraints and indexes, and write the migration that gets there safely. Use when modelling data in a relational database rather than querying it.
license: MIT
compatibility: Targets PostgreSQL; most guidance applies to any SQL database.
allowed-tools: Read Write Bash
metadata:
  category: data
---

# Relational modelling

Put the rules in the database, where they hold regardless of which application
writes the row.

## Keys

Choose one key strategy and apply it consistently. A natural key is only a key
if it can never change.

## Constraints

Express what must be true as a constraint: not null, unique, check and foreign
key. An application-level check is a convenience, not a guarantee.

## Indexes

Add an index because a measured query needs it. Every index costs write
throughput and storage.

## Migrations

Write migrations that are reversible, and run them against a copy of production
data before running them against production.
