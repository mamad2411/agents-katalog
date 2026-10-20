---
name: kubeblocks-observability-router
version: "0.1.0"
description: Primary observability entry for KubeBlocks-managed databases. Use this when the user broadly asks for monitoring or observability and you need to choose between integrating with an existing stack, bootstrapping a new stack, or declaring the current readiness level. The legacy kubeblocks-setup-monitoring skill remains only as a compatibility shim.
---

# Observability Router

Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) as the machine-readable truth for exporter evidence, scrape evidence, dashboard evidence, alerting evidence, and the maximum readiness ceiling for each Tier-1 engine.

## Routing Contract

- If Prometheus/Grafana already exists, route to [kubeblocks-observability-existing-stack](../kubeblocks-observability-existing-stack/SKILL.md).
- If no monitoring base exists but the engine has exporter evidence, route to [kubeblocks-observability-bootstrap-stack](../kubeblocks-observability-bootstrap-stack/SKILL.md).
- If the matrix says `exporter: false`, do not claim `scrape-ready` or higher without fresh evidence from the target environment.
- Always state whether the current state is `none`, `metrics-ready`, `scrape-ready`, `dashboard-ready`, or `alerting-ready`.
- If observability evidence is unclear or the live cluster state disagrees with the matrix, route to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md) before promising a higher readiness level.
