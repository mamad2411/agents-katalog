---
name: data-audit
description: Use to audit datasets for provenance, quality, leakage, privacy, bias, and license risk.
---

# Data Audit

## When to use

Use to inspect datasets for provenance, schema quality, leakage, missingness, duplicates, drift, label quality, privacy risk, and license constraints.

## Workflow

1. Inventory files, schemas, sources, licenses, and permitted uses.
2. Profile missing values, distributions, duplicates, and outliers.
3. Check train, validation, and test isolation plus target or temporal leakage.
4. Review labels, annotation process, inter-annotator agreement, and class imbalance.
5. Assess privacy, sensitive attributes, and de-identification.
6. Produce remediation steps with severity and reproducibility notes.

## Source hierarchy or evidence rules

1. Dataset documentation, datasheets, licenses, and official repositories.
2. Computed profiling results and reproducible audit scripts.
3. Known benchmark contamination reports and issue trackers.
4. Domain expert labels or annotation guidelines.
5. Informal dataset descriptions only as leads until verified.

## Output schema

Return Markdown unless JSON is requested. Include:

- `dataset`
- `provenance`
- `license`
- `schema_findings`
- `quality_findings`
- `leakage_risks`
- `privacy_risks`
- `bias_risks`
- `recommended_fixes`
- `audit_confidence`

## Citation rules

- Cite dataset source, version, license, and retrieval date.
- Cite profiling commands or scripts for computed findings.
- Do not expose private rows, secrets, personal data, or restricted samples.
- Mark inferred provenance as uncertain.
- Keep source URLs and checksums for reproducibility.

## Failure modes

- Dataset cannot be accessed or legally inspected.
- Schema or data dictionary is absent.
- Sensitive data appears without authorization.
- Sampling process is unknown.
- Audit would require copying restricted data.
