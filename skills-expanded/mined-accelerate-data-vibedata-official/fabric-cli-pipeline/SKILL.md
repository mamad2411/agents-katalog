---
name: fabric-cli-pipeline
description: Fabric CLI data pipeline operations — list, create, run with parameters, monitor, schedule, cancel, export, and import DataPipeline items. Use when working with .DataPipeline items via the fab CLI.
allowed-tools: "Bash(uv run *), Bash(fab *), Bash(cat *), Bash(grep *), Read, Write, Edit, Glob"
user-invocable: false
metadata:
  author: accelerate-data
---

# Fabric CLI — Pipeline Operations

Complete reference for managing and executing data pipelines via `fab` CLI.

## Execution Pattern

```bash
uv run --env-file .env fab <command>
```

## List Pipelines

```bash
# All items in workspace (pipelines have .DataPipeline extension)
uv run --env-file .env fab ls ws1.Workspace

# Detailed listing
uv run --env-file .env fab ls ws1.Workspace -l

# Filter to pipelines only
uv run --env-file .env fab ls ws1.Workspace -q "[?contains(name, 'DataPipeline')]"
```

## Check Existence

```bash
uv run --env-file .env fab exists ws1.Workspace/pip1.DataPipeline
```

## Get Pipeline Details

```bash
uv run --env-file .env fab get ws1.Workspace/pip1.DataPipeline
uv run --env-file .env fab get ws1.Workspace/pip1.DataPipeline -v
uv run --env-file .env fab get ws1.Workspace/pip1.DataPipeline -q displayName
```

## Create a Pipeline

```bash
uv run --env-file .env fab create ws1.Workspace/pip1.DataPipeline
```

## Rename a Pipeline

```bash
uv run --env-file .env fab set ws1.Workspace/pip1.DataPipeline -q displayName -i "New Pipeline Name"
```

## Delete a Pipeline

```bash
# With confirmation
uv run --env-file .env fab rm ws1.Workspace/pip1.DataPipeline

# Force
uv run --env-file .env fab rm ws1.Workspace/pip1.DataPipeline -f
```

## Run a Pipeline

### Synchronous (waits for completion)

```bash
# Basic run
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline

# With timeout (seconds)
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline --timeout 300
```

### Asynchronous (fire and forget)

```bash
uv run --env-file .env fab job start ws1.Workspace/pip1.DataPipeline
```

### With Parameters (`-P`)

Pass pipeline parameters using `param_name:type=value` format:

```bash
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline -P string_param:string=hello,int_param:int=42
```

**Supported parameter types:** `string`, `int`, `float`, `bool`, `object`, `array`, `secureString`

Complex types (object, array):

```bash
# Object parameter
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline -P 'obj_param:object={"key":{"nested_key":2}}'

# Array parameter
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline -P 'array_param:array=[1,2,3]'

# Combined
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline -P 'obj_param:object={"key":{"nested_key":2}},array_param:array=[1,2,3]'
```

### With Raw JSON Input (`-i`)

For full control over the request body:

```bash
# Inline JSON
uv run --env-file .env fab job start ws1.Workspace/pip1.DataPipeline -i '{"parameters": {"string_param": "value"}}'

# From file
uv run --env-file .env fab job start ws1.Workspace/pip1.DataPipeline -i ./pipeline_params.json
```

**Pipeline input JSON format:**

```json
{
  "parameters": {
    "string_param": "value",
    "int_param": 42,
    "obj_param": {"key": "value"},
    "array_param": [1, 2, 3]
  }
}
```

## Monitor Pipeline Runs

### List Runs

```bash
# All runs
uv run --env-file .env fab job run-list ws1.Workspace/pip1.DataPipeline

# Scheduled runs
uv run --env-file .env fab job run-list ws1.Workspace/pip1.DataPipeline --schedule
```

### Check Run Status

```bash
uv run --env-file .env fab job run-status ws1.Workspace/pip1.DataPipeline --id <run_id>
```

### Cancel a Run

```bash
uv run --env-file .env fab job run-cancel ws1.Workspace/pip1.DataPipeline --id <run_id>
```

## Schedule Pipeline Runs

### Create a Schedule

```bash
# Cron — every 30 minutes
uv run --env-file .env fab job run-sch ws1.Workspace/pip1.DataPipeline --type cron --interval 30

# Daily — at 06:00 and 18:00
uv run --env-file .env fab job run-sch ws1.Workspace/pip1.DataPipeline --type daily --interval 06:00,18:00

# Weekly — Monday, Wednesday, Friday at 08:00
uv run --env-file .env fab job run-sch ws1.Workspace/pip1.DataPipeline --type weekly --interval 08:00 --days Monday,Wednesday,Friday

# With date range
uv run --env-file .env fab job run-sch ws1.Workspace/pip1.DataPipeline --type daily --interval 06:00 --start 2026-04-01T06:00:00 --end 2026-07-01T00:00:00
```

