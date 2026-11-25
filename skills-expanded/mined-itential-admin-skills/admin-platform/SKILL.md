---
name: admin-platform
description: Monitor platform health, manage adapters and applications (start/stop/restart/configure), control workflow engine workers, manage database indexes, and check system status. Use for day-to-day platform operations and troubleshooting.
argument-hint: "[action or adapter-name]"
---

# Platform Administration - Health, Adapters, Applications & Engine

Day-to-day platform operations: is the platform healthy? Are adapters connected? Are workers running? Need to restart something? This skill covers monitoring, adapter/app lifecycle, engine control, and index management.

## Org, team & personal rules

Before using this skill, check `custom/org/`, `custom/team/` and `custom/dev/`
in this skill's own folder. Read every `.md` file found — any folder may be
empty or absent. Apply them on top of everything below; where a file overrides a
specific rule here, follow the override. More specific wins: dev > team > org >
this document. No customization may weaken this skill's safety
rules or put credentials in committed files.

---

## Concepts

- **Adapters** — connectors to external systems (ServiceNow, AWS, Meraki, etc.). Each has a state (RUNNING/STOPPED), connection config, and properties.
- **Applications** — internal platform apps (WorkFlowEngine, ConfigurationManager, MOP, etc.). Each can be started/stopped/restarted independently.
- **Workers** — job and task workers that execute workflow steps. Can be activated/deactivated.
- **Profiles** — saved configurations of adapter/app settings for different environments (dev/staging/prod).
- **Indexes** — MongoDB indexes used by platform apps. Can become stale and need rebuilding.

## Gotchas

- `GET /health/adapters` returns `{results: [...]}` — adapters are in the `results` array
- `GET /health/applications` also returns `{results: [...]}` — same shape
- Adapter lifecycle is `PUT` not `POST`: `PUT /adapters/{name}/restart`
- Adapter `{name}` is the **instance name** from `health/adapters` `id` field, NOT the package name
- Adapter properties endpoint: `PUT /adapters/{name}/properties` takes `{properties: {...}}` wrapper
- Application restart/stop/start uses the **app name** from `health/applications`, e.g., `WorkFlowEngine`
- `GET /health/system` returns OS-level stats (CPU, memory, uptime), NOT platform health
- `GET /health/server` returns platform version, node version, build info
- Accounts use `{results: [...], total: N}` shape — NOT `{data: [...]}`
- Workflow engine activate/deactivate is `POST` (no body required)
- **Rate limit can only be updated when workers are deactivated** — `POST /workflow_engine/deactivate` first, then update, then `POST /workflow_engine/activate`
- **Log level change uses a `properties` wrapper with `transport` and `level`** — `{"properties": {"transport": "file", "level": "debug"}}`, not `{"loglevel": ...}`. Transports: `file`, `console`, `syslog`
- `GET /adapters/{name}/changelogs` returns HTTP 500 with "Release notes are available online…" on 6.5 — release notes live at docs.itential.com, not in the API
- `GET /adapters/{name}/export` can fail with HTTP 500 (`Cannot read properties of undefined`); `GET /adapters/{name}` returns the same configuration (`name`, `type`, `model`, `properties`) and always works

## Health Monitoring

### Platform overview

```
GET /health/server
```
Returns: version, release, build, arch, platform, node version.
```json
{
  "version": "6.5.2",
  "release": "6.5.2",
  "build": "2025.114.11",
  "arch": "x64",
  "platform": "linux",
  "versions": {"node": "20.20.0", ...},
  "uptime": 123456,
  "memoryUsage": {...},
  "cpuUsage": {...},
  "dependencies": {...}
}
```

Quick version check: `GET /version` → returns just the version string.

### System health (OS-level)

```
GET /health/system
```
Returns OS-level stats: `arch`, `release` (kernel), `uptime`, `freemem`, `totalmem`, `loadavg`, `cpus`.

### Who am I?

```
GET /whoami
```
Returns current user: id, username, provenance, groups, roles.

### Adapter health

```
GET /health/adapters
```
```json
{
  "results": [
    {
      "id": "ServiceNow",
      "package_id": "@itentialopensource/adapter-servicenow",
      "type": "Adapter",
      "version": "...",
      "state": "RUNNING",
      "connection": {"state": "ONLINE"},
      "uptime": 123456
    }
  ],
  "total": 1
}
```

Key fields:
- `id` — instance name (use this for lifecycle commands)
- `package_id` — adapter package
- `state` — `RUNNING`, `STOPPED`, `ERROR`
- `connection.state` — upper-case, e.g. `ONLINE` when the adapter can reach its system

Adapter properties are not in the health response — use `GET /adapters/{name}`.

Single adapter: `GET /health/adapters/{name}`

### Application health

```
GET /health/applications
```
```json
{
  "results": [
    {
      "id": "WorkFlowEngine",
      "package_id": "@itential/app-workflow_engine",
      "type": "Application",
      "state": "RUNNING",
      "description": "...",
      "version": "..."
    }
  ],
  "total": 1
}
```

Single application: `GET /health/applications/{name}`

