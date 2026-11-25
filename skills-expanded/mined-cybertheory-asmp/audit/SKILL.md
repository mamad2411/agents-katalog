---
name: audit-skill
description: Verify document for secrets and policy before approval
version: "1.0"
---

# Audit Skill

Use this skill when the workflow state is **AUDIT** or **SECURITY_AUDIT**.

## Checklist

1. **Secrets**: Scan the provided document or code for hardcoded secrets (API keys, passwords, tokens).
2. **Policy**: Ensure the content complies with the stated policy (e.g. no PII in logs).
3. **Report**: Produce a structured report with:
   - `report_hash`: A short hash or id of the report (string).
   - `issue_count`: Number of issues found (integer).

## Example output

```json
{
  "report_hash": "audit_abc123",
  "issue_count": 0
}
```

If critical issues are found, use the **flag_critical** action with a `reason` instead of submitting the audit.
