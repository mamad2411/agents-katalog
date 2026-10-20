# SAP-040: React Monorepo Architecture - Agent Awareness Guide

**SAP ID**: SAP-040
**Name**: react-monorepo-architecture
**Status**: pilot
**Version**: 1.0.0
**For**: All AI agents (Claude, GPT-4, Gemini, etc.)
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-040?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 50-minute setup with tool decision tree for Turborepo, Nx, or pnpm workspaces
- 📚 **Time Savings** - 93.1% reduction (50 min vs 8-12 hours manual), 90% build time reduction with remote caching
- 🎯 **3 Tool Options** - Turborepo (fastest, free cache), Nx (code generation, enterprise), pnpm workspaces (baseline)
- 🔧 **Shared Packages** - @acme/ui, @acme/utils, @acme/config with workspace protocol for zero version conflicts
- 📊 **Remote Caching** - Vercel Remote Cache (Turborepo free), Nx Cloud (500h/mo free), 10x CI/CD speedup
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-021 (Testing), SAP-024 (Styling), SAP-028 (Publishing)

This AGENTS.md provides: Agent-specific patterns for monorepo architecture workflows.

---

## Tool Decision Tree

```
START: Which monorepo tool should I use?

Q1: Do you need code generation (nx generate @nx/react:component)?
├─ YES → Nx ✅ (powerful generators, schematics, standardized component creation)
└─ NO  → Continue to Q2

Q2: Do you have 100+ packages?
├─ YES → Nx ✅ (advanced affected detection, module boundaries, constraints)
└─ NO  → Continue to Q3

Q3: Do you need remote caching?
├─ YES → Turborepo ✅ (free Vercel Remote Cache, 90% build time reduction)
└─ NO  → Continue to Q4

Q4: Do you need task orchestration (build pipelines)?
├─ YES → Turborepo ✅ (simple pipelines, parallel execution)
└─ NO  → pnpm workspaces ✅ (baseline linking, no orchestration)

DEFAULT: Turborepo (80% of use cases)
```

---

## Tool Comparison

| Criteria | Turborepo | Nx | pnpm workspaces | Winner |
|----------|-----------|----|--------------------|--------|
| **Speed** | ⚡⚡⚡ Fastest (parallel + cache) | ⚡⚡ Fast | ⚡ Baseline | Turborepo |
| **Remote Cache** | ✅ Free (Vercel) | ✅ 500h/mo free | ❌ No | Turborepo |
| **Code Generation** | ❌ No | ✅ Yes | ❌ No | Nx |
| **Learning Curve** | Low (15 min) | High (2 hours) | Very Low (5 min) | pnpm |
| **Setup Time** | 20 min | 25 min | 15 min | pnpm |
| **Dependency Graph** | ❌ No (external tool) | ✅ Yes (nx graph) | ❌ No | Nx |
| **Affected Detection** | ✅ Good | ✅ Excellent | ❌ No | Nx |
| **Next.js Support** | ✅ Native (Vercel) | ✅ Plugin | ✅ Compatible | Turborepo |
| **Use Cases** | 2-50 packages, Next.js | 50-500+ packages | 2-5 packages | - |

**Recommendation**:
- **Turborepo**: 80% of use cases (fast, simple, free cache)
- **Nx**: 15% of use cases (enterprise, 100+ packages, code gen)
- **pnpm workspaces**: 5% of use cases (baseline, no orchestration)

---

## Common Workflows

### Workflow 1: Setup Monorepo with Turborepo (20 min)

**User Request**: "Create monorepo for Next.js web app + admin dashboard"

**Agent Steps**:

1. **Create directory structure** (2 min):
   ```bash
   mkdir my-monorepo && cd my-monorepo
   git init
   mkdir -p apps/web apps/admin packages/ui packages/utils
   ```

2. **Create root package.json** (2 min):
   ```json
   {
     "name": "my-monorepo",
     "version": "0.0.0",
     "private": true,
     "scripts": {
       "build": "turbo run build",
       "dev": "turbo run dev",
       "test": "turbo run test"
     },
     "devDependencies": {
       "turbo": "^2.0.0"
     },
     "packageManager": "pnpm@9.0.0"
   }
   ```

