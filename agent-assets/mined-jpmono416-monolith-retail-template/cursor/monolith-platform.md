---
description: Monolith platform index — stack overview and rule map
alwaysApply: true
---

# Monolith AI-Native Engineering Platform

Monorepo template for the Monolith platform. This file is the entry point — read the topic rule below before changing code in its area.

## Stack

| Layer | Technology |
|-------|------------|
| Monorepo | Turborepo + pnpm workspaces |
| Web | Next.js 15, React 19, Tailwind 4, shadcn/ui (`@monolith/ui`) |
| API | NestJS 11, Prisma, PostgreSQL |
| Cache/queues | Redis, BullMQ |
| Mobile | Expo (`apps/mobile`) |
| Tests | Vitest, Playwright |
| Local | Docker Compose (`postgres`, `redis`, optional `api`/`web`) |
| Deploy | Vercel (web), Railway (api), Supabase (db), Upstash (redis) |

## Rule map (canonical owners)

Every concern has one canonical rule file. Other rules reference it instead of duplicating.

| Rule | Owns | Globs |
|------|------|-------|
| `agent-behaviour.mdc` | AI workflow, scope discipline, output quality | always |
| `architecture.mdc` | Repo layout, layer boundaries, dependency direction | `apps/**`, `packages/**`, `prisma/**` |
| `backend.mdc` | Nest/Prisma/queue implementation, env wiring | `apps/api/**`, `prisma/**` |
| `frontend.mdc` | Next/Tailwind/shadcn implementation | `apps/web/**`, `packages/ui/**` |
| `api-design.mdc` | HTTP contracts, DTOs, response shapes | `apps/api/**`, `packages/types/**` |
| `naming.mdc` | File, symbol, env, DB, route casing | `**/*` |
| `monorepo.mdc` | pnpm workspace, Turbo tasks, Node/pnpm toolchain | workspace files |
| `testing.mdc` | What to test, how to test it | test files |
| `docker.mdc` | Local Compose, Dockerfiles | compose + dockerfiles |
| `infra.mdc` | CI, deploy, env-var registration across platforms | `.github/**`, `infrastructure/**` |
| `security.mdc` | Secrets, auth, validation policy | `apps/**`, `packages/**`, `.env.example` |

For overlap resolution and how to interpret cross-references, see [`docs/architecture/rule-system-overview.md`](../../docs/architecture/rule-system-overview.md).

## Key paths

```
apps/api/src/features/     # Feature folders
apps/api/src/infrastructure/
apps/web/src/app/          # Next.js App Router
packages/types/            # API contracts
prisma/schema.prisma
infrastructure/docker/
.github/workflows/ci.yml
```
