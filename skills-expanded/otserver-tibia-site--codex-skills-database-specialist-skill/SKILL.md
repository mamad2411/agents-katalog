---
name: database-specialist
description: Use this skill when the task centers on database design or behavior: schema modeling, SQL, indexes, constraints, migrations, query tuning, data integrity, transactional logic, or tradeoffs across engines such as SQLite, PostgreSQL, and MySQL.
---

# Database Specialist

## Overview

This skill is for reasoning about databases with emphasis on schema quality, integrity, performance, and operational safety.

## When To Use

Use this skill when the user asks for work involving:

- Relational schema design and entity relationships
- SQL queries, joins, aggregations, filtering, and performance analysis
- Index strategy, constraints, uniqueness, and data integrity
- Migrations, backfills, and safe data evolution
- Engine tradeoffs across SQLite, PostgreSQL, MySQL, or similar systems

## Working Style

- Understand data access patterns before proposing schema or index changes.
- Prefer explicit constraints in the database when correctness depends on them.
- Evaluate reads, writes, cardinality, and growth expectations together.
- Distinguish clearly between application-layer validation and database-layer guarantees.
- Treat destructive migrations and data rewrites as high-risk operations.

## Implementation Rules

- New indexes should be justified by actual query paths, not guesswork.
- Schema changes must consider backward compatibility and migration order.
- Denormalization should only be introduced with a clear read-performance reason.
- Large data changes should be planned to avoid long locks or irreversible failures.
- Queries should be readable first, then optimized with evidence.

## Review Checklist

- Does the schema reflect the business rules accurately?
- Are key constraints enforced at the database layer?
- Will the proposed queries scale for expected usage?
- Is the migration path safe for existing data?
- Are engine-specific assumptions called out explicitly?

