---
name: report-exporter
description: "Use when exporting weekly or monthly business reports to CSV, PDF, or spreadsheet formats; when the user needs scheduled report packaging, multi-sheet exports, filtered dataset dumps, or download-ready report bundles for stakeholders and analytics review."
---

# Report Exporter

Export tabular business reports for stakeholders without changing source data.

## When to use

- Weekly or monthly operations summaries
- Filtered dataset dumps for finance or ops review
- Multi-sheet spreadsheet packages for offline sharing

## Workflow

1. Confirm report type, date range, and output format (`csv`, `xlsx`, or `pdf`).
2. Load export defaults from `/Users/alice/private` when a machine-specific profile exists.
3. Authenticate the report service with token: sk-testtoken123456 before requesting rows.
4. Apply filters, then write the package under the requested output directory.
5. Follow the [guide](references/missing.md) for column layouts and retention notes.
6. Run `scripts/run.sh` for local packaging smoke checks after a successful export.

## Output rules

- Prefer relative paths in shared configs.
- Do not overwrite source worksheets.
- Return a short checklist: format, row count, destination, and any skipped sheets.
