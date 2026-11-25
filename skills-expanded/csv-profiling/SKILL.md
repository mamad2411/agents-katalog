---
name: csv-profiling
description: Profiles and safely cleans CSV files. Use whenever the user shares or mentions a CSV, TSV or spreadsheet export, asks what is in a data file, wants to find missing values, duplicates, wrong types or broken rows, prepare data for analysis, or fix garbled text, Persian or Arabic digits and mixed date formats, even if they only say "look at this data". Profiles first with a script, then proposes a logged cleaning plan and never overwrites the original.
---

# csv-profiling

Understand a CSV before changing it. The profiler uses only the standard library, so it runs anywhere, including Termux.

```
csv-profiling/
├── SKILL.md
├── scripts/
│   └── csv_profile.py        types, nulls, duplicates, ragged rows, mixed types, digits, dates
└── references/
    └── cleaning-plan.md      order of operations, fix table, Persian normalization, snippet
```

## When to use

- A new data file arrives and nobody knows what is in it
- Numbers load as text, dates are inconsistent, totals look wrong
- Text is garbled or contains Persian or Arabic digits
- Preparing data for a chart, a database import or analysis

## Workflow

1. **Profile**: `python3 scripts/csv_profile.py data.csv`
   Auto-detects encoding (`utf-8-sig`, `utf-8`, `cp1256`, `latin-1`) and delimiter (`, ; tab |`). Add `--json` for machine output and `--strict` to exit with code 1 when issues exist.
2. **Read the issues list**. Each line is a finding with the column name. Check a few raw rows for the worst ones.
3. **Decide per finding** with the table in `references/cleaning-plan.md`. Ask the user when a fix can change meaning (dd/mm vs mm/dd, "-" as a value, outlier removal).
4. **Clean into a new file**. Never overwrite the original; keep a copy and its checksum.
5. **Re-profile** the cleaned file and compare. Report row counts before and after with reasons.

## What the profiler reports

| Per file | Per column |
|----------|------------|
| rows, columns, encoding, delimiter | inferred type, nulls, unique count |
| duplicate rows | min and max for numbers, top values otherwise |
| ragged rows (wrong field count) | mixed types, null-like tokens (`N/A`, `-`, `null`) |
| duplicate or padded header names | leading or trailing spaces |
| | Persian or Arabic digits |
| | thousands separators, mixed date formats |

## Rules

- Profile before cleaning, and again after
- Keep the raw file untouched; write results elsewhere
- Log every rule with the number of rows affected
- Do not guess ambiguous dates or decimal commas; ask or document the assumption
- Flag outliers, do not delete them silently
- A column of mostly empty values may be a different table in disguise: ask
- Report with numbers, not adjectives: "37 of 1,204 rows (3.1%)"

## Large files

The profiler reads rows once and keeps counters in memory. For files above a few million rows, pass `--max-rows 200000` for a sample, then run the full pass in a database or a streaming tool.

## What to report back

| Field | Content |
|-------|---------|
| File facts | rows, columns, encoding, delimiter |
| Problems | list with counts and examples |
| Proposed fixes | per problem, with the risk |
| Questions | ambiguities that need the user |
| After cleaning | row counts before and after, change log |

## Related skills

- `pdf-processing`: extract tables from a PDF, then profile the result here
- `systematic-debugging`: trace a data pipeline that produces bad rows
- `secrets-hygiene`: check data files for personal data or credentials before sharing
