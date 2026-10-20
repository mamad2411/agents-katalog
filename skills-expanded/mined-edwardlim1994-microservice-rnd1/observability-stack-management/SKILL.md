# Observability Stack Management

## Purpose
Manages the shared observability stack infrastructure (OTEL, Alloy, Loki, Tempo, Prometheus, Grafana).

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
Cluster bootstrap; new datasource/dashboard need; pre-release health check.

## Inputs
- Observability stack deployment

## Process
Manages: OTEL collector, Alloy, Loki, Tempo, Prometheus, Grafana.
- Wires datasources in Grafana (Loki, Tempo, Prometheus).
- Configures scrape targets for Prometheus.
- Configures log ingestion pipelines for Alloy → Loki.
- Maintains infra dashboards (node CPU, memory, pod health, PVC usage).

Does NOT create business metric dashboards (Data Engineer's job). Does NOT instrument application code (Backend Developer's job).

Verifies observability stack healthy before each release deployment.

## Outputs
Healthy, wired observability stack with infra dashboards.

## Quality Gates
- [ ] All datasources wired in Grafana
- [ ] Scrape targets and log pipelines configured
- [ ] Infra dashboards maintained (not business metrics)
- [ ] Stack health verified before every release deployment

## References
- `.claude/skills/devops-engineer/cluster-bootstrapping/SKILL.md`
- `.claude/skills/devops-engineer/resource-monitoring/SKILL.md`
