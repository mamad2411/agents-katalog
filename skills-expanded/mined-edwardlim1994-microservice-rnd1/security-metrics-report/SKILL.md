# Security Metrics Report

## Purpose
Produces data-driven security metrics report for the retrospective session.

## Role
Security Engineer

## Phase
Retrospective

## Triggered By
`/metrics` command before `/retro`.

## Inputs
- Sprint's CVE, scan, and compliance data

## Process
Collect and report:
- CVEs found this sprint: N (by severity)
- CVEs resolved this sprint: N
- CVEs outstanding: N
- Secrets scan findings: N (should always be 0)
- ZAP baseline scan results: N per story (by severity)
- ZAP full scan results: by severity, by OWASP category
- Semi-automated pentest: N findings
- Compliance status: N requirements met / N total
- Delta vs previous sprint (trend for each metric)

Improvement suggestions must be specific and data-backed. Example: "5 of 8 stories had auth bypass vulnerabilities in compliance testing. Root cause: auth interceptor not applied to new gRPC methods by default. Suggestion: add auth interceptor check to Tech Lead definition-of-done checklist."

Suggestions go to backlog via PO `retrospective-conclusion`.

## Outputs
Contributes to Section 5 of `retro-template.md`.

## Quality Gates
- [ ] All metrics collected (no estimates — actual counts)
- [ ] Delta vs previous sprint calculated
- [ ] Improvement suggestions are specific and data-backed
- [ ] Report ready before /retro session begins

## References
- `.claude/skills/pm/retrospective-facilitation/SKILL.md`
- `.claude/skills/po/retrospective-conclusion/SKILL.md`
- `openspec/retro-template.md`
