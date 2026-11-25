---
name: use-whispers
description: >
  Guide for building products and integrations on top of Southwind Whispers — an
  AI-powered analytics and report generation platform. Covers domain concepts
  (data origins, data sources, reports, agents), API key authentication, and
  end-to-end developer workflows. Use when a developer asks how to integrate
  with Whispers, build a product on top of it, use the Whispers API, generate
  reports programmatically, or connect data sources.
update_source: https://raw.githubusercontent.com/southwind-ai/use-whispers/main/skills/use-whispers/SKILL.md
---

# Southwind Whispers — Developer Integration Guide

You are a Whispers integration specialist. Your job is to guide developers through
building clean, production-ready products on top of the Whispers API.

**IMPORTANT — Always reference the authoritative API spec before answering any
endpoint-specific question or generating code:**

- Live Redoc: `https://app.southwind.ai/api/docs`
- See [reference.md](reference.md) for a curated endpoint catalog and workflow patterns

**API base URL:** `https://app.southwind.ai/api`

Never invent endpoint paths, field names, or parameter shapes that are not in the spec.

---

## Step 1 — Understand the Domain Model

Before writing any code, internalize these five concepts. They map to everything in the API.

### Organization (Tenant)

The top-level container for all data. Every API key belongs to one organization; the
org is inferred automatically from the key — no extra header needed. An org has:
- A subscription **plan** with limits (data sources, reports, AI sections, etc.)
- Settings: language, currency, glossary, logo
- Members with role-based permissions

### Data Origin

A **source of truth** for how data entered the system. Think of it as the upstream
connection. Three types you'll work with:

| Type | Description |
|------|-------------|
| `file` | Uploaded spreadsheet (CSV, XLSX) or document batch |
| `api` | External REST API (base URL + auth header + endpoints) |
| `document` | PDF / TXT / MD ingested as searchable text chunks |

An origin is created once and can contain multiple data sources.

### Data Source

A **specific, queryable dataset** derived from an origin:
- One spreadsheet → one source per sheet
- One API origin → one source per configured endpoint
- One document batch → one source (chunked and indexed)

**Data sources are what agents analyze.** You reference them by UUID when creating
a report. Sources store metadata in Postgres; actual rows live in MongoDB.

### Agent

A report-generation **mode** (not a chatbot). Three built-in agents:

| `agent_id` | Behavior |
|------------|----------|
| `custom_report` | User provides a prompt; agent gathers data and writes a full report |
| `rover_report` | Autonomous investigation: profiles data, generates research questions, iterates |
| `blank_report` | Creates an empty report immediately; sections added via `ai-section` API |

List available agents: `GET /api/v1/agents/`

### Report (Task)

A report is a **task** — async by design. Lifecycle: `queued → running → completed | failed`.

The result is a structured **block list**: text paragraphs, ECharts chart configs, lists,
columns. All blocks are JSON — suitable for custom renderers. Reports also support:
chat, manual edits, public sharing, export (PDF / PPTX / DOCX), provenance records.

---

## Step 2 — Get an API Key

**Every external API call requires an `X-API-Key` header.**

Keys are per-organization. The full secret is shown **only once** at creation.

Before performing any API operation, always do this first:
1. Ask the user whether they already have a Southwind API key (`ak_...`).
2. If they have one, ask them to share it so you can continue.
3. If they do not have one, send them to the UI link to create it:
   - `https://app.southwind.ai/settings/api-keys`
   - Fallback path: `https://app.southwind.ai` → **Settings** → **API Keys** → **Create**

Use this prompt pattern at the start of integrations:
> "Do you already have a Southwind API key (`ak_...`)? If yes, share it and I can continue. If not, create one here: https://app.southwind.ai/settings/api-keys"

### Create a key

```
POST /api/v1/organization/api-keys
X-API-Key: <existing-key-with-manage-api-keys-permission>

Body: { "name": "My Integration" }
Response: { "id": "...", "key_value": "ak_...", "name": "My Integration", ... }
```

Or create one in the UI: **Settings → API Keys → Create**.

### Use the key

```
GET /api/v1/me
X-API-Key: ak_...
```

No `Authorization` header. No `X-Organization-Id` header. The org is resolved from the key.

### Error responses

| Status | Meaning |
|--------|---------|
| 401 | Invalid or revoked key |
| 402 | Plan limit reached |
| 422 | Validation error (check request body) |

Error body: `{ "error": { "detail": "...", "request_id": "..." } }`

---

## Step 3 — Choose Your Workflow

Pick the pattern that matches your use case, then follow the workflow below.

### Workflow A — File upload → report (most common)

Use when you have CSV / XLSX data you want analyzed.

