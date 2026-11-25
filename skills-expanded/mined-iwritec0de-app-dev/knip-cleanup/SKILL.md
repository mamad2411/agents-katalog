---
name: knip-cleanup
description: >-
  This skill should be used when the user asks to "find unused code", "clean up
  dead code", "find unused dependencies", "find unused exports", "find unused
  files", "remove dead code", "run knip", "check for unused imports", "clean up
  dependencies", "prune unused packages", or mentions "knip", "dead code
  detection", "unused exports", "unused dependencies", "unused files",
  "dependency cleanup", "export cleanup". Provides expert guidance on using knip
  for JavaScript/TypeScript project cleanup including configuration, analysis,
  auto-fixing, and safe removal workflows.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Knip — Dead Code & Dependency Cleanup

Knip finds unused files, dependencies, exports, types, and duplicate packages in JavaScript/TypeScript projects. Use this skill to analyze, report, and safely clean up projects.

## What Knip Detects

| Category | Description | Risk Level |
|----------|-------------|------------|
| Unused files | Source files not imported anywhere | Medium |
| Unused dependencies | Packages in `dependencies`/`devDependencies` not imported | High — safe to remove |
| Unlisted dependencies | Packages imported but not in `package.json` | Critical — must add |
| Unused exports | Named exports not consumed by other modules | Low — may be public API |
| Unused types | TypeScript types/interfaces not referenced | Low |
| Duplicate packages | Same package at multiple versions in lockfile | Medium |
| Unused binaries | Binaries declared but not used in scripts | Low |
| Unresolved imports | Imports that point to missing modules | Critical |

## Installation

```bash
# Install as dev dependency (recommended)
pnpm add -D knip

# Or run without installing
pnpm dlx knip
```

## Configuration

Knip works zero-config for many projects but supports `knip.json`, `knip.jsonc`, `.knip.json`, `knip.ts`, or a `knip` key in `package.json`.

### Basic Config (`knip.json`)

```json
{
  "$schema": "https://unpkg.com/knip@latest/schema.json",
  "entry": ["src/index.ts", "src/main.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["**/*.test.ts", "**/*.spec.ts"],
  "ignoreDependencies": ["@types/node"]
}
```

### Monorepo Config

```json
{
  "$schema": "https://unpkg.com/knip@latest/schema.json",
  "workspaces": {
    "packages/*": {
      "entry": ["src/index.ts"],
      "project": ["src/**/*.ts"]
    },
    "apps/web": {
      "entry": ["src/main.tsx", "next.config.{js,ts}"],
      "project": ["src/**/*.{ts,tsx}"]
    }
  }
}
```

### Common Framework Configurations

**Next.js:**
```json
{
  "entry": [
    "src/app/**/page.tsx",
    "src/app/**/layout.tsx",
    "src/app/**/route.ts",
    "src/app/**/loading.tsx",
    "src/app/**/error.tsx",
    "src/app/**/not-found.tsx",
    "src/middleware.ts",
    "next.config.{js,ts,mjs}"
  ],
  "project": ["src/**/*.{ts,tsx}"]
}
```

**Vite/React:**
```json
{
  "entry": ["src/main.tsx", "vite.config.ts"],
  "project": ["src/**/*.{ts,tsx}"]
}
```

**Express/Node API:**
```json
{
  "entry": ["src/index.ts", "src/server.ts"],
  "project": ["src/**/*.ts"],
  "ignoreDependencies": ["@types/express"]
}
```

## Built-in Plugin Support

Knip has built-in plugins for common tools and frameworks. These automatically detect entry points so you don't need to configure them manually:

- **Frameworks:** Next.js, Remix, Astro, Nuxt, Svelte, Angular, Gatsby
- **Build tools:** Vite, Webpack, Rollup, esbuild, tsup, Turbopack
- **Testing:** Jest, Vitest, Mocha, Playwright, Cypress, Storybook
- **Linting:** ESLint, Prettier, Stylelint, lint-staged, commitlint
- **Bundlers/Config:** TypeScript, Babel, PostCSS, Tailwind CSS
- **CI/CD:** GitHub Actions, Husky, Lefthook
- **Other:** Prisma, Drizzle, GraphQL Codegen, Sentry, MSW

When a plugin detects its config file, it automatically adds the right entry points. Override or extend with explicit config only when needed.

