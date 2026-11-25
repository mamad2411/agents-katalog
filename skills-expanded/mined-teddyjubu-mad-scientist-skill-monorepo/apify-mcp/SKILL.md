---
name: apify-mcp
description: "Enhanced Apify integration using mcpc (Model Context Protocol CLI). Provides dynamic actor discovery, direct tool calling, and better error handling via persistent MCP sessions. Use when you need to search, inspect, run, or monitor Apify actors with the full power of the MCP protocol."
version: 1.0.0
maintainer: James (OpenClaw agent)
requires:
  tools:
    - mcpc  # @apify/mcpc installed globally via npm
  env:
    - APIFY_TOKEN  # stored in .secrets/apify.env
---

# Apify MCP Integration

This skill provides a modern, protocol-native interface to Apify via `mcpc` (Model Context Protocol CLI).

**Why use this over `apify-actor-finder` or `apify-runner`?**
- **Dynamic discovery**: Use `mcpc @apify grep` to search tools/actors semantically
- **Better error handling**: MCP protocol-native validation and async task support
- **Session persistence**: Authenticated connection stays alive across commands
- **JSON-first**: All responses are MCP-spec compliant, easier to parse/pipe

---

## What This Skill Does

This skill Enhanced Apify integration using mcpc (Model Context Protocol CLI). Provides dynamic actor discovery, direct tool calling, and better error handling via persistent MCP sessions. Use when you need to search, inspect, run, or monitor Apify actors with the full power of the MCP protocol.

## Prerequisites

### 1. Ensure `mcpc` is installed
```bash
npm install -g @apify/mcpc
mcpc --version  # Should output 0.2.3 or higher
```

### 2. Create persistent session (one-time setup)
```bash
export APIFY_TOKEN="YOUR_APIFY_TOKEN_HERE"
mcpc connect mcp.apify.com @apify --header "Authorization: Bearer ${APIFY_TOKEN}"
```

Session is now live and persists across commands. To verify:
```bash
mcpc @apify
# Should show: [@apify → https://mcp.apify.com (HTTP)]
```

---

## Workflow: Dynamic Actor Discovery → Execution

### Step 1 — Search for actors using grep

Instead of custom Python scripts, use MCP's built-in search:

```bash
# Search all Apify tools/actors for keywords
mcpc @apify grep "google maps" --json

# Regex search
mcpc @apify grep "instagram|tiktok" -E --json

# Limit results
mcpc @apify grep "scraper" -m 10
```

**Output**: List of matching tools with names, descriptions, and relevance scores.

### Step 2 — Get actor schema

Fetch detailed input/output schema for any actor:

```bash
# Get full tool schema (input args, description, README)
mcpc @apify tools-get search-actors --json

# Example: Get schema for a specific actor tool
mcpc @apify tools-get apify--rag-web-browser --json
```

### Step 3 — Call the actor/tool

Execute the actor with validated input:

```bash
# Synchronous call (waits for completion)
mcpc @apify tools-call search-actors \
  keywords:="google maps scraper" \
  limit:=5 \
  --json

# Async call (returns immediately with runId)
mcpc @apify tools-call call-actor \
  actor:="compass~crawler-google-places" \
  input:='{"searchStringsArray":["coffee Austin TX"],"maxCrawledPlacesPerSearch":20}' \
  async:=true \
  --json
```

### Step 4 — Monitor async tasks

For long-running actors:

```bash
# List active tasks
mcpc @apify tasks-list --json

# Get task status
mcpc @apify tasks-get <taskId> --json

# Cancel a running task
mcpc @apify tasks-cancel <taskId>
```

### Step 5 — Fetch results

Retrieve actor output:

```bash
# Get actor run results
mcpc @apify tools-call get-actor-output \
  datasetId:="<dataset_id>" \
  fields:="title,url,price" \
  limit:=100 \
  --json

# Alternative: Get dataset items directly
mcpc @apify tools-call get-actor-run runId:="<run_id>" --json
```

