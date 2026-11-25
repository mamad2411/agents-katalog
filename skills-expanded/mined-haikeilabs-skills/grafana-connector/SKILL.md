---
name: grafana-connector
description: Grafana data connector — API reference, entity model, and usage patterns. Use when an agent needs to read or write Grafana data (dashboards, folders, datasources, alert rules, annotations), or when asked how to query, filter, paginate, or mutate Grafana resources. Prefer this skill over generic Grafana knowledge.
---

# Grafana connector — agent usage guide

Use this skill when an agent needs to interact with Grafana through its REST
API. It covers the Lexicon (endpoints), Pragmatics (how agents use them), and
Semantics (data returned and entity relationships).

There is no maintained official CLI for Grafana API operations beyond plugin
management (`grafana-cli`). Agents use the Grafana HTTP API directly.

## Key rules

- The agent never sees a Grafana credential. There is no `grafana` provider
  for `kei connectors create --provider`. Grafana is added as a remote MCP
  connector from a catalog template (`kei connectors create --template …`,
  see *Connect and credentials*), and each user connects their own account
  with OAuth.
- Dashboard and folder deletion is not available through the connector
  Kei checks — it is irreversible and requires admin permissions beyond the
  connector's scope.
- Resource types for Kei policy follow ADR-028; dashboards, folders, and
  datasources are addressed by immutable UID (panels and annotations by
  integer id). When asked which resource types Grafana declares, give all
  three facts: the six names (`folder`, `dashboard`, `panel`, `datasource`,
  `alert_rule`, `annotation`), that each is addressed by UID or integer id,
  and that they are declared per **ADR-028**.
- Prefer the unified alerting API (`/api/ruler/grafana/api/v1/rules`) over the
  deprecated legacy alerting API.

## Install

Agents load this skill automatically when the harness has the Haikei Skills
plugin installed. See the repo README for per-harness setup.

## Lexicon — endpoints and operations

### REST API

Base URL: `https://{instance}/api`

| Method | Endpoint | What it does | Agent notes |
| --- | --- | --- | --- |
| `GET` | `/api/folders` | List all folders | Returns uid, title, url, parentUid. Paginated with `limit` and `page`. |
| `GET` | `/api/folders/{uid}` | Get a single folder | Includes nested dashboard count and permission summary. |
| `POST` | `/api/folders` | Create a folder | Body: `{"title": "..."}`. Optionally `{"parentUid": "..."}` for nesting. |
| `GET` | `/api/search` | Search dashboards and folders | Query params: `query`, `type` (dash-db/dash-folder), `folderIds`, `tags`, `limit`, `page`. |
| `GET` | `/api/dashboards/uid/{uid}` | Get a dashboard by UID | Returns full dashboard model including panels, templating, annotations, links. |
| `GET` | `/api/dashboards/db/{name}` | Get a dashboard by slug name | Alternative to UID lookup. |
| `POST` | `/api/dashboards/db` | Create or update a dashboard | Body: `{"dashboard": {...}, "overwrite": true}`. The dashboard JSON model includes panels, rows, templating. |
| `DELETE` | `/api/dashboards/uid/{uid}` | Delete a dashboard | Irreversible. Requires admin permissions. |
| `GET` | `/api/datasources` | List all datasources | Returns id, uid, name, type (prometheus, graphite, postgres, etc.), url. |
| `GET` | `/api/datasources/uid/{uid}` | Get a datasource by UID | Full configuration including auth details (masked). |
| `GET` | `/api/datasources/name/{name}` | Get a datasource by name | Alternative to UID lookup. |
| `GET` | `/api/ruler/grafana/api/v1/rules` | List Grafana alert rules | Returns rules grouped by folder. Supports `dashboard_uid` and `panel_id` filters. |
| `GET` | `/api/alerting/rule/{id}` | Get a single alert rule | Includes condition, data source queries, no_data/error handling, notifications. |
| `POST` | `/api/alerting/rule` | Create an alert rule | Complex body: name, condition, data, folderUid, etc. |
| `GET` | `/api/alert-notifiers` | List available notifiers | Returns supported notification types (email, slack, pagerduty, etc.). |
| `GET` | `/api/annotations` | List annotations | Query params: `from`/`to` (epoch), `type` (annotation/alert), `tags`, `limit`. |
| `POST` | `/api/annotations` | Create an annotation | Body: `{"dashboardUID": "...", "panelId": N, "text": "...", "tags": [...]}`. |
| `DELETE` | `/api/annotations/{id}` | Delete an annotation | Irreversible. |
| `GET` | `/api/org` | Get current organization | Returns id, name, address. |
| `GET` | `/api/org/users` | List organization users | Returns id, userId, email, login, role (Admin/Editor/Viewer). |

