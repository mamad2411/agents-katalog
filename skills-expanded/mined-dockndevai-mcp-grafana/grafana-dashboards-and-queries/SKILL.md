---
name: grafana-dashboards-and-queries
description: Standards and working knowledge for operating Grafana through mcp-grafana — how Grafana is structured, the dashboard JSON model, querying datasources (PromQL/LogQL/SQL via the unified query API), and the conventions/rules to follow when building or editing dashboards. Use whenever a task involves reading, querying, building, or editing Grafana dashboards, panels, datasources, alerts, or annotations, so the same standards apply every time without being re-explained.
---

# Operating Grafana (mcp-grafana)

This skill is the durable standard for working with Grafana via `@dockndevai/mcp-grafana`. Follow it every time — it encodes how Grafana works and the conventions to keep, so nobody has to re-explain them.

## How Grafana is structured (mental model)

- **Org → Folders → Dashboards → Panels.** A dashboard is a JSON document; panels are its cells; each panel has one or more **targets** (queries) against a **datasource**.
- **Datasources** are backends (Prometheus, Loki, Mimir, InfluxDB, SQL, Tempo, …). Each has a stable **`uid`**. Queries go *through* Grafana, never directly to the backend.
- **Everything is addressed by `uid`**, not numeric id or title. Titles change; uids are stable. Always resolve a uid with `search`/`list_*` first.
- **Templating / variables** (`$var`) make a dashboard reusable across environments/instances. **Time range** and **refresh** are dashboard-level.
- **Alerts** are Grafana-managed rules (read them with `list_alert_rules`). **Annotations** are timestamped events overlaid on graphs (deploys, incidents).

## The read → edit → write loop (do it this way)

1. **Find** the dashboard: `search` (or `list_dashboards`) → get its `uid`.
2. **Read** the model: `get_dashboard(uid)` → returns `{ dashboard, meta }`. `dashboard` is the editable JSON model; `meta.folderUid`, `meta.version`, `meta.url` are context.
3. **Edit** the `dashboard` object in memory (add/change panels, targets, variables).
4. **Write** it back: `create_or_update_dashboard({ dashboard, folderUid, overwrite: true, message })`.
   - **Keep the existing `uid`** and set `overwrite: true` to update; **drop `id` and `version`** or pass them from meta — never invent them.
   - Grafana **versions every save**, so edits are reversible from history. Always pass a `message` describing the change.
5. Never hand-delete to "recreate" — deletes are irreversible via the API and gated behind admin + `GRAFANA_ALLOW_DELETE`.

## Dashboard JSON model — the standard shape

A minimal, correct dashboard model to create from:

```json
{
  "uid": "team-api-overview",
  "title": "API — Overview",
  "tags": ["api", "team-a", "owned:managed-by-mcp"],
  "schemaVersion": 39,
  "timezone": "browser",
  "time": { "from": "now-6h", "to": "now" },
  "refresh": "30s",
  "templating": { "list": [
    { "name": "ds", "type": "datasource", "query": "prometheus", "current": {} },
    { "name": "instance", "type": "query", "datasource": { "uid": "${ds}" },
      "query": "label_values(up, instance)", "refresh": 2, "includeAll": true, "multi": true }
  ]},
  "panels": [
    {
      "id": 1,
      "type": "timeseries",
      "title": "Request rate",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
      "datasource": { "type": "prometheus", "uid": "${ds}" },
      "fieldConfig": { "defaults": { "unit": "reqps" }, "overrides": [] },
      "targets": [
        { "refId": "A", "expr": "sum(rate(http_requests_total{instance=~\"$instance\"}[5m]))",
          "legendFormat": "{{method}}" }
      ]
    }
  ]
}
```

### Model rules (keep these)

- **`uid`**: short, stable, kebab-case, `<area>-<name>` (e.g. `payments-latency`). Reuse it for updates; never change it.
- **`title`**: `<Area> — <What>` (em dash), title case. The folder gives the team/environment; don't repeat it in the title.
- **`tags`**: always tag with the owning team and area; add `owned:managed-by-mcp` so machine-managed dashboards are discoverable. Tags are the primary way to find things later.
- **`schemaVersion`**: keep whatever `get_dashboard` returned when editing; use a current value (39+) for new ones.
- **`gridPos`**: 24-column grid. Standard panel is `w:12, h:8`; stat/gauge rows `w:6, h:4` or `w:4, h:4`. Lay panels left-to-right, top-to-bottom; don't overlap.
- **Panel `id`**: unique small integers within the dashboard; new panels get the next free id.
- **`datasource`** on panel and target: always `{ "type": "...", "uid": "..." }` (or `${ds}` variable). Never a bare name or numeric id.
- **`time`** default `now-6h` for overviews, `now-1h` for drill-downs; **`refresh`** `30s` for live ops boards, off for reports.

