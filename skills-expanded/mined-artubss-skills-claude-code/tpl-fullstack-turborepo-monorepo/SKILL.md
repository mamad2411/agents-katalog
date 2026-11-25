---
name: tpl-fullstack-turborepo-monorepo
description: Template do pack (fullstack/02-turborepo-monorepo.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/02-turborepo-monorepo.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Turborepo Monorepo (Next.js + Node API + Shared Packages)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/02-turborepo-monorepo.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Monorepo:** Turborepo 2.x + pnpm workspaces
- **Web App:** Next.js 15 (App Router)
- **API Server:** Node.js 22 + Express 5 + TypeScript
- **Shared packages:** `@repo/ui`, `@repo/config`, `@repo/types`, `@repo/db`
- **Database:** PostgreSQL via Drizzle ORM (shared `@repo/db`)
- **Language:** TypeScript 5.x (strict, project references)
- **CI:** GitHub Actions with Turborepo remote cache

---

## PROJECT STRUCTURE
```
apps/
├── web/                         # Next.js frontend
│   ├── src/
│   ├── package.json             # depends on @repo/ui, @repo/types
│   └── tsconfig.json
└── api/                         # Express API server
    ├── src/
    ├── package.json             # depends on @repo/db, @repo/types
    └── tsconfig.json
packages/
├── ui/                          # Shared React components (shadcn-based)
│   ├── src/
│   │   ├── button.tsx
│   │   └── index.ts
│   └── package.json
├── db/                          # Drizzle schema + client
│   ├── src/
│   │   ├── schema.ts
│   │   ├── client.ts
│   │   └── index.ts
│   └── package.json
├── types/                       # Shared TS interfaces, no runtime deps
│   ├── src/
│   │   └── index.ts
│   └── package.json
└── config/
    ├── eslint/
    │   └── library.js           # Shared ESLint config
    └── typescript/
        ├── base.json            # Base tsconfig
        ├── nextjs.json
        └── node.json
turbo.json
pnpm-workspace.yaml
package.json                     # Root: dev tooling only
```

---

## ARCHITECTURE RULES
1. **`packages/*` are internal packages** — no public npm publish; versioned via `"version": "0.0.0"`.
2. **`@repo/types` has zero runtime dependencies** — types only; any dependency is a TS dev dep.
3. **`@repo/db` is the only place Drizzle is imported** — apps use `@repo/db` exclusively.
4. **Shared packages export from `src/index.ts`** — `package.json` `"exports"` field points to dist or `src` (via `tsup`).
5. **`turbo.json` defines the full pipeline** — no app-level ad-hoc scripts; all tasks flow through turbo.
6. **`pnpm --filter` for isolated ops** — never run `npm` or `yarn` commands in workspaces.
7. **CI uses remote cache** — `TURBO_TOKEN` + `TURBO_TEAM` environment variables set in GitHub Actions.

---

## TURBO.JSON PIPELINE

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs":    ["src/**", "tsconfig.json", "package.json"],
      "outputs":   [".next/**", "dist/**", "!.next/cache/**"]
    },
    "dev": {
      "dependsOn": ["^build"],
      "persistent": true,
      "cache": false
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs":    ["src/**", "tests/**"],
      "outputs":   ["coverage/**"]
    },
    "lint": {
      "inputs": ["src/**", ".eslintrc.*"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs":    ["src/**", "tsconfig.json"]
    },
    "db:migrate": {
      "cache": false
    }
  }
}
```

---

## SHARED PACKAGE SETUP

```json
// packages/types/package.json
{
  "name": "@repo/types",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./dist/index.js"
    }
  },
  "devDependencies": { "typescript": "^5.0.0" }
}
```

```typescript
// packages/types/src/index.ts
export interface User {
  id:        string
  email:     string
  name:      string
  role:      'user' | 'admin'
  createdAt: Date
}

export interface Post {
  id:       string
  title:    string
  body:     string
  authorId: string
  published: boolean
}

export type ApiResponse<T> = { data: T; error?: never } | { data?: never; error: string }
```

---

## SHARED UI PACKAGE

```typescript
// packages/ui/src/button.tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from './utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:opacity-50',
  {
    variants: {
      variant: {
        default:   'bg-primary text-primary-foreground hover:bg-primary/90',
        outline:   'border border-input hover:bg-accent',
        ghost:     'hover:bg-accent hover:text-accent-foreground',
        destructive: 'bg-destructive text-destructive-foreground',
      },
      size: {
        sm:      'h-8 px-3',
        default: 'h-10 px-4 py-2',
        lg:      'h-11 px-8',
        icon:    'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = ({ className, variant, size, ...props }: ButtonProps) => (
  <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
)
```

---

## SHARED DB PACKAGE

```typescript
// packages/db/src/schema.ts
import { pgTable, text, boolean, timestamp } from 'drizzle-orm/pg-core'
import { createId } from '@paralleldrive/cuid2'

export const users = pgTable('users', {
  id:        text('id').primaryKey().$defaultFn(createId),
  email:     text('email').notNull().unique(),
  name:      text('name').notNull(),
  role:      text('role', { enum: ['user', 'admin'] }).notNull().default('user'),
  createdAt: timestamp('created_at').defaultNow(),
})

// packages/db/src/client.ts
import { drizzle } from 'drizzle-orm/node-postgres'
import { Pool }    from 'pg'
import * as schema from './schema'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
export const db = drizzle(pool, { schema })
export * from './schema'
```

---

## ROUTING TABLE (turborepo task → app)

| Task | Scope | Cache | Action |
|------|-------|-------|--------|
| `turbo build` | all | yes | Build all apps + packages |
| `turbo dev` | all | no | Start dev servers in parallel |
| `turbo test` | all | yes | Run all test suites |
| `turbo lint` | all | yes | ESLint all workspaces |
| `turbo typecheck` | all | yes | `tsc --noEmit` everywhere |
| `pnpm --filter web dev` | apps/web | no | Start Next.js only |
| `pnpm --filter api dev` | apps/api | no | Start Express only |
| `pnpm --filter @repo/db db:migrate` | packages/db | no | Run Drizzle migrations |
| `turbo build --filter=...web` | apps/web + deps | yes | Build web + its deps only |

---

## QUALITY GATES
- [ ] `turbo typecheck` — zero errors across all workspaces
- [ ] `turbo lint` — clean
- [ ] `turbo test` — all pass
- [ ] `turbo build` — all outputs produced
- [ ] No cross-package imports via relative paths (`../../packages/ui`) — use `@repo/ui`
- [ ] `pnpm install` from root only — never `cd packages/ui && npm install`
- [ ] Remote cache configured in CI (`TURBO_TOKEN` secret set)
- [ ] `packages/types` has zero runtime deps

---

## FORBIDDEN
- ❌ `import { User } from '../../packages/types/src'` — use `@repo/types`
- ❌ `npm` or `yarn` commands — pnpm only
- ❌ Individual `tsconfig.json` extending different bases than `@repo/config/typescript/*`
- ❌ `devDependencies` in `packages/*` that are also in `peerDependencies` of an app — resolve at root
- ❌ Publishing internal packages to npm registry
- ❌ Circular dependencies between packages (packages/a → packages/b → packages/a)
- ❌ App-specific code in shared packages (`if (process.env.NEXT_PUBLIC_*)` in `@repo/db`)
