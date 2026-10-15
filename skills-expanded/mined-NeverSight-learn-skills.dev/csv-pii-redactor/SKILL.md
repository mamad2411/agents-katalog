---
name: csv-pii-redactor
description: Vendor-neutral skill to detect and redact common PII in CSV files and produce a redaction report.
---

## When to invoke
- You need to share CSV data externally but want to reduce privacy risk.
- You want a quick, explainable scan for likely PII columns/values.

## Inputs needed
- `--input_csv`: Path to input CSV.
- `--output_csv`: Path to write the redacted CSV.
- `--report_json`: Path to write a JSON redaction report.
- Optional:
  - `--redact_with`: Replacement token (default: `[REDACTED]`).
  - `--min_match_rate`: Minimum fraction of non-empty values in a column that must match a PII pattern before redaction is applied (default: 0.2).

## Workflow
1. Load CSV and sample values per column.
2. For each column, run regex-based detectors on non-empty values:
   - email addresses
   - phone numbers (basic international/US patterns)
   - US SSN-like patterns
   - IPv4 addresses
   - credit card-like numbers (with Luhn check)
3. Decide whether to redact a column based on match rate threshold.
4. Produce:
   - Redacted CSV (only columns that exceed threshold are redacted).
   - JSON report with detectors triggered, match counts, and examples.

## Output format
- Redacted CSV with same headers/row count as input.
- JSON report:
  - `columns[].name`
  - `columns[].redacted` (boolean)
  - `columns[].detectors[]` with `type`, `matches`, `total_non_empty`, `match_rate`, `examples`

## Guardrails
- This is heuristic detection; it may miss PII or flag false positives.
- Do not treat output as compliance certification.
- Avoid printing raw PII to stdout; report examples are truncated.

## Reference code
- `csv_pii_redactor.py`
