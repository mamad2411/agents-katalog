---
name: fabric-cli-notebook
description: Fabric CLI notebook operations — list, create, export, import, edit, run, schedule, and monitor notebooks in Microsoft Fabric. Use when working with .Notebook items via the fab CLI.
allowed-tools: "Bash(uv run *), Bash(fab *), Bash(cat *), Bash(grep *), Read, Write, Edit, Glob"
user-invocable: false
metadata:
  author: accelerate-data
---

# Fabric CLI — Notebook Operations

Complete reference for managing and executing notebooks via `fab` CLI.

## Execution Pattern

```bash
uv run --env-file .env fab <command>
```

## List Notebooks

```bash
# All items in workspace (notebooks have .Notebook extension)
uv run --env-file .env fab ls ws1.Workspace

# Detailed listing
uv run --env-file .env fab ls ws1.Workspace -l

# Filter to notebooks only
uv run --env-file .env fab ls ws1.Workspace -q "[?contains(name, 'Notebook')]"
```

## Check Existence

```bash
uv run --env-file .env fab exists ws1.Workspace/nb1.Notebook
```

## Get Notebook Details

```bash
# Full details
uv run --env-file .env fab get ws1.Workspace/nb1.Notebook

# Verbose properties
uv run --env-file .env fab get ws1.Workspace/nb1.Notebook -v

# Specific field
uv run --env-file .env fab get ws1.Workspace/nb1.Notebook -q displayName
```

## Create a Notebook

```bash
uv run --env-file .env fab create ws1.Workspace/nb1.Notebook
```

## Rename / Set Properties

```bash
# Rename
uv run --env-file .env fab set ws1.Workspace/nb1.Notebook -q displayName -i "New Notebook Name"

# Set description
uv run --env-file .env fab set ws1.Workspace/nb1.Notebook -q description -i "My notebook description"

# Set default lakehouse (shorthand alias)
uv run --env-file .env fab set ws1.Workspace/nb1.Notebook -q lakehouse -i '{"known_lakehouses": [{"id": "<lakehouse-id>"}], "default_lakehouse": "<lakehouse-id>", "default_lakehouse_name": "lh1", "default_lakehouse_workspace_id": "<workspace-id>"}'

# Set default environment (shorthand alias)
uv run --env-file .env fab set ws1.Workspace/nb1.Notebook -q environment -i '{"environmentId": "<env-id>", "workspaceId": "<workspace-id>"}'
```

**Definition path aliases for notebooks:** `lakehouse`, `environment`, `warehouse` — shortcuts for deep JSON paths under `definition.parts[0].payload...`

## Export a Notebook

Export downloads the notebook definition to a local directory:

```bash
# Export to local
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp/exports

# Export with force (skip sensitivity label prompt, overwrite existing)
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp/exports -f

# Export as .ipynb format
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp/exports --format ipynb

# Export as .py format
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp/exports --format py

# Export to OneLake
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /ws1.Workspace/lh1.Lakehouse/Files/export -f
```

The exported artifact lands at `/tmp/exports/nb1.Notebook/` containing `notebook-content.ipynb` and `.platform`.

> **Important:** The output directory (`-o` path) must already exist — `fab export` will not create it. Run `mkdir -p /tmp/exports` first.

## Import a Notebook

Import uploads a local notebook definition to a workspace (creates or updates):

```bash
# Import (creates new or updates existing)
uv run --env-file .env fab import ws1.Workspace/nb1_imported.Notebook -i /tmp/exports/nb1.Notebook

# Import with force (skip confirmation)
uv run --env-file .env fab import ws1.Workspace/nb1.Notebook -i /tmp/exports/nb1.Notebook -f
```

## Copy a Notebook

```bash
# Copy within same workspace (renames)
uv run --env-file .env fab cp ws1.Workspace/nb1.Notebook ws1.Workspace/nb1_copy.Notebook

# Copy to another workspace
uv run --env-file .env fab cp ws1.Workspace/nb1.Notebook ws2.Workspace/nb1.Notebook
```

