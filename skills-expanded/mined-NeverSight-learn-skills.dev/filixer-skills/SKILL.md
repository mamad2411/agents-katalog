---
name: filixer-skills
description: Use when building fullstack features or setting up architecture with React 19, TanStack Start/Router/Query, Shadcn UI, Drizzle ORM, better-auth, or oRPC. Applies to route creation, database schema design, auth rules, API endpoints, and component standards.
---

Fullstack development skill for projects built with **React 19 + TypeScript**, **TanStack Start** (full-stack framework), **TanStack Router** (file-based routing), **TanStack Query** (server state management), **Shadcn UI** (components), **Drizzle ORM** (database), **better-auth** (authentication), and **oRPC** (type-safe API layer).

---

## 1. Non-Negotiable Code Rules

All code generated for this project MUST strictly follow these rules:

### Type Safety & Schema Inference
- **Explicit Type Annotations**: Annotate function parameters, return types, component props, and custom states. Never use `any`; prefer `unknown` when a type is genuinely unknown.
- **Infer from Schemas**: Use `z.infer<typeof schema>` and Drizzle's `typeof table.$inferSelect` / `typeof table.$inferInsert` instead of duplicating types manually.
- **Narrow Literals**: Use `satisfies` for type-checking object literals while preserving their narrow type, and `as const` for non-widening literal objects/tuples.

### ES6 Arrow Functions Only
- **No `function` Declarations**: Always use ES6 arrow functions for components, handlers, callbacks, server functions, and helper functions.
  ```tsx
  export const MyComponent = ({ title }: { title: string }): React.ReactNode => { ... }
  export const calculateTotal = (items: Item[]): number => { ... }
  ```

### Memoization (React Compiler First)
- **Rely on React 19 Compiler**: Do NOT add `useMemo`, `useCallback`, or `React.memo` by default.
- **Measure Before Adding**: Only add manual memoization if React DevTools profiling identifies a verified bottleneck. Document the rationale with a code comment.

### Feature-Based Organization
- **Thin Route Files**: Route files in `src/routes/` should ONLY handle routing, loaders, search params validation, and page assembly.
- **Domain Logic in `src/features/`**: Place feature-specific UI components, forms, hooks, and helpers inside `src/features/<feature_name>/`.
- **Reusable Primitives in `src/components/ui/`**: Place pure, generic UI components (Buttons, Inputs, Cards) in `src/components/ui/`.

### Clean Code & Workflow Efficiency
- **Clean Code First (No Redundant Typechecks/Builds)**: Do NOT run `typecheck` (e.g. `tsc`), `npm run build`, or build scripts after completing every small code snippet or incremental modification. Focus first on writing clean, well-structured, readable, and maintainable code. Run typecheck or build commands only at major feature milestones or when explicitly requested.

---

## 2. Recommended Directory Structure

```
src/
├── routes/                     # TanStack Router file-system routes
│   ├── __root.tsx             # Root document, global providers, navbar
│   ├── index.tsx              # Home page ("/")
│   ├── _authed.tsx            # Protected layout guard
│   ├── _authed/
│   │   ├── dashboard.tsx      # Protected dashboard ("/dashboard")
│   │   └── settings.tsx       # Protected settings ("/settings")
│   ├── login.tsx              # Public login route ("/login")
│   └── api/
│       └── auth/
│           └── $.tsx          # better-auth catch-all API handler
├── features/                  # Domain-driven feature modules
│   ├── auth/                  # Login / Register forms & components
│   ├── dashboard/             # Dashboard cards, charts, widgets
│   └── posts/                 # Post lists, detail views, form dialogs
├── server/                    # Server-only backend code
│   ├── db/
│   │   ├── index.ts           # Drizzle ORM client instance
│   │   ├── schema.ts          # PostgreSQL database schema & relations
│   │   └── seed.ts            # Database seeding script
│   ├── auth.ts                # better-auth server configuration
│   └── orpc.ts                # oRPC routers & procedure definitions
├── lib/                       # Shared client utilities & SDKs
│   ├── auth-client.ts         # better-auth client instance
│   ├── orpc.ts                # oRPC client & TanStack Query helpers
│   └── utils.ts               # cn() helper and formatting utilities
├── components/                # UI components
│   ├── ui/                    # Shadcn UI primitives (Button, Input, Card...)
│   └── theme-provider.tsx     # Theme (Dark/Light) context provider
├── env.ts                     # Zod-validated environment variables
├── router.tsx                 # TanStack Router instance creation
├── routeTree.gen.ts           # Auto-generated route tree (DO NOT EDIT)
└── styles.css                 # Global CSS and Tailwind directives
drizzle/                       # Generated SQL migration files
drizzle.config.ts              # Drizzle Kit migration configuration
vite.config.ts                 # Vite + TanStack Start plugin config
```

