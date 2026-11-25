# Production Release Trigger

## Purpose
Triggers production deployment after Edward's approval and monitors it post-deploy.

## Role
Release Manager

## Phase
Release

## Triggered By
Edward runs `/release-production` (Edward's approval detected).

## Inputs
- Edward's `/release-production` approval
- Staging-verified image tag

## Process
1. Trigger DevOps `production-deployment` skill.
2. Monitor production deployment.
3. Open a 30-minute post-deploy monitoring window: watch Grafana error rates, latency, Kafka lag.
4. If issues detected: immediately surface to Edward, suggest `/rollback`.

## Outputs
Production deployment triggered and monitored.

## Quality Gates
- [ ] Only triggered after explicit Edward approval
- [ ] Same image tag as staging used (no rebuild)
- [ ] 30-minute monitoring window observed
- [ ] Issues surfaced to Edward immediately with rollback suggestion

## References
- `.claude/skills/devops-engineer/production-deployment/SKILL.md`
- `.claude/skills/release-manager/post-release-monitoring/SKILL.md`
- `.claude/skills/release-manager/rollback-execution/SKILL.md`
