---
name: fabric-mcp
description: Microsoft Fabric MCP Server setup and usage — provides AI agents with access to Fabric public APIs, item definitions, OneLake data operations, and best-practice guidance. Use when configuring the Fabric MCP Server for Claude Code or other AI clients.
allowed-tools: "Bash(npx *), Bash(dotnet *), Bash(cat *), Bash(grep *), Read, Write, Edit, Glob"
user-invocable: false
metadata:
  author: accelerate-data
---

# Fabric MCP Server

The Fabric MCP Server is a local-first Model Context Protocol server that provides AI agents with access to Microsoft Fabric's public APIs, item definitions, and best practices. It runs locally on your machine.

## What It Provides

### API Documentation & Best Practices Tools

| Tool | Purpose |
|------|---------|
| `docs_workloads` | Lists available Fabric workload types with public API specs |
| `docs_workload-api-spec` | Retrieves OpenAPI specs for specific workloads |
| `docs_platform-api-spec` | Returns core Fabric platform API specifications |
| `docs_item-definitions` | JSON schema definitions for Fabric items (Lakehouse, Notebook, Pipeline, etc.) |
| `docs_best-practices` | Best practice documentation — pagination, error handling, throttling |
| `docs_api-examples` | Example API request/response files |

### OneLake Data Operations Tools

| Tool | Purpose |
|------|---------|
| `onelake_list_workspaces` | Lists available workspaces |
| `onelake_list_items` | Lists workspace items with metadata |
| `onelake_list_files` | Hierarchical file listing within items |
| `onelake_download_file` | Download files from OneLake |
| `onelake_upload_file` | Upload files to OneLake |
| `onelake_delete_file` | Delete OneLake files |
| `onelake_create_directory` | Create directories via DFS endpoint |
| `onelake_delete_directory` | Delete directories (optionally recursive) |
| `onelake_get_table_config` | Table API configuration for items |
| `onelake_list_table_namespaces` | List table schemas/namespaces |
| `onelake_get_table_namespace` | Retrieve namespace metadata |
| `onelake_list_tables` | List tables within a namespace |
| `onelake_get_table` | Get specific table definitions |

### Core Operations Tools

| Tool | Purpose |
|------|---------|
| `core_create-item` | Create new Fabric items (Lakehouses, Notebooks, etc.) |

## Installation

### Option 1: Node.js / npx (Recommended)

**Requirements:** Node.js 20 LTS or later.

No install needed — `npx` downloads and runs it on demand.

### Option 2: .NET Build from Source

**Requirements:** .NET 9 SDK or later.

```bash
git clone https://github.com/microsoft/mcp.git
cd mcp
dotnet build servers/Fabric.Mcp.Server/src/Fabric.Mcp.Server.csproj --configuration Release
```

## Configuration

### Claude Code — Project Config (`.mcp.json`)

```json
{
  "mcpServers": {
    "fabric-mcp-server": {
      "command": "npx",
      "args": ["-y", "@microsoft/fabric-mcp@latest", "server", "start", "--mode", "all"],
      "type": "stdio"
    }
  }
}
```

### Claude Code — User Config (`~/.claude.json`)

Same JSON structure, placed in the user-level config file.

### Claude Desktop

**macOS:** `~/.claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fabric-mcp-server": {
      "command": "npx",
      "args": ["-y", "@microsoft/fabric-mcp@latest", "server", "start", "--mode", "all"],
      "type": "stdio"
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` or `.cursor/mcp.json` (project-level):

```json
{
  "mcpServers": {
    "fabric-mcp-server": {
      "command": "npx",
      "args": ["-y", "@microsoft/fabric-mcp@latest", "server", "start", "--mode", "all"]
    }
  }
}
```

### VS Code

`.vscode/mcp.json` (workspace) or user `settings.json`:

Install the Fabric MCP Server extension from the VS Code Marketplace for automatic setup.

### .NET Build Config (if built from source)

```json
{
  "mcpServers": {
    "Fabric MCP Server": {
      "command": "/path/to/repo/servers/Fabric.Mcp.Server/src/bin/Release/fabmcp",
      "args": ["server", "start"],
      "type": "stdio"
    }
  }
}
```

**Platform notes:**
- macOS/Linux: Use path as-is
- Windows: Use backslashes and `.exe` extension

## Server Modes

The `--mode` flag controls which tools are available:

| Mode | Tools Available |
|------|----------------|
| `all` | All tools (docs + OneLake + core) |
| `docs` | Documentation tools only (no data access) |
| `onelake` | OneLake data operations only |

## Example Prompts

After setup, use these prompts with your AI client:

**Workload & API questions:**
- "What Fabric workload types are available?"
- "Show me OpenAPI operations for 'notebook' with sample creation body"

**Schema & definitions:**
- "Create a Lakehouse resource definition with string and datetime columns"
- "Show JSON schema for a Data Pipeline item definition"

**Best practices:**
- "Show best practices for handling API throttling in Fabric"
- "What pagination patterns exist for Fabric REST APIs?"

**Development:**
- "Help me scaffold a Fabric workspace with Lakehouse and notebooks"
- "Generate a data pipeline configuration with sample data sources"

## Community: ms-fabric-mcp-server (Live CRUD Operations)

A community-maintained MCP server that exposes actual Fabric CRUD operations against **live environments**. 60 tools covering workspaces, items, notebooks, pipelines, lakehouses, Livy Spark, semantic models, and SQL.

