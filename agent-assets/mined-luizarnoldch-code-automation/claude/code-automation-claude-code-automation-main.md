# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack automation platform for orchestrating tasks with AI agents. Manages projects, workflows, milestones, tasks, and executions with a CLI-driven architecture.

## Tech Stack

- **Backend**: Go 1.26.1 with SQLite (libsql/cgo)
- **Frontend**: Next.js 16.2+ with TypeScript
- **Package Manager**: Bun (client), Go modules (server)
- **Styling**: Tailwind CSS
- **Validation**: Zod (client), Go structs (server)

## Development Commands

### Server (Go)

```bash
cd server/

# Run development server
make run
# Or directly:
go run ./cmd/automation

# Build binary
make build
# Output: server/bin/automation

# Run tests
go test ./...
go test ./pkg/shared/... -v

# Create new migration
make migrate/create name=<migration_name>

# Apply migrations
make migrate/up

# Reset database (drop + recreate + migrate + seed)
make reset

# Database operations
make db/sync        # Migrate up and generate SQLC code
make migrate/down   # Rollback one migration
make migrate/force  # Force migration version
```

### Client (Next.js)

```bash
cd client/

# Install dependencies
bun install

# Run dev server (port 3000)
bun dev

# Build
bun build

# Lint with Biome
bun lint

# Format code
bun format
```

### Running Both Services

```bash
# Terminal 1 - Backend
cd server && make run

# Terminal 2 - Frontend
cd client && bun dev
```

The frontend proxies `/api/*` requests to the backend via Next.js rewrites configured in `client/next.config.ts`.

## Backend Architecture

### Project Structure

```
server/
├── cmd/
│   └── automation/          # Main application entry point
│       └── main.go
├── pkg/
│   ├── app/                 # App initialization, routing, dependency injection
│   ├── agents/              # Agent management
│   ├── database/            # DB connection, migrations, transaction manager
│   ├── file_system/         # File tree operations
│   ├── middleware/          # HTTP middleware (logging)
│   ├── orchestrator/        # Core domain: orchestrators, groups, runs
│   ├── shared/              # Shared utilities (path handling)
│   └── buildinfo/           # Build metadata
├── sql/
│   └── migrations/          # Goose-style migration files
├── docs/
│   └── bruno/               # Bruno API client specs
└── Makefile                 # Build automation
```

### Key Patterns

**Handler-Service-Repository Pattern**: Each domain follows this structure:
- `domain.go` - Domain models (structs)
- `handler.go` - HTTP handlers (API layer)
- `service.go` - Business logic
- `repository.go` - Data access (SQLite)
- `dto.go` - Request/response types
- `mappers.go` - Domain <-> DTO conversions

**Example - Orchestrator domain**:
- `server/pkg/orchestrator/handler.go` - HTTP routes for orchestrators, groups, runs
- `server/pkg/orchestrator/service.go` - Business logic for executing pipelines
- `server/pkg/orchestrator/repository.go` - SQL queries

### Database

- SQLite with `libsql` driver (supports CGO)
- Migrations use Goose-style naming: `XXX_description.{up,down}.sql`
- Transaction manager in `database.Manager` for atomic operations
- Default workspace root: `/mnt/d/Workspace` (see `pkg/shared/paths.go`)

### Testing

Go tests use testify:
```bash
go test ./pkg/shared/... -v
go test ./pkg/file_system/... -v
```

## Frontend Architecture

### Project Structure

```
client/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (dashboard)/     # Route group for dashboard layout
│   │   │   ├── orchestrator/
│   │   │   │   ├── list/           # /orchestrator/list
│   │   │   │   ├── preview/        # /orchestrator/preview
│   │   │   │   └── [orchestratorId]/
│   │   │   │       ├── files/[[...path]]/   # File explorer
│   │   │   │       └── pipeline/             # Pipeline view
│   │   │   └── layout.tsx
│   │   └── api/             # API routes (Inngest webhook handler)
│   ├── components/          # Shared UI components (shadcn/ui based)
│   ├── features/            # Feature-based modules
│   │   ├── agents/
│   │   ├── file_system/
│   │   ├── orchestator/     # Note: spelled "orchestator"
│   │   └── sidebar/
│   ├── hooks/               # Global React hooks
│   └── lib/
│       ├── api.ts           # Generic API fetcher
│       └── utils.ts         # Utility functions (cn helper)
├── biome.json               # Biome linting/formatting config
└── next.config.ts           # Next.js config with API proxy
```

### Key Patterns

**Feature-Based Organization**: Each feature is self-contained:
- `api/` - API functions using `apiFetch()` from `lib/api.ts`
- `components/` - Feature-specific React components
- `hooks/` - TanStack Query hooks (useQuery, useMutation, suspense variants)
- `schema/` - Zod schemas for validation
- `views/` - Page-level view components

**API Client**: Uses lightweight wrapper around native `fetch` in `lib/api.ts`:
```typescript
import { apiFetch } from "@/lib/api";
const data = await apiFetch<Orchestrator[]>('/orchestrator');
```

**Data Fetching**: TanStack Query for server state:
- Query hooks: `useListOrchestators()`, `useGetOrchestator(id)`
- Mutation hooks: `useCreateOrchestator()`, `useUpdateOrchestator()`
- Suspense variants: `useSuspenseListOrchestators()`

**State Management**: Zustand for client state (see `features/orchestator/hooks/use-orchestator-store.ts`)

### Path Aliases

- `@/` maps to `src/` (configured in tsconfig.json)

## Bruno API Documentation

API specs for testing endpoints are in `server/docs/bruno/automation-api/`:
- Open the folder in Bruno API client
- Environment variables defined in `environments/`

## Important Notes

- **Path Handling**: The server handles both Windows and WSL path formats (`/mnt/d/...` <-> `D:\...`)
- **Workspace Root**: Default is `/mnt/d/Workspace` - configurable via request context
- **Orchestrator Spelling**: Feature folder is named `orchestator` (missing 'r') - maintain consistency
- **Next.js Version**: 16.x has breaking changes from previous versions - check `node_modules/next/dist/docs/` for current API
- **Build Info**: Server embeds build metadata from `server/pkg/buildinfo/BuildInfo.txt`
