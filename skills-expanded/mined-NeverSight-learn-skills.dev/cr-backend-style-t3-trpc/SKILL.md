---
name: cr-backend-style-t3-trpc
description: Backend style for create-t3-app and tRPC projects. Use when creating or refactoring routers, procedures, zod schemas, and router-local backend utilities.
---

# Backend Style: T3 + tRPC

Use these defaults unless the project already has stronger backend conventions.

## Philosophy

- Favor the simple, practical structure common in create-t3-app projects.
- Keep router boundaries aligned with domains, entities, or clear backend features.
- Treat tRPC routers as domain boundaries.
- Use routers to keep entity or feature separation clear.
- Keep backend code boring, explicit, and easy to navigate.
- Prefer small files with clear responsibilities over dumping everything into one router file.

## Router File Structure

For non-trivial routers, prefer this structure:

- `index.ts` — compose and export the router
- `queries.ts` — read procedures
- `mutations.ts` — write procedures
- `schemas.ts` — zod schemas and shared input/output validators
- `utils.ts` — router-specific backend helpers when needed

Keep these files colocated in a router directory.

## Responsibilities

### `index.ts`

- Keep it tiny.
- Import `queries` and `mutations`.
- Export a router composed from those modules.
- Do not place business logic here.

### `queries.ts`

- Put read-only procedures here.
- Keep query handlers direct and easy to scan.
- Validate inputs with schemas imported from `schemas.ts`.
- Throw explicit `TRPCError`s for expected failure cases.

### `mutations.ts`

- Put write procedures here.
- Keep mutation handlers explicit about validation, authorization, persistence, and returned data.
- Use router-local utils when they remove meaningful complexity.
- Avoid hiding the main mutation flow behind too much indirection.

### `schemas.ts`

- Keep zod schemas separate from server logic.
- Put input and shared validation schemas here.
- This file should be safe to import on the frontend when client-side validation is useful.
- Do not leak server-only logic into schemas.
- Prefer named schemas for common inputs such as IDs, filters, payloads, and enums.

### `utils.ts`

- Use for router-specific helper logic only.
- Good candidates:
  - authorization helpers tied to the router domain,
  - entity-specific validation,
  - persistence helpers used by multiple procedures,
  - path or key builders tied to the router domain.
- Do not turn `utils.ts` into a generic dumping ground.
- If logic is used outside the router domain, move it to a more appropriate shared backend location.

## Procedure Style

- Prefer explicit `protectedProcedure`, `adminProcedure`, or other project-standard procedure wrappers.
- Validate inputs early and fail clearly.
- Keep procedure names literal, such as `getFile`, `listFiles`, `getUploadUrl`, `confirmFileUpload`, `deleteFileById`.
- Keep the happy path readable top-to-bottom.
- Destructure input near the top when it improves readability.
- Validate early.
- Throw clear `TRPCError`s for expected failures.
- Return plain, unsurprising shapes.

## Domain Separation

- Group procedures by domain, entity, or feature rather than by HTTP-style thinking.
- It is fine for a router to represent an entity-like boundary, but routers can also represent other clear backend domains.
- Keep related schemas, procedures, and helpers together so the domain is easy to understand.

## Abstraction Rules

- Avoid over-abstracting simple queries and mutations.
- Extract utils when logic is reused or meaningfully simplifies the procedure.
- Keep business flow visible in procedures unless the extracted helper clearly improves readability.
- Prefer router-local helpers over cross-backend abstractions when the logic is domain-specific.

## Examples

### Prefer small router composition in `index.ts`

```ts
import { createTRPCRouter } from '../../trpc';
import * as mutations from './mutations';
import * as queries from './queries';

export const filesRouter = createTRPCRouter({
  ...queries,
  ...mutations,
});
```

### Prefer schemas in a separate shared file

```ts
export const FileIdSchema = z.object({
  id: z.string(),
});

export const ListFilesSchema = z.object({
  userId: z.string().optional(),
  artistPageId: z.string().optional(),
  postId: z.string().optional(),
  purpose: FilePurposeSchema.optional(),
});
```

### Prefer direct procedures with visible flow

```ts
export const getFile = adminProcedure.input(FileIdSchema).query(async ({ ctx, input }) => {
  const file = await ctx.db.file.findUnique({
    where: { id: input.id },
  });

  if (!file) {
    throw new TRPCError({
      code: 'NOT_FOUND',
      message: 'File not found',
    });
  }

  return file;
});
```

### Prefer router-local utils for domain-specific logic

```ts
export const deleteFile = async ({ ctx, file }: { ctx: ProtectedTRPCContextType; file: File }) => {
  const authorizedToDelete =
    ctx.session.roles.includes('admin') || file.uploadedById === ctx.session.user_id;

  if (!authorizedToDelete) {
    throw new TRPCError({
      code: 'UNAUTHORIZED',
      message: '[FILES] You do not have permission to delete this file',
    });
  }

  await ctx.s3.deleteFile(file.path);
  return ctx.db.file.delete({ where: { id: file.id } });
};
```

### Avoid mixing everything into one oversized router file

```ts
// Avoid putting schemas, queries, mutations, and router-specific helpers
// in a single giant file once the router grows past something trivial.
```

## Output Checklist

Before finishing, check:

- Is the router split by responsibility when it is non-trivial?
- Are schemas separated from server-only logic?
- Are queries and mutations easy to find?
- Is domain-specific logic kept close to the router?
- Did I avoid unnecessary backend-wide abstractions?
- Is the procedure flow explicit and easy to scan?
