---
name: sql-injection-prevention
description: Finds queries built from strings and rewrites them as parameterized statements, with allowlists for column names, sort order and other identifiers.
---

# SQL injection prevention

Find every query that mixes text and input, and make the input unable to change the query shape.

## Steps

1. Search for query construction with dynamic parts: template strings or `+` near `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`, `LIMIT`; ORM escape hatches (`raw()`, `queryRawUnsafe`, `extra()`, `text()`, `literal()`); stored procedures called with built strings.
2. For each hit, trace where every interpolated value comes from. Skip values that are constants.
3. Values: replace with bound parameters and pass them separately (`?`, `$1`, `:name`, tagged-template helpers). Do not hand-escape quotes.
4. `IN` lists: generate one bound slot per item, or use `= ANY($1)` with an array. Guard against empty lists.
5. Identifiers and keywords cannot be bound. Map input to a fixed object, such as `{ price: "price", newest: "created_at" }`, and reject unknown keys. Direction is `asc` or `desc` only. Cast `LIMIT` and `OFFSET` to bounded integers.
6. `LIKE` patterns: bind the value and escape `%` and `_` when the user should not control wildcards.
7. Check the database account: does the app user need DDL or access to other schemas? Recommend least privilege.
8. Add a test per fixed query using inputs like `' OR 1=1 --` and `1; DROP TABLE x` that must return no extra rows or an error, never a changed result.

## Rules

- Do not rely on input filtering or on stripping quotes.
- Keep behaviour identical for valid input.

## Report

Each query fixed (`path:line`, before, after), identifiers allowlisted, tests, and any query left because it needs a design change.
