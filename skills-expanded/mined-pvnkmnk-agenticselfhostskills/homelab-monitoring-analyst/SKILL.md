---
name: homelab-monitoring-analyst
description: Analyzes metrics, alerts, and logs from homelab services to identify issues and recommend remediation.
---

# homelab-monitoring-analyst

Reads monitoring data from Prometheus, Grafana, Netdata, or equivalent observability stacks and translates raw metrics into actionable insights. Identifies anomalies, correlates events, and recommends next steps.

## Invocation

**OpenCode / Codex:** `Invoke homelab-monitoring-analyst`
**Freebuff:** `/skill homelab-monitoring-analyst`

## Workflow Steps

1. **Query metrics:** Pull current CPU, RAM, disk, and network stats from available monitoring endpoint.
2. **Check alerts:** Review any active or recently fired alerts.
3. **Log scan:** Check service logs for errors, warnings, or restart events.
4. **Correlate:** Link metric spikes to log events or recent changes.
5. **Diagnose:** Identify root cause or most likely cause.
6. **Recommend:** Propose remediation steps ranked by confidence.
7. **Log:** If a change is recommended, hand off to `homelab-change-planner`.

## Data Sources

- Prometheus / Alertmanager
- Grafana dashboards
- Netdata
- Docker/Podman container stats
- System journal (`journalctl`)
- Proxmox task logs

## Companion Skills

- `homelab-change-planner` — act on findings
- `homelab-safe-ops` — safety gate before any remediation
- `homelab-logbook` — log findings

## References

- Prometheus docs: https://prometheus.io/docs/
- Netdata: https://learn.netdata.cloud/
