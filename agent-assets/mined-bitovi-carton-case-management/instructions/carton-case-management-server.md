---
applyTo: packages/server/**
---

<!--
  GENERATED FILE - DO NOT EDIT.

  Edit the source CLAUDE.md instead, then run:  npm run sync:agent-docs
  Source of truth for this file: packages/server/CLAUDE.md
-->

# @carton/server Package Instructions

This package contains the Express/tRPC backend server.

## Package Purpose

- **tRPC Router**: API endpoint definitions with type inference
- **Database Operations**: All Prisma queries and mutations
- **Business Logic**: Server-side validation and processing
- **Authentication**: User session and auth middleware

## Directory Structure

```
packages/server/
├── src/
│   ├── index.ts           # Express server setup, exports AppRouter
│   ├── router.ts          # tRPC router definitions
│   ├── trpc.ts            # tRPC initialization and procedures
│   ├── context.ts         # Request context (Prisma, user)
│   └── middleware/        # Express middleware
│       └── autoLogin.ts
├── db/
│   ├── dev.db             # SQLite database file (gitignored, created by db:push)
│   ├── seed.ts            # Database seeding script
│   └── constants.ts       # Seed data constants
├── package.json
└── tsconfig.json
```

## Key Exports

### From `@carton/server`
```typescript
export type { AppRouter } from './router.js';
```

The `AppRouter` type is the key export - it enables end-to-end type safety with the client.

## Creating tRPC Procedures

### Basic Query
```typescript
import { z } from 'zod';
import { router, publicProcedure } from './trpc.js';

export const appRouter = router({
  entity: router({
    list: publicProcedure.query(async ({ ctx }) => {
      return ctx.prisma.entity.findMany();
    }),
    
    getById: publicProcedure
      .input(z.object({ id: z.string() }))
      .query(async ({ ctx, input }) => {
        return ctx.prisma.entity.findUnique({
          where: { id: input.id },
        });
      }),
  }),
});
```

### Mutation with Auth Check
```typescript
create: publicProcedure
  .input(z.object({
    title: z.string().min(1),
    description: z.string().min(1),
  }))
  .mutation(async ({ ctx, input }) => {
    if (!ctx.userId) {
      throw new TRPCError({
        code: 'UNAUTHORIZED',
        message: 'Not authenticated',
      });
    }
    
    return ctx.prisma.entity.create({
      data: {
        ...input,
        createdBy: ctx.userId,
      },
    });
  }),
```

## Import Rules

This package CAN import from:
- `@carton/shared` - Prisma client, schemas, utilities
- `zod` - Input validation
- `@trpc/server` - tRPC utilities
- `express` - Server framework

This package should NOT import from:
- `@carton/client` - Would create circular dependency

## Using Shared Schemas

Import Zod schemas from shared for input validation:

```typescript
import { casePrioritySchema, caseStatusSchema } from '@carton/shared';

update: publicProcedure
  .input(z.object({
    id: z.string(),
    status: caseStatusSchema.optional(),
    priority: casePrioritySchema.optional(),
  }))
  .mutation(async ({ ctx, input }) => {
    // ...
  }),
```

## Context

The tRPC context provides:
- `ctx.prisma` - PrismaClient instance
- `ctx.userId` - Current user ID (from cookie/session)

## Error Handling

Use tRPC errors for proper HTTP status codes:

```typescript
import { TRPCError } from '@trpc/server';

// 401 Unauthorized
throw new TRPCError({
  code: 'UNAUTHORIZED',
  message: 'Not authenticated',
});

// 404 Not Found
throw new TRPCError({
  code: 'NOT_FOUND', 
  message: 'Resource not found',
});

// 400 Bad Request
throw new TRPCError({
  code: 'BAD_REQUEST',
  message: 'Invalid input',
});
```

## Database Commands

Run from project root:
- `npm run db:generate` - Generate Prisma Client
- `npm run db:push` - Push schema to database
- `npm run db:seed` - Seed with test data
- `npm run db:studio` - Open Prisma Studio

## Adding a New Entity

1. Add Prisma model in `packages/shared/prisma/schema.prisma`
2. Run `npm run db:generate` then `npm run db:push`
3. Add router procedures in `src/router.ts`
4. Add seed data in `db/seed.ts` if needed

## Production Considerations

- Server uses `tsx` to run TypeScript directly (dev and prod)
- Static files served from `packages/client/dist` in production
- Database migrations via `prisma db push` at container startup
