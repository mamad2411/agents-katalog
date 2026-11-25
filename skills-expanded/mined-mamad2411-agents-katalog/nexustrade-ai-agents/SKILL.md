# AI Agent Instructions for Hyperliquid Trading Dashboard

This repository is a full-stack trading dashboard with an AI/agent-focused backend and a React/Vite frontend.

## Primary goals for AI coding agents

- Help developers build and maintain this repo using the existing architecture.
- Prefer `pnpm` and the repository scripts over ad hoc commands.
- Keep changes small and aligned with existing frontend/backend boundaries.
- Link to existing docs instead of duplicating them when possible.

## Build & development commands

Use these entry points for local work:

- `pnpm install`
- `pnpm dev` — start the local development server
- `pnpm build` — production build for frontend and backend bundle
- `pnpm start` — run the bundled production server
- `pnpm check` — type-check the repo with `tsc`
- `pnpm test` — run Vitest
- `pnpm format` — format code with Prettier
- `pnpm db:push` — generate and migrate Drizzle schema

> Always use `pnpm` unless the task explicitly requires another package manager.

## Key architecture

- `client/` — React 19 + Vite frontend.
- `server/` — Node backend using Express + tRPC.
- `shared/` — shared TypeScript types and utilities used by both client and server.
- `drizzle/` — Drizzle ORM schema, migrations, and SQL snapshots.
- `components.json` — UI component metadata (project-specific use).

### Important backend conventions

- The backend entry is `server/_core/index.ts`.
- tRPC routers are defined in `server/routers.ts`.
- Database access and agent log persistence are in `server/db.ts`.
- LLM analysis and integration code is in `server/llm-analysis.ts`.
- Authentication and session logic are in `server/_core/`.

### Important frontend conventions

- The app root is `client/src/App.tsx`.
- Routes use `wouter`.
- UI components and pages live under `client/src/components/` and `client/src/pages/`.
- Path aliases are configured for `@/*` → `client/src/*` and `@shared/*` → `shared/*`.

## Common development context

- This repo targets a local dev setup with `pnpm dev` and Docker-based MCP providers.
- Environment variable files include `.env.local.example` and `.env.local`.
- There are separate guides in `LOCAL_DEVELOPMENT_GUIDE.md`, `MCP_INTEGRATION_GUIDE.md`, and `README.md`.

## When editing code

- Preserve React/Vite styling patterns and Tailwind usage.
- Keep server code in `server/`; keep UI code in `client/`.
- Follow the existing tRPC and Drizzle ORM patterns for database queries and mutations.
- Prefer using shared types from `shared/` when touching both client and server.
- Avoid broad refactors unless they are clearly necessary for the task.

## Documentation links

- `README.md` — project overview, architecture, key features, quick start.
- `LOCAL_DEVELOPMENT_GUIDE.md` — local dev environment setup.
- `MCP_INTEGRATION_GUIDE.md` — MCP provider integration details.
- `SETUP.md` and `WINDOWS_QUICK_START.md` — additional setup guidance.

## Notes for AI agents

- Do not create an agent customization file if one already exists; update it instead.
- Prefer concise guidance and surface the relevant docs rather than copying large sections.
- Mention path aliases and `pnpm` explicitly to avoid incorrect tooling choices.
