---
name: databricks-fe-vm-workspace-deployment
description: Deploy and manage standard Databricks demo workspaces using the FE Vending Machine (FEVM) with automatic authentication and environment caching. Answers questions about which workspace was deployed or created at an earlier time. Do NOT use for custom IAM roles, custom VPCs, PrivateLink, cross-account S3 access, or other custom AWS integrations — use databricks-oneenv-workspace-deployment instead.
---

# FE Vending Machine Workspace Deployment Skill

This skill provides programmatic access to the FE Vending Machine (FEVM) for deploying and managing Databricks workspaces. It automatically handles authentication and caches environment information to minimize user interaction.

## Overview

The FE Vending Machine is used to create net-new demo environments that can live for up to 30 days. This skill:
- Automatically manages authentication via Chrome DevTools MCP
- Caches workspace information in `~/.vibe/fe-vm/` to avoid repeated browser interactions
- Supports deploying Serverless and Classic workspaces
- Can reuse existing workspaces when appropriate

## Instructions

### Step 1: Check Cached Environments First

Before deploying anything new, always check for existing environments:

```bash
python3 resources/environment_manager.py list
```

This shows all cached workspaces with their URLs, creation dates, and expiration dates.

### Step 2: Refresh Environment Cache (If Needed)

If no cached environments exist or you need fresh data:

```bash
python3 resources/fe_vm_client.py refresh-cache
```

This will:
1. Check for a valid session cookie in `~/.vibe/fe-vm/session.json`
2. If no valid session, use Chrome DevTools MCP to authenticate and capture the cookie
3. Fetch all deployments from FEVM and update the cache

### Step 3: Find or Deploy a Workspace

**To find an existing suitable workspace:**

```bash
python3 resources/environment_manager.py find --type serverless --min-days 7
```

This returns a workspace URL if one exists with at least 7 days remaining.

**To deploy a new Serverless workspace:**

```bash
python3 resources/fe_vm_client.py deploy-serverless --name my-demo --region us-east-1 --lifetime 30
```

**To deploy a new Classic workspace:**

```bash
python3 resources/fe_vm_client.py deploy-classic --name my-classic --region us-west-2 --lifetime 14
```

### Step 4: Check Deployment Status

For new deployments, monitor the progress:

```bash
python3 resources/fe_vm_client.py status --run-id <run_id>
```

Or wait for completion:

```bash
python3 resources/fe_vm_client.py wait --run-id <run_id>
```

### Step 5: Authenticate to the Workspace

Once deployed, use the databricks-authentication skill to set up CLI access:

```bash
databricks auth login <workspace_url> --profile=fe-vm-<workspace_name>
```

## Decision Flow

Use this flow to decide what to do:

1. **Check cached environments**: `python3 resources/environment_manager.py list`
2. **If suitable workspace exists** (correct type, >3 days remaining): Use it
3. **If no suitable workspace**: Refresh cache and check FEVM: `python3 resources/fe_vm_client.py refresh-cache`
4. **If still no suitable workspace**: Deploy new one based on requirements:
   - Need Apps/Lakebase? → Deploy Serverless
   - Need custom cloud config? → Deploy Classic
   - Basic demo? → Deploy Serverless (faster)

## Available Commands

### environment_manager.py

| Command | Description |
|---------|-------------|
| `list` | List all cached environments with details |
| `find --type <serverless\|classic> --min-days N` | Find suitable workspace |
| `get <workspace_name>` | Get details for specific workspace |
| `remove <workspace_name>` | Remove workspace from cache |
| `clear` | Clear all cached data |

### fe_vm_client.py

| Command | Description |
|---------|-------------|
| `refresh-cache` | Fetch latest from FEVM and update cache |
| `deploy-serverless [--name N] [--region R] [--lifetime D]` | Deploy serverless workspace |
| `deploy-classic [--name N] [--region R] [--lifetime D]` | Deploy classic workspace |
| `status --run-id ID` | Check deployment status |
| `wait --run-id ID [--timeout M]` | Wait for deployment to complete |
| `user-info` | Get current user info |
| `quota` | Get quota information |
| `templates` | List available deployment templates |

## Environment Storage

All environment data is stored in `~/.vibe/fe-vm/`:

```
~/.vibe/fe-vm/
├── session.json          # Session cookie and expiry
├── environments.json     # Cached workspace information
└── deployments/          # Individual deployment configs
    └── <workspace_name>.json
```

## Authentication Flow

When authentication is needed:

1. **Check existing session**: Look for valid cookie in `~/.vibe/fe-vm/session.json`
2. **If expired or missing**:
   - Open Chrome DevTools MCP to navigate to FEVM
   - User completes SSO login
   - Automatically extract `__Host-databricksapps` cookie
   - Save to `~/.vibe/fe-vm/session.json` with expiry timestamp
3. **Cookie typically valid for 24-48 hours**

## Template Reference

| Template | ID | Cloud | Use Case |
|----------|-----|-------|----------|
| AWS Serverless Stable | `aws_stable_serverless` | AWS | Apps, Lakebase, fast demos |
| AWS Stable Classic | `aws_stable_classic` | AWS | Custom networking, cloud integrations |
| AWS Sandbox Serverless | `aws_sandbox_serverless` | AWS | Sandbox serverless testing |
| AWS Sandbox Classic | `aws_sandbox_classic` | AWS | Sandbox classic testing |
| Azure Sandbox Classic | `azure_sandbox_classic` | Azure | Azure-specific demos |
| Azure Stable Classic | `azure_stable_classic` | Azure | Azure classic workspaces |
| GCP Sandbox Classic | `gcp_sandbox_classic` | GCP | GCP classic demos |
| GCP Sandbox Serverless | `gcp_sandbox_serverless` | GCP | GCP serverless demos |
| GCP Stable Classic | `gcp_stable_classic` | GCP | GCP stable classic |
| GCP Stable Serverless | `gcp_stable_serverless` | GCP | GCP stable serverless |

## AWS Regions

Available regions: `us-east-1`, `us-east-2`, `us-west-1`, `us-west-2`, `eu-central-1`, `ap-northeast-1`

## Workspace and Catalog Naming

FE-VM workspaces follow a standard naming convention:

| Component | Pattern | Example |
|-----------|---------|---------|
| Workspace name | `<name>` | `deep-research-agent` |
| Workspace URL | `https://fevm-<name>.cloud.databricks.com` | `https://fevm-deep-research-agent.cloud.databricks.com` |
| Standard catalog | `<name_with_underscores>_catalog` | `deep_research_agent_catalog` |

**Important:** Each FE-VM workspace comes with a pre-created Unity Catalog. The catalog name is derived from the workspace name by replacing hyphens with underscores and appending `_catalog`.

When creating schemas or tables, **always use the standard catalog** rather than creating a new one:

```sql
-- Use the existing catalog (example for workspace "deep-research-agent")
USE CATALOG deep_research_agent_catalog;

-- Create schemas within the standard catalog
CREATE SCHEMA IF NOT EXISTS my_demo_schema;

-- Create tables in the standard catalog
CREATE TABLE deep_research_agent_catalog.my_demo_schema.my_table (...);
```

This avoids permission errors and ensures consistency across the workspace.

## Notes

- **Always prefer reusing existing workspaces** to conserve quota and deployment time
- **Serverless workspaces** deploy in ~5-10 minutes
- **Classic workspaces** deploy in ~15-20 minutes
- **Maximum lifetime** is 30 days
