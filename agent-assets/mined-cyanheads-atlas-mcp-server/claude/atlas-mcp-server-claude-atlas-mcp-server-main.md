# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Development Commands

### Build and Development

- `npm run build` - Build the TypeScript project and make executable
- `npm run dev` - Watch mode for TypeScript compilation
- `npm run rebuild` - Clean and rebuild project completely
- `npm run format` - Format code with Prettier

### Database Operations

- `npm run db:backup` - Create database backup with timestamped directory
- `npm run db:import <backup_path>` - Restore database from backup (destructive)
- `docker-compose up -d` - Start Neo4j database
- `docker-compose down` - Stop Neo4j database

### Running the Server

- `npm run start:stdio` - Run with stdio transport (default for MCP clients)
- `npm run start:http` - Run with HTTP transport on localhost:3010
- `npm run inspector` - Run MCP inspector for debugging

### Testing and Quality

- `npm run webui` - Open basic web UI for viewing data
- `npm run tree` - Generate project structure documentation

## Core Architecture

ATLAS is an MCP (Model Context Protocol) server with a three-tier Neo4j-backed architecture:

**Transport Layer** (`src/mcp/transports/`):

- `stdioTransport.ts` - Direct stdio communication (default)
- `httpTransport.ts` - HTTP server with authentication/rate limiting

**MCP Layer** (`src/mcp/`):

- `server.ts` - Main MCP server setup, tool/resource registration
- `tools/` - MCP tool implementations (15 total tools)
- `resources/` - MCP resource handlers for direct data access

**Data Layer** (`src/services/neo4j/`):

- Core services: `projectService.ts`, `taskService.ts`, `knowledgeService.ts`
- `searchService.ts` - Unified search across all entities
- `backupRestoreService.ts` - Database backup/restore operations

**Three-Tier Data Model**:

```
PROJECT (top-level containers)
├── TASK (actionable items within projects)
├── KNOWLEDGE (information/context for projects)
└── DEPENDENCIES (relationships between entities)
```

## Configuration

Environment variables are validated via Zod schema in `src/config/index.ts`. Key settings:

**Database**: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
**Transport**: `MCP_TRANSPORT_TYPE` (stdio/http), `MCP_HTTP_PORT` (3010)  
**Logging**: `MCP_LOG_LEVEL` (debug), `LOGS_DIR` (./logs)
**Backup**: `BACKUP_FILE_DIR` (./atlas-backups), `BACKUP_MAX_COUNT` (10)

## Key Implementation Notes

- All tools support both single and bulk operations via `mode` parameter
- Comprehensive input validation using Zod schemas per tool
- Request context tracking for operations (`src/utils/internal/requestContext.ts`)
- Structured logging with Winston (`src/utils/internal/logger.ts`)
- Backup/restore creates timestamped directories with JSON exports
- Rate limiting and authentication available for HTTP transport
- LLM provider integration available via OpenRouter (`src/services/llm-providers/`)

## Database Schema

Neo4j constraints and indexes are auto-created on startup. Core node types:

- `Project` nodes with `id` property (unique constraint)
- `Task` nodes with `id` property, linked to projects via `BELONGS_TO`
- `Knowledge` nodes with `id` property, linked to projects via `BELONGS_TO`
- `DEPENDS_ON` relationships for dependency tracking

## Testing & Development

No formal test framework detected. Use:

- `npm run inspector` for MCP protocol testing
- Manual testing via stdio/HTTP transports
- Database backup/restore for data safety during development
- Web UI for visual data verification
