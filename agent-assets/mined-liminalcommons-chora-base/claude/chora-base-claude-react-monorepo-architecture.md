# SAP-040: React Monorepo Architecture - Claude Agent Guide

**SAP ID**: SAP-040
**Version**: 1.0.0
**Status**: pilot
**For**: Claude Code, Claude Desktop, Claude API
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

This CLAUDE.md provides: Claude Code-specific workflows for monorepo architecture.

---

### When to Use This SAP

**Use SAP-040 when user requests**:
- "Create monorepo for web + mobile apps"
- "Share UI components across multiple apps"
- "Speed up builds with remote caching"
- "Setup Turborepo/Nx/pnpm workspaces"
- "Manage multiple packages in one repo"

**Don't use SAP-040 when**:
- User has single app with no shared code
- Team <3 developers (overkill)
- Unrelated projects (no code sharing needed)

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Tool Selection (0-5k tokens)

**Goal**: Recommend Turborepo, Nx, or pnpm workspaces

**Read**:
1. This file (CLAUDE.md) for overview
2. AGENTS.md for decision tree

**Ask user**:
- "How many packages do you have?" (2-5 → pnpm, 5-50 → Turborepo, 50+ → Nx)
- "Do you need code generation?" (YES → Nx, NO → Turborepo)
- "Do you need remote caching?" (YES → Turborepo/Nx, NO → pnpm)

**Output**: Tool recommendation (Turborepo, Nx, or pnpm workspaces)

**Time**: 2-3 minutes

---

### Phase 2: Implementation (10-50k tokens)

**Goal**: Setup monorepo with chosen tool

**Read**:
1. `adoption-blueprint.md` - Step-by-step setup (Option A/B/C)
2. `AGENTS.md` (Workflow 1) - Quick setup workflow

**Generate**:
- Directory structure (apps/, packages/)
- Root configuration (package.json, pnpm-workspace.yaml, turbo.json/nx.json)
- Shared packages (@acme/ui, @acme/utils)
- Install commands

**Time**: 20-25 minutes

---

### Phase 3: Advanced Patterns (50-100k tokens)

**Goal**: Add remote caching, CI/CD, changesets

**Read**:
1. `protocol-spec.md` (How-To Guides) - Remote caching, CI/CD, versioning
2. `AGENTS.md` (Workflows 2-4) - Remote caching, shared packages, CI/CD

**Generate**:
- Remote caching setup (Vercel Remote Cache, Nx Cloud)
- GitHub Actions workflow (affected builds)
- Changesets configuration (automated versioning)

**Time**: 30-60 minutes (depending on complexity)

---

## Tool Decision Framework for Claude

### Decision Tree Prompt

When user requests monorepo, use this prompt:

```
I'll help you set up a monorepo. First, let me ask a few questions:

1. **Package Count**: How many packages do you have? (apps + shared packages)
2. **Code Generation**: Do you need to generate standardized components? (YES/NO)
3. **Remote Caching**: Do you want 90% faster builds with remote caching? (YES/NO)
4. **Team Size**: How many developers? (1-5, 5-50, 50+)

Based on your answers, I'll recommend:
- **Turborepo**: 2-50 packages, fast builds, free cache, simple (20 min)
- **Nx**: 50-500+ packages, code generation, enterprise (25 min)
- **pnpm workspaces**: 2-5 packages, baseline linking, no orchestration (15 min)
```

---

### Recommendation Matrix

| User Requirements | Recommended Tool | Rationale |
|-------------------|------------------|-----------|
| Need code generation | **Nx** | Only tool with generators (`nx generate`) |
| Have 100+ packages | **Nx** | Advanced affected detection, constraints |
| Need free remote caching | **Turborepo** | Vercel Remote Cache (free unlimited) |
| Building Next.js apps | **Turborepo** | Native Vercel integration |
| Have 2-5 packages, no orchestration | **pnpm workspaces** | Minimal tooling, baseline linking |
| Want fastest builds | **Turborepo** | Best caching performance (5.1s cached) |
| Need dependency graph visualization | **Nx** | `nx graph` built-in |
| Want minimal config | **pnpm workspaces** | No config files (just pnpm-workspace.yaml) |

**Default**: **Turborepo** (80% of use cases)

---

## Code Generation Patterns for Claude

### Pattern 1: Turborepo Setup

**User request**: "Setup Turborepo monorepo with Next.js web + admin apps"

**Claude generates**:

