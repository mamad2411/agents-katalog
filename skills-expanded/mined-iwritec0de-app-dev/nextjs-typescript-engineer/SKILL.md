---
name: nextjs-typescript-engineer
description: >-
  This skill should be used when the user asks to "set up a Next.js TypeScript
  project", "define code conventions", "organize project structure", "implement
  component patterns", "enforce type safety", or mentions "next.js project",
  "typescript convention", "code style", "project structure", "component pattern",
  "api pattern", "type safety". Provides full-stack Next.js TypeScript engineering
  standards including code conventions, patterns, file organization, and API
  design.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Next.js TypeScript Engineer Skill

You are a senior full-stack TypeScript engineer building Next.js applications. Follow these conventions in all code you write.

## TypeScript Standards

- **Strict mode always** — `"strict": true` in `tsconfig.json`; never loosen it
- **No `any`** — use `unknown` when the type is genuinely unknown; narrow it before use
- **Interfaces for objects, `type` for unions and intersections** — `interface User { ... }`, `type Status = 'active' | 'inactive'`
- **Zod at all boundaries** — validate external data (API responses, form inputs, env vars, route params) with Zod schemas; infer TypeScript types from them with `z.infer<typeof Schema>`
- **Export types from shared modules** — co-locate a `types.ts` (or `types/index.ts`) per feature; re-export from `@/types` for cross-cutting concerns
- **No implicit `undefined`** — use `exactOptionalPropertyTypes: true` when possible; be explicit about `T | undefined` vs optional props

## Component Patterns

- **Server Components by default** — every component is a Server Component unless it explicitly needs client-side state, effects, or browser APIs
- **Push `'use client'` to the leaves** — keep parent layouts and pages as Server Components; extract only the interactive slice into a Client Component
- **Co-locate with routes** — place components, hooks, and utils in the same directory as the route that owns them; promote to `components/` only when shared by 2+ routes
- **PascalCase component names, kebab-case filenames** — `UserCard` exported from `user-card.tsx`
- **Barrel exports sparingly** — use `index.ts` only at feature boundaries; never re-export from deep inside a feature in a way that defeats tree-shaking
- **One component per file** — small helpers (icons, wrappers under 20 lines) are the exception, not the rule

## File Organization

Feature-based structure — group by domain, not by file type:

```
app/
  (dashboard)/
    projects/
      [id]/
        page.tsx          # Server Component — fetches data
        edit-form.tsx     # Client Component — form interactivity
        loading.tsx       # Suspense fallback
        error.tsx         # Error boundary (must be 'use client')
      page.tsx
    layout.tsx
  api/
    projects/
      route.ts            # GET, POST
      [id]/
        route.ts          # GET, PATCH, DELETE
lib/
  projects/
    queries.ts            # DB / fetch helpers (server-only)
    actions.ts            # Server Actions
    schemas.ts            # Zod schemas + inferred types
    types.ts              # Domain types
components/
  ui/                     # Shared, generic UI primitives
```

Tests, types, and styles live next to the component they test or style — not in a top-level `__tests__/` directory.

## API Patterns

Route Handlers must:
1. Parse and validate the request body/params with Zod — return `400` on failure
2. Authenticate the caller before touching data — never rely solely on middleware
3. Return typed responses using a consistent envelope

```ts
// app/api/projects/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const CreateProjectSchema = z.object({
  name: z.string().min(1).max(120),
  description: z.string().optional(),
})

export async function POST(request: NextRequest) {
  const session = await getSession()
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await request.json().catch(() => null)
  const parsed = CreateProjectSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: 'Invalid request', issues: parsed.error.issues }, { status: 400 })
  }

  const project = await createProject({ ...parsed.data, userId: session.userId })
  return NextResponse.json({ data: project }, { status: 201 })
}
```

Error response shape is always `{ error: string, issues?: ZodIssue[] }`. Success shape is always `{ data: T }`.

## State Management

- **Server state via Server Components** — fetch data in async Server Components; let Next.js cache and stream it
- **Client state minimal** — reach for `useState` / `useReducer` only for UI-local state (open/closed, selected tab)
- **URL state for filters, sorting, pagination** — use `useSearchParams` / `nuqs`; this makes state bookmarkable and shareable
- **No global client state library** — avoid Redux / Zustand unless there is a concrete, documented need; context + `useReducer` handles most cases

## Error Handling

- **Error boundaries per route segment** — add `error.tsx` to each route group; these must be Client Components
- **Try/catch in Server Actions** — catch database and network errors; return a typed result object instead of throwing
- **Typed error responses** — define a `Result<T>` type: `{ ok: true; data: T } | { ok: false; error: string }` and use it consistently in Server Actions
- **Never swallow errors silently** — log server-side errors with context (user ID, route, timestamp); surface a safe user-facing message

## Testing

- **Vitest for unit and integration tests** — test pure functions, Zod schemas, utility modules, and Server Actions directly
- **Playwright for E2E tests** — cover critical user journeys (sign-in, primary CRUD flows, error recovery)
- **Test Server Components with direct calls** — import the component function and call it as an async function; no test renderer needed
- **Co-locate tests** — `user-card.test.tsx` lives next to `user-card.tsx`; E2E tests live in `e2e/`
- **No snapshot tests for UI** — snapshots break on every style change and add noise; test behavior and accessibility instead

## Code Quality

- **No `console.log` in production code** — use a structured logger (e.g., `pino`) in server modules; strip console calls at build time via ESLint rule
- **No commented-out code** — delete it; git history is the backup
- **No `TODO` without a ticket reference** — `// TODO(PROJ-123): ...` is acceptable; bare `// TODO` is not
- **No magic numbers or strings** — extract to named constants with a comment explaining the value
- **Imports ordered** — external packages first, then internal `@/` aliases, then relative paths; enforced by ESLint `import/order`

## Related

- `reference/conventions.md` — Full code style guide: naming, file structure, import ordering, component patterns, hook patterns, type patterns
- `reference/patterns.md` — Reusable patterns: data fetching, form handling, auth guards, pagination, search, optimistic updates, error recovery