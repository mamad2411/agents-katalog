---
name: grafana-dashboard-architect
description: Defines the architecture, philosophy, and structural contracts for the homelab Grafana dashboard system. Covers dashboard hierarchy, variable naming, drilldown flow, signal ownership, and scaling rules. Use when designing, building, or reviewing Grafana dashboards, panels, or queries for this homelab.
---

# Grafana Dashboard Architecture

Structural rules for the homelab Grafana system: hierarchy, ownership, variable contract, drilldown flow. Per-dashboard specs live in reference files. Targets **Grafana v12.x** (legacy schema v1; schema v2 not adopted). Docs: [Variables](https://grafana.com/docs/grafana/latest/visualizations/dashboards/variables/variable-syntax/) · [Data links](https://grafana.com/docs/grafana/latest/panels-visualizations/configure-data-links) · [URL variables](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/create-dashboard-url-variables).

## Guiding Principles

Overview = triage (what/where); workbenches = investigation (why). Every dashboard has an exit (links to next level). Variables are the API: same names/semantics everywhere. Time range = incident window; preserve it in drilldowns. Labels = schema (Alloy contract). Scale by labels, not by cloning. Fewer dashboards, more variables.

---

## MCP and Checking Your Own Work (Mandatory — Do Not Skip)

**Grafana MCP server (user-grafana)** is the source of truth for create/update and validation. Use it for: dashboard create/update, PromQL/LogQL query validation, datasource checks, and panel/dashboard PNG rendering. **Do not assume hand-written JSON is correct.**

### Phase 1 — Intent & Troubleshooting Goal

- Identify the **purpose** of the dashboard.
- Define **what problem** it helps detect.
- Define **how** it helps find root cause.
- Clarify the **main question** it should answer.

### Phase 2 — Design Before Implementation

Design the layout before writing JSON. Do not implement first and fix later.

- **Visual hierarchy:** Most important signals top-left; logical flow overview → breakdown → deep dive.
- **Grouping:** Use rows to separate sections (e.g. system overview, component breakdown, error/saturation, deep-dive).
- **Density:** Limit to 3–4 panels per row; consistent panel sizing; avoid clutter and unnecessary panels.
- **Clarity over density:** Prefer fewer strong panels over many small noisy ones. Do not overcrowd.

### Phase 3 — Implementation with Validation

When creating or modifying dashboards:

- **Use MCP** (user-grafana server) to create or update dashboards — do not assume hand-written JSON is correct.
- **Validate** that the dashboard saves successfully.
- **Validate** that all queries return data; ensure datasources are reachable; check for syntax errors or broken expressions.

Correctness is not confirmed until the dashboard saves and queries run. Do not assume correctness after writing JSON.

### Phase 4 — Mandatory Visual Verification Loop

After every dashboard creation or modification:

1. **Render** the dashboard or panels to PNG using Grafana MCP rendering (user-grafana).
2. **Inspect** the visual output for: overlapping legends, cluttered layouts, inconsistent panel sizes, poor spacing, bad color contrast, misleading Y-axis scales, empty or broken panels, unreadable labels.
3. If issues exist: update JSON → re-upload via MCP → re-render → repeat until clean and readable.

Rendering is **required**, not optional. Iterate until the result is clean and readable. Validate via API **and** visually; do not assume correctness after either step alone.

### Workflow Summary

Before building: (1) Define intent and troubleshooting goal. (2) Design layout first (hierarchy top-left → breakdown → deep dive; rows for sections; 3–4 panels per row; clarity over density). (3) Implement via MCP and validate save + queries. (4) Render → inspect → fix until clean.

---

## Dashboard Hierarchy

```
D00: Homelab Overview               ← entry (fleet health, triage)
 ├── D01a: Host Workbench           ← VM CPU, memory, disk, I/O
 ├── D01b: Container Workbench      ← container resources, lifecycle, per-service
 ├── D02: Log Workbench             ← log exploration, error triage
 ├── D03: Network/Connectivity      ← probes, DNS, throughput, TLS
 ├── D04: Media Pipeline            ← queue, transcoding, sessions (planned)
 └── D05: Hardware/Host             ← Proxmox host, temps, SMART (planned)
```

### Physical Topology Mapping

The dashboard hierarchy maps directly to the physical infrastructure layers. No dedicated "data center" or "node" dashboard is needed — the existing dashboards cover every level via the variable cascade.

| Physical Layer | Dashboard | Primary Variable | What You See |
|----------------|-----------|------------------|--------------|
| Fleet / DC | D00 Overview | `$node=All` | Aggregated health across all nodes and VMs |
| Proxmox Node | D05 Hardware/Host | `$node` | Bare-metal CPU, temps, SMART, VM allocation |
| VM | D01a Host Workbench | `$host` | Per-VM CPU modes, memory, disk, I/O |
| Container | D01b Container Workbench | `$service` | Per-container CPU, memory, network, lifecycle |

### Ownership Rules

| Dashboard | Owns | Does NOT Own |
|-----------|------|--------------|
| **D00 Overview** | Fleet health: availability, connectivity (public HTTP probe + internal DNS probe), error attribution (VM + service), change detection, resource saturation summaries, data freshness | Per-container detail, log text, service-specific metrics, historical trend analysis, warning-level log counts, per-probe breakdown |
| **D01a Host Workbench** | Host metrics (CPU/RAM/disk/swap/inodes), CPU steal time, OOM kill counter, I/O wait, I/O latency, load average, NFS mount filesystem metrics, compact container summary table (bridge to D01b) | Per-container time series, container lifecycle/restart timeline, log content, application-level metrics, probe results |
| **D01b Container Workbench** | Container resource consumption (CPU, memory, Mem Limit %, network), restart timeline, per-container detail time series, container lifecycle events | Host CPU modes, host memory breakdown, disk I/O, log content, probe results |
| **D02 Log Workbench** | Log exploration, error/warn streams, log volume rates, pattern detection | Host resource metrics, container lifecycle |
| **D03 Network/Connectivity** | All Blackbox probe results, DNS resolution detail, inter-VM reachability matrix, per-service proxy health, network throughput per VM/container, packet errors/drops, TLS cert expiry | Host resource metrics, log content |
| **D04 Media Pipeline** | Download queue depth, indexer reachability, Plex/Jellyfin active sessions and transcoding load, library stats | Infrastructure metrics, log text |
| **D05 Hardware/Host** | Proxmox host CPU/RAM/storage, VM allocation vs capacity, CPU temperatures, SMART disk health, container image currency | Per-VM application metrics |

### When to Create an Exception Dashboard

Only when ALL of these are true:

1. The domain has signals that are meaningless outside its context (e.g., queue depth, download rates, library size)
2. Those signals cannot be surfaced via a workbench variable filter
3. The target audience would otherwise need to mentally join 2+ workbenches

If in doubt, add a row to a workbench first.

### Signals That Commonly Get Misplaced

| Signal | Wrong placement | Correct placement | Reason |
|--------|----------------|-------------------|--------|
| Network throughput per VM | D00 | D01a | No meaningful fleet threshold — 50 MB/s on media is normal, same on core is suspicious |
| Per-probe breakdown (which DNS/HTTP check failed) | D00 | D03 | D00 only needs binary pass/fail; investigation belongs on D03 |
| CPU steal time | D00 | D01a | Proxmox-specific signal; investigation context, not triage |
| OOM kill count | D01a only | D00 (change detection) + D01a (timeline) | An OOM kill is a fleet-level event worth surfacing immediately; `node_vmstat_oom_kill` is the metric |
| Inode exhaustion | disk panel | D01a separate panel | Standard disk % hides inode exhaustion; they are independent failure modes. `node_filesystem_files_free / node_filesystem_files` |
| TLS cert expiry | D00 | D03 (with days-to-expiry warning forwarded to D00 if critical) | Expiry timeline is investigation detail; only "expires in <3 days" is triage-urgent |
| NAS storage remaining | invisible (not currently shown) | D00 Disk panel (current %) + D04 (media volume trend) | VM root disks are shown but NAS is invisible. `node_filesystem_avail_bytes{fstype=~"nfs|nfs4"}` on the mounting VM requires no new tooling. |
| NFS mount health (stale/hung?) | D03 TCP probe alone | D03 TCP probe + D01a (mountpoint metrics present) + D02 (I/O error logs) | TCP to port 2049 confirms NAS is up; it does not confirm the mount is working. Three signals together cover the full failure surface. |
| Swap usage | memory panel | D01a separate stat | Swap being used at all means memory pressure exceeded RAM; deserves its own signal, not a footnote on the memory gauge |
| Container Mem Limit % | D01a host view | D01b container resource table | Memory limit pressure is per-container investigation; meaningless without container context |
| Container restart timeline | D01a host view | D01b container lifecycle section | Restart events are container-level signals; the host workbench only needs the summary count in the bridge table |

---

## Source of Truth

Read before building: **`docker_compose/monitoring/bootstrap.py`** — Alloy label contract (`ensure_alloy_config()`), Prometheus targets (`ensure_prometheus_config()`), Grafana provisioning. **`docker_compose/monitoring/compose.yml`** — containers, ports. Canonical labels: bootstrap.py wins over tables below.

### Planned Signal Sources (not yet in stack)

| Component | Adds | Needed by |
|-----------|------|-----------|
| **Blackbox Exporter** | HTTP/DNS/TCP/ICMP/TLS probes from monitoring VM | D00 Connectivity panel (HTTP + DNS + NAS TCP), D03 Network dashboard |
| **Proxmox node_exporter** (on pve1) | Host-level CPU, RAM, disk, temperatures | D05 Hardware/Host |
| **smartd_exporter** or `node_exporter` SMART collector | Disk SMART health data | D05 Hardware/Host |
| **Reverse proxy metrics endpoint** (Nginx stub_status, Traefik /metrics, Caddy /metrics) | Request rates, 5xx counts, response latency per service | D03 (per-service proxy health) |
| **Diun or Watchtower** | Container image update availability | D01b or D05 |
| **NAS node_exporter** (Synology community package or Docker) | NAS disk, CPU, RAM, temperature from the NAS itself | D04 (NAS storage trend), D05 (hardware health). Without this, NAS storage is visible only via the NFS-mounted filesystem metrics on the mounting VM — useful but indirect. |

**NAS/NFS signal availability without extra tooling:** If a VM (e.g., `media`) has the NAS NFS-mounted, node_exporter on that VM already exports `node_filesystem_avail_bytes{fstype=~"nfs|nfs4"}` for the mount path. This is collected by Prometheus today with no changes. The D00 Disk panel and D04 NAS storage trend can use this immediately for the NAS volumes that are mounted on that VM.

Do not design panels for these until the source is running and scraped.

---

## Label Contract (Quick Reference)

Authoritative: `ensure_alloy_config()` in `bootstrap.py`. `M` = on Prometheus metrics.

| Label | Meaning | Example | On Metrics |
|-------|---------|---------|------------|
| `node` | Proxmox host | `pve1` | M (all jobs) |
| `host` | VM hostname (globally unique) | `monitoring`, `core`, `media` | M (all jobs) |
| `vm_role` | VM's functional role | `monitoring`, `core`, `media`, `apps`, `accelerated` | M (all jobs) |
| `env` | Environment | `prod` | M (all jobs) |
| `service` | Logical service identity | `grafana`, `sonarr`, `alloy` | M (all jobs; cAdvisor via relabeling) |
| `container` | Container instance name | `grafana`, `sonarr-1` | M (cAdvisor via relabeling; alias for `name`) |
| `source` | Log origin type | `docker` | — (logs only) |

**`host`:** Must be globally unique (all `by (host)` and `{{host}}` rely on it). Proxmox singleton model guarantees one VM per hostname.

### Strong (present when available)

| Label | Meaning | On Metrics |
|-------|---------|------------|
| `level` | Normalized: `trace`, `debug`, `info`, `warn`, `error`, `fatal`, `unknown` | — (logs only) |
| `compose_project` | Docker Compose project name | M (cAdvisor via relabeling) |
| `image` | Container image (tag only, no digest) | M (cAdvisor; digest stripped via relabeling) |
| `stream` | `stdout` / `stderr` | — (logs only) |

### Compatibility (do not use as canonical in new dashboards)

| Label | Maps to |
|-------|---------|
| `job` | = `service` |
| `instance` | = `host` |

---

## Variable Contract

Same names everywhere so drilldown URLs work. Cascade: `$node → $vm_role → $host → $service`; each query filters by upstream.

| Variable | Type | Multi | Purpose |
|----------|------|-------|---------|
| `$datasource_prometheus` / `$datasource_loki` | datasource | no | Switch without editing queries |
| `$node` | query | yes | Proxmox node |
| `$vm_role` | query | yes | Primary grouping |
| `$host` | query | yes | VM hostname |
| `$service` | query | yes | Service identity |
| `$env` | custom | no | `prod` (hidden) |

**Formats:** `${host}` = regex for PromQL/LogQL. **Drilldown URLs:** use `${host:queryparam}` for multi-value (produces `var-host=media&var-host=core`); plain `var-host=${host}` is regex-escaped and wrong for URL params.

Each variable's query filters by the selections upstream. This ensures selecting `vm_role=media` only shows hosts and services that belong to the media VM.

### Variable Definitions

| Variable | Type | Multi | Default | Purpose |
|----------|------|-------|---------|---------|
| `$datasource_prometheus` | datasource | no | Prometheus | Allows switching without editing queries |
| `$datasource_loki` | datasource | no | Loki | Same for log queries |
| `$node` | query | yes | All | Proxmox node filter (currently single-node `pve1`; multi-node not planned but supported by the label contract) |
| `$vm_role` | query | yes | All | Primary grouping axis |
| `$host` | query | yes | All | VM hostname, filtered by `$node` + `$vm_role` |
| `$service` | query | yes | All | Service identity, filtered by upstream vars |
| `$env` | custom | no | `prod` | Hidden; exists for future staging support |

Not every dashboard exposes every variable. The overview may hide `$service` (too granular). But the **names must match** so links work.

### Variable Format Options (Reference)

When interpolating variables in queries or URLs, Grafana supports format suffixes. The most useful for this dashboard system:

| Format | Syntax | Output | Use case |
|--------|--------|--------|----------|
| Default (regex) | `${host}` | `(media\|core)` | PromQL/LogQL label matchers (automatic) |
| Pipe | `${host:pipe}` | `media\|core` | Manual regex contexts |
| CSV | `${host:csv}` | `media,core` | Non-regex contexts |
| Query param | `${host:queryparam}` | `var-host=media&var-host=core` | Building drilldown URLs — handles multi-value correctly |
| Raw | `${host:raw}` | `media,core` | Unescaped comma-separated; use when Grafana's auto-escaping interferes |
| Percent encode | `${host:percentencode}` | `media%2Ccore` | URL-safe encoding for external links |

> The `:queryparam` format is particularly useful for drilldown URLs when a variable might have multiple values selected. Instead of `var-host=${host}` (which produces a single regex-escaped string), `${host:queryparam}` produces proper multi-value URL parameters that Grafana interprets correctly on the target dashboard.

### Variable Queries (Pattern)

Variables cascade using **Label values** queries with optional metric filters.

> **Grafana v12+ (structured query editor):** The Prometheus data source provides a dropdown-based **Query type** selector. Use the **Label values** query type with explicit `label` and optional `metric` fields instead of the legacy `label_values()` string syntax, which is now classified as **Classic query** and deprecated.

#### Structured query editor (preferred — Grafana v12+)

| Variable | Query Type | Label | Metric (filter) |
|----------|-----------|-------|-----------------|
| `$node` | Label values | `node` | `up` |
| `$vm_role` | Label values | `vm_role` | `up{node=~"$node"}` |
| `$host` | Label values | `host` | `up{node=~"$node", vm_role=~"$vm_role"}` |
| `$service` | Label values | `service` | `up{host=~"$host"}` |

#### Classic query syntax (deprecated — avoid in new dashboards)

```
label_values(up, node)
label_values({node=~"$node"}, vm_role)
label_values({node=~"$node", vm_role=~"$vm_role"}, host)
label_values({host=~"$host"}, service)
```

If the existing dashboards still use classic `label_values()` strings, they continue to work. Migrate to the structured editor when next editing variable definitions.

---

## Drilldown Flow

### URL Contract

Drilldown links pass context via URL parameters:

```
/d/<dashboard-uid>?${__url_time_range}&var-vm_role=${vm_role}&var-host=${host}
```

Every drilldown link MUST include:

1. **Time range**: `${__url_time_range}` (expands to `from=<epoch>&to=<epoch>`) or the explicit `from=${__from}&to=${__to}` form
2. **Relevant variables**: only the ones the target dashboard uses

> **Grafana v11+:** `${__url_time_range}` is the preferred shorthand for time range propagation. It produces the same `from=...&to=...` query string but avoids manual parameter assembly. The explicit `from=${__from}&to=${__to}` form still works and is equivalent.

### Flow Map

```
D00 (Overview)
 │
 ├─ [VM status / saturation / OOM] ──→ D01a (Host Workbench)
 │     passes: time, $vm_role, $host
 │
 ├─ [Container deficit / restarts] ──→ D01b (Container Workbench)
 │     passes: time, $vm_role, $host
 │
 ├─ [Error rate spike] ──→ D02 (Log Workbench)
 │     passes: time, $vm_role, $host, level=error
 │
 └─ [Domain signal] ──→ D03+ (Exception)
       passes: time, $vm_role, $host

D01a (Host Workbench)
 │
 └─ [Container summary table row] ──→ D01b (Container Workbench)
       passes: time, $host, $service

D01b (Container Workbench)
 │
 └─ [Container with errors / "View Logs"] ──→ D02 (Log Workbench)
       passes: time, $host, $service
```

Time range = incident window; drilldowns carry `from`/`to`. Every anomaly should have a click path to the next level.

---

## Interactivity Contract

Every visible signal should be clickable. Dashboards follow a **Focus → Investigate** progressive disclosure pattern. The Drilldown Flow section above covers cross-dashboard URL mechanics. This section defines the click *philosophy* — what happens when the operator clicks, and what insight they should expect next.

### Progressive Disclosure

Two click depths, applied consistently across all dashboards:

1. **Focus (same dashboard):** Clicking a series, row, or cell narrows the current view. A time series showing all containers' network traffic, when one container's line is clicked, updates `$service` to that container. The dashboard re-renders showing only that container's data across all panels.

2. **Investigate (cross-dashboard):** From a focused view, a second click drills to the workbench that owns the next level of detail. From the focused container on D01b, a "View Logs" link opens D02 pre-filtered to that service at the same time window.

Every visible anomaly should have a click path to its explanation. The operator should never see something interesting without knowing where to click next.

### Implementation Patterns

**Same-dashboard focus (variable update via self-link):**

```
/d/${__dashboard.uid}?${__url_time_range}&var-service=${__data.fields.service}&var-node=${node}&var-vm_role=${vm_role}&var-host=${host}
```

Navigates to the same dashboard with one variable narrowed. All upstream variables are preserved to prevent cascade resets. The dashboard re-renders with narrowed scope.

**Cross-dashboard drilldown:**

```
/d/<target-uid>?${__url_time_range}&var-host=${__data.fields.host}&var-service=${__data.fields.service}
```

**Rules for all click links:**

- Every link includes `${__url_time_range}` (or the equivalent `from=${__from}&to=${__to}`) — the time window is the incident context
- Same-dashboard focus links preserve all upstream variables (`$node`, `$vm_role`, `$host`) to prevent cascade resets
- Cross-dashboard links include only the variables the target dashboard uses
- Use `${__data.fields.<name>}` for row/cell-specific values (tables, stat panels)
- Use `${__field.labels.<labelname>}` when you need a specific Prometheus/Loki label from the series (alternative to `${__data.fields.*}` when the field name matches a label)
- Use `${variable_name}` for current dashboard variable values (filter-wide drilldowns)

### What the Next Click Should Show

The expected next insight depends on what the operator is looking at:

| Signal type on screen | Focus action (same dashboard) | Investigate action (cross-dashboard) |
|----------------------|------------------------------|-------------------------------------|
| Multi-host resource metric | Filter to one host | → D01a (from D00) or → D02 logs (from D01a) |
| Multi-container time series | Update `$service` to one container | → D02 for that service's logs |
| Error count or rate | Update `$service` to one service | → D02 with `level=error` |
| Container restart event | — (already specific) | → D02 with time narrowed to restart |
| Probe failure | — (already specific) | → D02 for service logs; D01a for host health |
| High network throughput | Filter to one host or container | → D03 (from D01a) or → D02 logs |
| Disk/storage warning | Filter to specific mount | → D02 for I/O error logs |
| Log error pattern | Filter log stream to that pattern | Terminal — operator reads and acts |
| Physical hardware signal | — (already specific) | → D01a for the affected VM |
| Container summary row (on D01a) | — (bridge table, no focus) | → D01b with `$host` + `$service` |

### Click Depth by Dashboard

| Dashboard | Typical depth | Pattern |
|-----------|--------------|---------|
| **D00 Overview** | 1 click | Always routes outward to a workbench. D00 never focuses itself. |
| **D01a Host** | 1–2 clicks | Click host panel → focus on host (1). Click bridge table row → D01b (2). |
| **D01b Container** | 1–2 clicks | Click table row → focus on container (1). Click focused panel → D02 logs (2). |
| **D02 Logs** | 1–2 clicks | Click service line → focus (1). Read logs → act (terminal). |
| **D03 Network** | 1–2 clicks | Click VM in throughput → focus (1). Click focused signal → D02 or D01a (2). |
| **D04 Media** | 1 click | Click pipeline stage → D02 for logs or D01a for resources. |
| **D05 Hardware** | 1 click | Click VM in allocation → D01a for that VM. |

### D00 Is Always Depth 1

The overview never focuses itself. Every click on D00 routes to a workbench. This is by design — the overview's job is routing, not investigation. If the instinct is "filter D00 to just this VM," the right action is opening D01a for that VM.

Each dashboard spec includes a **Click Flow Map** table documenting every clickable element, its action type (focus or investigate), and its target.

---

## Scaling Rules

**New VM:** Deploy with label contract + Prometheus scrape targets; no dashboard changes. Label values and variable-filtered queries include it automatically. **New Proxmox node:** Deploy node_exporter with `node=pve2`, etc.; `$node` and cascade handle it. (Current homelab is single-node; this is future-proofing.) **VM migration:** `host` stays, `node` changes → Prometheus shows two series over the migration window; expected, both have same `host`. **New signal source:** Put on the owning workbench; add D00 summary only if it indicates fleet-level health. D00 = aggregations only, never raw series.

---

## Visualization Reference

**Use:** Time series for `rate()`/`increase()`/metrics over time; Stat for KPIs/sparklines; Gauge for bounded % (e.g. CPU toward 100%); Bar gauge for per-VM saturation; State timeline for discrete states (container lifecycle, probe pass/fail); Table for Top Offenders, bridge tables, multi-column (cell modes: Color background, `applyToRow` for full-row, Sparkline, Gauge); Logs for D02. **Avoid:** Time series for discrete states; Stat for breakdowns; Pie for >6–7 slices or without absolute count. See [Grafana visualizations](https://grafana.com/docs/grafana/latest/panels-visualizations/) for full catalog.

---

## Transformations & Expressions Reference

Transformations manipulate query results client-side before rendering. Expressions compute server-side and can combine data across data sources. Both are critical tools for building the cross-query panels in this dashboard system (e.g., the Top Offenders table merging Loki error counts with cAdvisor restart data).

### Transformations (client-side, per-panel)

Transformations apply in order — each step receives the output of the previous step. Dashboard variables are interpolated before transformations run.

| Transformation | What it does | Used in this system |
|---------------|-------------|---------------------|
| **Merge** | Combines frames with matching fields into one frame (UNION-style). Matches by ALL shared label fields. | D00 Top Offenders: merging Loki error counts + cAdvisor restart counts |
| **Join by field** | Joins frames on a specific field (like SQL JOIN). Use when frames share a key but have different columns. | Pairing metrics from different queries by `host` or `service` |
| **Organize fields** | Rename, reorder, hide columns. | Every table panel — hide raw labels like `env`, `__name__`, `instance` |
| **Filter by name** | Show/hide specific fields by name or regex. | Removing internal Prometheus labels from table views |
| **Filter data by values** | Keep/exclude rows matching conditions (e.g., value > 0). | D00 Top Offenders: hiding zero-error rows |
| **Group by** | Group rows by field values and apply aggregations (sum, mean, count, min, max, first, last). | Aggregating per-service metrics before display |
| **Sort by** | Sort rows by a field. | Ranking Top Offenders by error count descending |
| **Reduce** | Collapse each series to a single value (last, mean, sum, count, min, max). | Converting time series to table values for instant-query tables |
| **Concatenate fields** | Combine all fields from all frames into a single frame. | Merging independent query results into one table |
| **Add field from calculation** | Create computed columns (binary math, unary ops, cumulative functions, window functions). | Health % column = Up / Expected |
| **Config from query results** | Use one query's results to dynamically set another query's panel config (thresholds, min, max, units, value mappings). | Dynamic thresholds from a config query — e.g., different CPU warning levels per VM role |
| **Convert field type** | Change field types (string → time, number → enum). | Formatting timestamps in restart tables |
| **Extract fields** | Parse JSON, key-value pairs, or regex from a field into separate fields. | Extracting structured data from log metadata |
| **Rows to fields** | Transpose rows into field configurations. Often paired with Config from query results. | Building per-host dynamic configurations |

**Non-obvious capabilities:**
- **Config from query results** can build value mappings dynamically from a query. A config query returning `Value | Text | Color` columns creates mappings applied to the real data query — enabling data-driven color schemes without hardcoding.
- **Filter by query** — when a panel has multiple queries, a transformation can be restricted to only one query's output using the filter icon on the transformation row.
- **Debug mode** — click the bug icon on any transformation row to see its input and output data frames side-by-side. Essential when chaining multiple transformations.

### Server-Side Expressions (cross-query computation)

Expressions run on the Grafana server, not the browser. They work with any backend data source and are the foundation of Grafana Alerting rules. Useful when combining metrics from Prometheus and Loki in the same panel, or performing math that neither data source can do natively.

| Expression type | What it does | Example |
|----------------|-------------|---------|
| **Math** | Free-form arithmetic, relational, and logical operations between query results. Supports `abs()`, `log()`, `round()`, `ceil()`, `floor()`, `is_nan()`, `is_null()`, `is_inf()`. | `$A / $B * 100` to compute percentage from two separate queries |
| **Reduce** | Collapse a time series into a single number (mean, min, max, sum, count, last). Labels are preserved. | Converting a time series to an instant value for alerting thresholds |
| **Resample** | Align timestamps across series to a common interval. Required when doing math between series with different scrape intervals. Supports pad, backfill, and fillna for empty windows. | Aligning node_exporter (15s) and cAdvisor (30s) metrics before division |

**Union semantics in Math:** When combining `$A + $B`, the expression engine joins by matching labels. If `$A` has `{host=media}` and `$B` has `{host=media}`, they match. Partial label matches (subset) also join. Two single-item collections always join regardless of labels.

---

## Best Practices

**Official reference:** [Grafana dashboard best practices](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/) — observability strategies (USE/RED, Four Golden Signals), dashboard maturity, creating and managing dashboards. The homelab rules below extend and align with that guidance.

### Strategy alignment

- **USE** (Utilization, Saturation, Errors) for infrastructure — host/container CPU, memory, disk, queues. D01a/D01b and D05 own these.
- **RED** (Rate, Errors, Duration) for services and user-facing behavior — alert on symptoms (RED) rather than causes (USE). D00 triage and D03/D04 service health follow RED where applicable.
- **Four Golden Signals** (Latency, Traffic, Errors, Saturation) — when adding service-level panels, prefer these over ad-hoc metrics.
- **Dashboard tells a story:** Logical progression (large → small, general → specific). Each dashboard answers a clear question; avoid dashboards without a goal.
- **Reduce cognitive load:** Graphs should be obvious at a glance; use meaningful color (e.g. thresholds: blue = good, red = bad), normalize axes (e.g. CPU by % not raw cores) where it helps.

### Design and workflow (homelab)

Design first; verify with MCP + render (do not assume). Layout: overview → breakdown → deep dive; rows for sections; 3–4 panels per row; clarity over density. When editing existing dashboards: improve clarity and flow, don't add redundant panels. **Avoid stacking** unless intentional — it can hide important data; turn off in most cases.

### Managing dashboards (from Grafana docs)

- **Avoid sprawl:** No duplicate dashboards for "one change"; use template variables and URL parameters for view customization. Prefix temporary dashboards with `TEST` or `TMP`; delete when done.
- **Don't copy then forget:** Copies miss updates; prefer links to the master dashboard + URL params. If you must copy, rename clearly and do **not** copy tags (tags drive search).
- **Directed browsing:** Most dashboards should be reachable via alerts or links from overview/dashboard-of-dashboards; browsing by search is the exception.
- **Documentation:** Add a Text panel for dashboard purpose, links, and instructions; add panel descriptions (visible on the (i) icon) for non-obvious panels.
- **Refresh rate:** Match to data cadence; avoid aggressive refresh (e.g. 30s) when data changes hourly.

### Query & panel essentials

**Queries:** Use `[$__rate_interval]` in `rate()`/`increase()`; instant queries for "current value" tables; recording rules for expensive aggregations (`level:metric:operations`).

**Panels:** Value mappings skip unit formatting (e.g. "All Up"); regex field overrides for bulk styling; `applyToRow: true` for full-row table color; state timeline for discrete states. Use left/right Y-axes when showing series with different units or ranges. **Variables:** `${host:queryparam}` for multi-value drilldown URLs. Repeat by variable: row = per-VM sections, panel = stat grids.

**Pitfalls:** Transformations break on field name changes (prefer regex in Filter by name). NoData in expressions → use `or on() vector(0)`. Pie charts hide magnitude — pair with absolute count. Stacked series: put anomalous at top. Stat sparklines are not interactive (no zoom/drilldown).

---

## Dashboard-Specific Specs

| Dashboard | File | Status |
|-----------|------|--------|
| D00 — Homelab Overview | [dashboard-00-overview.md](dashboard-00-overview.md) | Built |
| D01a — Host Workbench | [dashboard-01a-host-workbench.md](dashboard-01a-host-workbench.md) | Built |
| D01b — Container Workbench | [dashboard-01b-container-workbench.md](dashboard-01b-container-workbench.md) | Built |
| D02 — Log Workbench | [dashboard-02-log-workbench.md](dashboard-02-log-workbench.md) | Planning |
| D03 — Network/Connectivity | [dashboard-03-network.md](dashboard-03-network.md) | Planning |
| D04 — Media Pipeline | [dashboard-04-media-pipeline.md](dashboard-04-media-pipeline.md) | Planning — requires exportarr, qbittorrent-exporter, Jellyfin metrics |
| D05 — Hardware/Host | [dashboard-05-hardware-host.md](dashboard-05-hardware-host.md) | Planning — requires node_exporter on pve1, SMART collector |
