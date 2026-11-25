---
name: monitoring-guard
description: Validates Prometheus metrics, Grafana dashboards, and the monitoring stack configuration to prevent silent breakage when exporter versions change
when_to_use: |
  Use this skill when the user:
  - Updates an exporter version in Docker Compose
  - Modifies Grafana dashboard JSON files
  - Changes Prometheus recording rules or alert rules
  - Reports that a dashboard shows "No data" or metrics are missing
  - Updates the monitoring role or Docker Compose configuration
  - Adds a new exporter or scrape target
  - Says "dashboard is broken", "metrics missing", "alerts not firing"
---

# Monitoring Guard — Olympus Cluster

## Monitoring Stack Architecture

The monitoring stack runs on **VM 203** (10.220.1.63) as Docker Compose services:

```
monitoring/
├── prometheus/       # Metrics collection + alerting
├── grafana/          # Dashboards + visualization
├── loki/             # Log aggregation
├── promtail/         # Log shipping (runs on all cluster nodes)
└── exporters/
    ├── node-exporter     # All 6 Proxmox nodes + all VMs
    ├── pve-exporter      # Proxmox VE metrics (runs on monitoring VM)
    ├── ceph-exporter     # Ceph cluster metrics
    ├── ipmi-exporter     # iDRAC hardware metrics
    ├── pbs-exporter      # Proxmox Backup Server metrics
    └── unifi-poller      # UniFi Dream Machine Pro metrics
```

## Health Check Commands

```bash
# SSH to monitoring VM
ssh ubuntu@10.220.1.63

# Check all containers running
docker compose ps

# Check each exporter is actually scraping
curl -s localhost:9100/metrics | head -5   # node_exporter
curl -s localhost:8082/pve                 # pve-exporter (check for 200 OK)
curl -s localhost:9283/metrics | head -5   # ceph-exporter

# Prometheus health
curl -s localhost:9090/-/healthy
curl -s localhost:9090/api/v1/targets | python3 -m json.tool | grep -E '"health"|"job"'
```

## Diagnosing "No Data" in Grafana

### Step 1: Check the exporter

```bash
# On monitoring VM — verify exporter returns data
curl -s localhost:<exporter_port>/metrics | grep <metric_name>
```

### Step 2: Check Prometheus is scraping

```bash
# Check target health in Prometheus
curl -s 'localhost:9090/api/v1/targets' | python3 -m json.tool | grep -A3 '"job": "<job_name>"'

# Query for a metric
curl -s 'localhost:9090/api/v1/query?query=<metric_name>' | python3 -m json.tool
```

### Step 3: Check if metric name changed

See `references/metric-registry.md` for known metric name changes between exporter versions.

In Prometheus, explore available metrics:
```bash
curl -s 'localhost:9090/api/v1/label/__name__/values' | python3 -m json.tool | grep <keyword>
```

### Step 4: Check recording rules

```bash
curl -s 'localhost:9090/api/v1/rules' | python3 -m json.tool | grep -E '"name"|"health"'
```

## Validating Dashboard Changes

When modifying a Grafana dashboard JSON:

1. **Extract metric names** — search for `"expr":` fields in the dashboard JSON
2. **Query each metric** in Prometheus to verify it exists
3. **Check label matchers** — `instance`, `job`, `host` labels must match what Prometheus records

```bash
# Extract all metric expressions from a dashboard JSON
cat roles/monitoring/files/grafana/dashboards/<dashboard>.json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); \
  [print(p.get('expr','')) for panel in d.get('panels',[]) \
  for t in panel.get('targets',[]) for p in [t]]"
```

## Common Breakage Patterns

### Config file permissions

Docker containers running as non-root can't read files created with mode 0600.

```bash
# Check permissions on config files
ls -la /opt/monitoring/prometheus/
# All .yml files should be 0644
sudo chmod 644 /opt/monitoring/prometheus/*.yml
```

### Prometheus scrape target not reachable

```bash
# Verify node_exporter is running on a Proxmox host
ssh root@10.220.1.8 "systemctl status prometheus-node-exporter"
# Should be active/running and listening on port 9100

# Verify from monitoring VM
curl -s 10.220.1.8:9100/metrics | head
```

### Loki not receiving logs

Promtail runs on each Proxmox node. Check:

```bash
# On a Proxmox node
systemctl status promtail
journalctl -u promtail -n 30

# rsyslog must be forwarding to promtail's port
cat /etc/rsyslog.d/99-promtail.conf
# Should contain: *.* action(type="omfwd" target="localhost" port="1514" protocol="tcp")
```

## Adding a New Exporter

When adding a new exporter to the monitoring stack:

1. Add the container to `roles/monitoring/templates/docker-compose.yml.j2`
2. Add config template to `roles/monitoring/templates/` or `files/`
3. Add Prometheus scrape job to `roles/monitoring/files/prometheus/prometheus.yml`
4. Add any required secrets to vault (`vault_<exporter>_api_token`)
5. Verify config file permissions will be `0644` in the role task
6. Test with `docker compose up -d <new_container>` before applying via Ansible

See `references/metric-registry.md` for the metric names exposed by each exporter.
