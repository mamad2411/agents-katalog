---
name: approval-skill
description: Approve or reject after review
version: "1.0"
---

# Approval Skill

Use this skill when the workflow state is **REVIEW** or **FINAL_DECISION**.

## Options

- **approve**: Mark the item as approved. No body required unless the workflow expects optional fields.
- **reject**: Reject with a reason. Body must include:
  - `reason` (string, required): Human-readable reason for rejection.

## Example (reject)

```json
{
  "reason": "Audit found 2 critical issues; requires remediation."
}
```

Always prefer the **approve** action when the audit is clear and no escalation is needed.
