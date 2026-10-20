# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FABRK Framework is a monorepo that provides the first UI framework designed specifically for AI coding agents. It enables AI assistants (Claude Code, Cursor, GitHub Copilot, v0.dev) to build full-stack applications in minutes by importing pre-built components and tools instead of writing everything from scratch.

**Tech Stack:** TypeScript 5.x • pnpm workspaces • Turbo monorepo • React 19 • Next.js 16 • Changesets for versioning

**Requirements:** Node.js 22+ • pnpm 9+

**Source Material:** Code is being extracted from `/Users/jasonpoindexter/Documents/GitHub/_active/fabrk-dev` boilerplate

---

## Commands

```bash
# Setup
pnpm install              # Install all dependencies (run this first!)

# Development
pnpm dev                  # Build all packages in watch mode
pnpm build                # Build all packages for production
pnpm type-check           # TypeScript validation across all packages
pnpm lint                 # Lint all packages
pnpm test                 # Run tests across all packages
pnpm clean                # Remove all build artifacts

# Package-specific (from package directory)
cd packages/components
pnpm build                # Build single package
pnpm dev                  # Watch mode for single package

# Documentation
pnpm generate-docs        # Generate AGENTS.md files for AI agents

# Version Management
pnpm changeset            # Create a changeset for versioning
pnpm version-packages     # Version packages based on changesets
pnpm release              # Build and publish to npm
```

---

## Architecture

This is a **pnpm workspace monorepo** orchestrated by **Turbo**. Dependencies flow from foundational packages outward:

```
@fabrk/config (foundational — Zod schemas, no deps)
@fabrk/design-system (foundational — themes, no deps)
    ↓
@fabrk/core (depends on config, design-system)
    ↓
@fabrk/payments (depends on core)
@fabrk/auth (depends on core)
@fabrk/email (depends on core)
@fabrk/storage (depends on core)
@fabrk/security (depends on core)
    ↓
@fabrk/ai (depends on core)
@fabrk/components (depends on core, design-system)
    ↓
Templates & Examples (depend on all packages)
```

### Package Structure

```
fabrk-framework/
├── packages/
│   ├── core/              # @fabrk/core - Framework runtime, plugins, middleware, teams, jobs, flags
│   ├── components/        # @fabrk/components - 105+ UI components, 8 charts, dashboard shell, AI chat, admin, security
│   ├── ai/                # @fabrk/ai - AI toolkit (cost tracking, validation, streaming, prompts)
│   ├── design-system/     # @fabrk/design-system - 18 themes, design tokens
│   ├── config/            # @fabrk/config - Type-safe config builder (12 sections, Zod)
│   ├── payments/          # @fabrk/payments - Stripe, Polar, Lemon Squeezy adapters
│   ├── auth/              # @fabrk/auth - NextAuth, API keys, MFA (TOTP + backup codes)
│   ├── email/             # @fabrk/email - Resend adapter + email templates
│   ├── storage/           # @fabrk/storage - S3, R2, local filesystem adapters
│   ├── security/          # @fabrk/security - CSRF, CSP, rate limiting, audit, GDPR, CORS
│   └── cli/               # create-fabrk-app - CLI scaffolding tool
├── templates/             # Starter templates (basic, ai-saas, dashboard)
├── examples/              # Example applications (basic-usage, docs, saas-analytics, ecommerce)
└── docs/                  # Documentation
```

### Package Build System

Each package uses:
- **tsup** for building (ESM + CJS + TypeScript declarations)
- **TypeScript** for type checking
- Exports via `package.json` `exports` field for proper module resolution
- Source maps enabled for debugging
- Peer dependencies for React/Next.js to avoid version conflicts

Build order is handled automatically by Turbo based on `^build` dependencies in `turbo.json`.

---

## Key Design Patterns

### 1. Dynamic Design System (mode)

All components use the `mode` design system from `@fabrk/design-system` for theme-aware styling. The design system is **runtime-dynamic** via CSS variables.

**Critical Rules:**
- **Full borders** (`border`, `border-2`) → ALWAYS add `mode.radius`
- **Partial borders** (`border-t`, `border-b`, `border-l`, `border-r`) → NEVER add `mode.radius`
- **Table cells** (`<th>`, `<td>`) → NEVER add `mode.radius` (breaks layout)
- **Switches** → Always `rounded-full` (pill-shaped by design)

