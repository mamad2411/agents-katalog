# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Overture is an MCP (Model Context Protocol) server that provides visual plan execution and approval workflows for AI coding agents. It intercepts AI agent planning phases and renders them as interactive visual flowcharts before code is written.

## Build & Development Commands

```bash
# Development with hot reload
npm run dev

# Build for production (outputs to dist/)
npm run build

# Run linting
npm run lint

# Start production server
npm run start

# Clean build artifacts
npm run clean
```

## Architecture

### Core Components

**MCP Server (`src/index.ts`)**
- Entry point that initializes the MCP server using `@modelcontextprotocol/sdk`
- Exposes tools: `submit_plan`, `get_approval`, `update_node_status`, `plan_completed`, `plan_failed`, `check_rerun`, `check_pause`, `get_resume_info`, `request_plan_update`, `create_new_plan`, `get_usage_instructions`
- Starts HTTP server (default port 3031) and WebSocket server (default port 3030)
- Configuration via env vars: `OVERTURE_HTTP_PORT`, `OVERTURE_WS_PORT`, `OVERTURE_AUTO_OPEN`

**Tool Handlers (`src/tools/handlers.ts`)**
- Implements all MCP tool logic
- Uses `StreamingXMLParser` to parse plan XML into nodes/edges
- Manages project context via hashed workspace paths for multi-project support
- Post-processes plans: filters decision nodes, rewires edges, detects branch points from graph structure

**Plan Store (`src/store/plan-store.ts`)**
- `MultiProjectPlanStore`: Manages plans for multiple projects simultaneously
- Handles approval flow with Promise-based resolvers
- Tracks pause/resume states, rerun requests per project
- Auto-saves active projects every 3 seconds to `~/.overture/history.json`

**WebSocket Server (`src/websocket/ws-server.ts`)**
- `WebSocketManager`: Manages client connections and project subscriptions
- Supports relay mode when port is already in use (multiple agents can share one UI)
- Broadcasts plan updates to subscribed clients
- Handles client messages: approve, cancel, pause, resume, rerun requests

**HTTP Server (`src/http/server.ts`)**
- Serves the React UI from `ui-dist/`
- API endpoints: `/api/test-plan`, `/api/mcp-marketplace` (CORS proxy), `/api/attachments/save`

**XML Parser (`src/parser/xml-parser.ts`)**
- `StreamingXMLParser`: SAX-based streaming parser for plan XML
- Parses `<plan>`, `<node>`, `<edge>`, `<field>`, `<branch>` elements

**History Storage (`src/storage/history-storage.ts`)**
- Persists plans to `~/.overture/history.json`
- Debounced writes to prevent excessive disk I/O

### Type System (`src/types.ts`)

Key types:
- `PlanNode`: Task or decision node with status, fields, branches, attachments
- `PlanEdge`: Connection between nodes (from → to)
- `Plan`: Plan metadata with status lifecycle (streaming → ready → approved → executing → completed/failed)
- `ProjectContext`: Multi-project support via workspace path hashing
- `WSMessage` / `WSClientMessage`: WebSocket protocol types

### Agent-Specific Prompts (`prompts/`)

Contains usage instructions for different AI agents:
- `claude-code.md`, `cline.md`, `cursor.md`, `sixth.md`, `gh_copilot.md`
- Loaded by `get_usage_instructions` tool based on `agent_type` parameter

## Key Patterns

- Plans are identified by `projectId` (SHA256 hash of workspace path, first 12 chars)
- Branch points detected from graph structure: nodes with multiple outgoing edges
- Decision nodes (legacy format) are filtered out and edges rewired during post-processing
- WebSocket relay mode allows multiple MCP server instances to share one UI
