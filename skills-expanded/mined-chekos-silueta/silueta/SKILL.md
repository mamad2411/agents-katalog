---
name: silueta
description: Profile datasets (CSV, Excel workbooks, Parquet, SQLite) into a value-free shape profile and model from it — use whenever data files may contain PII/PHI, when asked to scan/profile a dataset safely, or before scaffolding dbt models or warehouse landing tables from raw files. Never read the data files directly.
---

# silueta: model data you must not read

silueta profiles the *shape* of data — types, nulls, cardinality, value
masks, PII/PHI flags, join candidates — and emits zero raw cell values.
Work from its profile instead of opening data files.

## Workflow

1. Never open, `cat`, `head`, or query raw data files. If a data file may
   contain PII/PHI, the profile is your only source.
2. Profile: `uvx silueta scan <files...> --out profile.json --report report.md`
   (multi-sheet Excel, CSV, Parquet, and SQLite all work; multiple files in
   one scan enables cross-table join detection).
3. Read `profile.json`. Key fields per column: `physical_type` (+
   `type_recovered` when text was promoted — trust the promoted type),
   `nulls.rate`, `distinct`/`uniqueness_ratio`, `masks` (value shapes like
   `999-99-9999`), `semantic` (email/ssn/npi/etc. with match rates),
   `alerts`, and table-level `recovery` (headers/footers that were fixed)
   and `relations` (join candidates with containment scores).
4. Model from the profile: uniqueness 1.0 + id-ish mask → key; `relations`
   entries → foreign keys / dbt relationships tests; `nulls.rate` → NOT
   NULL decisions; `numeric` magnitudes and precision facts → column types;
   `semantic` high-severity flags → masking policies and PII tags in the
   warehouse.
5. Alerts are modeling signals: `near_unique` on a non-key is a data-quality
   red flag to surface, `typed_as_text_*`/`recovered_from_text` means fix
   the type at landing, `sensitive_*` means apply the org's PII handling,
   `possible_leading_zero_loss` means the column must land as text.
6. For a new drop of the same data: profile it, then
   `uvx silueta diff old-profile.json new-profile.json` and react to drift
   instead of re-deriving the model.

## Boundaries

- The profile is the only data-derived artifact you may read or quote.
- Never work around a blocked data read — the block is the point.
- Generated scaffolds must be derived from profile fields, never from
  guessed example values; do not invent sample data in comments.
