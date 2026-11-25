---
name: fabric-cli-onelake
description: Fabric CLI OneLake file operations — upload, download, copy, move, list, create, and delete files and folders in OneLake storage. Use when working with files inside Lakehouse Files/ or Tables/ paths.
allowed-tools: "Bash(uv run *), Bash(fab *), Bash(cat *), Bash(grep *), Read, Write, Edit, Glob"
user-invocable: false
metadata:
  author: accelerate-data
---

# Fabric CLI — OneLake File Operations

Complete reference for reading and writing files in OneLake storage via `fab` CLI.

## Execution Pattern

```bash
uv run --env-file .env fab <command>
```

## OneLake Path Format

OneLake storage lives inside items (Lakehouse, Warehouse, etc.) with two root sections:

```
ws1.Workspace/lh1.Lakehouse/Files/          ← Unstructured file storage
ws1.Workspace/lh1.Lakehouse/Tables/         ← Delta tables (managed)
ws1.Workspace/wh1.Warehouse/Tables/dbo/     ← Warehouse tables (schema-qualified)
```

**Path examples:**

```
ws1.Workspace/lh1.Lakehouse/Files/data.csv
ws1.Workspace/lh1.Lakehouse/Files/raw-data/2024/january/sales.parquet
ws1.Workspace/lh1.Lakehouse/Tables/dbo/customer_profiles
ws1.Workspace/wh1.Warehouse/Tables/dbo/orders
ws1.Workspace/sem1.SemanticModel/Tables
```

## Navigate OneLake

```bash
# Change directory into OneLake
uv run --env-file .env fab cd ws1.Workspace/lh1.Lakehouse/Files
uv run --env-file .env fab cd ws1.Workspace/lh1.Lakehouse/Tables
uv run --env-file .env fab cd ws1.Workspace/lh1.Lakehouse/Files/raw-data/2024
```

## List Files and Folders

```bash
# List files in a lakehouse
uv run --env-file .env fab ls ws1.Workspace/lh1.Lakehouse/Files

# List tables
uv run --env-file .env fab ls ws1.Workspace/lh1.Lakehouse/Tables

# List warehouse tables (schema-qualified)
uv run --env-file .env fab ls ws1.Workspace/wh1.Warehouse/Tables/dbo

# List semantic model tables
uv run --env-file .env fab ls ws1.Workspace/sem1.SemanticModel/Tables
```

## Check Existence

```bash
# Check if a folder exists
uv run --env-file .env fab exists ws1.Workspace/lh1.Lakehouse/Files/data-processing

# Check if a file exists
uv run --env-file .env fab exists ws1.Workspace/lh1.Lakehouse/Files/datasets/sales.parquet
```

## Get File/Folder Metadata

```bash
# Full metadata
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse/Files/datasets

# Query specific field
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse/Files/datasets -q paths[0]

# Full JSON
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse/Files/datasets -q .

# Save metadata to file
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse/Files/datasets -q paths[0] -o /tmp/metadata
```

## Upload Files (Local → OneLake)

```bash
# Upload a single file
uv run --env-file .env fab cp /tmp/local-data/dataset.csv ws1.Workspace/lh1.Lakehouse/Files/upload/

# Upload to a specific path
uv run --env-file .env fab cp ./local/data.csv ws1.Workspace/lh1.Lakehouse/Files/data.csv
```

## Download Files (OneLake → Local)

```bash
# Download a file
uv run --env-file .env fab cp ws1.Workspace/lh1.Lakehouse/Files/csv/fab.csv /tmp/mydir

# Download to specific path
uv run --env-file .env fab cp ws1.Workspace/lh1.Lakehouse/Files/data.csv ./local/
```

## Copy Files Within OneLake

```bash
# Copy between paths in same lakehouse
uv run --env-file .env fab cp ws1.Workspace/lh1.Lakehouse/Files/csv/data.csv ws1.Workspace/lh1.Lakehouse/Files/dest/

# Copy between workspaces
uv run --env-file .env fab cp ws1.Workspace/lh1.Lakehouse/Files/data.csv ws2.Workspace/lh2.Lakehouse/Files/data.csv

# Force overwrite
uv run --env-file .env fab cp ./data.csv ws1.Workspace/lh1.Lakehouse/Files/data.csv -f

# Recursive copy (all files in a folder)
uv run --env-file .env fab cp ws1.Workspace/lh1.Lakehouse/Files/source/ ws1.Workspace/lh1.Lakehouse/Files/dest/ -r
```

