---
description: Project map — where things live and "Where do I put X?" (TIMER).
globs: "**/*.ts, **/*.tsx"
alwaysApply: false
---

## Quick orientation

- **Runtime**: Next.js App Router (`app/`)
- **UI**: Tailwind + shadcn (`components/ui/`)
- **Data**: React Query hooks (`hooks/`) → API routes (`app/api/`) → server actions (`actions/`) → Prisma (`prisma/`)
- **Auth**: Clerk (`middleware.ts`, `lib/clerk.ts`, `actions/auth/*`)
- **DB**: PostgreSQL via Prisma (`prisma/schema.prisma`)

## Folder-by-folder

- **app/** — Next.js routes, layouts, route-level UI. Key: `layout.tsx` (providers, toasts), `page.tsx`, `app/*` (in-app routes), `api/*` (thin controllers calling actions).
- **components/** — Feature-first; see rule 110 for taxonomy. **components/ui/** — design system only (shadcn/Radix), no feature logic.
- **actions/** — Server actions (`"use server"`) for DB and business logic. Auth/ownership via `actions/auth/authCheck.ts`.
- **hooks/** — Client hooks (React Query, state). Key: `use-timers.ts`, `use-timer-state.ts`, `timers/use-flattened-intervals.ts`, `timers/use-advanced-timer-playback.ts`.
- **lib/** — App/feature infrastructure (constants, navigation, timer-tree, sound). Tree logic in `lib/timer-tree/`. Constants in `lib/constants/*`.
- **schema/** — Zod schemas for API/form boundaries only.
- **types/** — Domain types, const enums, type guards, `*.d.ts`. No business logic, no React, no Zod.
- **utils/** — Pure, framework-agnostic helpers. No React, no app/lib imports. Examples: `compute-total-time`, `format-time`, `time-input`.
- **prisma/** — Schema, migrations, DB helpers, DB tests.

## Where do I put X?

- New route/page → `app/.../page.tsx`
- Feature component → `components/<feature>/...`
- Reusable UI primitive → `components/ui/...`
- Client data hook → `hooks/...` (prefer React Query for server data)
- Server-side business logic → `actions/...`
- API boundary → `app/api/.../route.ts` (thin, call actions)
- Constants → `lib/constants/...`
- Pure utilities → `utils/...`; app/feature glue → `lib/...`
- Domain types / type guards → `types/...`
- Validation schemas → `schema/...`

**Rule**: Components are UI only. Pure domain or tree logic goes in `lib/` or `utils/`, not under `components/`.
