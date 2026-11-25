---
name: fabric-cli-basics
description: Core Fabric CLI (fab) operations — workspace navigation, item management, authentication, resource types, path format, output formatting. Use when listing workspaces/items, creating/deleting resources, checking existence, describing items, or configuring the CLI.
allowed-tools: "Bash(uv run *), Bash(fab *), Bash(cat *), Bash(grep *), Read, Write, Edit, Glob"
user-invocable: false
metadata:
  author: accelerate-data
---

# Fabric CLI Basics

Core operations for Microsoft Fabric CLI (`fab`). All commands run through `uv` with `.env` for authentication tokens.

## Execution Pattern

```bash
uv run --env-file .env fab <command>
```

Authentication tokens are pre-set in `.env`:

| Variable | Purpose |
|----------|---------|
| `FAB_TOKEN` | Authentication token for Fabric |
| `FAB_TOKEN_ONELAKE` | Authentication token for OneLake |
| `FAB_TOKEN_AZURE` | Authentication token for Azure |
| `FAB_TENANT_ID` | Tenant ID |

These are managed by VD Studio — the agent does not need to authenticate manually.

## Current Workspace Context

The `.env` file also contains the current workspace and lakehouse context, set automatically when an intent is created:

| Variable | Purpose | Example |
|----------|---------|---------|
| `WORKSPACE_ID` | Current workspace GUID | `cdb8142c-f4d1-4f48-ac27-2e24b7a960e7` |
| `WORKSPACE_NAME` | Current workspace name | `ephm_yo__new-intent-e388f802` |
| `LAKEHOUSE_ID` | Default lakehouse GUID | `724fee7d-2fdd-4a62-b9c8-eac42b02d249` |
| `LAKEHOUSE` | Default lakehouse name | `ai_lake2_new_intent_e388f802` |
| `SCHEMA` | Default schema | `dbo` |

**Use these instead of running `fab ls` to discover workspace/lakehouse names.** Build paths directly:

```bash
# Read from .env — no need to browse workspaces
uv run --env-file .env fab ls "${WORKSPACE_NAME}.Workspace"
uv run --env-file .env fab ls "${WORKSPACE_NAME}.Workspace/${LAKEHOUSE}.Lakehouse/Tables"
uv run --env-file .env fab table schema "${WORKSPACE_NAME}.Workspace/${LAKEHOUSE}.Lakehouse/Tables/dbo/my_table"
uv run --env-file .env fab cp ./data.csv "${WORKSPACE_NAME}.Workspace/${LAKEHOUSE}.Lakehouse/Files/data.csv"
```

## Resource Hierarchy

Fabric organizes resources in a tree:

```
Tenant (root, implicit)
├── Workspaces
│   ├── Folders (nestable)
│   │   └── Items
│   ├── Items (Lakehouse, Notebook, DataPipeline, Report, etc.)
│   │   └── OneLake storage (Files/, Tables/)
│   └── Virtual containers (.sparkpools, .managedidentities, etc.)
└── Virtual containers (.capacities, .connections, .domains, .gateways)
```

## Path Format

All paths use `name.Type` notation:

```
/myworkspace.Workspace
/myworkspace.Workspace/mylakehouse.Lakehouse
/myworkspace.Workspace/myfolder.Folder/mynotebook.Notebook
/myworkspace.Workspace/mylakehouse.Lakehouse/Files/data.csv
/myworkspace.Workspace/mylakehouse.Lakehouse/Tables/dbo/customers
/.capacities/cap1.Capacity
/myworkspace.Workspace/.sparkpools/spark1.SparkPool
```

## Resource Types

### Item Types (32)

`.Notebook`, `.SparkJobDefinition`, `.DataPipeline`, `.Report`, `.SemanticModel`, `.KQLDatabase`, `.KQLDashboard`, `.KQLQueryset`, `.Lakehouse`, `.Warehouse`, `.SQLDatabase`, `.MirroredDatabase`, `.MirroredWarehouse`, `.Eventhouse`, `.Eventstream`, `.Dashboard`, `.Datamart`, `.CopyJob`, `.Environment`, `.MLExperiment`, `.MLModel`, `.MountedDataFactory`, `.PaginatedReport`, `.Reflex`, `.SQLEndpoint`, `.VariableLibrary`, `.GraphQLApi`, `.Dataflow`, `.ApacheAirflowJob`, `.CosmosDBDatabase`, `.DigitalTwinBuilder`, `.GraphQuerySet`, `.UserDataFunction`

### Workspace Virtual Item Types

`.ExternalDataShare`, `.ManagedIdentity`, `.ManagedPrivateEndpoint`, `.SparkPool`

### Tenant Virtual Item Types

