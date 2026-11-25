---
name: productize-write-query
description: >-
  Write optimized SQL for a specific dialect with best practices. Use when translating a
  natural language data need into SQL, building a multi-CTE query with joins and aggregations,
  optimizing a large partitioned-table query, or getting Snowflake, BigQuery, Postgres, or
  other dialect syntax.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Write Query

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `write-query`
- **Lifecycle**: Plan
- **Category**: Analytics
- **Primary artifact**: Write Query delivery brief with scope, requirements, priorities, risks, and acceptance criteria

Write a SQL query from a natural-language description, optimized for the user's SQL dialect and use case.

## Argument Hint

`<description of what data you need>`

## Usage

```text
/write-query <description of what data you need>
```

## Extended Reference

Load `references/extended-reference.md` when the request mentions `sql generator`, `bigquery`, `postgres`, `mysql`, `schema diagram`. Use this reference material to sharpen this Productize skill.

## Workflow

### 1. Understand the Request

Parse the user's description to identify:
- Output columns.
- Filters: time ranges, segments, statuses, exclusions.
- Aggregations: counts, sums, averages, rates, distincts.
- Joins and required entities.
- Ordering.
- Limits, top-N, or sample requirements.
- Expected grain: one row per what.

If the request is ambiguous, ask only for the missing detail that changes query correctness.

### 2. Determine SQL Dialect

If not known, ask which dialect they use:
- PostgreSQL, including Aurora, RDS, Supabase, Neon.
- Snowflake.
- BigQuery.
- Redshift.
- Databricks SQL.
- MySQL.
- SQL Server.
- DuckDB.
- SQLite.
- Other.

Use `sql-queries` for dialect-specific syntax, date functions, semi-structured data, performance notes, and debugging.

### 3. Discover Schema

If a warehouse or schema tool is connected:
1. Search for relevant tables.
2. Inspect column names, types, and relationships.
3. Check partition, clustering, sort, or distribution keys.
4. Look for existing views or materialized views.

If no warehouse is connected:
- Ask for table names, schema, or sample rows.
- If the schema is unknown, provide a query template with clearly marked placeholders.

### 4. Write the Query

Structure:
- Use CTEs for multi-step logic.
- Use one CTE per logical transformation or source.
- Name CTEs descriptively.
- Keep the final SELECT easy to scan.

Performance:
- Avoid `SELECT *` in production queries.
- Filter early, especially on dates and partitions.
- Use partition filters for BigQuery/Databricks and clustering/sort-aware filters for Snowflake/Redshift.
- Use appropriate join types.
- Avoid correlated subqueries when joins or windows are clearer.
- Watch for many-to-many joins and potential row multiplication.
- Prefer approximate distinct functions only when accuracy tradeoffs are acceptable and stated.

Readability:
- Add comments for non-obvious business logic.
- Use consistent formatting and indentation.
- Use meaningful table aliases.
- Put major clauses on their own lines.

Correctness:
- Protect rate denominators with `NULLIF` or dialect-safe division.
- Define timezones and date boundaries.
- Deduplicate before aggregation when needed.
- Keep metric definitions explicit.

### 5. Present the Query

Provide:
1. Complete SQL code block.
2. Short explanation of each CTE or major section.
3. Performance notes and likely bottlenecks.
4. Modification suggestions for date range, granularity, dimensions, or filters.
5. Validation checks the user can run.

### 6. Offer Execution or Review

If a warehouse is connected, offer to run the query and inspect results. If the user will run it themselves, make the query copy-paste ready.

## Output Template

````markdown
## Query

```sql
-- SQL here
```

## How It Works
- `[cte_name]`: ...

## Performance Notes
- ...

## Validation Checks
- Row count before and after joins.
- Date range coverage.
- Duplicate key checks.
- Aggregate reconciliation.

## Common Modifications
- To change time range: ...
- To group by another dimension: ...
````

## Examples

- Count orders by status for the last 30 days.
- Cohort retention by signup month with activity at 1, 3, 6, and 12 months.
- Top 100 users by event count in the last 7 days from a large partitioned events table.

## Rules

- Do not invent exact table or column names when schema is unknown; use placeholders or ask for schema.
- If using assumptions, state them next to the query.
- For recurring queries, parameterize date ranges when the dialect supports it.
- For high-stakes analysis, recommend `validate-data` after results are produced.