### Update a Schedule

```bash
# Disable
uv run --env-file .env fab job run-update ws1.Workspace/pip1.DataPipeline --id <schedule_id> --disable

# Enable
uv run --env-file .env fab job run-update ws1.Workspace/pip1.DataPipeline --id <schedule_id> --enable
```

### Schedule Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--type` | Schedule type | `cron`, `daily`, `weekly` |
| `--interval` | Frequency or time(s) | `30` (minutes) or `06:00,18:00` |
| `--days` | Days of week (weekly only) | `Monday,Wednesday,Friday` |
| `--start` | Start date (UTC) | `2026-04-01T06:00:00` |
| `--end` | End date (UTC) | `2026-07-01T00:00:00` |
| `--enable` | Enable schedule | — |
| `--disable` | Disable schedule | — |
| `--id` | Schedule ID (for update) | `<guid>` |

### Delete a Schedule

```bash
# With confirmation
uv run --env-file .env fab job run-rm ws1.Workspace/pip1.DataPipeline --id <schedule_id>

# Force delete
uv run --env-file .env fab job run-rm ws1.Workspace/pip1.DataPipeline --id <schedule_id> -f
```

### Configure Timeout Behavior

By default, `job run` cancels the pipeline on timeout. To change:

```bash
uv run --env-file .env fab config set job_cancel_ontimeout false
```

### Custom Polling Interval

```bash
uv run --env-file .env fab job run ws1.Workspace/pip1.DataPipeline --polling_interval 10
```

## Export / Import

```bash
# Export pipeline definition
uv run --env-file .env fab export ws1.Workspace/pip1.DataPipeline -o /tmp/exports

# Export with force (skip sensitivity label, overwrite existing)
uv run --env-file .env fab export ws1.Workspace/pip1.DataPipeline -o /tmp/exports -f

# Import pipeline definition (creates or updates)
uv run --env-file .env fab import ws1.Workspace/pip1_imported.DataPipeline -i /tmp/exports/pip1.DataPipeline

# Import with force
uv run --env-file .env fab import ws1.Workspace/pip1.DataPipeline -i /tmp/exports/pip1.DataPipeline -f
```

## Copy / Move

```bash
# Copy
uv run --env-file .env fab cp ws1.Workspace/pip1.DataPipeline ws2.Workspace/pip1_copy.DataPipeline

# Move
uv run --env-file .env fab mv ws1.Workspace/pip1.DataPipeline ws2.Workspace
```

## Open in Browser

```bash
uv run --env-file .env fab open ws1.Workspace/pip1.DataPipeline
```

## Parameter Type Reference

| Type | Format | Example |
|------|--------|---------|
| `string` | `name:string=value` | `env:string=prod` |
| `int` | `name:int=value` | `batch_size:int=1000` |
| `float` | `name:float=value` | `threshold:float=0.95` |
| `bool` | `name:bool=value` | `dry_run:bool=true` |
| `object` | `name:object={...}` | `config:object={"key":"val"}` |
| `array` | `name:array=[...]` | `ids:array=[1,2,3]` |
| `secureString` | `name:secureString=value` | `token:secureString=abc123` |

## Pipeline Definition Structure

When exported, a pipeline definition contains:

- `.platform` file — metadata with `type` and `displayName`
- `pipeline-content.json` — activities array defining the pipeline steps

> **Important:** The output directory (`-o` path) must already exist — `fab export` will not create it. Run `mkdir -p /path` first.

For notebook execution activities, use `TridentNotebook` type with `notebookId` and `workspaceId` in `typeProperties`.

## Practical Tips

- **run-status limitation:** `job run-status` only returns pass/fail — no error details. Check Fabric UI or OneLake logs for failure debugging.
- **Get pipeline ID:** `uv run --env-file .env fab get ws1.Workspace/pip1.DataPipeline -f -q "id"`
- **Create empty then import:** Use `fab mkdir` to create, then `fab import -f` to overwrite with definition.

## Common Issues

| Issue | Fix |
|-------|-----|
| Parameters not applied | Use `-P param:type=value` format — type is required |
| Complex JSON escaping | Use `-i ./file.json` instead of inline JSON |
| Pipeline timeout | Increase `--timeout` or use async `job start` |
| Schedule not triggering | Check `--enable` flag and date range (`--start`/`--end`) |
| `ERROR_WORKSPACE_NOT_FOUND` | Verify workspace name and `.Workspace` extension |
| Cancel fails | Ensure you have the correct `--id` from `job run-list` |
