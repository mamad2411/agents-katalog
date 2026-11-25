---
name: monorepo
description: "Apply when setting up or working in a monorepo with multiple apps and shared packages. Covers: workspace config, shared code patterns, dependency management, CI matrix, affected-only builds. Trigger for: monorepo, workspace, shared packages, nx, turborepo, pnpm workspace."
---

# MONOREPO — Structure & Patterns

## Structure (recommended)
```
my-monorepo/
├── apps/
│   ├── api/           # FastAPI backend
│   ├── web/           # Next.js frontend
│   └── worker/        # Job processor
├── packages/
│   ├── shared-types/  # TypeScript types shared by web + api
│   ├── ui/            # Shared React components
│   └── config/        # ESLint, TS configs
├── tools/
│   └── scripts/       # Build, deploy scripts
├── pnpm-workspace.yaml  # or turbo.json, nx.json
└── package.json
```

## pnpm Workspace
```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

## Shared Package Pattern
```json
// packages/shared-types/package.json
{
  "name": "@myapp/shared-types",
  "version": "0.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts"
}
```
```typescript
// apps/web uses it
import type { Job, JobStatus } from "@myapp/shared-types"
```

## Turborepo Pipeline
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],    // build deps first
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "cache": false               // always run tests fresh
    },
    "lint": { "cache": true }
  }
}
```
```bash
# Build only affected packages
turbo run build --filter=...[origin/main]

# Test specific app
turbo run test --filter=@myapp/api
```

## Forbidden
❌ Copying code between apps instead of shared package
❌ Different versions of the same dep in different apps (use root deps)
❌ No build caching (turbo/nx cache is the main benefit)
❌ Putting unrelated apps in same monorepo (use it for cohesive product)