**Allowed:**
```tsx
import { mode } from '@fabrk/design-system'

// Full border - needs mode.radius
<Card className={cn("border border-border", mode.radius)}>

// Partial border - NO mode.radius
<div className="border-t border-border">

// Button with all mode properties
<Button className={cn(mode.radius, mode.font, "text-xs")}>
```

**Banned:**
```tsx
// Hardcoded colors break theme switching
<div className="bg-purple-500 text-white">

// Missing mode.radius on full border
<Card className="border rounded-lg">
```

### 2. Terminal Text Casing

| Element | Casing | Example |
|---------|--------|---------|
| UI Labels/Badges | UPPERCASE | `[SYSTEM]`, `[STATUS]` |
| Buttons | UPPERCASE with `>` prefix | `> SUBMIT`, `> CONTINUE` |
| Headlines (H1/H2) | UPPERCASE | `WELCOME TO YOUR APP` |
| Body Text | Normal sentence case | "Get started by..." |

**Never use underscores in user-facing text** - use spaces for readability.

### 3. Design Tokens Only

```tsx
// GOOD - Uses semantic tokens
className="bg-primary text-primary-foreground"
className="bg-card border-border"

// BAD - Hardcoded colors break theming
className="bg-blue-500 text-white"
className="bg-gray-100"
```

Available tokens:
- Backgrounds: `bg-background`, `bg-card`, `bg-muted`, `bg-primary`, `bg-secondary`, `bg-destructive`
- Text: `text-foreground`, `text-muted-foreground`, `text-primary`, `text-destructive`, `text-success`
- Borders: `border-border`, `border-primary`

### 4. Workspace Dependencies

Packages reference each other via `workspace:*` protocol:

```json
{
  "dependencies": {
    "@fabrk/design-system": "workspace:*",
    "@fabrk/core": "workspace:*"
  }
}
```

pnpm automatically links local packages during development.

---

## Development Workflow

### Adding Components

When extracting or adding components from fabrk-dev:

1. **Copy files to appropriate package:**
   ```bash
   # UI components
   cp -r ../fabrk-dev/src/components/ui/button.tsx packages/components/src/ui/

   # Charts
   cp -r ../fabrk-dev/src/components/charts/bar-chart.tsx packages/components/src/charts/
   ```

2. **Update imports:**
   ```tsx
   // Remove @ path aliases
   - import { cn } from '@/lib/utils'
   + import { cn } from '@fabrk/core'

   // Update design system imports
   - import { mode } from '@/design-system'
   + import { mode } from '@fabrk/design-system'
   ```

3. **Add to barrel export:**
   ```tsx
   // packages/components/src/index.ts
   export * from './ui/button'
   export * from './charts/bar-chart'
   ```

4. **Test build:**
   ```bash
   cd packages/components
   pnpm build
   ```

### Adding Features to Packages

1. Create feature files in package's `src/` directory
2. Export from package's `src/index.ts`
3. Run `pnpm type-check` to validate TypeScript
4. Run `pnpm build` to ensure it builds correctly
5. Create changeset: `pnpm changeset`

### Working Across Packages

When a change affects multiple packages:

1. Make changes in dependency order (design-system → core → components)
2. Build affected packages: `pnpm build`
3. Test dependents rebuild correctly
4. Create changesets for all affected packages

---

## Testing Changes

```bash
# Type check everything
pnpm type-check

# Build everything (verifies exports)
pnpm build

# Test specific package
cd packages/components
pnpm build
pnpm type-check

# Clean slate rebuild
pnpm clean
pnpm install
pnpm build
```

---

## Important Files

- **`pnpm-workspace.yaml`** - Defines workspace packages
- **`turbo.json`** - Build pipeline configuration
- **`tsconfig.json`** - Base TypeScript config (extended by packages)
- **`.changeset/config.json`** - Versioning configuration
- **`package.json` (root)** - Workspace scripts and shared dev dependencies
- **`packages/*/package.json`** - Individual package configs with exports

### Package.json Exports Pattern

```json
{
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}
```

This enables proper ESM/CJS dual-module support and TypeScript resolution.

---

## Critical Design System Rules

From DESIGN_SYSTEM_RULES.md (must preserve when extracting components):

1. **Full borders need mode.radius:**
   ```tsx
   <Card className={cn("border", mode.radius)}>
   ```