## Move a Notebook

```bash
# Move to another workspace
uv run --env-file .env fab mv ws1.Workspace/nb1.Notebook ws2.Workspace

# Move and rename
uv run --env-file .env fab mv ws1.Workspace/nb1.Notebook ws2.Workspace/renamed.Notebook
```

## Delete a Notebook

```bash
# With confirmation
uv run --env-file .env fab rm ws1.Workspace/nb1.Notebook

# Force (no confirmation)
uv run --env-file .env fab rm ws1.Workspace/nb1.Notebook -f
```

## Run a Notebook

### Synchronous (waits for completion)

```bash
# Basic run — blocks until done
uv run --env-file .env fab job run ws1.Workspace/nb1.Notebook

# With timeout (seconds)
uv run --env-file .env fab job run ws1.Workspace/nb1.Notebook --timeout 120
```

### Asynchronous (fire and forget)

```bash
# Start and return immediately
uv run --env-file .env fab job start ws1.Workspace/nb1.Notebook
```

### With Parameters (`-P`)

Pass notebook parameters using `param_name:type=value` format:

```bash
uv run --env-file .env fab job run ws1.Workspace/nb1.Notebook -P string_param:string=new_value,int_param:int=10
```

**Supported parameter types:** `string`, `int`, `float`, `bool`

Multiple parameters are comma-separated:

```bash
uv run --env-file .env fab job run ws1.Workspace/nb1.Notebook -P "name:string=test,count:int=5,flag:bool=true"
```

### With Configuration (`-C`)

Configure the notebook's execution environment:

```bash
# From config file
uv run --env-file .env fab job start ws1.Workspace/nb1.Notebook -C ./config_file.json

# Inline — set default lakehouse
uv run --env-file .env fab job run ws1.Workspace/nb1.Notebook -C '{"defaultLakehouse": {"name": "mylh", "id": "abc-123"}}'

# Inline — use workspace Spark pool
uv run --env-file .env fab job start ws1.Workspace/nb1.Notebook -C '{"useWorkspacePool": "my-pool"}'
```

**Configuration JSON options:**

| Key | Purpose | Example |
|-----|---------|---------|
| `defaultLakehouse` | Set the notebook's default lakehouse | `{"name": "lh1", "id": "<guid>", "workspaceId": "<optional>"}` |
| `useWorkspacePool` | Use a specific Spark pool | `"pool-name"` |
| `useStarterPool` | Use the starter pool (default true) | `false` |
| `conf` | Spark configuration key-values | `{"spark.conf1": "value"}` |
| `environment` | Set execution environment | `{"id": "<env-id>", "name": "<env-name>"}` |

You can combine `-P` (parameters) and `-C` (config) in a single run:

```bash
uv run --env-file .env fab job run ws1.Workspace/nb1.Notebook -P "name:string=test" -C '{"environment": {"id": "<id>", "name": "<name>"}}'
```

## Monitor Notebook Runs

### List Runs

```bash
# List all runs
uv run --env-file .env fab job run-list ws1.Workspace/nb1.Notebook

# List scheduled runs
uv run --env-file .env fab job run-list ws1.Workspace/nb1.Notebook --schedule
```

### Check Run Status

```bash
uv run --env-file .env fab job run-status ws1.Workspace/nb1.Notebook --id <run_id>
```

### Cancel a Run

```bash
uv run --env-file .env fab job run-cancel ws1.Workspace/nb1.Notebook --id <run_id>
```

## Schedule Notebook Runs

### Create a Schedule

```bash
# Cron — every 10 minutes
uv run --env-file .env fab job run-sch ws1.Workspace/nb1.Notebook --type cron --interval 10

# Daily — at 10:00 and 16:00
uv run --env-file .env fab job run-sch ws1.Workspace/nb1.Notebook --type daily --interval 10:00,16:00

# Weekly — Monday and Friday at 10:00
uv run --env-file .env fab job run-sch ws1.Workspace/nb1.Notebook --type weekly --interval 10:00 --days Monday,Friday

# With date range
uv run --env-file .env fab job run-sch ws1.Workspace/nb1.Notebook --type daily --interval 09:00 --start 2026-04-01T09:00:00 --end 2026-06-01T00:00:00
```

