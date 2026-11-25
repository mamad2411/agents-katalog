---
name: kumo-ui-agents
description: Official Kumo UI agent/LLM context from the Cloudflare team's AGENTS.md. Covers the monorepo structure, where to find component implementations, how codegen works, CLI commands, and key architectural decisions. Trigger when working on or within the Kumo UI codebase itself, contributing new components, or needing to understand internal architecture.
---

# Kumo UI — Agent Context (AGENTS.md)

> Source: [`packages/kumo/AGENTS.md`](https://github.com/cloudflare/kumo/blob/main/packages/kumo/AGENTS.md)

React component library: **Base UI + Tailwind v4 + Vite library mode**. ESM-only, tree-shakeable per-component exports.

---

## Package Structure

```
packages/kumo/
├── src/
│   ├── components/          # 39 UI components → see src/components/AGENTS.md
│   ├── blocks/              # Installable blocks (NOT library exports; via CLI `kumo add`)
│   ├── primitives/          # AUTO-GENERATED Base UI re-exports (40 files)
│   ├── catalog/             # JSON-UI rendering runtime (DynamicValue, visibility conditions)
│   ├── code/                # Shiki-based code highlighting (lazy-loaded, 16 bundled languages)
│   ├── command-line/        # CLI: ls, doc, add, blocks, init, migrate
│   ├── styles/              # CSS: kumo-binding.css + theme files (AUTO-GENERATED)
│   ├── utils/               # cn(), safeRandomId, LinkProvider
│   ├── registry/            # Type-only exports for registry metadata
│   └── index.ts             # Main barrel export (PLOP_INJECT_EXPORT marker)
├── ai/                      # AUTO-GENERATED: component-registry.{json,md}, schemas.ts
├── scripts/
│   ├── component-registry/  # Registry codegen (13 sub-modules, 930+ lines orchestrator)
│   ├── theme-generator/     # Theme CSS codegen from config.ts
│   ├── generate-primitives.ts
│   └── css-build.ts         # Post-Vite CSS processing
├── lint/                    # 5 custom oxlint rules (superset of root lint/)
├── tests/imports/           # Structural validation: export paths, package.json, build entries
├── vite.config.ts           # Library mode, dynamic primitive discovery, PLOP marker
└── vitest.config.ts         # happy-dom, v8 coverage, path aliases
```

---

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Component implementation | `src/components/{name}/{name}.tsx` | Always check registry first |
| Component API reference | `ai/component-registry.json` | **Source of truth** for props/variants |
| Variant definitions | `KUMO_{NAME}_VARIANTS` export in component file | Machine-readable + lint-enforced |
| CLI commands | `src/command-line/commands/` | `ls`, `doc`, `add`, `blocks`, `init`, `migrate` |
| Catalog runtime | `src/catalog/` | JSON pointer resolution, visibility conditions |
| Code highlighting | `src/code/` | ShikiProvider, lazy-loaded highlighter, 16 bundled languages |
| Blocks source | `src/blocks/{name}/` | Installed to consumers via CLI, not exported |
| Theme tokens | `scripts/theme-generator/config.ts` | Edit this, then run `pnpm codegen:themes` |
| Auto-generated primitives | `src/primitives/` | Never edit directly, run `pnpm codegen:primitives` |
| Custom lint rules | `lint/` | 5 oxlint rules enforcing variant typing and structure |

---

## CLI Commands

```bash
# List all components and blocks
npx @cloudflare/kumo ls

# Get component documentation (triggers registry lookup)
npx @cloudflare/kumo doc Button
npx @cloudflare/kumo doc Select

# Scaffold a block into your project source
npx @cloudflare/kumo add PageHeader
npx @cloudflare/kumo add ResourceList
npx @cloudflare/kumo add DeleteResource

# Initialize Kumo in a new project
npx @cloudflare/kumo init

# Migrate from an older Kumo version
npx @cloudflare/kumo migrate
```

---

## Codegen Commands (Monorepo Dev Only)

```bash
# Regenerate all auto-generated files
pnpm codegen

# Individual targets:
pnpm codegen:registry    # Regenerate ai/ directory (component-registry.json/.md, schemas.ts)
pnpm codegen:themes      # Regenerate theme CSS from scripts/theme-generator/config.ts
pnpm codegen:primitives  # Regenerate src/primitives/ from Base UI
```

> **Never hand-edit files in `ai/`, `src/primitives/`, or `src/styles/theme-*.css`** — they are overwritten on every codegen run.

---

## Key Architectural Rules

### 1. Component Variant System
Every component with variants must:
- Export a `KUMO_{NAME}_VARIANTS` const with all valid values
- This const is machine-readable, lint-enforced, and referenced by the registry

```typescript
// ✅ Required pattern for any component with variants
export const KUMO_BADGE_VARIANTS = {
  variant: ["info", "warning", "success", "danger", "orange", "teal", "neutral"],
  size: ["sm", "md"],
} as const;
```

### 2. New Component Scaffold
Use PLOP to scaffold new components consistently:
```bash
# In the monorepo root
pnpm plop component
```
This creates the component file, tests, and injects the export into `index.ts` at the `PLOP_INJECT_EXPORT` marker.

### 3. ESM-Only, Tree-Shakeable
- All exports are ESM-only (no CJS)
- Each component has its own export path for granular imports:
  ```tsx
  // Full import (via barrel)
  import { Button } from "@cloudflare/kumo";
  
  // Granular import (smaller bundle)
  import { Button } from "@cloudflare/kumo/components/button";
  ```

### 4. Blocks are NOT Exports
Blocks (`src/blocks/`) are **never exported** from the package. They are template source files that the CLI copies into consumer projects via `kumo add`. Once installed, they belong to the consumer's codebase and can be modified freely.

### 5. Primitives are Auto-Generated
`src/primitives/` contains ~40 re-export files wrapping Base UI primitives. Never edit these — run `pnpm codegen:primitives` after adding new Base UI dependencies.

---

## Test Structure

```bash
# Run all tests
pnpm test

# Import validation (ensures all export paths and package.json entries are correct)
pnpm test:imports

# Component tests
pnpm vitest
```

Import validation tests (`tests/imports/`) are particularly important — they verify that the package exports are structurally sound before publishing.

---

## Parent Context

See the [root AGENTS.md](https://github.com/cloudflare/kumo/blob/main/AGENTS.md) for monorepo-wide context covering the full Kumo monorepo (docs site, design tokens, shared tooling, etc.).