2. **Partial borders NO mode.radius:**
   ```tsx
   <div className="border-t"> // Correct
   ```

3. **Always use design tokens:**
   ```tsx
   className="bg-primary text-primary-foreground" // ✅
   className="bg-blue-500 text-white" // ❌
   ```

4. **Terminal text casing:**
   - Labels: UPPERCASE `[SYSTEM]`
   - Buttons: UPPERCASE with `>`: `> SUBMIT`
   - Headlines: UPPERCASE
   - Body: Normal case

---

## Component Extraction Process

This monorepo is being built by extracting code from the fabrk-dev boilerplate. When extracting:

### From fabrk-dev to this repo:

1. **Components:** `fabrk-dev/src/components/` → `packages/components/src/`
2. **AI utilities:** `fabrk-dev/src/lib/ai/` → `packages/ai/src/`
3. **Design system:** `fabrk-dev/src/design-system/` → `packages/design-system/src/`

### Import transformations:

```tsx
// fabrk-dev imports (path aliases)
import { Button } from '@/components/ui/button'
import { mode } from '@/design-system'
import { cn } from '@/lib/utils'

// Transform to framework imports (explicit packages)
import { Button } from '@fabrk/components'
import { mode } from '@fabrk/design-system'
import { cn } from '@fabrk/core'
```

### Preserve:

- All design system rules (see DESIGN_SYSTEM_RULES.md)
- Component prop types and interfaces
- Terminal aesthetic (monospace font, uppercase buttons, bracket labels)
- Accessibility attributes

### Remove:

- `@/` path aliases
- Next.js-specific imports (unless in templates)
- Application-specific business logic

---

## Git Workflow

```bash
# Make changes
git add .
git commit -m "feat: extract UI components from fabrk-dev"
git push origin main

# Use conventional commits
# feat: new feature
# fix: bug fix
# docs: documentation
# chore: maintenance
# refactor: code refactoring
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Type errors after adding dependency | Run `pnpm install` at root |
| Build fails on package | Check `tsconfig.json` extends root config |
| Import not found | Verify package exports in `package.json` |
| Turbo cache stale | Run `pnpm clean && pnpm build` |
| Workspace link broken | Delete `node_modules`, run `pnpm install` |

---

## Reference Documentation

Read these files for context:

- **CONTRIBUTING.md** - How to contribute (setup, adding components/adapters, design rules)
- **CHANGELOG.md** - Release history
- **DESIGN_SYSTEM_RULES.md** - Design rules to preserve
- **COMPONENT_INVENTORY.md** - List of all 105+ components

### Current Stats

- **20/20 packages build** (18 packages + 2 examples)
- **1,286 tests** across 38 files (unit + rendering + integration)
- **23/23 type-check**, **18/18 lint** (0 errors, 0 warnings)
- **105+ components**, 8 chart types, 18 themes
- **4 examples**: basic-usage, docs site, saas-analytics, ecommerce
- **Docs site**: 8 pages with Cmd+K search and sticky TOC

---

## For AI Agents Reading This

This framework exists to make YOUR job easier. Instead of generating 500 lines of custom components from scratch, you can:

```typescript
// When user says: "Build me a dashboard"
// You generate this:
import {
  DashboardShell, DashboardHeader, StatsGrid, TierBadge,
  BarChart, LineChart, KPICard, DataTable
} from '@fabrk/components'
import { mode } from '@fabrk/design-system'

export default function Dashboard() {
  return (
    <DashboardShell
      sidebarItems={[
        { id: 'overview', label: 'Overview', href: '/dashboard' },
        { id: 'repos', label: 'Repos', href: '/dashboard/repos' },
      ]}
      user={{ name: 'Jason', tier: 'pro' }}
      logo={<span className="text-accent text-xl">#</span>}
      onSignOut={() => signOut()}
    >
      <DashboardHeader title="Overview" />
      <StatsGrid items={[
        { label: 'Files', value: 1572 },
        { label: 'Components', value: 279, change: '+12%' },
      ]} />
      <LineChart data={weekTrend} />
    </DashboardShell>
  )
}
```

Result: Full dashboard with sidebar, responsive layout, KPIs, charts — in minutes.

Each package includes `AGENTS.md` files documenting all components, props, and usage examples specifically for AI consumption.