---

## 3. Core Configuration & Bootstrap

### Type-Safe Environment Variables (`src/env.ts`)

```ts
import { z } from "zod"

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  BETTER_AUTH_SECRET: z.string().min(1),
  VITE_APP_URL: z.string().url().default("http://localhost:3000"),
})

export const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET,
  VITE_APP_URL: import.meta.env.VITE_APP_URL,
})
```

### Vite Setup (`vite.config.ts`)

```ts
import { defineConfig } from "vite"
import { tanstackStart } from "@tanstack/react-start/plugin/vite"
import viteReact from "@vitejs/plugin-react"

export default defineConfig({
  server: {
    port: 3000,
  },
  resolve: {
    tsconfigPaths: true,
  },
  plugins: [
    tanstackStart(),
    viteReact(), // must come AFTER tanstackStart()
  ],
})
```

### Router Instance (`src/router.tsx`)

```ts
import { createRouter as createTanStackRouter } from "@tanstack/react-router"
import { QueryClient } from "@tanstack/react-query"
import { routeTree } from "./routeTree.gen"

export const createRouter = (): ReturnType<typeof createTanStackRouter> => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutes default stale time
      },
    },
  })

  return createTanStackRouter({
    routeTree,
    defaultPreload: "intent",
    context: { queryClient },
  })
}

declare module "@tanstack/react-router" {
  interface Register {
    router: ReturnType<typeof createRouter>
  }
}
```

### Root Document & Providers (`src/routes/__root.tsx`)

```tsx
import {
  Outlet,
  ScrollRestoration,
  createRootRouteWithContext,
} from "@tanstack/react-router"
import { Meta, Scripts } from "@tanstack/react-start"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Toaster } from "@/components/ui/sonner"

export const Route = createRootRouteWithContext<{
  queryClient: QueryClient
}>()({
  component: (): React.ReactNode => (
    <html lang="en">
      <head>
        <Meta />
      </head>
      <body className="min-h-screen bg-background text-foreground antialiased">
        <Outlet />
        <Toaster />
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  ),
})
```

---

## 4. End-to-End Development Lifecycle Pattern

When implementing any end-to-end feature (e.g. "Posts"), follow this exact sequence:

```
┌──────────────────────────┐      ┌──────────────────────────┐
│ 1. Define Drizzle Schema │ ───► │ 2. Create oRPC Procedure │
│    (src/server/db/schema)│      │    (src/server/orpc.ts)  │
└──────────────────────────┘      └──────────────────────────┘
                                                │
                                                ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ 4. Build UI Component    │ ◄─── │ 3. Prefetch in Loader    │
│    (src/features/posts/) │      │    (src/routes/posts.tsx)│
└──────────────────────────┘      └──────────────────────────┘
```

1. **Database Schema**: Add table definition in `src/server/db/schema.ts` and generate migration (`npx drizzle-kit generate`).
2. **oRPC Procedure**: Define typed input/output procedure in `src/server/orpc.ts` with Zod validation.
3. **Route & Loader**: In `src/routes/posts/$postId.tsx`, define search params schema, and prefetch query data in `loader` using `queryClient.ensureQueryData(orpc.posts.find.queryOptions(...))`.
4. **Feature Component**: In `src/features/posts/post-detail.tsx`, consume data using `useQuery(orpc.posts.find.queryOptions(...))` and render with Shadcn UI components.

---

## 5. Detailed Reference Guides

Refer to these specialized documents in `references/` for deep dive implementation guidelines:

- 📖 **[TanStack Router & Start Guide](references/tanstack-router-start.md)**  
  File routing conventions, `validateSearch` with Zod, loader prefetching, protected routes, pending UI skeletons, error boundaries, server functions (`createServerFn`), and dynamic SEO head tags.

