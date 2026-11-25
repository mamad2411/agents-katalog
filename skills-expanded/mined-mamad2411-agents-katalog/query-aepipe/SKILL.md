---
name: query-aepipe
description: "Interact with aepipe Analytics Engine API — query logs, ingest events, list projects/logstores, and process query results with Python. Use this skill whenever the user mentions aepipe, analytics engine logs, log querying, event ingestion, logstore management, or wants to analyze/export/visualize data from their aepipe instance. Also triggers when the user wants to set up aepipe config, check aepipe connectivity, or work with structured event data stored in Cloudflare Analytics Engine."
---

# query-aepipe

A toolkit for interacting with the [aepipe](../../README.md) HTTP API — a multi-tenant log ingestion and query service backed by Cloudflare Analytics Engine.

## Install

```bash
npx skills add loadchange/aepipe
```

## Prerequisites

Python 3.8+ is required for the data processing scripts. No external pip packages are needed — scripts use only the standard library (`urllib`, `json`, `csv`, `sqlite3`).

## Configuration

The ADMIN_TOKEN and API endpoint are stored persistently in `~/.config/query-aepipe/config.json`:

```json
{
  "base_url": "https://your-aepipe-worker.example.com",
  "admin_token": "your-bearer-token"
}
```

### First-time setup

If the config file doesn't exist, run the setup script to create it:

```bash
python3 <skill-path>/scripts/setup_config.py
```

This prompts for the base URL and token, validates connectivity by calling `GET /v1/projects`, and saves the config. You can also pass values directly:

```bash
python3 <skill-path>/scripts/setup_config.py --base-url https://example.com --token SECRET
```

Before running any other script, always check if `~/.config/query-aepipe/config.json` exists. If not, run setup first.

## API Overview

aepipe organizes data into **projects** (top-level tenants) and **logstores** (log categories within a project). All endpoints require `Authorization: Bearer <ADMIN_TOKEN>`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/projects` | List all projects |
| `GET` | `/v1/{project}/logstores` | List logstores in a project |
| `POST` | `/v1/{project}/{logstore}/ingest` | Write up to 250 event points |
| `POST` | `/v1/{project}/{logstore}/query` | Run SQL query (auto-scoped to project/logstore) |
| `POST` | `/v1/{project}/{logstore}/log` | Write structured logs (via Workers Observability) |
| `POST` | `/v1/{project}/{logstore}/rawlog` | Query raw Worker logs (via CF Telemetry REST API) |

### Data Point Structure (ingest)

Each ingested point has:
- `event` (string, required) — the event name
- `level` (string, optional, default "info") — log level
- `blobs` (string[], optional) — up to 16 extra string fields (mapped to blob5–blob20)
- `doubles` (number[], optional) — up to 20 numeric fields (mapped to double1–double20)

### Query SQL Field Mapping

When writing SQL for the query endpoint, use these Analytics Engine column names:

| Column | Meaning |
|--------|---------|
| `blob1` | project name (auto-filtered) |
| `blob2` | logstore name (auto-filtered) |
| `blob3` | event |
| `blob4` | level |
| `blob5`–`blob20` | user blobs[0..15] |
| `double1`–`double20` | user doubles[0..19] |
| `timestamp` | event timestamp |
| `_sample_interval` | sampling interval |

The query endpoint automatically injects `blob1 = '{project}' AND blob2 = '{logstore}'` — you do NOT need to include these filters yourself.

### Log Entry Structure (log)

The `log` endpoint writes structured logs to Workers Observability (not Analytics Engine). Each log entry:
- `message` (string, required) — the log message
- `level` (string, optional, default "info") — log level ("info", "warn", "error", "debug"), controls which console method is used
- Any additional fields are preserved in the JSON output

Request body: `{"logs": [{"message": "something happened", "level": "error", "extra": "data"}]}`

### Raw Log Query (rawlog)

The `rawlog` endpoint queries Workers invocation logs via the CF Telemetry REST API, filtered by project/logstore. Request body:
- `limit` (number, optional, default 50, max 200) — number of invocations to fetch
- `start` (ISO string, optional, default 6 hours ago) — start of time range
- `end` (ISO string, optional, default now) — end of time range

Returns `{logs: [{timestamp, level, data}], count}` where `data` is the parsed JSON log content.

## Scripts

All scripts are in `<skill-path>/scripts/` and read config from `~/.config/query-aepipe/config.json`.

### aepipe_client.py — Full API Client

A unified CLI for all aepipe API operations:

```bash
# List projects
python3 <skill-path>/scripts/aepipe_client.py projects

