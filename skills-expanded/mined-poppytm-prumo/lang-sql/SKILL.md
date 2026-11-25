---
name: lang-sql
description: SQL dialect precision, mandatory parameterization, explicit projection (prohibit SELECT *), transactional isolation, and index safety.
---

# SQL Engineering & Safety Contract

## 1. Parameterization & Zero Injection
- Raw SQL string concatenation or interpolation is strictly prohibited.
- All runtime values must be bound via parameterized query placeholders (\`$1\`, \`?\`, \`:name\`).
- Prohibit dynamic \`EXEC\` or \`EXECUTE\` with concatenated query strings.

## 2. Query Discipline & Performance
- Prohibit \`SELECT *\` in production application queries. Always specify explicit column lists to prevent memory bloat and schema drift crashes.
- All high-frequency filtering columns (\`WHERE\`), sorting columns (\`ORDER BY\`), and join keys must be backed by appropriate indexes.
- Identify and eliminate N+1 query patterns using batch joins or database aggregation.

## 3. Schema Migrations & Integrity
- All migrations must be deterministic, idempotent, reversible (\`up\` and \`down\`), and wrapped in transactional blocks.
- Unchecked destructive migrations (\`DROP TABLE\`, \`DROP COLUMN\`) require formal review, backup verification, and multi-phase zero-downtime deprecation.
- Enforce constraints (\`NOT NULL\`, \`FOREIGN KEY\`, \`CHECK\`, \`UNIQUE\`) at the database level.\n