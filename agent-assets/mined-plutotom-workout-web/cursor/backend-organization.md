---
description: Organize Convex backend schemas and routes by feature as the app grows
globs: backend/**/*
alwaysApply: false
---

# Backend organization (Convex)

Keep `backend/` scalable by splitting **schemas** and **routes** by domain. One top-level entry file for schema composition; feature folders for functions.

## Schemas

- Put table definitions in `backend/schemas/` — one file per domain (e.g. `users.ts`, `workouts.ts`, `sets.ts`).
- `backend/schema.ts` is the **only** file that calls `defineSchema`. Import and spread domain schemas there.

```ts
// backend/schemas/workouts.ts
import { defineTable } from "convex/server";
import { v } from "convex/values";

export const workoutTables = {
  workouts: defineTable({ /* ... */ }).index("by_user", ["userId"]),
};

// backend/schema.ts
import { defineSchema } from "convex/server";
import { workoutTables } from "./schemas/workouts";

export default defineSchema({
  ...workoutTables,
});
```

Add a new domain → new file under `schemas/`, then wire it in `schema.ts`. Do not define tables directly in `schema.ts` once a domain file exists.

## Routes (queries, mutations, actions)

- Put Convex functions in `backend/routes/`, grouped by feature.
- One folder (or file) per area: `auth/`, `workouts/`, `templates/`, etc.
- Name files by what they expose (`queries.ts`, `mutations.ts`) or by resource (`sessions.ts`) — stay consistent within a folder.

```
backend/
  schema.ts
  auth.config.ts
  schemas/
    users.ts
    workouts.ts
  routes/
    auth/
      users.ts
    templates/
      hello.ts
    workouts/
      queries.ts
      mutations.ts
```

Convex API paths follow the file path (e.g. `routes/templates/hello:getMessage`). Prefer **feature folders** over a flat pile of files at `backend/` root.

## When adding features

1. Schema needed? → `schemas/<domain>.ts`, then register in `schema.ts`.
2. New API surface? → `routes/<feature>/` (new file or folder), not a loose file at `backend/` root.
3. Keep cross-cutting config (`auth.config.ts`, `http.ts`, `convex.config.ts`) at `backend/` root.

## Avoid

- Monolithic `schema.ts` with every table inline.
- Many unrelated queries/mutations in one giant file.
- New top-level `backend/*.ts` function files when a feature folder fits.