# List logstores in a project
python3 <skill-path>/scripts/aepipe_client.py logstores <project>

# Ingest events
python3 <skill-path>/scripts/aepipe_client.py ingest <project> <logstore> \
  --event "user_login" --level info \
  --blobs '["chrome","mac"]' --doubles '[1.5, 200]'

# Ingest from JSON file (array of DataPoint objects)
python3 <skill-path>/scripts/aepipe_client.py ingest <project> <logstore> \
  --file events.json

# Query with SQL
python3 <skill-path>/scripts/aepipe_client.py query <project> <logstore> \
  --sql "SELECT blob3 AS event, count() AS cnt FROM aepipe GROUP BY event ORDER BY cnt DESC LIMIT 10"

# Query with output format
python3 <skill-path>/scripts/aepipe_client.py query <project> <logstore> \
  --sql "SELECT * FROM aepipe LIMIT 100" \
  --format csv --output results.csv

# Write structured logs (Workers Observability)
python3 <skill-path>/scripts/aepipe_client.py log <project> <logstore> \
  --message "deploy completed" --level info

# Write log with extra fields
python3 <skill-path>/scripts/aepipe_client.py log <project> <logstore> \
  --message "request failed" --level error --extra '{"url":"/api","status":500}'

# Write logs from JSON file
python3 <skill-path>/scripts/aepipe_client.py log <project> <logstore> \
  --file logs.json

# Query raw Worker logs (last 6 hours by default)
python3 <skill-path>/scripts/aepipe_client.py rawlog <project> <logstore>

# Query raw logs with time range and limit
python3 <skill-path>/scripts/aepipe_client.py rawlog <project> <logstore> \
  --start "2026-03-20T00:00:00Z" --end "2026-03-20T12:00:00Z" --limit 100

# Export raw logs to JSON
python3 <skill-path>/scripts/aepipe_client.py rawlog <project> <logstore> \
  --format json --output rawlogs.json
```

### query_processor.py — Advanced Query Processing

For sophisticated data analysis after querying. Reads query results (JSON or CSV) and applies transformations:

```bash
# Basic query and process pipeline
python3 <skill-path>/scripts/aepipe_client.py query myproject mylog \
  --sql "SELECT blob3, blob4, double1, timestamp FROM aepipe LIMIT 1000" \
  --format json --output raw.json

# Process: filter, aggregate, sort, export
python3 <skill-path>/scripts/query_processor.py raw.json \
  --filter 'blob4 == "error"' \
  --group-by blob3 \
  --agg 'count:cnt,sum:double1:total,avg:double1:average' \
  --sort-by cnt --desc \
  --format table

# Export to CSV
python3 <skill-path>/scripts/query_processor.py raw.json \
  --group-by blob3 \
  --agg 'count:cnt' \
  --format csv --output summary.csv

# Export to SQLite for further analysis
python3 <skill-path>/scripts/query_processor.py raw.json \
  --to-sqlite analysis.db --table events

# Time-based aggregation
python3 <skill-path>/scripts/query_processor.py raw.json \
  --time-bucket hour --time-field timestamp \
  --agg 'count:cnt' \
  --format table

# Top-N analysis
python3 <skill-path>/scripts/query_processor.py raw.json \
  --group-by blob3 --agg 'count:cnt' --sort-by cnt --desc --limit 20 \
  --format table
```

## Common Workflows

### Explore what's in the system

```bash
# Step 1: See all projects
python3 scripts/aepipe_client.py projects

# Step 2: See logstores in a project
python3 scripts/aepipe_client.py logstores myproject

# Step 3: Sample recent events
python3 scripts/aepipe_client.py query myproject mylog \
  --sql "SELECT blob3 AS event, blob4 AS level, timestamp FROM aepipe ORDER BY timestamp DESC LIMIT 20"
```

### Error analysis

```bash
# Query errors
python3 scripts/aepipe_client.py query myproject mylog \
  --sql "SELECT blob3, blob4, double1, timestamp FROM aepipe LIMIT 5000" \
  --format json --output raw.json

# Filter and aggregate errors
python3 scripts/query_processor.py raw.json \
  --filter 'blob4 == "error"' \
  --group-by blob3 --agg 'count:cnt' --sort-by cnt --desc \
  --format table
```

### Bulk ingest from file

Prepare a JSON file with an array of data points:
```json
[
  {"event": "page_view", "level": "info", "blobs": ["/home"], "doubles": [1.2]},
  {"event": "click", "level": "info", "blobs": ["buy_btn"], "doubles": [0.5]}
]
```

```bash
python3 scripts/aepipe_client.py ingest myproject mylog --file events.json
```