3. **Create pnpm-workspace.yaml** (1 min):
   ```yaml
   packages:
     - 'apps/*'
     - 'packages/*'
   ```

4. **Create turbo.json** (2 min):
   ```json
   {
     "$schema": "https://turbo.build/schema.json",
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": [".next/**", "dist/**"]
       },
       "dev": {
         "cache": false,
         "persistent": true
       }
     }
   }
   ```

5. **Create shared UI package** (5 min):
   ```bash
   # packages/ui/package.json
   {
     "name": "@acme/ui",
     "version": "0.0.0",
     "main": "./src/index.ts",
     "dependencies": {
       "react": "^18.3.0"
     }
   }

   # packages/ui/src/button.tsx
   export function Button({ children }) {
     return <button>{children}</button>;
   }

   # packages/ui/src/index.ts
   export { Button } from './button';
   ```

6. **Create Next.js apps** (5 min):
   ```bash
   cd apps/web
   npx create-next-app@latest . --typescript --tailwind
   # Update package.json to add @acme/ui dependency
   ```

7. **Install dependencies** (2 min):
   ```bash
   pnpm install
   ```

8. **Build** (1 min):
   ```bash
   turbo run build
   ```

**Total Time**: 20 minutes

---

### Workflow 2: Setup Remote Caching (10 min)

**User Request**: "Enable Vercel Remote Cache for faster builds"

**Agent Steps**:

1. **Login to Vercel** (3 min):
   ```bash
   npx turbo login
   # Opens browser, authenticate
   ```

2. **Link project** (2 min):
   ```bash
   npx turbo link
   # Select team + project
   ```

3. **Enable in turbo.json** (1 min):
   ```json
   {
     "remoteCache": {
       "enabled": true
     }
   }
   ```

4. **Set environment variables** (2 min):
   ```bash
   # .env (gitignored)
   TURBO_TOKEN="your-token"
   TURBO_TEAM="your-team-id"
   ```

5. **Test** (2 min):
   ```bash
   turbo run build  # First run: cache miss (5 min)
   turbo run build  # Second run: cache hit (10s)
   ```

**Total Time**: 10 minutes

**Performance**: 5 min → 10s (90% faster)

---

### Workflow 3: Add Shared Package (10 min)

**User Request**: "Create @acme/utils package with shared utilities"

**Agent Steps**:

1. **Create directory** (1 min):
   ```bash
   mkdir -p packages/utils/src
   ```

2. **Create package.json** (2 min):
   ```json
   // packages/utils/package.json
   {
     "name": "@acme/utils",
     "version": "0.0.0",
     "private": true,
     "main": "./src/index.ts",
     "types": "./src/index.ts"
   }
   ```

3. **Create utility** (3 min):
   ```typescript
   // packages/utils/src/cn.ts
   export function cn(...classes: string[]): string {
     return classes.filter(Boolean).join(' ');
   }

   // packages/utils/src/index.ts
   export { cn } from './cn';
   ```

4. **Add to app** (2 min):
   ```json
   // apps/web/package.json
   {
     "dependencies": {
       "@acme/utils": "workspace:*"
     }
   }
   ```

5. **Install** (1 min):
   ```bash
   pnpm install
   ```

6. **Use in app** (1 min):
   ```tsx
   // apps/web/app/page.tsx
   import { cn } from '@acme/utils';

   export default function HomePage() {
     return <div className={cn('flex', 'items-center')}></div>;
   }
   ```

**Total Time**: 10 minutes

---

### Workflow 4: Integrate with CI/CD (10 min)

**User Request**: "Run tests only for changed packages in GitHub Actions"

**Agent Steps**:

