# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Key Docs to Read
- `README.md` for Docker/Makefile workflows, environment variables, and MCP setup.
- `.github/copilot-instructions.md` for architecture notes and development commands.

## Common Commands

### Backend (.NET)
- Build solution: `dotnet build OpenDeepWiki.sln`
- Run API: `dotnet run --project src/OpenDeepWiki/OpenDeepWiki.csproj`

### Frontend (Next.js)
- Install deps: `cd web && npm install`
- Dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`
- Prod start: `npm run start`

### Docker/Makefile
- Build all images: `make build`
- Run all services (logs): `make dev`
- Run backend only: `make dev-backend`
- Start services (detached): `make up`
- Stop services: `make down`
- Tail logs: `make logs`

## High-Level Architecture

### Solution Layout
- `OpenDeepWiki.sln` includes current OpenDeepWiki projects plus legacy KoalaWiki projects; favor `src/OpenDeepWiki/*` and `web/*` for active development.

### Backend (ASP.NET Core)
- API entry point: `src/OpenDeepWiki/Program.cs` (MiniApis + OpenAPI + Scalar in dev).
- Agent orchestration: `src/OpenDeepWiki/Agents/` (constructed via `AgentFactory`).
- Models & services: `src/OpenDeepWiki/Models/` and `src/OpenDeepWiki/Services/` for request/response DTOs and domain services.

### Data Layer (EF Core)
- Entities: `src/OpenDeepWiki.Entities/` (e.g., Users, Repositories, DocDirectory).
- Core context contract + base: `src/OpenDeepWiki.EFCore/MasterDbContext.cs` with `IContext` and shared model configuration.
- Provider contexts: `src/EFCore/OpenDeepWiki.Sqlite/SqliteDbContext.cs` and `src/EFCore/OpenDeepWiki.Postgresql/PostgresqlDbContext.cs`.

### Frontend (Next.js App Router)
- App entry/layout: `web/app/layout.tsx` with routes in `web/app/*`.
- Shared UI: `web/components/*` and hooks in `web/hooks/*`.
- API/types: `web/types/*` and `web/middleware.ts` for routing middleware.

## Configuration Pointers
- App settings: `src/OpenDeepWiki/appsettings.json` and `appsettings.Development.json`.
- LLM config: `AI` section in appsettings; environment variables fallback (`CHAT_API_KEY`, `ENDPOINT`, `MODEL_PROVIDER`).
- Docker envs: see `README.md` for full list of required environment variables.