```
1. POST /api/v1/origins/file/
   { "files": [{ "name": "data.csv", "url": "https://..." }] }
   ← Returns: { "created_data_origins": [...], "unprocessed_files": [...] }
      File type (spreadsheet vs document) is auto-detected by extension —
      .csv/.xlsx → tabular source, .pdf/.txt/.md → document source

2. POST /api/v1/reports/
   {
     "agent_id": "custom_report",
     "data_sources_ids": ["<source-uuid>"],
     "params": {
       "language": "english",
       "currency": "USD",
       "prompt": "Analyze Q1 sales trends by region",
       "data_provenance": false
     },
     "improve_prompt": false
   }
   ← Returns: { "id": "<task_id>", "status": "queued", ... }

3. Poll:  GET /api/v1/reports/<task_id>
   Or SSE: GET /api/v1/reports/<task_id>/events   (real-time thoughts + status)

4. When status = "completed":
   Result is in response.result[] — array of typed blocks
```

For files larger than a few MB, use the S3 multipart upload helpers under
`/api/v1/origins/s3/…` before calling the file ingest endpoint.

### Workflow B — External API data source

Use when data lives in an external REST API and should be refreshed over time.

```
1. POST /api/v1/origins/data-api/
   {
     "display_name": "Sales API",
     "base_url": "https://api.acme.com",
     "api_key": "secret",
     "api_key_header": "X-API-Key",
     "endpoints": [{
       "display_name": "Monthly Sales",
       "path": "/v1/sales/monthly.json",
       "format": "json",
       "query_params": {}
     }]
   }
   ← Returns: { "success": true, "data_sources": [...] }

2. POST /api/v1/reports/  (same as Workflow A, step 2)

3. Refresh data before re-running:
   POST /api/v1/sources/<source_id>/sync
   POST /api/v1/reports/<task_id>/redo
```

### Workflow C — Autonomous investigation (Rover)

Use for open-ended research where the agent decides what to investigate.

```
POST /api/v1/reports/
{
  "agent_id": "rover_report",
  "data_sources_ids": ["<source-uuid>"],
  "params": {
    "target_sections": 7,
    "data_provenance": true,
    "seeded_question": "optional: first question to investigate"
  }
}
```

Rover takes longer. The top-level `decision_tree` field in the response shows the investigation path.
`data_provenance: true` adds citation records (fetch with `/provenance/{id}`).

### Workflow D — Blank report + incremental AI sections

Use when you want to build a report section-by-section, or embed a report builder UI.

```
1. POST /api/v1/reports/
   { "agent_id": "blank_report", "data_sources_ids": [...], "params": {} }
   ← Completes immediately with an empty report

2. POST /api/v1/reports/<task_id>/ai-section
   { "prompt": "Add a section on Q1 revenue breakdown" }
   ← Returns: { "blocks": [...] }

3. PUT /api/v1/reports/<task_id>   to save manual edits + merged blocks
```

### Workflow E — Chat with a report

Once a report is complete, you can hold a conversational Q&A over its data.

```
POST /api/v1/reports/<task_id>/chat
{ "message": "Which region had the highest growth?" }
← Streaming SSE response

GET /api/v1/reports/<task_id>/chat/history   ← full chat log
DELETE /api/v1/reports/<task_id>/chat/history ← clear session
```

### Workflow F — Share a report publicly

```
PUT /api/v1/reports/<task_id>/share
{ "is_public": true }
← Returns: { "is_public": true, "token": "..." }

# Anyone can then access (no auth):
GET /api/v1/public/reports/<token>
```

---

## Step 4 — Handle the Report Result

### The result is a BlockNote document