1. **Create workflow** (5 min):
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   on:
     pull_request:
       branches: [main]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0  # Required for affected detection

         - uses: pnpm/action-setup@v2
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: 'pnpm'

         - run: pnpm install

         # Test only affected packages
         - run: turbo run test --filter=[origin/main...HEAD]
           env:
             TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
             TURBO_TEAM: ${{ secrets.TURBO_TEAM }}
   ```

2. **Add secrets** (3 min):
   - Go to GitHub repo → Settings → Secrets
   - Add `TURBO_TOKEN` and `TURBO_TEAM`

3. **Test** (2 min):
   - Push PR
   - Verify CI runs only affected tests

**Total Time**: 10 minutes

**Performance**: 10 packages × 1 min = 10 min → 1 package × 1 min = 1 min (90% faster)

---

## Shared Package Patterns

### Pattern 1: UI Components (@acme/ui)

**Structure**:
```
packages/ui/
├── src/
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── index.ts         # Barrel export
├── package.json
├── tsconfig.json
└── tailwind.config.ts
```

**package.json**:
```json
{
  "name": "@acme/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}
```

**Usage**:
```tsx
import { Button, Input, Card } from '@acme/ui';
```

---

### Pattern 2: Utilities (@acme/utils)

**Structure**:
```
packages/utils/
├── src/
│   ├── cn.ts           # className utility
│   ├── format-date.ts  # Date formatting
│   ├── validation.ts   # Zod schemas
│   └── index.ts
└── package.json
```

**Usage**:
```typescript
import { cn, formatDate, validateEmail } from '@acme/utils';
```

---

### Pattern 3: Shared Configs (@acme/config)

**Structure**:
```
packages/config/
├── eslint-preset.js    # Shared ESLint config
├── tailwind-preset.ts  # Shared Tailwind config
└── package.json
```

**Usage**:
```javascript
// apps/web/eslint.config.js
import { preset } from '@acme/config/eslint-preset';
export default preset;

// apps/web/tailwind.config.ts
import { preset } from '@acme/config/tailwind-preset';
export default preset;
```

---

### Pattern 4: TypeScript Configs (@acme/tsconfig)

**Structure**:
```
packages/tsconfig/
├── base.json           # Base config
├── nextjs.json         # Next.js-specific config
├── react-library.json  # React library config
└── package.json
```

**Usage**:
```json
// apps/web/tsconfig.json
{
  "extends": "@acme/tsconfig/nextjs.json",
  "compilerOptions": {
    "outDir": "dist"
  }
}
```

---

## Cache Optimization Checklist

Use this checklist to maximize cache hit rate:

### 1. Configure Outputs Correctly

**Turborepo**:
```json
{
  "pipeline": {
    "build": {
      "outputs": [".next/**", "dist/**", "build/**"]
    }
  }
}
```

**Why**: Cache only what's necessary (not node_modules)

---

### 2. Use Deterministic Builds

**Avoid**:
```typescript
// ❌ Non-deterministic (includes timestamp)
const buildTime = new Date().toISOString();
```

**Prefer**:
```typescript
// ✅ Deterministic (uses env var or git hash)
const buildTime = process.env.BUILD_TIME || 'development';
```

**Why**: Non-deterministic builds break caching

---

### 3. Minimize Global Dependencies

**Turborepo**:
```json
{
  "globalDependencies": [
    ".env",
    "tsconfig.json"
  ]
}
```

**Why**: Changes to global files invalidate all caches

---

### 4. Use Affected Detection

**Turborepo**:
```bash
turbo run test --filter=[origin/main...HEAD]
```

**Nx**:
```bash
nx affected:test --base=origin/main
```

**Why**: Don't run tests for unchanged packages

---

### 5. Enable Remote Caching

**Turborepo**:
```json
{
  "remoteCache": {
    "enabled": true
  }
}
```

**Nx**:
```bash
npx nx connect-to-nx-cloud
```

**Why**: Share cache across team + CI (90% faster builds)

---

## Integration with Other SAPs

### SAP-020 (React Foundation)

**Integration**: Monorepo with Next.js 15 App Router

**Pattern**:
```
my-monorepo/
├── apps/
│   ├── web/              # Next.js 15 app
│   └── admin/            # Next.js 15 app
└── packages/
    ├── ui/               # Shared Server Components
    └── api/              # Shared Server Actions
```

**Usage**:
```tsx
// packages/ui/src/server-button.tsx (Server Component)
export function ServerButton({ children }: { children: React.ReactNode }) {
  return <button>{children}</button>;
}

// apps/web/app/page.tsx
import { ServerButton } from '@acme/ui';
export default function HomePage() {
  return <ServerButton>Click Me</ServerButton>;
}
```

---

### SAP-021 (Testing)

**Integration**: Share Vitest config across packages

**Pattern**:
```
packages/config/vitest-preset.ts
```

**Usage**:
```typescript
// packages/config/vitest-preset.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
  },
});