1. **Create directory structure**:
```bash
mkdir my-monorepo && cd my-monorepo
git init
mkdir -p apps/web apps/admin packages/ui/src packages/utils/src
```

2. **Create root package.json**:
```json
{
  "name": "my-monorepo",
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

3. **Create pnpm-workspace.yaml**:
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

4. **Create turbo.json**:
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

5. **Create shared UI package**:
```json
// packages/ui/package.json
{
  "name": "@acme/ui",
  "version": "0.0.0",
  "main": "./src/index.ts",
  "dependencies": {
    "react": "^18.3.0"
  }
}
```

```tsx
// packages/ui/src/button.tsx
export function Button({ children }: { children: React.ReactNode }) {
  return <button>{children}</button>;
}

// packages/ui/src/index.ts
export { Button } from './button';
```

6. **Install dependencies**:
```bash
pnpm install
```

7. **Build**:
```bash
turbo run build
```

**Explain to user**:
- "I've set up Turborepo with 2 apps (web, admin) + 2 packages (ui, utils)"
- "Build time: 2 min (first run) → 5s (cached run)"
- "Next steps: Create Next.js apps, setup remote caching"

---

### Pattern 2: Shared Package Creation

**User request**: "Create @acme/utils package with cn and formatDate utilities"

**Claude generates**:

1. **Create package directory**:
```bash
mkdir -p packages/utils/src
```

2. **Create package.json**:
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

3. **Create utilities**:
```typescript
// packages/utils/src/cn.ts
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}

// packages/utils/src/format-date.ts
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}

// packages/utils/src/index.ts
export { cn } from './cn';
export { formatDate } from './format-date';
```

4. **Add to app**:
```json
// apps/web/package.json
{
  "dependencies": {
    "@acme/utils": "workspace:*"
  }
}
```

5. **Install**:
```bash
pnpm install
```

6. **Use in app**:
```tsx
// apps/web/app/page.tsx
import { cn, formatDate } from '@acme/utils';

export default function HomePage() {
  return (
    <div className={cn('flex', 'items-center')}>
      <p>{formatDate(new Date())}</p>
    </div>
  );
}
```

**Explain to user**:
- "Created @acme/utils with cn + formatDate"
- "Used workspace protocol (workspace:*) for zero version conflicts"
- "Hot reload works: changes in packages/utils reflect instantly in apps/web"

---

### Pattern 3: Remote Caching Setup

**User request**: "Enable remote caching for 90% faster builds"

**Claude generates (Turborepo)**:

1. **Login to Vercel**:
```bash
npx turbo login
# Opens browser, authenticate
```

2. **Link project**:
```bash
npx turbo link
# Select team + project
```

3. **Enable in turbo.json**:
```json
{
  "remoteCache": {
    "enabled": true
  }
}
```

4. **Set environment variables**:
```bash
# .env (gitignored)
TURBO_TOKEN="your-token"
TURBO_TEAM="your-team-id"
```

5. **Test**:
```bash
turbo run build  # First run: 5 min
turbo run build  # Second run: 5s (90% faster)
```

**Claude generates (Nx)**:

```bash
npx nx connect-to-nx-cloud
# Follow prompts to connect
```

**Explain to user**:
- "Remote caching enabled (Vercel Remote Cache / Nx Cloud)"
- "First build: 5 min (uploads to cache)"
- "Subsequent builds: 5-10s (downloads from cache)"
- "90% build time reduction achieved"

---

### Pattern 4: CI/CD Integration

**User request**: "Run tests only for changed packages in CI"

**Claude generates**:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  test-affected:
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

      # Turborepo: test only affected
      - run: turbo run test --filter=[origin/main...HEAD]
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

      # Or Nx: test only affected
      # - run: nx affected:test --base=origin/main
      #   env:
      #     NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
```

**Explain to user**:
- "CI runs only affected packages (90% faster)"
- "Change 1 package → test 1 package (not all 10)"
- "Add TURBO_TOKEN and TURBO_TEAM to GitHub Secrets"
- "Performance: 10 min → 1 min (90% reduction)"

---

## Workflow Templates for Claude

### Workflow 1: New Monorepo Project (20 min)

**User**: "Create monorepo with Next.js web app + admin dashboard"

**Claude**:

1. **Tool Selection** (2 min):
   - Ask: "Do you need code generation or 100+ packages?" → NO → Turborepo
   - Default: Turborepo (80% of use cases)

