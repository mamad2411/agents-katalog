# AGENTS.md — services/web

> **AI Primer:** Read this file completely before writing, editing, or scaffolding any code in this service.
> Check `../../docs/TASKS/02_Task_List` for tasks.
> This file is your complete context for the Next.js frontend service.

> ⚠️ **This is NOT the Next.js you know.** This app runs Next.js **16.2.0** (app router on `src/app`) with React **19**.
> APIs, conventions, and file structure may differ from your training data.
> Read `node_modules/next/dist/docs/` before touching any framework-specific behavior.

---

## Service Overview

| Concern         | Technology                                       |
| --------------- | ------------------------------------------------ |
| Framework       | Next.js 16.2.0 — App Router                      |
| Language        | TypeScript 5                                     |
| Runtime         | React 19.2.4                                     |
| Package Manager | Bun                                              |
| Styling         | Tailwind CSS 4 + shadcn/ui (radix-ui)            |
| Data Fetching   | TanStack Query v5 (REST via `src/lib/api.ts`)    |
| Forms           | TanStack Form v1                                 |
| Tables          | TanStack Table v8                                |
| State           | Zustand v5                                       |
| Validation      | Zod v4                                           |
| Linting/Format  | Biome 2.2.0                                      |
| Real-time       | WebSocket via `src/lib/websocket-provider.tsx`   |
| Backend         | Go Core API proxied via Next.js `/api/*` rewrite |
| Deployment      | Docker Compose (standalone output)               |

---

## Package Structure

```
services/web/
├── src/
│   ├── app/                         ← Next.js App Router root
│   │   ├── layout.tsx               ← root layout
│   │   ├── globals.css              ← global Tailwind styles
│   │   ├── (dashboard)/             ← route group: dashboard layout + pages
│   │   │   ├── layout.tsx           ← shared dashboard layout (sidebar, etc.)
│   │   │   ├── page.tsx             ← dashboard home
│   │   │   ├── orchestrator/        ← /orchestrator pages
│   │   │   └── projects/            ← /projects pages
│   ├── components/                  ← shared shadcn/ui + custom components
│   ├── features/                    ← feature modules (one folder per domain)
│   │   ├── agents/
│   │   ├── execution/
│   │   ├── file_system/
│   │   ├── milestone/
│   │   ├── orchestrator/
│   │   ├── pipeline/
│   │   ├── project/
│   │   ├── sidebar/
│   │   ├── task/
│   │   └── workflow/
│   ├── hooks/                       ← global React hooks
│   ├── lib/
│   │   ├── api.ts                   ← central REST fetch wrapper (use this always)
│   │   ├── websocket-provider.tsx   ← WebSocket context + provider
│   │   └── utils.ts                 ← cn() and misc utilities
│   └── trpc/                        ← scaffold only — NOT the main data path
├── next.config.ts                   ← rewrites /api/* → NEXT_BACKEND_URL
├── biome.json                       ← lint + format config
├── components.json                  ← shadcn/ui config
└── tsconfig.json                    ← path alias: @/ → src/
```

---

## Commands

```bash
cd services/web

bun install      # install dependencies
bun dev          # start dev server (port 3000)
bun build        # production build (standalone output)
bun start        # start production server
bun lint         # Biome check
bun format       # Biome format --write
```

---

## Feature Module Layout

Every domain under `src/features/` follows this exact shape. New features **must** match:

```
features/[entity]/
├── api/          ← apiFetch() calls to the Go backend
├── components/   ← feature-specific React components
├── hooks/        ← TanStack Query hooks (useQuery, useMutation, suspense variants)
├── schema/       ← Zod schemas for forms and validation
└── views/        ← page-level view components (consumed by app/ pages)
```

---

## API Client — `src/lib/api.ts`

- Server-side: uses `NEXT_BACKEND_URL` env var (internal Docker network).
- Client-side: uses `/api` (same-origin proxy rewrite in `next.config.ts`).
- Always import and use `apiFetch<T>()` — never scatter raw `fetch` in components or pages.

```typescript
import { apiFetch } from "@/lib/api";
const data = await apiFetch<Project[]>("/project");
```

---

## Environment Variables

| Variable              | Description                            | Default / Example       |
| --------------------- | -------------------------------------- | ----------------------- |
| `NEXT_BACKEND_URL`    | Internal URL of the Go Core API (SSR)  | `http://core:8080`      |
| `NEXT_PUBLIC_API_URL` | Public-facing API URL prefix (browser) | `/api`                  |
| `NEXT_APP_URL`        | Public URL of this Next.js app         | `http://localhost:3000` |

---

## Key Conventions

- **Path alias:** `@/` maps to `src/`. Always use it — no relative `../../` imports.
- **tRPC is scaffold only.** `src/trpc/` exists but is not the main data path. Do not route new features through tRPC.
- **Auth is not implemented.** `wsToken` in `providers.tsx` is `undefined`. Some queries may use hardcoded IDs. Treat as current behavior.
- **Biome, not ESLint.** Run `bun lint` and `bun format` — do not add ESLint or Prettier config.
- **shadcn/ui components** live in `src/components/ui/`. Add new ones with `bunx shadcn add <component>`.
- **Next.js 16 + React 19.** Do not assume older App Router conventions. Check `node_modules/next/dist/docs/` for current APIs.

---

## What NOT to Do

- Do NOT use raw `fetch` in page components or views — always go through `src/lib/api.ts`.
- Do NOT use the `src/trpc/` tree as the primary data integration path.
- Do NOT add ESLint, Prettier, or other linters — Biome is the only one.
- Do NOT assume Next.js 13/14/15 App Router conventions — this is 16.2.0 with React 19.
- Do NOT hand-edit `src/components/ui/` files generated by shadcn — re-generate instead.
- Do NOT implement auth logic until the backend middleware is enabled.