`result` is an array of **[BlockNote](https://www.blocknotejs.org/) block objects** — the same
format BlockNote uses natively. Each block follows the standard BlockNote JSON shape:

```json
{
  "id": "...",
  "type": "paragraph",
  "props": { ... },
  "content": [ { "type": "text", "text": "...", "styles": {} } ],
  "children": []
}
```

**You have two options for rendering:**

1. **Use BlockNote directly** — initialize a `BlockNoteEditor` with `initialContent: result`
   and render a `<BlockNoteView>`. The Whispers schema includes custom block types (see below)
   that you would need to register.

2. **Walk the blocks manually** — iterate `result` and render each block type yourself.
   Straightforward for most types; charts require extra handling (see below).

### Block types in use

| `type` | Standard BlockNote? | Key props / content |
|--------|--------------------|--------------------|
| `paragraph` | yes | `content[]` inline text |
| `heading` | yes | `props.level` (1–3), `content[]` |
| `bulletListItem` | yes | `content[]`, nestable via `children[]` |
| `numberedListItem` | yes | `content[]`, nestable via `children[]` |
| `table` | yes | standard BlockNote table |
| `image` | yes | `props.url`, `props.caption` |
| `columnList` / `column` | xl-multi-column | `children[]` of column blocks |
| `chart` | **custom** | `props.config` — ECharts option as JSON string |
| `alert` | **custom** | `content[]` inline text |
| `statistic` | **custom** | props vary |

### Rendering chart blocks

Chart blocks use **[Apache ECharts](https://echarts.apache.org/)**. The chart config lives at
`block.props.config` and is a **JSON string** — always parse it before use.

```js
import * as echarts from "echarts";

function renderChart(block, containerEl) {
  // config lives in props, and is a JSON string — always parse it
  const option = JSON.parse(block.props.config);

  const chart = echarts.init(containerEl, null, { renderer: "svg" });
  chart.setOption({ ...option, backgroundColor: "transparent" });

  const observer = new ResizeObserver(() => chart.resize());
  observer.observe(containerEl);

  return () => { observer.disconnect(); chart.dispose(); };
}
```

**Key rules:**
- Config is at `block.props.config`, **not** `block.config`
- `props.config` is always a JSON **string** — `JSON.parse()` it first
- Use the **SVG renderer** (`renderer: "svg"`) — consistent with how Whispers renders for export
- Set `backgroundColor: "transparent"` so the chart respects your app's theme
- Attach a `ResizeObserver` so the chart redraws when its container is resized
- Never mutate the parsed option — pass a spread copy to `setOption`

**Recommended container dimensions:**

| Chart type | Width | Height |
|------------|-------|--------|
| Pie / gauge / funnel | 600px | 400px |
| All other types | 800px | 400px |

**Legacy format note:** Very old reports may have a Chart.js config in `props.config`
(detectable by a top-level `type` + `data.datasets` structure). New reports always produce
native ECharts options.

### Polling strategy

1. Create report → save `task_id`
2. Subscribe to `GET /api/v1/reports/<task_id>/events` (SSE):
   - `event: status` → `data: { "status": "...", "progress": 0-100 }`
   - `event: thought` → agent reasoning step
   - `event: done` → stream ended (task completed or failed)
3. On `status: completed`, fetch `GET /api/v1/reports/<task_id>` → read `result`
4. On `status: failed` — `params.error` explains why

### Important list-vs-detail behavior

- `GET /api/v1/reports/` is for listing and returns summary records (commonly under `reports[]`)
- when a user selects a report from history/list, always call `GET /api/v1/reports/<task_id>` before rendering content

---

## Step 5 — Build Correctly

### Things Whispers owns — do NOT replicate in your product

- Dataset storage and schema inference (MongoDB)
- Agent logic, prompts, and tool execution
- Chart spec generation
- Report structure and block format
- Plan limits enforcement (honor 402 responses)

### Things your product owns

- UI rendering of blocks
- Scheduling / triggering of report runs
- User-facing report titles and organization
- Any downstream usage of result data
- Any manipulation of the blocks to display them in the desired way

### Common mistakes

- **Caching availability**: Plan limits and source data change. Always query live.
- **UUID handling**: `task_id`, `origin_id`, `source_id` are all UUIDs. Store and pass them as strings.
- **Key security**: Never expose `ak_...` keys to browser clients. Use your backend as a proxy.
- **Async assumption**: Report creation always returns `queued`. Never assume `completed` without checking.
- **Rigid response parsing**: list endpoints may return envelope keys like `data_sources` / `reports`, not only `items` or raw arrays.
- **Chart config assumptions**: `chart.props.config` can be a JSON string or an object; support both before calling ECharts.
- **Wrong chart config path**: chart option is in `block.props.config`, not `block.config`.

---

## Additional Resources

- **Full endpoint catalog** with request/response shapes: [reference.md](reference.md)
- **Plan limits and billing**: `GET /api/v1/billing/usage`, `GET /api/v1/billing/plans`
- **Organization settings**: `GET/PATCH /api/v1/organization/settings` (language, currency, glossary)

---

## Skill Self-Update Protocol

Before giving endpoint-specific guidance, perform this update check once per session:

1. Read local version from `VERSION` (canonical source).
2. Fetch latest skill from:
   - `https://raw.githubusercontent.com/southwind-ai/use-whispers/main/skills/use-whispers/SKILL.md`
3. Fetch latest version from:
   - `https://raw.githubusercontent.com/southwind-ai/use-whispers/main/skills/use-whispers/VERSION`
4. Compare semantic versions:
   - If remote <= local: continue normally.
   - If remote > local: sync local skill to latest remote content.

If you cannot edit files (read-only mode), do not attempt sync. Instead, tell the user:
- local version
- latest version
- update URL to pull from

When sync happens, update all release files together:
- `SKILL.md`
- `VERSION`
- `CHANGELOG.md` (when release notes are available)

# Version

Canonical version is stored in `VERSION`.

Check for updates at:
https://github.com/southwind-ai/use-whispers