# ZAP Baseline Scan

## Purpose
Quick passive security scan against each story's UAT environment to catch obvious issues early.

## Role
Security Engineer

## Phase
UAT (per story)

## Triggered By
Story deployed to `uat-{KAN-N}.uat.internal`.

## Inputs
- UAT environment URL

## Type
Passive scan only (~2 minutes). Tool: OWASP ZAP `docker run zaproxy/zap-stable zap-baseline.py`. Target: `uat-{KAN-N}.uat.internal`.

## Process
1. Wait for ArgoCD to confirm UAT environment healthy.
2. Run ZAP baseline (passive) scan against UAT URL.
3. Review scan results:
   - Critical/High findings → create bug kanban card (blocks UAT approval)
   - Low/Info findings → note for full scan report
4. Do NOT block UAT testing for Low/Info findings.
5. Include findings in `security-metrics-report`.

## Outputs
Bug cards for Critical/High findings; scan results logged for reporting.

## Quality Gates
- [ ] Scan run after environment confirmed healthy
- [ ] Critical/High findings create bug cards
- [ ] Results documented for security-metrics-report

## References
- `.claude/skills/security-engineer/compliance-application-testing/SKILL.md`
- `.claude/skills/security-engineer/security-metrics-report/SKILL.md`
