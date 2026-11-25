---
name: sim-studio
description: Sim Studio AI agent orchestration — build, deploy, and invoke visual workflows as MCP tools. Use when automating multi-step tasks, creating agent workflows, or orchestrating AI pipelines via Sim Studio.
version: 1.0.0
triggers:
  - sim studio
  - sim workflow
  - agent workflow
  - orchestrate workflow
  - visual workflow
  - sim automation
tools:
  - sim-studio (MCP)
  - brave-search
  - playwright
---

# Sim Studio Automation Skill

## Overview

Sim Studio is a visual AI agent orchestration platform running locally. Claude Code connects to it via MCP to invoke deployed workflows as tools.

## Local Instance

| Property | Value |
|----------|-------|
| App URL | `http://localhost:3100` |
| Realtime | `http://localhost:3102` |
| Database | `postgresql://postgres:simstudio_local_2026@localhost:5433/simstudio` |
| Admin API Key | Stored in `~/Projects/sim/.env` |
| Auth | Disabled (anonymous sessions) |
| Repo | `~/Projects/sim/` |
| Docker Compose | `docker-compose.prod.yml` + `docker-compose.override.yml` |

## Architecture

```
Claude Code (CoreMind)
    │
    ├── MCP Server: sim-studio
    │   └── Invokes deployed Sim workflows as callable tools
    │
    ├── Admin API (REST)
    │   └── Export/import/manage workflows programmatically
    │
    └── Direct API
        ├── /api/chat/{id}         — Chat with deployed workflows
        ├── /api/mcp/servers       — Manage MCP servers
        ├── /api/mcp/tools/execute — Execute MCP tools
        └── /api/v1/admin/*        — Admin operations
```

## Starting / Stopping

```bash
# Start
cd ~/Projects/sim && docker compose -f docker-compose.prod.yml -f docker-compose.override.yml up -d

# Stop
cd ~/Projects/sim && docker compose -f docker-compose.prod.yml -f docker-compose.override.yml down

# View logs
cd ~/Projects/sim && docker compose -f docker-compose.prod.yml -f docker-compose.override.yml logs -f simstudio

# Restart
cd ~/Projects/sim && docker compose -f docker-compose.prod.yml -f docker-compose.override.yml restart simstudio
```

## Admin API

The Admin API enables programmatic workflow management (GitOps).

```bash
# List workspaces
curl -s -H "x-admin-key: $ADMIN_API_KEY" http://localhost:3100/api/v1/admin/workspaces

# Export a folder of workflows
curl -s -H "x-admin-key: $ADMIN_API_KEY" http://localhost:3100/api/v1/admin/folders/{folderId}/export

# Audit logs
curl -s -H "x-admin-key: $ADMIN_API_KEY" http://localhost:3100/api/v1/admin/audit-logs
```

Admin API key is in `~/Projects/sim/.env` as `ADMIN_API_KEY`.

## MCP Integration

### How It Works
1. Build a workflow visually in Sim Studio UI (http://localhost:3100)
2. Deploy the workflow
3. In Deploy panel, go to MCP tab
4. Configure tool name, description, and parameter descriptions
5. Add to an MCP server
6. Claude Code can now invoke it via the `sim-studio` MCP server

### Creating a Workflow MCP Server (via UI)
1. Go to Settings > MCP Servers
2. Click "Create Server"
3. Name it and copy the server URL
4. The URL format is: `http://localhost:3100/api/mcp/serve/{serverId}`

### Updating Claude Code MCP Config
After creating a server in Sim Studio, update `~/.claude.json`:
```json
{
  "mcpServers": {
    "sim-studio": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:3100/api/mcp/serve/{YOUR_SERVER_ID}",
               "--header", "X-API-Key:{YOUR_API_KEY}"]
    }
  }
}
```

## Workflow Patterns for Automation

### Pattern 1: Research Pipeline
Build a workflow that chains: Web Search > Content Extract > LLM Summarize > Output
Deploy as MCP tool `research_topic` — Claude Code calls it with a topic.

### Pattern 2: Data Processing
Build: File Upload > Parse > Transform > Database Write
Deploy as MCP tool `process_document`.

### Pattern 3: Multi-LLM Consensus
Build: Fan-out to 3 LLMs > Collect > Consensus Agent > Final Answer
Deploy as MCP tool `consensus_answer`.

### Pattern 4: Scheduled Monitoring
Use Sim's schedule trigger for recurring tasks (cron-style).
Results can be sent via webhook or stored in DB.

### Pattern 5: Webhook-Triggered Automation
Set up webhook trigger in Sim Studio.
External services POST to the webhook URL to kick off workflows.

## Ollama Integration

Sim Studio connects to your local Ollama at `http://host.docker.internal:11434`.
Any models you have in Ollama are available as LLM providers in workflows.

## Key Files

| File | Purpose |
|------|---------|
| `~/Projects/sim/.env` | All secrets and config |
| `~/Projects/sim/docker-compose.prod.yml` | Production Docker setup |
| `~/Projects/sim/docker-compose.override.yml` | Port overrides (3100, 3102, 5433) |
| `~/.claude.json` | MCP server config (sim-studio entry) |

## Troubleshooting

### Sim Studio not responding
```bash
docker ps --filter name=sim  # Check container status
docker compose -f docker-compose.prod.yml -f docker-compose.override.yml logs simstudio --tail 50
```

### MCP tools not showing
1. Ensure a workflow is deployed AND added to an MCP server
2. Verify the server ID in `~/.claude.json` matches the Sim Studio MCP server
3. Restart Claude Code after config changes

### Database issues
```bash
docker compose -f docker-compose.prod.yml -f docker-compose.override.yml logs db --tail 50
```