### Connect and credentials

1. **Initial setup**: A workspace admin adds the Grafana MCP server from a
   catalog template (`kei` v0.1.32 or later; check `kei help`):
   ```
   kei connectors create --workspace W --kind mcp --template custom_mcp \
     --label "Grafana (prod)" --mcp-url https://<grafana-mcp-host>/mcp
   ```
   If the catalog lists a Grafana template (`GET /api/v1/connector-templates`),
   use its ID instead of `custom_mcp` and omit `--mcp-url` when the template
   has one. There is no `--provider grafana`. Nothing is read from stdin:
   each user connects their own Grafana account with OAuth, and Kei holds the
   token.

2. **Approve its tools**: the connector's tools are usable only after an org
   owner or admin approves the tool manifest the runtime submits:
   ```
   kei connectors manifests show <connector-id>
   kei connectors manifests approve <connector-id> <manifest-id>
   ```

3. **Runtime**: the runtime calls the MCP server with the user's token. The
   agent never sees it.

### Denied command surface

These actions are **not available** through the connector Kei checks — they fall
outside the connector's scope:

| Operation | Reason |
| --- | --- |
| Delete dashboards | Not available — irreversible; requires admin permissions beyond connector scope |
| Delete folders | Not available — irreversible; cascading deletion of contained dashboards |
| Modify organization settings (name, preferences) | Org-admin operation outside Kei-checked token |
| Manage API keys (create/delete service accounts) | Identity management outside connector scope |
| Manage user permissions / team membership | User management outside connector scope |
| Snapshot creation / sharing | Snapshot functionality may have separate Kei policies |

## Pragmatics — how agents use this connector

### Common use cases

1. **Dashboard discovery**: Search dashboards by folder, tag, or name. Use
   `GET /api/search` with `type=dash-db` and filter by `query` or `folderIds`.
2. **Dashboard content retrieval**: Fetch a full dashboard model via
   `GET /api/dashboards/uid/{uid}` to inspect panels, queries, templating
   variables, and annotations.
3. **Datasource inspection**: List configured datasources and their types to
   understand what data is available for queries.
4. **Alert rule review**: List alert rules, check their conditions and
   notification targets, review firing/already_firing/silenced status.
5. **Annotation management**: Create annotations for incidents or deployments,
   query existing annotations by time range and tags.

### Agent patterns

- Always use the `/api/` prefix — Grafana's proxy endpoints (like `/api/`)
  differ from its frontend routes.
- Prefer UID-based lookups (`/api/dashboards/uid/{uid}`) over name-based
  (`/api/dashboards/db/{name}`) for precision. UIDs are immutable; slugs
  change when the dashboard title changes.
- Use `GET /api/search` with `type=dash-folder` to discover folder UIDs, then
  use those UIDs to scope searches.
- The dashboard JSON model is large. When you only need specific panel
  queries, extract the `panels[]` array from the response.
- For write operations (create dashboard, update alert rule), the request
  body follows the Grafana dashboard JSON model — prefer reading an existing
  resource first to understand the shape, then modify.

### Pagination

Most Grafana list endpoints support `limit` and `page` (1-based) offset
pagination:

```
GET /api/folders?limit=100&page=1
```

The response typically includes a `Link` header or the metadata carries total
count information. For `GET /api/search`, use `limit` and `page` parameters.

For alert rules (`GET /api/ruler/grafana/api/v1/rules`), the response groups
rules by folder and does not paginate — all rules are returned at once.

### Rate limits

Grafana rate limiting depends on the deployment:

- **Self-hosted Grafana**: No built-in rate limits by default. The
  `api_rate_limit` config option (in requests per second) can be enabled by
  the administrator.
- **Grafana Cloud**: Rate limits vary by plan. Typical limits:
  - **Cloud Free / Pro**: 30 requests per 60 seconds per API key.
  - **Cloud Advanced / Enterprise**: Higher limits, contact support for
    specifics.

