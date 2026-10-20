# Go/No-Go Assessment

## Purpose
Consolidates QA and Security staging results into a GO or NO-GO recommendation for production release.

## Role
Release Manager

## Phase
Staging (after QA + Security sign-off)

## Triggered By
QA `staging-sign-off` and Security `security-metrics-report` (staging phase) complete.

## Inputs
- QA `staging-sign-off`
- Security `security-metrics-report`
- `release-readiness-assessment` items

## Process
1. Consolidate QA `staging-sign-off` and Security staging results.
2. Check all `release-readiness-assessment` items.
3. Produce GO or NO-GO recommendation with specific justification.
4. Send to Edward for final decision via `/release-production`.
5. NO-GO: escalate to Edward with specific blocking reason.

## Outputs
GO/NO-GO recommendation to Edward.

## Quality Gates
- [ ] QA and Security inputs both consolidated
- [ ] All release-readiness-assessment items checked
- [ ] Recommendation includes specific justification
- [ ] NO-GO always escalated with specific reason

## References
- `.claude/skills/qa-engineer/staging-sign-off/SKILL.md`
- `.claude/skills/security-engineer/security-metrics-report/SKILL.md`
- `.claude/skills/release-manager/release-readiness-assessment/SKILL.md`
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
