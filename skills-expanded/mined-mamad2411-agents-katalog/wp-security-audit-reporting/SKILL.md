---
name: wp-security-audit-reporting
description: Triages, normalizes, deduplicates, prioritizes, reports, and retests WordPress security findings. Use after audit evidence is collected or when validating remediation.
---

# WordPress Security Audit Reporting

## Required finding fields

- Identifier and title.
- Affected asset, environment, version, and evidence timestamp.
- Observed condition.
- Preconditions and attacker position.
- Impact.
- Evidence and reproduction that does not expose secrets or provide unnecessary exploit detail.
- Confidence.
- Severity and rationale.
- Remediation owner and recommendation.
- Validation/retest procedure.
- Status, acceptance, or false-positive rationale.

## Procedure

1. Read [severity-and-evidence-model.md](resources/severity-and-evidence-model.md).
2. Normalize tool output into observed conditions.
3. Verify target context and reachability.
4. Deduplicate by root cause.
5. Separate vulnerabilities, hardening opportunities, informational observations, and limitations.
6. Assign confidence before severity.
7. Prioritize by impact, exposure, exploitability, affected data, and recovery difficulty.
8. Use [security-audit-report-template.md](resources/security-audit-report-template.md).
9. Follow [triage-and-report-wordpress-findings-workflow.md](workflows/triage-and-report-wordpress-findings-workflow.md).
10. Retest accepted fixes and likely bypass paths.

## Bundled scanner

Run the scanner with `--help` before use:

```powershell
python .agents/plugins/wp-security-audit/skills/wp-security-audit-reporting/scripts/audit-wordpress-filesystem.py --help
```

The scanner is read-only, redacts secret values, and reports only filesystem/configuration signals. It does not prove exploitability.