## Adapter Lifecycle

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/adapters/{name}/restart` | Restart an adapter |
| PUT | `/adapters/{name}/start` | Start a stopped adapter |
| PUT | `/adapters/{name}/stop` | Stop a running adapter |
| GET | `/adapters/{name}` | Get full adapter configuration |
| PUT | `/adapters/{name}` | Update adapter configuration |
| PUT | `/adapters/{name}/properties` | Update adapter properties only |
| PUT | `/adapters/{name}/loglevel` | Change adapter log level |
| GET | `/adapters/{name}/changelogs` | Change history — returns 500 on 6.5 (see Gotchas) |
| GET | `/adapters/{name}/export` | Export adapter configuration — may return 500; use `GET /adapters/{name}` |
| DELETE | `/adapters/{name}` | Delete an adapter |
| POST | `/adapters/import` | Import adapter configuration |

**Restart an adapter:**
```
PUT /adapters/ServiceNow/restart
```
No body required. Returns the updated adapter state.

**Update adapter properties:**
```
PUT /adapters/ServiceNow/properties
```
```json
{
  "properties": {
    "host": "https://instance.service-now.com",
    "authentication": {
      "username": "admin",
      "password": "new-password"
    }
  }
}
```
Note: the `properties` wrapper is required.

**Change log level:**
```
PUT /adapters/ServiceNow/loglevel
```
```json
{
  "properties": {
    "transport": "file",
    "level": "debug"
  }
}
```
Levels for `file` and `console`: `error`, `warn`, `info`, `debug`, `trace`, `spam`. For `syslog`: `debug`, `info`, `warning`, `error`. `PUT /applications/{name}/loglevel` takes the same body.

**Get adapter configuration schema:**
```
GET /schema/adapters/{name}
```
Returns the JSON Schema defining valid adapter properties. Use this to understand what fields are configurable.

## Application Lifecycle

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/applications/{name}/restart` | Restart an application |
| PUT | `/applications/{name}/start` | Start a stopped application |
| PUT | `/applications/{name}/stop` | Stop a running application |
| GET | `/applications/{name}` | Get full application configuration |
| PUT | `/applications/{name}` | Update application configuration |
| PUT | `/applications/{name}/properties` | Update application properties only |
| PUT | `/applications/{name}/loglevel` | Change log level |
| GET | `/applications/{name}/changelogs` | Get change history |

**Restart an application:**
```
PUT /applications/WorkFlowEngine/restart
```

**Get application schema:**
```
GET /schema/applications/{name}
```

## Workflow Engine Control

### Worker status

```
GET /workflow_engine/workers/status
```
```json
{
  "jobWorker": {"running": true, "clusterValue": "not defined", "localValue": "not defined", "startupValue": true},
  "taskWorker": {"running": true, "clusterValue": "not defined", "localValue": "not defined", "startupValue": true}
}
```

### Activate/deactivate engine

```
POST /workflow_engine/activate
POST /workflow_engine/deactivate
```
No body required. Controls whether the engine processes jobs.

### Rate limiting

```
GET /workflow_engine/workers/rate_limit
```
```json
{"rateLimit": 0, "rateLimitPeriod": 1}
```

```
PUT /workflow_engine/workers/rate_limit
```
```json
{"rateLimit": 10, "rateLimitPeriod": 1}
```
- `rateLimit` — max jobs per period (0 = unlimited)
- `rateLimitPeriod` — period in seconds

## Database Indexes

### List all indexes

```
GET /indexes
```
Returns an object keyed by collection name, each with `application` and an `indexes` array.

### Check index status

```
GET /indexes/status
```
Shows which collections have pending index rebuilds.

```
GET /indexes/{collection}/status
```
Status for one collection: `{"missing": [], "misnamed": [], "external": [], "indexed": 3, "total": 3, "collectionSize": 91391, "inProgress": false}` — rebuild when `missing` or `misnamed` isn't empty.

### Rebuild indexes

```
POST /indexes/{collection}
```
Triggers index rebuild for a collection. Use when queries are slow or after migrations.

## Customization

### Platform banner

```
GET /customization/banner
PUT /customization/banner
```
Set a platform-wide banner message (e.g., "Maintenance window tonight 10pm-2am"). `GET` returns `{"result": {...}}`; `PUT` takes the banner itself — `text`, `active`, `startTime`, `dismissible` and `allPages` are required:
```json
{
  "text": "Maintenance window tonight 10pm-2am",
  "active": true,
  "startTime": "2026-10-09T22:00:00.000Z",
  "endTime": "2026-10-10T02:00:00.000Z",
  "dismissible": true,
  "allPages": true,
  "backgroundColor": "#007dbc"
}
```

## Admin Scenarios

### 1. Platform health check
```
1. GET /version                              → confirm platform version
2. GET /health/server                        → check server health
3. GET /health/adapters                      → check all adapter states
4. GET /health/applications                  → check all app states
5. GET /workflow_engine/workers/status        → check workers running
6. Flag any STOPPED/ERROR adapters or apps
```

### 2. Restart a failing adapter
```
1. GET /health/adapters/{name}               → confirm it's in ERROR/STOPPED
2. PUT /adapters/{name}/restart              → restart it
3. GET /health/adapters/{name}               → verify RUNNING
4. If still failing: GET /adapters/{name}    → check configuration
5. GET /schema/adapters/{name}               → understand configurable properties
6. PUT /adapters/{name}/properties           → fix config if needed
```

### 3. Troubleshoot slow job processing
```
1. GET /workflow_engine/workers/status        → are workers running?
2. GET /workflow_engine/workers/rate_limit    → is rate limiting active?
3. GET /indexes/status                       → are indexes stale?
4. POST /indexes/{collection}                → rebuild if needed
5. PUT /workflow_engine/workers/rate_limit    → adjust if rate limited
```
