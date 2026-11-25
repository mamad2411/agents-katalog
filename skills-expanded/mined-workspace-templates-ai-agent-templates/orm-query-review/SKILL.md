---
name: orm-query-review
description: "Reviews ORM code for N+1 queries, lazy loading, over-fetching and missing transactions, and proves each finding by counting queries."
---

# ORM query review

Show the SQL the ORM really sends. Judge the code by statements per request, not by how it reads.

## Steps

1. Turn on query logging for the framework in use (Django `connection.queries`, Rails log, Hibernate `show_sql`, SQLAlchemy `echo`, Prisma `log: ['query']`). Run the target request or test and count statements.
2. Find N+1 patterns: a loop that touches a relation, a serializer or template that reads a related field, a property that queries on access. Confirm by seeing one parent query followed by N near-identical queries.
3. Fix with the ORM's eager loading: join or prefetch the relation in the one query that loads the parents. Use batch loading when a join would multiply rows.
4. Find over-fetching: whole rows loaded to read two fields, or entire tables loaded to count or check existence. Select only needed columns; use `count`, `exists` and aggregates in the database, not in memory.
5. Find missing transactions: two or more writes that must succeed together, read-then-write sequences, counters updated in memory. Wrap them in a transaction, and lock the row (`select for update`) or use an atomic update expression when two requests could collide.
6. Look for unbounded queries without limit or pagination, and filters on columns with no index.
7. Re-run and show the statement count before and after.

## Rules

- Never fix a query you have not seen the SQL for.
- Keep fixes local; do not rewrite the data layer.
- Keep transactions short and free of network calls.

## Report

Per finding: file and line, statements before and after, and the change.
