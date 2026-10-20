---
name: nessus-cis-csv-analysis
description: Parse Nessus/Tenable CIS Compliance Remediation Instruction CSV exports into a deterministic multi-host HCR report. Use when analyzing CIS/HCR CSVs, separating FAILED/WARNING/manual-review findings from PASSED controls, creating a self-contained Advanced HTML report, or overlaying an optional Risk Acceptance register and structured TISO risk-assessment workbook.
---

# Nessus CIS CSV Analysis

Generate one concise, self-contained HTML report for all hosts discovered in a Nessus/Tenable CIS/HCR CSV.

## Default workflow

1. Validate required CSV headers: `Plugin`, `Plugin Name`, `Severity`, `IP Address`, `DNS Name`, `Plugin Output`.
2. Include only genuine CIS controls whose `Plugin Name` begins with a numeric CIS control ID.
3. Ignore discovery/inventory rows entirely from CIS counts and report tables.
4. Detect all unique non-empty IP addresses automatically. Do not ask whether to generate one report per host; generate one multi-host report.
5. Parse `Plugin Output` into `Status`, `Information`, `Actual Value`, `Policy Value`, and `Remediation/Solution` when present.
6. Keep scanner status independent from governance treatment:
   - `FAILED` = scanner non-compliance.
   - `WARNING`, `ERROR`, `UNKNOWN`, or conflict = manual review.
   - `PASSED` = currently passing; do not call it `FIXED` without historical evidence.
7. Default user-facing output is one Advanced HTML report. JSON is optional evidence/debug output.

## Advanced HTML

Use these tabs:

- `Dashboard`
- `Action Explorer`
- `Risk Acceptance`
- `TISO Risk Groups`
- `Unique Controls`
- `Evidence & Mapping`

Support host/status/treatment/acceptance/risk/mapping filters, search, dense view, expandable evidence, print-friendly layout, and filtered CSV export.

Show PASSED counts on the Dashboard but omit detailed PASSED rows from Action Explorer unless a future explicit mode requests them.

## Risk Acceptance

When an operator supplies a Risk Acceptance register XLSX, keep these concepts separate:

- **Treatment**: `Remediate`, `Risk Acceptance`, or `Review Required`.
- **Risk Acceptance**: `Pending TISO`, `Accepted`, `Rejected`, `Not Accepted`, or `—`.

Never convert a scanner `FAILED` result into `PASSED` because a risk is accepted.
Never infer acceptance from wording such as `proposed exception` or `Pending security review`. Approval requires explicit decision/evidence in the supplied register.

## TISO risk mapping

When an operator supplies a structured TISO risk-assessment XLSX, extract the sheet containing `Risk ID` and `Risk Statement`, then extract `CS-*` groups, titles, initial/residual risk, and CIS references.

Apply deterministic mapping precedence:

1. Current control explicitly mapped in the Risk Acceptance register → `HIGH`.
2. Exact current CIS ID found in the TISO Risk Statement → `HIGH`.
3. Exact normalized control-title match with a different CIS ID → `REVIEW` because benchmark/control numbering may differ.
4. Otherwise → `UNMAPPED`.

Never use fuzzy/AI guessing to silently map an unmatched control. A `REVIEW` mapping is thematic/cross-benchmark evidence, not proof of one-to-one CIS-number equivalence.

If an optional workbook does not contain the expected structured headers, fail clearly rather than inventing a mapping.

## Script

Run the Advanced generator from this skill directory:

```text
python3 scripts/hcr_advanced_report.py <nessus.csv> --html-out <report.html>
```

Optional overlays:

```text
--risk-register <risk-register.xlsx>
--tiso-risk <tiso-risk-assessment.xlsx>
--json-out <structured.json>
```

The script uses only the Python standard library and writes no source/customer workbook content into the skill repository.

## Validation

Before presenting a generated report, verify:

- discovered host count matches the CSV;
- non-CIS inventory rows are excluded;
- FAILED/WARNING/manual-review counts match parsed scanner results;
- Risk Acceptance candidates remain distinct from accepted decisions;
- cross-benchmark mappings are visibly labelled `REVIEW`;
- unmapped controls remain `UNMAPPED`;
- no AWS query, scan, remediation, or policy action occurred unless separately requested and authorized.

## Out of scope by default

- historical `FIXED / REGRESSED / NEW` comparison;
- AWS Inspector comparison or AWS mutation;
- arbitrary TISO workbook inference without structured risk fields;
- universal parsing for unrelated Nessus export formats;
- committing generated HCR reports or source assessment files to this repository.
