# Resource Monitoring

## Purpose
Creates Grafana dashboards for cluster and service resource visibility, and automates cleanup/retention.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New resource visibility need; ongoing operation.

## Inputs
- Observability stack (from `observability-stack-management`)

## Process
Creates Grafana dashboards for resource visibility:
- Per-namespace CPU + memory (UAT namespaces especially)
- PostgreSQL connection pool utilisation per service
- Kafka consumer lag per topic (leading indicator of processing issues)
- Harbor storage consumption
- PVC usage per service
- Node-level resource headroom

Automated PVC cleanup: Kubernetes CronJob runs daily, cleans orphaned PVCs. Harbor image retention: automated policy (keep last 10 tags per branch). Alert thresholds: notify PM + DevOps when cluster reaches 80% capacity.

Purpose: DevOps exposes data, QA interprets results during performance testing.

## Outputs
Resource dashboards, automated PVC cleanup, capacity alerts.

## Quality Gates
- [ ] All listed dashboards created
- [ ] Daily PVC cleanup CronJob running
- [ ] Harbor retention policy automated
- [ ] 80% capacity alert notifies PM + DevOps

## References
- `.claude/skills/devops-engineer/observability-stack-management/SKILL.md`
- `.claude/skills/qa-engineer/performance-testing/SKILL.md`
- `.claude/skills/qa-engineer/stress-testing/SKILL.md`
