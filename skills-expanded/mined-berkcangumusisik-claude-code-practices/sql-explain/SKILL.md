---
name: sql-explain
description: Explains a SQL query in plain language and suggests optimizations
argument-hint: <sql-query-or-file>
user-invocable: true
allowed-tools: Read Bash
effort: low
---

## SQL Query Explanation

Query: **$ARGUMENTS**

1. If a file path was given, read the file. If a query was pasted, use it directly.

2. **Plain English explanation:**
   - What tables are involved?
   - What data is being filtered/joined?
   - What is the final result set?
   - Walk through execution order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER → LIMIT)

3. **Potential issues:**
   - Missing indexes on WHERE/JOIN columns
   - Cartesian products (missing JOIN condition)
   - `SELECT *` when specific columns would do
   - Subqueries that could be CTEs or JOINs
   - Functions on indexed columns preventing index use (`WHERE LOWER(email) = ...`)

4. **Optimization suggestions** (with rewritten query):
   - Indexes to add (with `CREATE INDEX` statement)
   - Query rewrite if applicable
   - For Postgres/MySQL: suggest running `EXPLAIN ANALYZE`

5. Estimate complexity: O(n), O(n log n), O(n²) roughly.
