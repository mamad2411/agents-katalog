---
name: contracts
description: Zod-as-contract pattern — one shared package holding schemas that serve as both compile-time types and runtime validation, imported by apps as types and by the API as schemas. Use when designing a request/response shape, adding a new endpoint, or wiring request validation middleware.
---

Apply the following pattern wherever a request/response shape crosses a process boundary (app ↔ API, API ↔ Inngest event).

## One schema, two uses

A shared package (e.g. `libs/contracts`) holds zod schemas as the single source of truth. Every schema exports the schema constant **and** the inferred type, declared right next to each other:

```ts
// libs/contracts/src/project.ts
import { z } from 'zod';

export const createProjectSchema = z.object({
  name: z.string().min(1).max(200),
  ownerId: z.string().uuid(),
  dueDate: z.string().datetime().optional(),
});
export type CreateProjectInput = z.infer<typeof createProjectSchema>;

export const projectSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  ownerId: z.string().uuid(),
  createdAt: z.string().datetime(),
});
export type Project = z.infer<typeof projectSchema>;
```

Never hand-roll a duplicate `interface Project { ... }` in an app — if the API's actual response shape and the app's hand-written type drift, TypeScript has no way to catch it because they were never the same declaration.

## Who imports what

- **Apps** (the frontend, or any consumer that only needs compile-time shape checking) import the **type**, with `import type` so it's erased at build time and never pulls zod into a bundle that doesn't need runtime validation:

  ```ts
  import type { Project, CreateProjectInput } from '@repo/contracts';
  ```

- **The API layer** imports the **schema** for runtime validation at the request boundary — `.parse()` when an invalid payload should throw, `.safeParse()` when the caller wants to handle the error itself:

  ```ts
  import { createProjectSchema } from '@repo/contracts';

  const input = createProjectSchema.parse(req.body); // throws ZodError on invalid input
  ```

The type has zero runtime cost and gives the app editor autocomplete + compile errors; the schema is the actual security boundary, because a client-side type only prevents *your own code* from sending the wrong shape — it does nothing to stop a malformed or malicious request from reaching the handler.

## Deriving a contract from reality, not an ideal design

When writing a contract for an endpoint that **already exists** (the common case when adding this pattern to an established codebase), pin the schema to what the handler actually accepts and returns today — not what it "should" accept in an idealized redesign. Read the current handler's body, note every field it reads off `req.body` and every field it puts in the response, and write the schema to match exactly. Then add a test that runs a known real payload through `schema.parse()` and asserts it passes:

```ts
it('accepts a real production-shaped payload', () => {
  const realPayload = { name: 'Acme Onboarding', ownerId: '...', dueDate: '2026-10-01T00:00:00Z' };
  expect(() => createProjectSchema.parse(realPayload)).not.toThrow();
});
```

Only once the contract is pinned to reality with that test in place should you evolve it — tighten a field, add a new optional one, deprecate another — changing the schema and the handler together in the same commit. Designing the "correct" abstract shape first and then discovering the real handler doesn't match it is how a contracts migration silently breaks production requests that were valid before.

## Validation middleware

A small reusable wrapper runs the right schema against each part of the request and short-circuits with a structured error on failure, so route handlers don't each hand-roll `try { schema.parse(...) } catch`:

```ts
// middleware/validateRequest.ts
import { ZodSchema } from 'zod';
import { Request, Response, NextFunction } from 'express';

type Schemas = { body?: ZodSchema; query?: ZodSchema; params?: ZodSchema };

export const validateRequest =
  ({ body, query, params }: Schemas) =>
  (req: Request, res: Response, next: NextFunction) => {
    const result = { body, query, params } as const;
    for (const [key, schema] of Object.entries(result)) {
      if (!schema) continue;
      const parsed = schema.safeParse((req as any)[key]);
      if (!parsed.success) {
        return res.status(422).json({ error: 'validation_failed', field: key, issues: parsed.error.issues });
      }
      (req as any)[key] = parsed.data;
    }
    next();
  };
```

```ts
router.post('/projects', requireAuth, validateRequest({ body: createProjectSchema }), handler);
```

422 (not 400) signals "well-formed request, invalid content" — pick one status convention for validation failures and use it everywhere so API consumers can branch on it reliably.
