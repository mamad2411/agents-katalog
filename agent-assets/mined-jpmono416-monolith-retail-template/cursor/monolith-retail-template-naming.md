---
description: Naming conventions for files, packages, env vars, database, and code symbols
globs:
  - "**/*"
alwaysApply: false
---

# Naming

## Purpose

One vocabulary across repos, env vars, APIs, and DB so humans and AI agents infer location and meaning without guessing.

## Required patterns

### Packages (pnpm workspace)

| Package | Name |
|---------|------|
| API app | `@monolith/api` |
| Web app | `@monolith/web` |
| Mobile app | `@monolith/mobile` |
| Shared types | `@monolith/types` |
| Shared UI | `@monolith/ui` |
| Shared config | `@monolith/config` |
| ESLint config | `@monolith/eslint-config` |
| TS config | `@monolith/tsconfig` |

- New shared packages: `@monolith/<short-name>`, kebab-case folder under `packages/`.

### Files & folders

| Kind | Convention | Example |
|------|------------|---------|
| Feature folder | kebab-case | `features/order-items/` |
| Nest files | kebab-case + suffix | `orders.service.ts`, `orders.controller.ts` |
| DTO files | kebab-case + `.dto.ts` | `create-order.dto.ts` |
| React components (file) | PascalCase or kebab-case matching colocated default export | `OrderList.tsx` |
| Tests | same base + `.spec.ts` / `.test.ts` | `orders.service.spec.ts` |
| Constants | kebab-case file, SCREAMING_SNAKE exports | `queue.constants.ts` → `QUEUE_NAMES` |

### TypeScript symbols

- **Types/interfaces**: PascalCase (`OrderSummary`, `AppConfig`)
- **Classes**: PascalCase (`OrdersService`, `CreateOrderDto`)
- **Functions/methods/variables**: camelCase (`findById`, `databaseUrl`)
- **Enums**: PascalCase name, PascalCase members (`OrderStatus.Shipped`)
- **Boolean** vars/props: `is`, `has`, `can` prefix (`isActive`, `hasAccess`)

### Environment variables

- SCREAMING_SNAKE_CASE
- Prefix by domain:
  - `NEXT_PUBLIC_` — browser-safe web config
  - `API_` — Nest bind/host/port
  - `DATABASE_URL`, `DIRECT_URL` — Prisma (standard names, no rename)
  - `REDIS_URL`, `BULLMQ_PREFIX`
  - `JWT_`, `SUPABASE_`, `UPSTASH_` — feature-specific

### Database (Prisma)

- Models: PascalCase singular (`User`, `Order`, `OrderItem`)
- Fields: camelCase (`createdAt`, `userId`)
- Tables: plural snake_case via `@@map` only when required; default Prisma mapping is acceptable
- IDs: `String @id @default(cuid())` unless domain requires UUID
- Timestamps: `createdAt`, `updatedAt` on all mutable entities

### API & types

- JSON properties: camelCase
- Route segments: kebab-case, plural resources (`/api/order-items`)
- Shared types exported from `packages/types/src/index.ts` (barrel) — one export per concept

## Forbidden patterns

- Abbreviations unclear to new contributors (`ordSvc`, `usrMgr`).
- Hungarian notation (`strName`, `IUser` interface prefix).
- `utils.ts` / `helpers.ts` at feature root without domain prefix — use `<feature>-<purpose>.ts`.
- Renaming established env vars without updating `.env.example`, compose, and CI.
- Package names outside `@monolith/*` scope in this monorepo.

## Implementation expectations

- Renames require updating imports across workspace and any docs referencing old names.
- New Prisma models: run `pnpm db:migrate` with descriptive migration names (`add_orders_table`).

## Consistency expectations

- Reference implementation matching is owned by `agent-behaviour.mdc`.
- Git branches: `feature/`, `fix/`, `chore/` prefixes.

## Examples

**Good**

```prisma
model Order {
  id        String   @id @default(cuid())
  userId    String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

```typescript
export const QUEUE_NAMES = { default: 'default', email: 'email' } as const;
```

**Bad**

```typescript
export const queueNames = { Default: 'default' }; // ❌ inconsistent casing
```