### Panel type by intent

| Intent | Panel type | Notes |
|---|---|---|
| A metric over time | `timeseries` | the default; set `unit` on `fieldConfig.defaults` |
| A single current number | `stat` | add thresholds (green/amber/red) |
| Utilisation 0–100% | `gauge` | set `min`/`max`, thresholds |
| Distribution / top-N | `bargauge` or `table` | |
| Logs | `logs` | Loki datasource, LogQL target |
| Heatmap of histograms | `heatmap` | |

Always set a **`unit`** (e.g. `reqps`, `s`, `percent`, `bytes`, `Bps`) — an unlabelled axis is a bug. Add **thresholds** for stat/gauge so a glance conveys health.

## Querying datasources (`query_datasource`)

Reads data through Grafana's unified query API. Give a **datasource uid** (from `list_datasources`), a query, and a **bounded time range**. Keep `maxDataPoints` small (default 100) — this feeds a model, not a screen.

- **Prometheus / Mimir** → `expr` = PromQL. Prefer `rate(counter[5m])` for counters, `histogram_quantile(0.95, sum by (le) (rate(bucket[5m])))` for latency, `sum by (label) (...)` to aggregate. Never graph a raw counter.
- **Loki** → `expr` = LogQL, e.g. `{app="api"} |= "error"` or a metric query `sum(rate({app="api"} |= "error" [5m]))`.
- **SQL** (Postgres/MySQL/ClickHouse via Grafana) → `rawSql` = a single **read-only SELECT**. Bound it with `LIMIT`; use the datasource's macros (`$__timeFilter(...)`, `$__timeGroup(...)`) so the range applies.
- Time range: `from`/`to` accept Grafana relative (`now-1h`, `now-24h`) or epoch-ms strings.
- Reading only — `query_datasource` never mutates. If a datasource isn't in `GRAFANA_DATASOURCE_ALLOWLIST` (when set), the call is refused.

### Query conventions (keep these)

- **Aggregate before returning**: `sum`/`avg by (...)` to a handful of series, not thousands.
- **Rate windows** ≥ 4× scrape interval (usually `[5m]`).
- **Percentiles** for latency (`p95`/`p99`), not averages.
- **Label-match with variables** (`instance=~"$instance"`) so a query works across targets.
- Return the smallest range and resolution that answers the question.

## Folder & organisation standard

- One folder per team or environment; keep `production` (or the configured `GRAFANA_PROTECTED_FOLDERS`) **read-only** — never write to or delete from a protected folder.
- Put new dashboards in the correct `folderUid`; don't leave them in *General*.
- Use `create_folder` before saving a dashboard into a new area.

## Safe operation rules (non-negotiable)

1. **Read before write.** Always `get_dashboard` before `create_or_update_dashboard` on an existing uid, and preserve its `uid`.
2. **Start read-only.** Only raise `GRAFANA_MODE` when the task truly needs writes; only enable `GRAFANA_ALLOW_DELETE` for a specific delete, then turn it back off.
3. **Never echo secrets.** Datasource credentials are redacted by the server; don't try to route around it.
4. **Deletes are last resort.** Prefer editing/versioning over delete; a delete of a dashboard or folder is not recoverable through the API.
5. **Annotate change.** When you deploy or run a risky op, `create_annotation` with a `deploy`/`incident` tag so the graphs tell the story later.

## Tool ↔ task map

- Discover: `get_health`, `search`, `list_dashboards`, `list_folders`, `list_datasources`.
- Understand: `get_dashboard`, `get_folder`, `get_datasource`, `list_alert_rules`, `list_annotations`.
- Query data: `query_datasource`.
- Build/edit: `create_or_update_dashboard`, `create_folder`, `create_annotation`.
- Remove (admin + allow-delete): `delete_dashboard`, `delete_folder`, `delete_annotation`.
