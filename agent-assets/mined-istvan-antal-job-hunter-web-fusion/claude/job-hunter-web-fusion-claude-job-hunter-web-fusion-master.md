# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- `bun run server` - Run both client and server in development (sets CLIENT_DEV=1)
- `npm run dev` - Run client only (requires separate server on port 14001)  
- `npm run build` - Build for production (TypeScript compilation + Vite build)
- `npm run lint` - Run ESLint with TypeScript and React plugins
- `npm run preview` - Preview production build

## Architecture Overview

This is a React + Vite frontend with Express server that acts as a thin wrapper around the sibling `job-hunter` Deno backend. The key architectural pattern is direct cross-repo imports using relative paths.

### Cross-Repository Integration
- Imports backend entities directly: `../../../../job-hunter/entities/Job.ts`
- Imports AI functions: `../../../../job-hunter/ai/computeCompatibility`  
- Requires both `job-hunter-web-fusion` and `job-hunter` repos to be sibling directories
- DB schema and migrations are owned by the backend repo

### Server API Pattern
- Server exposes POST `/api/:function` endpoints
- Functions are registered in `src/main/functions.ts` and auto-exposed
- Each function receives `(args..., context)` where `context.user` comes from JWT cookie
- Add new APIs by creating `src/**/api/*.ts` files and exporting from functions.ts

### Database Access
- Uses TypeORM with entities imported from backend repo
- Shared `dataSource` from `src/core/db.ts` - always use this instance
- Query with `getRepository(Job)` for simple operations
- Use QueryBuilder for complex aggregations (see `src/stats/api/fetchStats.ts`)

### Client-Server Communication  
- Client hooks in `src/core/data.ts` and `src/core/serverHooksCreators.ts`
- Query pattern: `useQuery('functionName', { params: [...] })`  
- Mutation pattern: `createServerHook('functionName')`
- Server can return cookies via `withCookies()` from `src/core/http.ts`

## Environment Variables

Required:
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` - Postgres connection
- `DB_LOGGING` - Enable TypeORM query logging

Optional:
- `PORT` - Express server port (default: 14001)
- `JWT_SECRET` - For cookie authentication  
- `VITE__PORT` - Vite dev server port

## Key File Locations

- `src/main/server.ts` - Express server, JWT handling, API dispatch
- `src/main/functions.ts` - Registry of all server functions  
- `src/core/db.ts` - TypeORM DataSource configuration
- `src/core/data.ts` & `src/core/serverHooksCreators.ts` - Client query/mutation hooks

## Important Conventions

- Server functions must return serializable JSON (use `null` for void endpoints)
- Always import `reflect-metadata` before TypeORM usage (already done in db.ts)
- Client Job interface uses Mongo-style `_id`, but server uses TypeORM entities with `id`
- Backend handles all DB migrations via `deno task migrate` and `deno task generate-migration`