- 📖 **[oRPC Patterns & Best Practices Guide](references/orpc-patterns.md)**  
  Defining procedures, auth & RBAC middleware composition, typed error handling (`ORPCError`), `@orpc/tanstack-query` client setup, mutation invalidation patterns, and toast notifications integration.

- 📖 **[Drizzle ORM Recipes Guide](references/drizzle-recipes.md)**  
  Schema creation, PK/FK constraints, pgEnum, relations, index setup, client initialization, relational queries, upserts, database transactions (`db.transaction`), and database seeding scripts (`seed.ts`).

- 📖 **[better-auth Integration Guide](references/better-auth-guide.md)**  
  Server config with Drizzle adapter, `tanstackStartCookies()` setup, client `authClient`, server session helpers (`getServerSession`), social OAuth providers (Google, GitHub), catch-all route handler, and protected layout guard.

- 📖 **[Shadcn UI & Forms Reference Guide](references/shadcn-forms-ui.md)**  
  React Hook Form + Zod form validation, Shadcn `<Form />` wrappers, Sonner toast alerts, dark mode theme provider setup, dynamic data tables, and modal dialogs controlled via URL search params.

- 📖 **[Testing & Quality Assurance Guide](references/testing-guide.md)**  
  Vitest component testing, React Testing Library, direct oRPC procedure testing, and Playwright E2E specs for login & route guards.

- 📖 **[File Upload & Cloud Storage Guide](references/file-upload-storage.md)**  
  Presigned URL pattern (S3/R2), Zod metadata validation, direct browser PUT upload, and upload progress bar UI component.

- 📖 **[Production Deployment & Docker Guide](references/deployment-docker.md)**  
  Multi-stage Dockerfile for TanStack Start, safe database migration strategy with Drizzle Kit, GitHub Actions CI/CD pipeline, and Pino structured logging.

- 📖 **[Feature Module Pattern](references/feature-module-pattern.md)**  
  Standard directory structure, Context-driven state management, action/current flow, query/mutation placement rules, and step-by-step checklist for building any `src/features/<name>/` module.

- 📖 **[Streaming & Server-Sent Events Guide](references/realtime-sse.md)**  
  Non-blocking deferred route data loading with `defer()` and React 19 `<Suspense>`, Server-Sent Events (SSE) route handlers, and custom `useEventStream` hook.

---

## 6. Library Documentation (llms.txt)

Bundled `llms.txt` from each core library for quick API reference. Fetch from source URLs for the latest version.

| Library | Local | Source |
| :--- | :--- | :--- |
| oRPC | [llms/orpc.txt](llms/orpc.txt) | https://orpc.dev/llms.txt |
| TanStack Router | [llms/tanstack-router.txt](llms/tanstack-router.txt) | https://tanstack.com/router/latest/llms.txt |
| TanStack Query | [llms/tanstack-query.txt](llms/tanstack-query.txt) | https://tanstack.com/query/latest/llms.txt |
| TanStack Start | [llms/tanstack-start.txt](llms/tanstack-start.txt) | https://tanstack.com/start/latest/llms.txt |
| Drizzle ORM | [llms/drizzle.txt](llms/drizzle.txt) | https://orm.drizzle.team/llms.txt |
| better-auth | [llms/better-auth.txt](llms/better-auth.txt) | https://better-auth.com/llms.txt |
| Shadcn UI | [llms/shadcn-ui.txt](llms/shadcn-ui.txt) | https://ui.shadcn.com/llms.txt |

---

## 7. Essential CLI Commands

```bash
# Development Server
npm run dev                  # Start TanStack Start dev server

# Database Operations (Drizzle Kit)
npx drizzle-kit generate     # Generate migration files from schema changes
npx drizzle-kit migrate      # Apply pending migrations to PostgreSQL
npx drizzle-kit push         # Push schema changes directly to DB (dev only)
npx drizzle-kit studio       # Launch interactive Drizzle Studio database GUI
npx tsx src/server/db/seed.ts # Run database seed script

# Authentication
npx @better-auth/cli generate --config src/server/auth.ts # Generate better-auth database schema

# UI Components (Shadcn CLI)
npx shadcn@latest add button card input form dialog toast table # Add UI components

# Code Quality & Build
npm run typecheck            # Run tsc --noEmit check
npm run build                # Create production bundle
```
