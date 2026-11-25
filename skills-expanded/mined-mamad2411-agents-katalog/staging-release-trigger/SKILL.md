# Staging Release Trigger

## Purpose
Triggers deployment to Staging and notifies QA and Security to begin their staging-phase testing.

## Role
Release Manager

## Phase
Release

## Triggered By
`release-readiness-assessment` passes.

## Inputs
- Release-ready image tag

## Process
1. Trigger DevOps `staging-deployment` skill.
2. Monitor staging deployment health.
3. Notify QA: "Staging ready — begin performance + stress testing".
4. Notify Security Engineer: "Staging ready — begin ZAP full scan + pentest".

## Outputs
Staging deployment triggered; QA and Security notified.

## Quality Gates
- [ ] DevOps staging-deployment triggered only after readiness assessment passes
- [ ] Deployment health monitored until confirmed
- [ ] QA and Security both explicitly notified

## References
- `.claude/skills/devops-engineer/staging-deployment/SKILL.md`
- `.claude/skills/qa-engineer/performance-testing/SKILL.md`
- `.claude/skills/security-engineer/zap-full-scan/SKILL.md`
