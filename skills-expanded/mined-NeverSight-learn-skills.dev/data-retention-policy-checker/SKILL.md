---
name: data-retention-policy-checker
description: Vendor-neutral skill to check a data retention schedule for completeness and risk (coverage, deletion handling, legal holds) and produce a structured findings report.
---

## When to invoke
- You are drafting or reviewing a data retention policy / schedule.
- You need a quick gap analysis before legal/security review.

## Inputs needed
- A JSON policy with:
  - datasets (name, data_class, system, retention_days, deletion_method)
  - legal_hold_supported (bool)
  - backup_retention_days (int)
  - notes (optional)

## Workflow
1. Validate schema and required fields.
2. Flag missing or inconsistent retention values.
3. Check for common high-risk patterns:
   - indefinite retention for personal data without justification
   - missing deletion method
   - backup retention longer than primary without rationale
   - no legal hold process
4. Output a human-readable report (Markdown) plus a machine-readable summary section.

## Output format
Markdown with:
- Summary (counts by severity)
- Findings table (severity, dataset, issue, recommendation)
- Notes and assumptions

## Guardrails
- This is not legal advice; report must say it is a preliminary check.
- Do not claim compliance with any specific regulation.

## Reference code
- `check_retention_policy.py` reads JSON policy and writes Markdown findings.
