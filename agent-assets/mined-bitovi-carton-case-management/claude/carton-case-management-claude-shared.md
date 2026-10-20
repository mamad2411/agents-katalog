# @carton/shared Package Instructions

This package contains shared code used by both server and client packages.

## Package Purpose

- **Prisma schema**: Single source of truth for data models
- **Generated types**: Zod schemas auto-generated from Prisma
- **Utilities**: Helper functions safe for both server and browser
- **Constants**: Shared constants and options

## Directory Structure

```
packages/shared/
├── prisma/
│   └── schema.prisma      # Prisma schema (THE source of truth)
├── src/
│   ├── index.ts           # Main entry (server-safe, full exports)
│   ├── client.ts          # Browser-safe entry (no Prisma runtime)
│   ├── prisma.ts          # PrismaClient instance
│   ├── types.ts           # Type definitions and schemas
│   ├── utils.ts           # Utility functions
│   └── generated/         # Auto-generated Zod schemas
│       └── index.ts
└── package.json
```

## Two Entry Points

### `@carton/shared` (index.ts)
Full exports including Prisma. **Server-only**.

Exports:
- `prisma` - PrismaClient instance
- All Zod schemas from generated/
- All types and utilities

### `@carton/shared/client` (client.ts)
Browser-safe exports. **No Prisma runtime**.

Exports:
- Zod enum schemas (CasePrioritySchema, CaseStatusSchema)
- Type aliases (CasePriority, CaseStatus)
- UI constants (CASE_PRIORITY_OPTIONS, CASE_STATUS_OPTIONS)
- Utility functions (formatDate, formatCaseNumber)

## Adding Code to This Package

### New Utility Function

1. Add to `src/utils.ts`
2. Export from `src/index.ts`
3. If browser-safe, also export from `src/client.ts`

### New Type or Schema

1. If based on Prisma: It's auto-generated, just re-export
2. If custom: Add to `src/types.ts`, export from both entry points if browser-safe

### New Prisma Model

1. Add model to `prisma/schema.prisma`
2. Run `npm run db:generate` from project root
3. Generated Zod schemas appear in `src/generated/index.ts`

## What NOT to Put Here

- ❌ Server-specific logic (put in @carton/server)
- ❌ React components (put in @carton/client)
- ❌ API route definitions (put in @carton/server)
- ❌ Types that depend on AppRouter (creates circular dependency)

## Import Rules

This package should NOT import from:
- `@carton/server` - Would create circular dependency
- `@carton/client` - Would create circular dependency

This package CAN import from:
- `zod` - For schema definitions
- `@prisma/client` - For Prisma types and client

## Generated Code

The `src/generated/` directory contains auto-generated Zod schemas from `zod-prisma-types`.

**Never edit files in generated/ manually** - they will be overwritten.

To regenerate:
```bash
npm run db:generate
```

## Browser Compatibility

Code in `client.ts` must be browser-safe:
- ✅ Pure functions
- ✅ Type definitions
- ✅ Zod schemas (they work in browser)
- ✅ Constants
- ❌ PrismaClient
- ❌ Node.js APIs
- ❌ File system access
