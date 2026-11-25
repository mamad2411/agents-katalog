---
name: json-data-wrangling
description: Flatten and normalize nested JSON exports (Firebase, API responses, event logs, NoSQL dumps) into tabular form — flattening nested objects with key-path column names, exploding arrays vs joining, type coercion, inconsistent/missing keys, schema inference across records, converting to CSV/Excel-ready tables or dataframes. Use when turning a nested JSON/dict export into a spreadsheet, CSV, or dataframe for analysis.
---

# JSON Data Wrangling (nested export → table)

## The core decision: one row per WHAT?

Before flattening anything, name the unit of analysis. A nested export mixes grains
(user → orders → items); "flatten it" is meaningless until you choose the row grain.
Every later choice (explode vs join, aggregation) follows from it.

## Flattening rules

- **Nested objects** → dotted key-path columns: `user.address.city`. Keep the full path;
  truncating to leaf names (`city`) collides silently when two branches share a leaf.
- **Arrays of scalars** → either join into one cell (`"a;b;c"`, lossy but single-grain) or
  explode to rows (grain change — say so). Never mix both in one table.
- **Arrays of objects** → separate child table with a foreign key back to the parent id,
  or explode with duplicated parent columns. Duplicated parent values mean parent-level
  aggregates must dedupe first — the classic double-counting trap.
- **Dict-as-collection** (Firebase pattern: `{"-Nx3f…": {...}, "-Nx4a…": {...}}`) — the keys
  ARE ids, not fields: promote the key into an `id` column, then flatten the values.

## Schema inference across records

Records rarely share a schema. Scan ALL records (or a large sample) for the union of key
paths before writing headers — inferring columns from the first record drops fields that
appear later. Report per-column fill rate; a column present in 3% of rows is a schema
question, not a data point.

## Type coercion

- Distinguish missing key vs explicit `null` vs empty string — they mean different things
  in the source system; collapsing them silently loses information (flag which you merged).
- Timestamps: detect epoch seconds vs milliseconds (13 digits ≈ ms) and normalize to one
  timezone-labeled format; mixed units in one column is the most common silent corruption.
- Numbers arriving as strings ("1,234", "12%"): coerce with a locale rule stated up front;
  count coercion failures rather than zero-filling them.

## Excel/CSV output hygiene

- Escape/quote delimiters and newlines inside values; UTF-8 with BOM if Excel is the consumer.
- Long numeric ids (Firebase push ids are fine, but 16+ digit numerics) must be written as
  text — Excel silently rounds them past 15 digits.
- One sheet/file per grain; a "flattened" table that mixes parent and child grains is wrong
  even when it opens cleanly.

## Failure modes — what wrong looks like

- Row counts change unexplainedly after flattening: an explode happened without being chosen.
- Aggregates double-count after an explode (parent columns duplicated across child rows).
- Columns missing because the first record lacked them.
- Ids corrupted by spreadsheet numeric coercion; epoch ms read as epoch s (dates in 56399 AD).
- `null` vs missing silently merged, then read as "user answered nothing".

## Reviewer checklist

- [ ] Row grain stated; explode vs join decisions listed with their grain effects
- [ ] Column set derived from the union of records, with per-column fill rates
- [ ] Missing vs null vs empty distinguished or their merge explicitly declared
- [ ] Timestamps normalized with unit and timezone stated; coercion failures counted
- [ ] Long ids protected from spreadsheet numeric mangling
- [ ] Output row count reconciled against source record count (with the explode math shown)

Provenance: standard data-wrangling practice (tidy data, JSON normalization as in
pandas `json_normalize`); no external sources cited — derived from common tooling behavior.