### Update a Schedule

```bash
# Disable
uv run --env-file .env fab job run-update ws1.Workspace/nb1.Notebook --id <schedule_id> --disable

# Enable
uv run --env-file .env fab job run-update ws1.Workspace/nb1.Notebook --id <schedule_id> --enable
```

### Delete a Schedule

```bash
# With confirmation
uv run --env-file .env fab job run-rm ws1.Workspace/nb1.Notebook --id <schedule_id>

# Force delete
uv run --env-file .env fab job run-rm ws1.Workspace/nb1.Notebook --id <schedule_id> -f
```

### Schedule Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--type` | Schedule type | `cron`, `daily`, `weekly` |
| `--interval` | Frequency or time(s) | `10` (minutes) or `10:00,16:00` |
| `--days` | Days of week (weekly only) | `Monday,Friday` |
| `--start` | Start date (UTC) | `2026-04-01T09:00:00` |
| `--end` | End date (UTC) | `2026-06-01T00:00:00` |
| `--enable` | Enable schedule | — |
| `--disable` | Disable schedule | — |
| `--id` | Schedule ID (for update) | `<guid>` |

## Edit a Notebook Workflow

To edit a notebook's content:

1. **Export** the notebook to a local directory
2. **Edit** the definition files locally
3. **Import** the updated notebook back (or overwrite with `rm` + `import`)

```bash
# Step 1: Export
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp/nb_edit

# Step 2: Edit locally (modify files in /tmp/nb_edit/nb1.Notebook/)

# Step 3: Delete the old notebook and re-import
uv run --env-file .env fab rm ws1.Workspace/nb1.Notebook -f
uv run --env-file .env fab import ws1.Workspace/nb1.Notebook -i /tmp/nb_edit/nb1.Notebook
```

## Open in Browser

```bash
uv run --env-file .env fab open ws1.Workspace/nb1.Notebook
```

## Edit a Notebook Programmatically

Notebook definitions are JSON files. The cell `source` field **must be a list of strings** (lines with `\n`), not a single string.

```json
{
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "import dlt\n",
        "print('hello')\n"
      ]
    }
  ]
}
```

Use a Python script to edit notebook JSON — direct text editing can break the format.

## Practical Tips

- **Token efficiency:** Use `fab cp` to download files + `Read` tool to inspect, instead of MCP download + base64 decode. Never paste base64 strings in echo commands.
- **Get item ID:** `uv run --env-file .env fab get ws1.Workspace/nb1.Notebook -f -q "id"`
- **run-status limitation:** `job run-status` returns status (Completed/Failed) and a `failureReason` field, but for notebooks the error detail is often minimal (e.g. just "Failed"). For full error messages and stack traces, check logs via OneLake files or the Fabric UI.
- **Fabric notebooks** don't come with pre-installed packages. Install dependencies with `!pip install [packages]` in a cell.
- **Lakehouse attachment:** A lakehouse must be attached for `/lakehouse/default/` paths to work inside the notebook.

## Common Issues

| Issue | Fix |
|-------|-----|
| `ERROR_WORKSPACE_NOT_FOUND` | Check workspace name and `.Workspace` extension in path |
| Notebook run timeout | Increase `--timeout` value or use async `job start` |
| Parameters not applied | Ensure `param_name:type=value` format — types: string, int, float, bool |
| Config JSON parse error | Wrap JSON in single quotes, check for shell escaping issues |
| Schedule not running | Verify `--enable` flag is set, check date range with `--start`/`--end` |
| Export produces empty dir | Notebook may not have a persisted definition yet — open and save in Fabric first |
| `InvalidNotebookContent` | Cell `source` must be a list of strings, not a single string |
| No error details from run | `run-status` only shows pass/fail — check OneLake logs for details |
