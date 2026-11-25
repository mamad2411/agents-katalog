---
name: sql-from-question
description: Turns a plain-language question into a SQL query that fits your real schema, explains each part and runs only read-only statements.
disable-model-invocation: true
---

Write SQL that answers this question: $ARGUMENTS

1. Find the schema before writing anything: migrations, `schema.sql`, ORM models or Prisma/Drizzle files. If a database connection is documented, use `\d` or `information_schema` to confirm. Note the SQL dialect.
2. Restate the question in one sentence and list the tables and columns you will use, with the join keys. If the question is ambiguous (which date, which status counts as paid), list the choices and pick the likeliest, saying so.
3. Write the query with explicit joins, readable aliases, and filters that handle nulls and time zones. Use CTEs for steps.
4. Explain each clause in one line each.
5. Warn about cost: missing indexes on filtered columns, huge tables, no LIMIT.

Only SELECT or EXPLAIN may be run, never INSERT, UPDATE, DELETE or DDL. Show the query and ask: "Run it read-only?" If yes, run it with a row limit and interpret the result in plain words.