// apps/web/vitest.config.ts
import { defineConfig } from 'vitest/config';
import preset from '@acme/config/vitest-preset';

export default defineConfig({
  ...preset,
  test: {
    ...preset.test,
    include: ['**/*.test.{ts,tsx}'],
  },
});
```

---

### SAP-024 (Styling)

**Integration**: Shared Tailwind config in @acme/config

**Pattern**:
```typescript
// packages/config/tailwind-preset.ts
import type { Config } from 'tailwindcss';

export const preset: Partial<Config> = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
      },
    },
  },
};

// apps/web/tailwind.config.ts
import type { Config } from 'tailwindcss';
import { preset } from '@acme/config/tailwind-preset';

export default {
  presets: [preset],
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
  ],
} satisfies Config;
```

---

### SAP-028 (Publishing)

**Integration**: Automated publishing with changesets

**Pattern**:
```bash
# Install changesets
pnpm add -Dw @changesets/cli
npx changeset init

# Create changeset
npx changeset
# ? Which packages? @acme/ui, @acme/utils
# ? What kind of change? patch

# Version packages
npx changeset version

# Publish (if public packages)
npx changeset publish
```

---

## Troubleshooting Guide

### Issue 1: Package Not Found

**Symptoms**:
- `Error: Cannot find module '@acme/ui'`
- TypeScript can't resolve imports

**Diagnosis**:
```bash
# Check if package is linked
ls node_modules/@acme/ui
```

**Solutions**:

1. **Install dependencies**:
   ```bash
   pnpm install
   ```

2. **Verify workspace protocol**:
   ```json
   // apps/web/package.json
   {
     "dependencies": {
       "@acme/ui": "workspace:*"  // Correct
       // "@acme/ui": "^1.0.0"    // Wrong (tries to use npm)
     }
   }
   ```

3. **Check pnpm-workspace.yaml**:
   ```yaml
   packages:
     - 'apps/*'
     - 'packages/*'  # Must include packages
   ```

---

### Issue 2: Cache Not Working

**Symptoms**:
- `turbo run build` always rebuilds (no cache hit)
- CI never uses cache

**Diagnosis**:
```bash
# Check turbo cache
ls .turbo/cache
```

**Solutions**:

1. **Enable remote cache**:
   ```json
   // turbo.json
   {
     "remoteCache": {
       "enabled": true
     }
   }
   ```

2. **Set environment variables**:
   ```bash
   export TURBO_TOKEN="your-token"
   export TURBO_TEAM="your-team-id"
   ```

3. **Check outputs**:
   ```json
   // turbo.json
   {
     "pipeline": {
       "build": {
         "outputs": [".next/**", "dist/**"]  // Must match actual output
       }
     }
   }
   ```

4. **Force rebuild** (clear cache):
   ```bash
   turbo run build --force
   ```

---

### Issue 3: Build Order Issues

**Symptoms**:
- `Error: Cannot find module '@acme/ui'` during build
- App builds before dependencies

**Diagnosis**:
```bash
# Check dependency graph
nx graph
```

**Solutions**:

1. **Add dependsOn**:
   ```json
   // turbo.json
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"]  // Build dependencies first
       }
     }
   }
   ```

2. **Verify package.json dependencies**:
   ```json
   // apps/web/package.json
   {
     "dependencies": {
       "@acme/ui": "workspace:*"  // Must be declared
     }
   }
   ```

---

### Issue 4: Hot Reload Not Working

**Symptoms**:
- Change in `packages/ui` doesn't hot reload in `apps/web`
- Need to restart dev server

**Diagnosis**:
```bash
# Check if packages are linked
ls -la node_modules/@acme/ui
# Should be symlink: node_modules/@acme/ui -> ../../packages/ui
```

**Solutions**:

1. **Use transpilePackages** (Next.js):
   ```typescript
   // apps/web/next.config.ts
   export default {
     transpilePackages: ['@acme/ui', '@acme/utils'],
   };
   ```

2. **Run package in watch mode**:
   ```bash
   # Terminal 1: Watch packages
   turbo run dev --filter=@acme/ui

   # Terminal 2: Run app
   turbo run dev --filter=@acme/web
   ```

3. **Check Webpack config** (if custom):
   ```typescript
   // Ensure symlinks are resolved
   resolve: {
     symlinks: true
   }
   ```

---

### Issue 5: TypeScript Errors

**Symptoms**:
- `Cannot find name 'Button'`
- TypeScript can't resolve imports

**Diagnosis**:
```bash
# Check tsconfig.json paths
cat apps/web/tsconfig.json
```

**Solutions**:

1. **Use TypeScript project references**:
   ```json
   // apps/web/tsconfig.json
   {
     "extends": "@acme/tsconfig/nextjs.json",
     "references": [
       { "path": "../../packages/ui" },
       { "path": "../../packages/utils" }
     ]
   }
   ```

2. **Ensure package has types**:
   ```json
   // packages/ui/package.json
   {
     "main": "./src/index.ts",
     "types": "./src/index.ts"  // Must be set
   }
   ```

3. **Restart TypeScript server** (VS Code):
   - Cmd+Shift+P → "TypeScript: Restart TS Server"

---

## Quick Command Reference

### Turborepo

```bash
# Run task across all packages
turbo run build
turbo run test

