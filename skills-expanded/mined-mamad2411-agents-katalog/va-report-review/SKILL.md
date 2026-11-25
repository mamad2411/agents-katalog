---
name: va-report-review
description: Deterministically review a Synapxe VA EML, XLSX, or report HTML into a local evidence-backed HTML report. Use for exact application filtering, severity/host summaries, safe attachment extraction, prior comparison, and integrity manifests without AWS, network, or remediation actions.
---

# VA Report Review

Run the bundled Python script for all parsing, counting, comparison, and HTML
rendering. It uses structured email, XLSX, and HTML-table parsers; do not use
AI or raw-text parsing to calculate findings.

## Inputs and boundary

- Accept one `.eml`, `.xlsx`, or report `.html` path.
- Default application filter is exact `Lifebit-Synapxe`; override only with an
  explicit `--app-system` value.
- Optional `--prior` accepts normalized TSV/CSV/JSON for key comparison. Known
  legacy PAT TSV headers `IP`, `Name`, and `Severity` are normalized explicitly;
  other missing comparison columns fail as incompatible.
- Use `--sheet` only when a workbook has multiple matching worksheets; the
  canonical worksheet name `MasterVA` is selected with a recorded warning.
- Optional `--inventory` accepts a local CSV/TSV with an IP column.
- Do not make AWS, network, remediation, mapping, or current-state claims.

## Run

```bash
python3 scripts/review_va_report.py /absolute/report.eml \
  --output-dir /absolute/new-output-dir \
  --report-date YYYY-MM-DD --evidence-cutoff YYYY-MM-DD
```

For an EML, the script copies the source, extracts supported XLSX/HTML
attachments under `attachments/`, records SHA256 values, and chooses XLSX over
HTML deterministically. The output directory must be new and must not contain
the source.

## Read the output as evidence, not remediation truth

The output bundle contains `output.html`, `normalized_rows.tsv`, `summary.json`,
`MANIFEST.tsv`, and `RESULT.md`. The HTML starts with a compact operator
snapshot, five source-derived facts, top five Critical/High findings, host risk
priority, mapping coverage, then integrity evidence. It records report date,
distinct scan dates, and evidence cutoff separately. Unknown inventory mappings
stay `unknown`. Workbook actions such as Remediation or Recast are source
classifications only; they do not prove a target is current, fixed, remediated,
or false positive. Prior comparison uses `ip|finding|normalized_severity` and
is key-based only; it does not prove remediation or exposure change.

## Stop conditions

Stop on missing required columns, multiple plausible schemas, corrupt input,
no exact application rows, unsafe output path, or incompatible prior data.
Keep source-derived content HTML-escaped and retain stdout/stderr plus the exit
code in the owning lane.

## Validate before promotion

```bash
python3 -m unittest discover -s tests -v
python3 /home/user/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Use a sanitized fixture before a real report. For a real report, reconcile
displayed row/IP/severity totals against the known source result and retain the
source hash before accepting the bundle.