**Repository:** [github.com/bablulawrence/ms-fabric-mcp-server](https://github.com/bablulawrence/ms-fabric-mcp-server)
**PyPI:** `ms-fabric-mcp-server`

### Setup

```json
{
  "mcpServers": {
    "fabric-ops": {
      "command": "uvx",
      "args": ["ms-fabric-mcp-server"],
      "env": {
        "FABRIC_BASE_URL": "https://api.fabric.microsoft.com/v1",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Authentication:** Uses `DefaultAzureCredential` — works with `az login`, environment variables (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`), VS Code credentials, or Managed Identity.

### Key Tool Categories (60 tools)

| Category | Count | Examples |
|----------|-------|---------|
| Workspace | 1 | `list_workspaces` |
| Item | 9 | `list_items`, `get_item`, `create_folder`, `delete_item`, `rename_item` |
| Lakehouse | 4 | `create_lakehouse`, `list_lakehouse_files`, `upload_lakehouse_file`, `delete_lakehouse_file` |
| Notebook | 6 | `create_notebook`, `get_notebook_definition`, `update_notebook_definition`, `get_notebook_run_details` |
| Job | 4 | `run_on_demand_job`, `get_job_status` |
| Livy Spark | 8 | `livy_create_session`, `livy_run_statement`, `livy_get_session_status` |
| Pipeline | 11 | `create_pipeline`, `add_copy_activity_to_pipeline`, `add_notebook_activity_to_pipeline` |
| Dataflow | 3 | `create_dataflow`, `get_dataflow_definition`, `run_dataflow` |
| Semantic Model | 9 | `create_semantic_model`, `add_table_to_semantic_model`, `execute_dax_query` |
| SQL (optional) | 3 | `get_sql_endpoint`, `execute_sql_query`, `execute_sql_statement` |

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `FABRIC_BASE_URL` | `https://api.fabric.microsoft.com/v1` | Fabric API base URL |
| `FABRIC_API_CALL_TIMEOUT` | `30` | API timeout (seconds) |
| `FABRIC_MAX_RETRIES` | `3` | Max retry attempts |
| `LIVY_API_CALL_TIMEOUT` | `120` | Livy timeout (seconds) |
| `LIVY_SESSION_WAIT_TIMEOUT` | `240` | Livy session wait (seconds) |

**Warning:** This server includes destructive operations (delete items, etc.) — use in development environments only.

## Fabric RTI MCP Server (Real-Time Intelligence)

Official Microsoft MCP server for Real-Time Intelligence / Eventhouse / Azure Data Explorer. 38 tools.

**Repository:** [github.com/microsoft/fabric-rti-mcp](https://github.com/microsoft/fabric-rti-mcp)
**PyPI:** `microsoft-fabric-rti-mcp`

### Setup

```json
{
  "mcpServers": {
    "fabric-rti-mcp": {
      "command": "uvx",
      "args": ["microsoft-fabric-rti-mcp"],
      "env": {
        "KUSTO_SERVICE_URI": "https://your-cluster.kusto.windows.net/",
        "KUSTO_SERVICE_DEFAULT_DB": "YourDatabase",
        "FABRIC_API_BASE_URL": "https://api.fabric.microsoft.com/v1"
      }
    }
  }
}
```

### Capabilities

- KQL query execution against Eventhouse/ADX
- Natural language to KQL (NL2KQL) translation
- Schema discovery for KQL databases
- Eventstream management (17 tools)
- Activator alerts (2 tools)
- Map visualization (7 tools)

## Recommended Combined Config

For full Fabric coverage in Claude Code `.mcp.json`:

```json
{
  "mcpServers": {
    "fabric-mcp-server": {
      "command": "npx",
      "args": ["-y", "@microsoft/fabric-mcp@latest", "server", "start", "--mode", "all"]
    },
    "fabric-ops": {
      "command": "uvx",
      "args": ["ms-fabric-mcp-server"]
    }
  }
}
```

**Prerequisites:** Node.js 20+ (official server), Python 3.10+ with `uv`/`uvx` (community server), Azure auth (`az login`).

## Relationship to fabric-cli

The `fab` CLI (`ms-fabric-cli` on PyPI) is a **separate tool** — a file-system-inspired command-line interface. It does **not** have MCP support. The MCP servers are independent projects for AI agent integration, while `fab` is for interactive/scripted terminal use.

## Security Notes

- The official Fabric MCP Server runs locally — documentation tools do not connect to live Fabric
- OneLake tools (official) and the community server do connect to your Fabric tenant
- Microsoft telemetry can be disabled per the repo documentation

## Resources

- [Fabric MCP Server README](https://github.com/microsoft/mcp/blob/main/servers/Fabric.Mcp.Server/README.md)
- [Fabric MCP Blog Post](https://blog.fabric.microsoft.com/en-US/blog/introducing-fabric-mcp-public-preview/)
- [ms-fabric-mcp-server (community)](https://github.com/bablulawrence/ms-fabric-mcp-server)
- [Fabric RTI MCP Repo](https://github.com/microsoft/fabric-rti-mcp)
- [Microsoft MCP Catalog](https://github.com/microsoft/mcp)
- [NuGet Package](https://www.nuget.org/packages/Microsoft.Fabric.Mcp/)