## Running Knip

### Basic Commands

```bash
# Full scan — all issue types
pnpm knip

# Specific reporters
pnpm knip --reporter compact    # Condensed output
pnpm knip --reporter json       # Machine-readable JSON
pnpm knip --reporter markdown   # Markdown table format

# Filter by issue type
pnpm knip --include files           # Only unused files
pnpm knip --include dependencies    # Only unused deps
pnpm knip --include exports         # Only unused exports
pnpm knip --include types           # Only unused types
pnpm knip --include duplicates      # Only duplicate packages
pnpm knip --include unlisted        # Only unlisted deps

# Exclude issue types
pnpm knip --exclude exports    # Everything except unused exports

# Production mode (skip devDependencies analysis)
pnpm knip --production

# Strict mode (also flag re-exports and namespace imports as unused)
pnpm knip --strict

# Show which plugins are activated
pnpm knip --debug

# Performance profiling
pnpm knip --performance
```

### Auto-Fix Mode

```bash
# Remove unused exports and dependencies automatically
pnpm knip --fix

# Preview what --fix would change (dry run)
pnpm knip --fix --dry-run

# Only fix specific categories
pnpm knip --fix --include exports
pnpm knip --fix --include dependencies

# Remove unused files (moves to trash by default if trash-cli is installed)
pnpm knip --fix --allow-remove-files
```

**Important `--fix` behavior:**
- Removes unused `export` keywords from declarations
- Removes unused dependency entries from `package.json`
- Does NOT delete files unless `--allow-remove-files` is passed
- Does NOT run your package manager's install after removing deps — you must run `pnpm install` after
- Always review changes with `git diff` after running `--fix`

## Safe Removal Workflow

Follow this order when cleaning up knip findings to avoid cascading false positives:

### Step 1: Fix Unlisted Dependencies First
```bash
pnpm knip --include unlisted
# Add any missing packages to package.json
pnpm add <missing-package>
```

### Step 2: Remove Unused Dependencies
```bash
pnpm knip --include dependencies --fix
pnpm install   # Regenerate lockfile
```

### Step 3: Remove Unused Exports
```bash
# Preview first
pnpm knip --include exports --fix --dry-run
# Then apply
pnpm knip --include exports --fix
```

### Step 4: Remove Unused Files
```bash
# List unused files
pnpm knip --include files
# Review each file manually before deletion
# Only use --allow-remove-files when confident
```

### Step 5: Verify Nothing Broke
```bash
pnpm tsc --noEmit       # Type check
pnpm test               # Run tests
pnpm build              # Verify build
pnpm knip               # Re-run to confirm clean
```

## Handling False Positives

Knip may flag things as unused that are actually needed:

### Dynamic imports / runtime usage
```json
{
  "ignoreDependencies": ["sharp", "pg-native"]
}
```

### Exports consumed by external packages (library authors)
```json
{
  "entry": ["src/index.ts!"],
  "ignore": ["src/internal/**"]
}
```
The `!` suffix means "include all exports from this entry as used."

### Framework magic (decorators, auto-imports, etc.)
Use the appropriate plugin or add explicit entry points.

### Per-file export ignore
```typescript
/** @public */
export function myPublicAPI() {} // knip respects JSDoc @public tag
```

Or use the `@knip` tag in comments:
```typescript
// @knip — used by external consumers
export const API_VERSION = "2.0";
```

### Ignore patterns
```json
{
  "ignore": [
    "**/*.d.ts",
    "**/generated/**",
    "scripts/**"
  ],
  "ignoreDependencies": [
    "@types/*",
    "dotenv"
  ]
}
```

## Interpreting Results

When presenting knip results:

1. **Group by severity** — unlisted deps and unresolved imports are critical; unused types are informational
2. **Check before removing exports** — they may be part of a public API consumed by other packages
3. **Cross-reference unused deps** — check if they're used in scripts, CI configs, or Dockerfiles that knip doesn't scan
4. **Unused files** — verify they aren't dynamically imported, used as templates, or referenced in config files
5. **Duplicate packages** — these bloat bundles; resolve by aligning versions in `package.json` or using `pnpm dedupe`

## Integration with Quality Gate

Knip is included in the quality gate as a WARN-level check. For standalone deep analysis, use the `/knip` command instead, which provides more granular control and guided cleanup workflows.
