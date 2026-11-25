---
name: productize-explore-data
description: >-
  Profile and explore a dataset to understand its shape, quality, and patterns. Use when
  encountering a new table or file, checking null rates and distributions, spotting duplicates
  or suspicious values, or deciding which dimensions and metrics to analyze.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Explore Data

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

- **Skill**: `explore-data`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: Explore Data analytics diagnosis with metric readout, caveats, decision, and next instrumented step

Generate a comprehensive data profile for a table or file before deeper analysis.

## Argument Hint

`<table or file>`

## Usage

```text
/explore-data <table_name or file>
```

## Workflow

### 1. Access Data

If a data warehouse or analytics MCP is connected:
1. Resolve the table name, including schema prefixes.
2. Query table metadata: columns, types, descriptions, size, update metadata if available.
3. Run profiling queries against live data. Use sampling for very large tables and disclose it.

If a file is provided:
1. Load CSV, Excel, Parquet, or JSON into a working dataset.
2. Infer column types and normalize obvious parsing issues.

If neither is available, ask for a table name, file, pasted sample, or schema description. If only a schema is provided, give profiling SQL the user can run.

### 2. Understand Structure

Answer table-level questions:
- Rows and columns.
- Grain: one row per what.
- Primary key or natural key, and whether it is unique.
- Last updated timestamp and expected refresh cadence if known.
- Date coverage and earliest/latest records.

Classify columns:
- Identifier: primary keys, foreign keys, entity IDs.
- Dimension: categorical attributes for grouping/filtering.
- Metric: quantitative values.
- Temporal: dates and timestamps.
- Text: free-form strings.
- Boolean: true/false flags.
- Structural: JSON, arrays, nested data.

### 3. Profile Columns

Table-level:
- Total row count.
- Column count and type breakdown.
- Approximate table size if available.
- Date range for temporal columns.

All columns:
- Null count and null rate.
- Distinct count and cardinality ratio.
- Top 5-10 most common values with frequencies.
- Rare values when useful for anomaly detection.

Numeric columns:
- Min, max, mean, median, standard deviation.
- Percentiles: p1, p5, p25, p75, p95, p99.
- Zero count and negative count.
- Distribution shape and outliers.

String columns:
- Min, max, and average length.
- Empty string count.
- Pattern consistency.
- Case consistency.
- Leading/trailing whitespace.

Temporal columns:
- Min and max dates.
- Null and future dates.
- Distribution by month/week.
- Time series gaps.

Boolean columns:
- True count, false count, null count, true rate.

### 4. Flag Data Quality Issues

Use severity labels: high, medium, low.

Flag:
- High null rates: warn above 5 percent, alert above 20 percent.
- Duplicate natural keys.
- Low-cardinality IDs or unexpectedly high-cardinality categorical fields.
- Suspicious values: negative amounts, future dates, placeholders, test values, impossible ranges.
- Skewed distributions that make averages misleading.
- Encoding and formatting issues: mixed case, whitespace, inconsistent formats.
- Cross-column rule violations: completed status with missing completed_at, end date before start date.
- Staleness or unexpected load lag.

### 5. Discover Patterns

Look for:
- Foreign key candidates.
- Natural hierarchies such as country -> state -> city.
- Numeric correlations worth investigating.
- Derived columns that appear calculated from other fields.
- Redundant or near-identical columns.
- Natural segments based on categorical fields with useful cardinality.

### 6. Recommend What To Analyze Next

Suggest:
- Best dimensions for slicing data.
- Key metric columns.
- Time columns suitable for trends.
- Natural groupings or hierarchies.
- Potential join keys.
- 3-5 concrete follow-up analyses.

Examples:
- Trend analysis on `[metric]` by `[time_column]` grouped by `[dimension]`.
- Distribution deep dive on `[skewed_column]`.
- Data quality investigation on `[problematic_column]`.
- Correlation analysis between `[metric_a]` and `[metric_b]`.
- Cohort analysis using `[date_column]` and `[status_column]`.

## Output Format

```markdown
## Data Profile: [table_or_file]

### Overview
- Rows:
- Columns:
- Grain:
- Primary key:
- Date range:
- Last updated:

### Column Details
[Summary table grouped by IDs, dimensions, metrics, dates, booleans, text, structural fields]

### Data Quality Issues
[Severity, field, issue, evidence, recommendation]

### Patterns and Relationships
[Join keys, hierarchies, correlations, derived/redundant fields]

### Recommended Explorations
[Numbered list of follow-up analyses]
```

## Quality Framework

Completeness:
- Complete: more than 99 percent non-null.
- Mostly complete: 95-99 percent.
- Incomplete: 80-95 percent.
- Sparse: below 80 percent.

Consistency checks:
- Same concept represented multiple ways.
- Numbers stored as strings.
- Dates in inconsistent formats.
- Foreign keys without parents.
- Business rule violations.

Accuracy red flags:
- Placeholder values such as 0, -1, 999999, N/A, TBD, test, xxx.
- Suspicious default values.
- Stale active-system data.
- Impossible values.
- Round-number bias.

Timeliness:
- Last updated time.
- Expected update frequency.
- Event-to-load lag.
- Gaps in expected time series.

## Schema Documentation Template

When documenting the dataset for team use, include:
- Description.
- Grain.
- Primary key.
- Row count and date.
- Update frequency.
- Owner if known.
- Key columns table.
- Relationships.
- Known issues.
- Common query patterns.

## SQL Discovery Patterns

Use dialect-appropriate schema queries. For PostgreSQL-style systems:

```sql
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'my_table'
ORDER BY ordinal_position;
```

For other warehouses, adapt to the warehouse dialect and metadata tables.