**Copy flags:** `-f` force (overwrite), `-r` recursive

## Create Folders

```bash
# Create a folder
uv run --env-file .env fab create ws1.Workspace/lh1.Lakehouse/Files/data-processing

# Create nested folders
uv run --env-file .env fab create ws1.Workspace/lh1.Lakehouse/Files/raw-data/2024/january
```

## Delete Files and Folders

```bash
# Delete a folder (with confirmation)
uv run --env-file .env fab rm ws1.Workspace/lh1.Lakehouse/Files/old-data

# Force delete a file (no confirmation)
uv run --env-file .env fab rm ws1.Workspace/lh1.Lakehouse/Files/temp/temporary-file.csv -f
```

## Shortcuts

Shortcuts provide virtual access to external data without copying:

```bash
# Create internal OneLake shortcut
uv run --env-file .env fab ln ws1.Workspace/lh1.Lakehouse/Files/shared_data.Shortcut --type oneLake --target ../../shared.Workspace/source.Lakehouse/Files/datasets

# Create external Azure Data Lake shortcut
uv run --env-file .env fab ln ws1.Workspace/lh1.Lakehouse/Tables/external_sales.Shortcut --type adlsGen2 -i '{"location": "https://storageaccount.dfs.core.windows.net/container", "subpath": "/data/sales", "connectionId": "<guid>"}'

# Check shortcut exists
uv run --env-file .env fab exists ws1.Workspace/lh1.Lakehouse/Files/external_data.Shortcut

# Get shortcut target
uv run --env-file .env fab get ws1.Workspace/lh1.Lakehouse/Files/external_data.Shortcut -q target

# Rename shortcut
uv run --env-file .env fab set ws1.Workspace/lh1.Lakehouse/Files/updated_name.Shortcut -q name -i external_data

# Delete shortcut
uv run --env-file .env fab rm ws1.Workspace/lh1.Lakehouse/Files/old_data.Shortcut -f
```

Shortcuts work in both `/Files` and `/Tables` sections.

## Common Patterns

### Upload a batch of CSV files

```bash
# Upload each file in a local directory
for f in /tmp/data/*.csv; do
  uv run --env-file .env fab cp "$f" ws1.Workspace/lh1.Lakehouse/Files/uploads/
done
```

### Download and inspect

```bash
# Download to temp
uv run --env-file .env fab cp ws1.Workspace/lh1.Lakehouse/Files/reports/summary.csv /tmp/

# Inspect locally
cat /tmp/summary.csv | head -20
```

### Verify upload

```bash
# Upload
uv run --env-file .env fab cp ./data.parquet ws1.Workspace/lh1.Lakehouse/Files/data.parquet

# Verify it exists
uv run --env-file .env fab exists ws1.Workspace/lh1.Lakehouse/Files/data.parquet
```

## Practical Tips

- **Token efficiency:** Use `fab cp` to download files + `Read` tool to inspect content locally. Never use MCP download + base64 decode — it wastes context tokens. Never paste base64 strings in echo commands.
- **Quoting paths with spaces:** Wrap OneLake paths containing spaces in double quotes: `"ai_pro_wp.Workspace/ai_fork_lake.Lakehouse/Files/my folder/data.csv"`

## Common Issues

| Issue | Fix |
|-------|-----|
| `ERROR_WORKSPACE_NOT_FOUND` | Check workspace name and `.Workspace` extension |
| File not found after upload | Verify full path including `/Files/` prefix |
| Cannot list Tables | Tables are managed by Spark/SQL — use `fab table schema` for details |
| Copy fails between workspaces | Ensure both workspaces exist and auth tokens have access |
| Shortcut creation fails | Check `--type` (oneLake, adlsGen2, s3, etc.) and connection ID |
| Permission denied | Verify `FAB_TOKEN_ONELAKE` is set in `.env` |
