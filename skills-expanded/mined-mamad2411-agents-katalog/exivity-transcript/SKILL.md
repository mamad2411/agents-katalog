---
name: exivity-transcript
description: create, review, debug, and explain exivity transcript transformer scripts for mapping, normalization, enrichment, aggregation, service generation, and report preparation. use when a user asks for a .trs transformer, wants extracted csv data reshaped into exivity-ready datasets, needs help with dset or column logic, or wants generic etl logic rewritten in valid transcript syntax. especially relevant for import/default dset flows, correlate, aggregate, services blocks, normalize steps, and preparing rdf or exported outputs from extracted data.
---

# Exivity Transcript

Use this skill to produce real Transcript transformer scripts, not generic ETL pseudocode. Favor complete `.trs` tasks that can be pasted into `system/config/transcript/` with only source names, column names, or business rules adjusted.

## Working style

1. Identify the extracted source files or source aliases being consumed.
2. Identify the desired output: cleaned dataset, service definitions, exported CSV/JSON, or RDF.
3. Build a Transcript task with valid one-line statements and correct DSET references.
4. Shape the flow in a practical order: import, select default dset, transform, enrich, aggregate, export or finish.
5. When input schema is incomplete, make explicit assumptions in comments and keep the task runnable.

## Non-negotiable Transcript rules

- Keep every statement on a single line.
- Use `source.alias` naming consistently and set a `default dset` early when one DSET drives most operations.
- Remember that Transcript allows `@FUNCTION()` directly in `var` assignments; unlike USE, extra parentheses are optional.
- Use `[ColumnName]` inside expressions and `source.alias.ColumnName` when disambiguation is required.
- Use regex variable syntax such as `${/.*Operations/}` when the user has variable column headings.
- After `correlate`, handle default or missing values explicitly, often via `EXIVITY_NOT_FOUND`.
- When using `aggregate`, remember that Transcript automatically creates `EXIVITY_AGGR_COUNT`.
- Keep `where` blocks limited to statements Transcript actually permits there.
- Choose `finish` when the user wants RDF/report output, and `export` when they want an intermediate CSV or JSON file.

## Preferred transformer workflow

### Standard shaping flow

1. Import extracted source data.
2. Set the default DSET.
3. Clean column names or values with `rename`, `dequote`, `lowercase`, `uppercase`, or `replace`.
4. Add or compute columns with `create`, `calculate`, and `set`.
5. Enrich with `correlate`.
6. Normalize or standardize numeric signs and units when required.
7. Aggregate only after the detail-level logic is correct.
8. Build services or final outputs.
9. End with `finish`, `finish source.alias`, or `export`.

### Mapping and normalization tasks

Prefer Transcript for:

- field mapping from vendor exports into Exivity naming
- cost and quantity normalization
- aggregation to billing/report levels
- service construction from transformed usage data
- enrichment through correlations with metadata DSETs

## What to include in answers

When generating or repairing a Transcript script:

- Return a full `.trs` task in a code block.
- Keep comments concise and operational.
- Use realistic DSET names and column names when the user provides them.
- Explain only the non-obvious parts after the script, such as why `aggregate` is placed where it is or how a `services` block maps columns.

When reviewing a Transcript script:

- Start with exact syntax or control-flow problems.
- Then fix Exivity-specific design issues such as wrong DSET references, missing `default dset`, incorrect `where` usage, premature aggregation, or weak handling of missing correlations.
- Prefer direct corrected code over abstract advice.

## Example user requests this skill should handle

- “Write a Transcript transformer that imports this extracted CSV and builds services.”
- “Normalize negative credits and aggregate by customer and service.”
- “Fix this .trs task; correlate is not returning the values I expect.”
- “Map these vendor column names to Exivity fields and finish as RDF.”
- “Create a transformer that consumes extracted API data and prepares billable usage.”

## References to consult

- Read `references/transcript-syntax.md` for the distilled Transcript rules and edge cases.
- Read `references/transcript-patterns.md` for common flow designs and transformation patterns.