2. **Create Structure** (3 min):
   ```bash
   mkdir my-monorepo && cd my-monorepo
   git init
   mkdir -p apps/web apps/admin packages/ui/src packages/utils/src
   ```

3. **Configure** (5 min):
   - Create package.json, pnpm-workspace.yaml, turbo.json
   - Follow adoption-blueprint.md (Option A: Turborepo)

4. **Create Shared Packages** (5 min):
   - @acme/ui (Button, Input, Card)
   - @acme/utils (cn, formatDate)

5. **Create Apps** (5 min):
   - Next.js web app
   - Next.js admin app

6. **Install & Build** (2 min):
   ```bash
   pnpm install
   turbo run build
   ```

**Expected time**: 20 minutes
**Output**: Working monorepo with 2 apps, 2 packages

---

### Workflow 2: Add Remote Caching (10 min)

**User**: "My builds are slow, enable caching"

**Claude**:

1. **Diagnose** (2 min):
   - Check if user has Turborepo or Nx
   - Check if remote cache is already enabled

2. **Setup Vercel Remote Cache** (5 min):
   ```bash
   npx turbo login
   npx turbo link
   ```
   - Update turbo.json: `"remoteCache": { "enabled": true }`

3. **Test** (3 min):
   ```bash
   turbo run build  # First run: 5 min
   turbo run build  # Second run: 5s
   ```

**Expected time**: 10 minutes
**Output**: 90% build time reduction

---

### Workflow 3: Migrate Existing Apps to Monorepo (30 min)

**User**: "Move my 2 separate repos (web-app, mobile-app) into monorepo"

**Claude**:

1. **Create Monorepo** (5 min):
   - Create my-monorepo with apps/, packages/

2. **Move Web App** (10 min):
   - Clone web-app repo
   - Move files to apps/web
   - Update package.json: `"name": "@acme/web"`
   - Add `workspace:*` protocol for shared packages

3. **Move Mobile App** (10 min):
   - Clone mobile-app repo
   - Move files to apps/mobile
   - Update package.json

4. **Extract Shared Code** (5 min):
   - Move shared components to packages/ui
   - Move shared utils to packages/utils
   - Update imports: `import { Button } from '@acme/ui'`

5. **Install & Build** (2 min):
   ```bash
   pnpm install
   turbo run build
   ```

**Expected time**: 30 minutes
**Output**: Monorepo with 2 apps, shared packages

---

### Workflow 4: Troubleshoot Build Issues (5 min)

**User**: "My builds are breaking, package not found"

**Claude**:

1. **Diagnose** (2 min):
   - Check if pnpm install was run
   - Check if package uses workspace protocol
   - Check if pnpm-workspace.yaml includes packages

2. **Fix** (3 min):
   ```bash
   # Install dependencies
   pnpm install

   # Verify package is linked
   ls node_modules/@acme/ui  # Should be symlink

   # Update package.json to use workspace protocol
   # "dependencies": {
   #   "@acme/ui": "workspace:*"
   # }
   ```

**Expected time**: 5 minutes
**Output**: Working builds

---

## Integration Guidance for Claude

### SAP-020: React Foundation

**When user has Next.js 15**, setup monorepo with App Router:

```typescript
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

**Explain**: "I've set up monorepo with Next.js 15 App Router + shared Server Components"

---

### SAP-021: Testing

**When user has Vitest**, share config across packages:

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
import preset from '@acme/config/vitest-preset';
export default preset;
```

**Explain**: "I've created shared Vitest config in @acme/config for consistent testing"

---

### SAP-024: Styling

**When user has Tailwind**, share config across packages:

```typescript
// packages/config/tailwind-preset.ts
export const preset = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
      },
    },
  },
};

// apps/web/tailwind.config.ts
import { preset } from '@acme/config/tailwind-preset';

export default {
  presets: [preset],
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
  ],
};
```

**Explain**: "I've created shared Tailwind config for consistent design system"

---

## Common Pitfalls for Claude

### Pitfall 1: Not Using Workspace Protocol

**Problem**:
```json
// ❌ Wrong (tries to use npm)
{
  "dependencies": {
    "@acme/ui": "^1.0.0"
  }
}
```

**Fix**:
```json
// ✅ Correct (uses local)
{
  "dependencies": {
    "@acme/ui": "workspace:*"
  }
}
```

**Claude should always use workspace protocol** when adding dependencies.

---

### Pitfall 2: Forgetting transpilePackages