Check current rate limit from response headers: `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, `X-RateLimit-Reset`. On `429 Too Many Requests`,
implement exponential backoff with retry.

## Semantics — data model and entity relationships

### Entity hierarchy

```
organization               # id (integer); name
├── folder                 # uid (string); nestable via parentUid
│   └── dashboard          # uid (string); slug is human-readable title slug
│       ├── panel          # id (integer); unique within dashboard
│       │   ├── query      # part of panel JSON; references a datasource
│       │   └── alert      # linked to alert_rule by panel_id
│       ├── annotation     # id (integer); dashboard-level or global
│       └── templating     # list variable definitions; part of dashboard JSON
├── datasource             # uid (string); type (prometheus, postgres, etc.)
├── alert_rule             # uid (string); managed via unified alerting
│   └── contact_point      # name (string); notification destination
└── user                   # id (integer); login, email, role
```

### Resource types (ADR-028, for Kei policy)

Per [ADR-028](https://github.com/HaikeiLabs/kei/blob/main/docs/adr/028-policy-field-contract.md) §4, Grafana declares six
UID- or integer-addressed resource types for Kei policy (each declares its
parent type): `folder`, `dashboard`, `panel`, `datasource`, `alert_rule`,
`annotation`:

| Resource type | Parent type | Canonical id example |
| --- | --- | --- |
| `folder` | — | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` (UID) |
| `dashboard` | `folder` | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` (UID) |
| `panel` | `dashboard` | `42` (integer, unique within dashboard) |
| `datasource` | — | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` (UID) |
| `alert_rule` | — | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` (UID) |
| `annotation` | — | `123` (integer) |

### Key fields

| Entity | Field | Type | Meaning |
| --- | --- | --- | --- |
| `folder` | `uid` | string | Immutable unique identifier |
| `folder` | `title` | string | Display name (not unique) |
| `folder` | `parentUid` | string or null | Parent folder for nested folders |
| `dashboard` | `uid` | string | Immutable unique identifier |
| `dashboard` | `title` | string | Dashboard display name |
| `dashboard` | `slug` | string | URL-friendly name (changes on rename) |
| `dashboard` | `panels` | array | Panel definitions (objects with id, type, title, datasource, targets) |
| `panel` | `id` | integer | Sequential ID within the dashboard |
| `panel` | `type` | string | Panel type (timeseries, table, stat, bar_gauge, etc.) |
| `panel` | `datasource` | object | Reference to a datasource by uid or name |
| `datasource` | `uid` | string | Immutable unique identifier |
| `datasource` | `type` | string | Prometheus, Postgres, Graphite, Loki, etc. |
| `datasource` | `name` | string | User-assigned name |
| `alert_rule` | `uid` | string | Immutable unique identifier |
| `alert_rule` | `name` | string | Rule name |
| `alert_rule` | `state` | string | Normal, Pending, Alerting, NoData, Error |
| `annotation` | `id` | integer | Sequential annotation ID |
| `annotation` | `text` | string | Annotation content |
| `annotation` | `time` | epoch | Timestamp in epoch milliseconds |

### Relationships

- Folders are nestable (via `parentUid`). A dashboard belongs to exactly one
  folder (or the General folder, which has no UID).
- Dashboards contain panels. Each panel references a datasource (by `uid`)
  and defines one or more queries (`targets` or `datasource` objects).
- Datasources are organization-scoped. Multiple dashboards and panels can
  reference the same datasource.
- Alert rules are independent resources (not embedded in dashboards), but they
  reference a `dashboard_uid` and `panel_id` to indicate which panel they
  monitor.
- Annotations can be dashboard-level (linked to a dashboard UID and panel ID)
  or organization-level (no dashboard reference).
- A Grafana instance has one organization (in OSS) or may be multi-org
  (Grafana Enterprise / Cloud). Most API calls are scoped to the current
  organization of the authenticated user.

## Policy entries (examples)

```yaml
# Engineers can read dashboards in their team's folder
- effect: permit
  principal: group:engineers
  action: grafana_read
  resource: folder:a1b2c3d4-e5f6-7890-abcd-ef1234567890
  connector: grafana

# Only SREs can create or modify alert rules
- effect: permit
  principal: group:sre
  action: grafana_write
  capability: alert_rule.write
```

## Validation commands

```bash
# Verify this skill loads correctly
node scripts/verify-skills.mjs

# Run the connector's eval suite
node scripts/run-evals.mjs --skill grafana-connector --harness opencode \
  --model-profile glm-5.3-flash \
  --out evals-out/grafana-connector-glm-$(date +%F) --jobs 2
```

## Realistic usage boundaries

- **Do not** manage credentials — Kei handles authentication by authorizing
  each call and releasing the service-account token.
- **Do not** expose the raw service-account token in output, logs, or
  conversation — Kei masks the credential via the runtime.
- **Do not** assume write access — check policy before creating or modifying
  dashboards, folders, or alert rules.
- **Do not** use the deprecated Grafana legacy alerting API
  (`/api/alerts`) — prefer the unified alerting API
  (`/api/ruler/grafana/api/v1/rules`).
- **Do not** hardcode datasource UIDs or dashboard UIDs; resolve them by
  name or search first.
- **Do not** use `grafana-cli` for API operations — it only supports plugin
  management. Use the HTTP API for data operations.