`.Capacity`, `.Connection`, `.Domain`, `.Gateway`, `.Workspace`

## Core Commands

### List (`ls` / `dir`)

```bash
# List workspaces
uv run --env-file .env fab ls

# List items in a workspace
uv run --env-file .env fab ls "Sales Analytics.Workspace"

# Detailed listing with metadata
uv run --env-file .env fab ls ws1.Workspace -l

# Query specific fields
uv run --env-file .env fab ls ws1.Workspace -q [].name

# Filter by type
uv run --env-file .env fab ls ws1.Workspace -q "[?contains(name, 'Notebook')]"
```

### Check Existence (`exists`)

```bash
uv run --env-file .env fab exists ws1.Workspace/nb1.Notebook
```

### Get Details (`get`)

```bash
# Full item details
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse

# Verbose properties (all JSON fields)
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse -v

# JMESPath query for specific field
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse -q displayName

# Get item ID (force to skip sensitivity label)
uv run --env-file .env fab get ws1.Workspace/nb1.Notebook -f -q "id"

# Save to file
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse -q . -o /tmp/metadata
```

**Flags:** `-q` JMESPath query, `-v` verbose, `-f` force (skip label prompt), `-o` output path

### Describe (`desc`)

Show available commands for a resource type or specific item:

```bash
# By extension (shows supported commands for that type)
uv run --env-file .env fab desc .Notebook
uv run --env-file .env fab desc .DataPipeline
uv run --env-file .env fab desc .Lakehouse

# By path (specific item)
uv run --env-file .env fab desc ws1.Workspace/nb1.Notebook

# Show all supported element types
uv run --env-file .env fab desc all
```

### Create (`mkdir` / `create`)

```bash
# Create a lakehouse
uv run --env-file .env fab create ws1.Workspace/lh1.Lakehouse

# Create with parameters
uv run --env-file .env fab create ws1.Workspace/lh1.Lakehouse -P enableSchemas=true

# Create a folder
uv run --env-file .env fab create ws1.Workspace/folder1.Folder
```

**Cannot create:** Dashboard, Datamart, MirroredWarehouse, PaginatedReport, SQLEndpoint.

### Delete (`rm` / `del`)

```bash
# Delete with confirmation prompt
uv run --env-file .env fab rm ws1.Workspace/nb1.Notebook

# Force delete (no confirmation)
uv run --env-file .env fab rm ws1.Workspace/lh1.Lakehouse -f
```

### Copy (`cp` / `copy`)

```bash
# Copy item between workspaces (renames)
uv run --env-file .env fab cp ws1.Workspace/source.Notebook ws2.Workspace/dest.Notebook

# Copy with force (overwrite if exists, skip sensitivity label)
uv run --env-file .env fab cp ws1.Workspace/nb1.Notebook ws2.Workspace/nb1.Notebook -f

# Recursive copy (all items in workspace/folder)
uv run --env-file .env fab cp ws1.Workspace ws2.Workspace -r

# Block on path collision (prevent name conflicts across folders)
uv run --env-file .env fab cp ws1.Workspace/nb1.Notebook ws2.Workspace -bpc
```

**Flags:** `-f` force, `-r` recursive, `-bpc` block on path collision

### Move (`mv` / `move`)

```bash
# Move to another workspace
uv run --env-file .env fab mv ws1.Workspace/nb1.Notebook ws2.Workspace

# Rename during move
uv run --env-file .env fab mv ws1.Workspace/nb1.Notebook ws2.Workspace/renamed.Notebook
```

### Update Properties (`set`)

```bash
# Rename an item
uv run --env-file .env fab set ws1.Workspace/nb1.Notebook -q displayName -i "New Name"

# Set description
uv run --env-file .env fab set ws1.Workspace/nb1.Notebook -q description -i "My description"
```

### Export / Import

```bash
# Export a single item to local
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp

# Export with force (skip sensitivity label prompt)
uv run --env-file .env fab export ws1.Workspace/nb1.Notebook -o /tmp -f

# Export all items from a workspace
uv run --env-file .env fab export ws1.Workspace -o /tmp -a

# Export to OneLake
uv run --env-file .env fab export ws1.Workspace/rep1.Report -o /ws1.Workspace/lh1.Lakehouse/Files/export -f

# Import from local (creates or updates)
uv run --env-file .env fab import ws1.Workspace/nb1_imported.Notebook -i /tmp/exports/nb1.Notebook

# Import with force (overwrite without confirmation)
uv run --env-file .env fab import ws1.Workspace/nb1.Notebook -i /tmp/nb1.Notebook -f
```

**Export flags:** `-o` output path, `-f` force, `-a` all, `--format` definition format
**Import flags:** `-i` input path, `-f` force, `--format` definition format

