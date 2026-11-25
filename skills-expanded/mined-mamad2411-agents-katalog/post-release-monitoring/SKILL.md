# Post-Release Monitoring

## Purpose
Monitors production health for 30 minutes immediately after deployment.

## Role
Release Manager

## Phase
Release (30 minutes after production deployment)

## Triggered By
`production-release-trigger` deployment completes.

## Inputs
- Grafana dashboards (error rate, latency, Kafka lag, pod restarts)

## Process
Monitor Grafana dashboards:
- Error rate: baseline + 10% acceptable, above = investigate
- Response times: p99 within SLA thresholds
- Kafka consumer lag: increasing trend = investigate
- Pod restarts: should be 0 (any restart = investigate)

Report: all clear OR specific issue to Edward.

## Outputs
All-clear confirmation or specific issue report to Edward.

## Quality Gates
- [ ] All four metrics monitored for the full 30-minute window
- [ ] Any threshold breach investigated immediately
- [ ] Report to Edward is specific, not generic

## References
- `.claude/skills/release-manager/production-release-trigger/SKILL.md`
- `.claude/skills/release-manager/rollback-execution/SKILL.md`
- `.claude/skills/devops-engineer/observability-stack-management/SKILL.md`