---

## Common Use Cases

### Use Case 1: Search actors by keywords

```bash
# Find Instagram scrapers
mcpc @apify tools-call search-actors keywords:="instagram scraper" limit:=5 --json \
  | jq '.content[0].text | fromjson | .items[] | {name, title, totalUsers}'
```

### Use Case 2: Run Google Maps scraper

```bash
# Step 1: Get actor details
mcpc @apify tools-call fetch-actor-details \
  actor:="compass~crawler-google-places" \
  --json

# Step 2: Run with proper input
mcpc @apify tools-call call-actor \
  actor:="compass~crawler-google-places" \
  input:='{"searchStringsArray":["pizza near me"],"maxCrawledPlacesPerSearch":10,"proxyConfig":{"useApifyProxy":true}}' \
  --json
```

### Use Case 3: Pipeline with jq

```bash
# Chain: search → select best → fetch schema → run
mcpc @apify tools-call search-actors keywords:="twitter scraper" --json \
  | jq -r '.content[0].text | fromjson | .items[0].name' \
  | xargs -I {} mcpc @apify tools-call fetch-actor-details actor:="{}" --json \
  | jq '.content[0].text | fromjson | .readme' \
  | head -50
```

---

## Available Tools (as of session creation)

Run `mcpc @apify tools-list` to see all available tools. Key tools:

| Tool | Description | Args |
|------|-------------|------|
| `search-actors` | Find actors in Apify Store | `keywords`, `limit`, `offset` |
| `fetch-actor-details` | Get actor README + schema | `actor` |
| `call-actor` | Execute an actor | `actor`, `input`, `async` |
| `get-actor-run` | Check run status | `runId` |
| `get-actor-output` | Fetch dataset results | `datasetId`, `fields`, `limit` |
| `search-apify-docs` | Search Apify docs | `query`, `docSource` |
| `apify--rag-web-browser` | General web scraper | `query`, `maxResults` |

---

## Error Handling

| Error | Fix |
|-------|-----|
| `Session not found` | Run setup command: `mcpc connect mcp.apify.com @apify --header "Authorization: Bearer ${APIFY_TOKEN}"` |
| `Tool execution failed` | Check input schema with `mcpc @apify tools-get <tool>` |
| `401 Unauthorized` | Verify `APIFY_TOKEN` in `.secrets/apify.env` |
| `Task timeout` | Increase actor timeout or use `async:=true` |

---

## Session Management

```bash
# Check session status
mcpc @apify

# Restart session (if crashed/expired)
mcpc @apify restart

# Close session (removes from list)
mcpc @apify close

# List all sessions
mcpc
```

---

## Integration Notes

- **JSON output**: All `--json` responses follow [MCP spec](https://modelcontextprotocol.io/specification/latest)
- **Async tasks**: Supported natively via `async:=true` parameter
- **Credential security**: Token stored in OS keychain (or `~/.mcpc/credentials.json` on headless systems)
- **Session persistence**: Bridge process keeps connection alive automatically

---

## When to Use This vs Other Skills

| Scenario | Use This Skill (`apify-mcp`) | Use `apify-actor-finder` | Use `apify-runner` |
|----------|------------------------------|--------------------------|---------------------|
| Dynamic actor discovery | ✅ `mcpc grep` | ✅ Python search script | ❌ |
| Quick actor execution | ✅ One command | ⚠️ Multi-step | ✅ Simple runs |
| Async task monitoring | ✅ Native support | ❌ | ❌ |
| CSV output | ⚠️ Via `jq` pipe | ✅ Built-in | ✅ Built-in |
| Complex pipelines | ✅ Shell composition | ❌ | ❌ |

**Rule of thumb**: Use `apify-mcp` for discovery, monitoring, and complex workflows. Use `apify-runner` for quick one-off CSV exports.