# Filter by package
turbo run build --filter=@acme/ui

# Filter by affected (Git)
turbo run test --filter=[origin/main...HEAD]

# Force rebuild (ignore cache)
turbo run build --force

# Parallel execution
turbo run build --parallel=10

# Clear cache
turbo prune

# Login to Vercel Remote Cache
npx turbo login
npx turbo link
```

---

### Nx

```bash
# Run target
nx build @acme/ui
nx test @acme/web

# Run for all projects
nx run-many --target=build --all

# Run for affected projects
nx affected:build --base=origin/main

# Dependency graph
nx graph

# Code generation
nx generate @nx/react:component Button --project=ui

# Clear cache
nx reset
```

---

### pnpm workspaces

```bash
# Install dependencies
pnpm install

# Add dependency to package
pnpm add zod --filter @acme/ui

# Add dependency to root
pnpm add -Dw turbo

# Run script in package
pnpm --filter @acme/ui build

# Run script in all packages
pnpm -r build

# Run script in all packages (parallel)
pnpm -r --parallel build
```

---

## Best Practices Summary

### 1. Workspace Structure
- ✅ Use apps/ and packages/ separation
- ✅ Scope package names (@acme/ui)
- ✅ Use workspace protocol (workspace:*)
- ❌ Don't nest apps inside packages

### 2. Build Configuration
- ✅ Enable remote caching
- ✅ Configure outputs correctly
- ✅ Use dependsOn for build order
- ❌ Don't cache node_modules

### 3. Performance
- ✅ Use affected detection in CI
- ✅ Enable parallel execution
- ✅ Share cache across team
- ❌ Don't rebuild everything

### 4. Development
- ✅ Use hot reload (transpilePackages)
- ✅ Run packages in watch mode
- ✅ Use TypeScript project references
- ❌ Don't duplicate configs

### 5. CI/CD
- ✅ Use remote caching
- ✅ Test only affected packages
- ✅ Store TURBO_TOKEN as secret
- ❌ Don't run full suite on every PR

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release
- Three-tool architecture (Turborepo, Nx, pnpm workspaces)
- Tool decision tree (4 questions)
- 4 common workflows (setup, remote caching, shared packages, CI/CD)
- 4 shared package patterns (ui, utils, config, tsconfig)
- Cache optimization checklist (5 tips)
- Integration patterns (SAP-020, SAP-021, SAP-024, SAP-028)
- Troubleshooting guide (5 common issues)
- Quick command reference (Turborepo, Nx, pnpm)

---

**Status**: Pilot (awaiting first production adoption)
**Time Savings**: 8-12h → 50min (93.1% reduction)
**Next Steps**: See [adoption-blueprint.md](./adoption-blueprint.md) for step-by-step setup
