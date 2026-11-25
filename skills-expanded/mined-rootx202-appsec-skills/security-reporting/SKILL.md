---
name: security-reporting
description: Generates a professional, consolidated security report (Markdown or HTML) from findings produced by other security skills, including an executive summary and an overall security score out of 100. Use at the end of any security audit/scan/pentest-style session, or whenever the user asks for a formal write-up of security findings for any project.
---

# Security Reporting — Final Report Generator

A skill for consolidating the results of any prior security assessment (from `code-audit`, `vulnerability-scanner`, `database-security`, etc.) into a single professional report.

## When to use this
- At the end of any security assessment session
- Explicit request for a formal report (for an employer, client, or internal record)

## Mandatory Report Structure

```markdown
# Security Report — [Project Name]
Date: [YYYY-MM-DD]

## Executive Summary
[3–5 sentences: scope of the assessment, key findings, overall posture]

## Security Score: XX/100

## Findings Breakdown
| Severity | Count |
|---|---|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |

## Critical Issues
[For each: Vulnerability/Severity/Location/Impact/Proof/Fix]

## High Issues
[...]

## Medium Issues
[...]

## Low Issues
[...]

## Fixed Issues
[Any fixes applied during this session via remediation-engine]

## Remaining Risks
[Any unresolved finding, and why — pending decision, technical complexity, etc.]

## Recommendations
[General recommendations: recurring review cadence, automated security tests in CI, team training, etc.]

## Production Readiness
Production Ready: YES / NO
[Brief justification for the verdict]
```

## Security Score Methodology (out of 100)
Start at 100 and subtract by severity (a guideline — adjust for project scale and context):
- Each Critical finding: -15
- Each High finding: -8
- Each Medium finding: -3
- Each Low finding: -1
- Floor at 0

Any single unresolved Critical finding automatically forces `Production Ready: NO`, regardless of the overall numeric score.

## Rules
- The report is based only on findings actually produced during this session by the other skills — never fabricate findings to pad the report.
- Use professional, decision-maker-friendly language in the executive summary (the reader may not be deeply technical), and precise technical language in the detailed findings.
- If requested, produce an HTML version with the same structure, using available file-creation tools (defer to the docx/pdf skill if the user wants Word or PDF instead of Markdown/HTML).