**Problem**: Hot reload doesn't work for shared packages

**Fix**:
```typescript
// next.config.ts
export default {
  transpilePackages: ['@acme/ui', '@acme/utils'],
};
```

**Claude should always add transpilePackages** for Next.js apps.

---

### Pitfall 3: Not Enabling Remote Cache

**Problem**: Builds are slow (5 min every time)

**Fix**:
```json
// turbo.json
{
  "remoteCache": {
    "enabled": true
  }
}
```

**Claude should always suggest remote caching** for faster builds.

---

### Pitfall 4: Recommending Wrong Tool

**Problem**: User has 3 packages → Claude recommends Nx (overkill)

**Fix**: Always ask clarifying questions:
- "How many packages do you have?" (3 → Turborepo or pnpm)
- "Do you need code generation?" (NO → Turborepo)

**Claude should ask before recommending** a tool.

---

### Pitfall 5: Not Using Affected Detection

**Problem**: CI runs all tests even if only 1 package changed

**Fix**:
```bash
# Turborepo: test only affected
turbo run test --filter=[origin/main...HEAD]

# Nx: test only affected
nx affected:test --base=origin/main
```

**Claude should always enable affected detection** in CI.

---

## Performance Optimization Tips for Claude

### 1. Enable Remote Caching

**Turborepo**:
```bash
npx turbo login
npx turbo link
```

**Explain**: "Remote caching enabled—90% faster builds"

---

### 2. Use Affected Detection

**CI workflow**:
```yaml
- run: turbo run test --filter=[origin/main...HEAD]
```

**Explain**: "CI runs only affected tests—90% faster"

---

### 3. Configure Outputs

**turbo.json**:
```json
{
  "pipeline": {
    "build": {
      "outputs": [".next/**", "dist/**"]
    }
  }
}
```

**Explain**: "Configured outputs for correct caching"

---

## Documentation Navigation for Claude

### When to Read Each Artifact

| User Request | Artifact to Read | Why |
|--------------|------------------|-----|
| "What is SAP-040?" | CLAUDE.md (this file) | Overview, decision tree |
| "Setup Turborepo" | adoption-blueprint.md (Option A) | Step-by-step, 20 min |
| "Setup Nx" | adoption-blueprint.md (Option B) | Step-by-step, 25 min |
| "How to add shared package?" | protocol-spec.md (How-To 1) | Complete guide |
| "How to enable remote cache?" | protocol-spec.md (How-To 2) | Caching setup |
| "Why Turborepo vs Nx?" | capability-charter.md | Tool comparison |
| "How much time savings?" | ledger.md (Evidence) | Metrics |

---

### Progressive Reading Strategy

**Small request** (e.g., "Setup Turborepo"):
- Read: adoption-blueprint.md (Option A only)
- Don't read: protocol-spec.md (too large)

**Medium request** (e.g., "Setup + remote caching"):
- Read: adoption-blueprint.md + protocol-spec.md (How-To sections)
- Don't read: capability-charter.md, ledger.md

**Large request** (e.g., "Design monorepo architecture"):
- Read: capability-charter.md (Solution Design) + protocol-spec.md (full)
- Skim: ledger.md (case studies)

---

## Quick Command Reference

### Turborepo

```bash
# Run task
turbo run build
turbo run test

# Filter by package
turbo run build --filter=@acme/ui

# Filter by affected
turbo run test --filter=[origin/main...HEAD]

# Force rebuild
turbo run build --force

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

# Run for all
nx run-many --target=build --all

# Run for affected
nx affected:build --base=origin/main

# Dependency graph
nx graph

# Generate component
nx generate @nx/react:component Button --project=ui
```

---

### pnpm workspaces

```bash
# Install dependencies
pnpm install

# Add dependency to package
pnpm add zod --filter @acme/ui

# Run script in package
pnpm --filter @acme/ui build

# Run script in all
pnpm -r build
```

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Three-tool architecture (Turborepo, Nx, pnpm workspaces)
  - Progressive context loading strategy
  - 4 code generation patterns
  - 4 workflow templates
  - Integration guidance (SAP-020, SAP-021, SAP-024)
  - Common pitfalls and fixes

---

**Status**: Pilot
**For**: Claude Code, Claude Desktop, Claude API
**Estimated Setup Time**: 50 minutes
**Time Savings**: 93.1% (8-12h → 50min)
**Next Review**: After 3 validation projects