> **Important:** The `-o` output directory must already exist — `fab export` will not create it.

### Open in Browser

```bash
uv run --env-file .env fab open ws1.Workspace/lh1.Lakehouse
```

## Parameters Reference

### Common Flags

| Flag | Long | Purpose |
|------|------|---------|
| `-a` | `--all` | Select or show all |
| `-f` | `--force` | Force execution, skip validation |
| `-l` | `--long` | Detailed listing |
| `-i` | `--input` | JSON input (path or inline) |
| `-o` | `--output` | Output path |
| `-q` | `--query` | Filter JSON output with JMESPath |
| `-n` | `--name` | Specify a name |
| `-P` | `--params` | Parameters in key=value format |
| `-v` | `--version` | Show fab version |
| `-w` | `--wait` | Wait for job completion |
| `-C` | `--config` | Config for job |
| `-H` | `--headers` | HTTP headers for API (key=value) |
| `-X` | `--method` | HTTP method for API request |
| `-A` | `--audience` | Audience for API token |
| `-R` | `--role` | Access control role |
| `-W` | `--workspace` | Workspace name for assign/unassign |

### Auth Flags

| Flag | Long | Purpose |
|------|------|---------|
| `-u` | `--username` | Service principal clientId |
| `-p` | `--password` | Service principal clientSecret |
| `-t` | `--tenant` | Tenant ID |
| `-I` | `--identity` | Entra managed identity |
| | `--certificate` | Path to certificate |
| | `--federated-token` | Federated token |

## Output Formats

### Text (default)

Clean, formatted display with color-coded status. Headers shown with `-l` or `-q`.

### JSON

```bash
uv run --env-file .env fab ls --output_format json
```

**JSON response structure:**

```json
{
  "timestamp": "2026-01-06T08:00:00.000Z",
  "status": "Success",
  "command": "ls",
  "result": {
    "data": [],
    "hidden_data": [".capacities", ".gateways"],
    "message": "Operation completed successfully"
  }
}
```

**Error response:**

```json
{
  "timestamp": "2026-01-06T08:00:00.000Z",
  "status": "Failure",
  "command": "ls",
  "result": {
    "message": "Unable to find workspace",
    "error_code": "ERROR_WORKSPACE_NOT_FOUND"
  }
}
```

**Set persistent format:**

```bash
uv run --env-file .env fab config set output_format json
uv run --env-file .env fab config get output_format
```

**Stream behavior:** stdout = results, stderr = warnings/progress.

## JSON Input (`-i` flag)

Use single quotes around JSON:

```bash
# Bash
uv run --env-file .env fab set item.Resource -q query -i '{"key":"value"}'

# From file
uv run --env-file .env fab job start ws1.Workspace/pip1.DataPipeline -i ./input_file.json
```

## Modes

| Mode | Activation | Behavior |
|------|-----------|----------|
| `command_line` | `fab config set mode command_line` | Single commands with `fab` prefix (default for scripting) |
| `interactive` | `fab config set mode interactive` | Shell-like `fab:/$` prompt, no prefix needed |

**Re-authentication is required after switching modes.**

## Access Control (`acl`)

```bash
uv run --env-file .env fab acl ws1.Workspace/lh1.Lakehouse -R Admin
```

## Direct API Calls (`api`)

```bash
uv run --env-file .env fab api /v1/workspaces -X GET
uv run --env-file .env fab api /v1/workspaces/{id}/items -X GET -H "Content-Type=application/json"
```

## Shortcuts (`ln`)

```bash
# Internal OneLake shortcut
uv run --env-file .env fab ln ws1.Workspace/lh1.Lakehouse/Files/shared.Shortcut --type oneLake --target ../../shared.Workspace/source.Lakehouse/Files/datasets

# External Azure shortcut
uv run --env-file .env fab ln ws1.Workspace/lh1.Lakehouse/Tables/ext.Shortcut --type adlsGen2 -i '{"location": "...", "subpath": "...", "connectionId": "..."}'

# Check shortcut
uv run --env-file .env fab exists ws1.Workspace/lh1.Lakehouse/Files/external_data.Shortcut

# Get shortcut target
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse/Files/external_data.Shortcut -q target

# Delete shortcut
uv run --env-file .env fab rm ws1.Workspace/lh1.Lakehouse/Files/old_data.Shortcut -f
```

## Deploy

```bash
# Config-based deployment
uv run --env-file .env fab deploy --config config.yml -tenv dev

# Filter by item type
uv run --env-file .env fab deploy --config config.yml -P 'config_override={"core": {"item_types_in_scope": ["Notebook"]}}'
```
