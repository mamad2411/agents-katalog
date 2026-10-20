<!-- GSD:project-start source:PROJECT.md -->
## Project

**React Tauri Todo App**

A simple todo list app built with React and Tauri v2, targeting Android and iOS as native mobile apps. Lives in `apps/tauri-todo` within the monorepo. The purpose is to explore how Tauri works for mobile development — a self-contained experiment with no backend dependencies.

**Core Value:** Prove that Tauri v2 can build and install a React app as a native mobile app on Android and iOS.

### Constraints

- **Monorepo**: Must work within pnpm workspace and Turbo task orchestration
- **TypeScript**: Must use project TypeScript setup (shared tsconfig)
- **Tauri v2**: Must use latest stable Tauri v2 (not v1)
- **Mobile only**: Configure only Android and iOS targets
- **No backend**: All data stays on-device via Tauri Store plugin
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- TypeScript 5.9.3 - Used across all packages and applications for type-safe development
- JavaScript - Used in config files and build tooling
- JSX/TSX - React component syntax used in UI package and showcase app
## Runtime
- Node.js 24+ (specified in `package.json` engines field and `.nvmrc`)
- pnpm 10.29.3
- Lockfile: `pnpm-lock.yaml` (enforced with `preferFrozenLockfile: true`)
## Frameworks
- React 19.2.5 - UI library for building components
- React DOM 19.2.5 - React rendering for web
- Base UI React 1.4.0 - Headless component library for accessible UI components
- Tailwind CSS 4.2.2 - Utility-first CSS framework
- @tailwindcss/vite 4.2.2 - Vite plugin for Tailwind CSS integration
- @tailwindcss/postcss - PostCSS plugin for Tailwind CSS compilation
- PostCSS - CSS transformation tool (via postcss.config.mjs in UI package)
- Vite 8.0.8 - Fast build tool and dev server
- Turbo 2.9.6 - Monorepo task orchestration
- tsup 8.5.1 - TypeScript bundler (used for UI package and eslint-config)
- Playwright 1.59.1 - E2E testing framework (showcase app)
- Vitest 4.1.4 - Vite-native unit test framework
- @vitest/coverage-v8 4.1.4 - V8-based coverage provider
- ESLint 10.2.0 - JavaScript linting with flat config support
- Prettier 3.8.2 - Code formatter
- typescript-eslint 8.58.2 - TypeScript support for ESLint
- @eslint-react/eslint-plugin 4.2.3 - React-specific ESLint rules
- eslint-plugin-perfectionist 5.8.0 - Sorting plugins for consistency
- eslint-plugin-react-hooks 7.0.1 - React Hooks linting rules
- eslint-config-prettier 10.1.8 - Disables conflicting ESLint rules
- eslint-plugin-prettier 5.5.5 - Prettier integration for ESLint
- shadcn 4.2.0 - Component library CLI tool for adding pre-built components
- class-variance-authority 0.7.1 - Type-safe component variant creation
- clsx 2.1.1 - Conditional className utility
- tailwind-merge 3.5.0 - Merge Tailwind CSS classes intelligently
- lucide-react 1.8.0 - Icon library
- cmdk 1.1.1 - Command menu component
- date-fns 4.1.0 - Date manipulation library
- react-day-picker 9.14.0 - Calendar component
- embla-carousel-react 8.6.0 - Carousel component library
- input-otp 1.4.2 - OTP input component
- react-resizable-panels 4.10.0 - Resizable panel library
- recharts 3.8.0 - React charting library
- sonner 2.0.7 - Toast notification library
- vaul 1.1.2 - Drawer component library
- next-themes 0.4.6 - Theme switching utility
- tw-animate-css 1.4.0 - Tailwind animation utilities
- @fontsource-variable/inter 5.2.8 - Inter variable font
- @testing-library/react 16.3.2 - React component testing utilities
- @testing-library/jest-dom 6.9.1 - Custom Jest matchers for DOM
- @testing-library/user-event 14.6.1 - User event simulation for testing
- jsdom 29.0.2 - JavaScript implementation of web standards for testing
- rimraf 6.1.3 - Cross-platform file deletion utility
- glob 13.0.6 - File pattern matching (used in tsup config)
- globals 17.5.0 - Global object/variable definitions for linting
- husky 9.1.7 - Git hooks manager
- @commitlint/cli 20.5.0 - Commit message linting
- @commitlint/config-conventional 20.5.0 - Conventional commits config
## Configuration
- No `.env` files detected - This is a template/showcase project with no external dependencies requiring secrets
- Configuration primarily through `tsconfig.base.json` with esnext target and bundler module resolution
- Turbo configuration: `turbo.json` - Defines task dependencies, caching, and inputs/outputs
- TypeScript: `tsconfig.base.json` - Base config with strict mode, module detection, noUncheckedIndexedAccess enabled
- Prettier: `.prettierrc` - Semi-colon disabled, 120 character print width
- PostCSS: `packages/ui/postcss.config.mjs` - Loads Tailwind CSS PostCSS plugin
- pnpm workspaces: `pnpm-workspace.yaml` - Defines workspace packages in `apps/*` and `packages/*`
- Catalog dependencies: All testing, type, and tooling packages use pnpm catalog for version management
- Dedupe enabled: `dedupePeerDependents: true`
## Platform Requirements
- Node.js >= 24
- pnpm 10.29.3
- System supporting Node.js v24
- No backend/server infrastructure required - This is a frontend component library and showcase application
- Deployment target: Static site hosting (compatible with any static host via Vite output)
## Workspace Structure
- `packages/ui` - React component library with export subpaths for components, hooks, CSS, and utilities
- `packages/tsconfig` - Shared TypeScript configuration with base config extending @tsconfig/node24
- `packages/eslint-config` - Shared ESLint and Prettier configuration with node and react presets
- `apps/showcase` - Vite + React showcase application demonstrating UI components, includes E2E tests with Playwright
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- kebab-case for all files: `button-group.tsx`, `utils.test.ts`, `eslint.config.ts`
- Component files use `.tsx` extension
- Test files use `.test.ts` or `.spec.ts` suffix
- camelCase for all functions: `mergeProps()`, `useRender()`, `cn()`
- React components use PascalCase: `ButtonGroup`, `Tabs`, `Card`
- camelCase for all variable declarations: `buttonGroupVariants`, `className`, `orientation`
- Exported constants use camelCase: `node` (ESLint config), `react` (ESLint config)
- PascalCase for all types: `VariantProps`, `ComponentProps`
- Import types using `import type` syntax: `import type { VariantProps } from "class-variance-authority"`
- Generic type parameters prefixed with `T`: `TItem` (though rarely used in this codebase)
## Code Style
- Prettier with configuration: `{ "semi": false, "printWidth": 120 }`
- No semicolons at end of statements
- 120 character line width
- Config file: `.prettierrc`
- ESLint with flat config (v9+)
- Separate configs for Node and React:
- Config files: `eslint.config.ts` (not `.eslintrc.json`)
- `@typescript-eslint/consistent-type-imports`: error — enforces `import type` for type-only imports
- `perfectionist/sort-imports`: error — alphabetically sorts imports
- `prettier/prettier`: warn — integration with Prettier
- React-specific rules:
## Import Organization
- `@ui` — maps to `packages/ui/src` (used in tests)
- `@monorepo-template/ui` — package export name (used in apps)
- `@` — maps to `src` root in app projects (e.g., `@/components/example`)
## Error Handling
- No explicit try-catch patterns found in codebase
- Functions do not use Result types
- Components assume props are valid; no runtime validation
- React components rely on TypeScript for type safety
## Logging
- No logging calls found in component code
- Logging reserved for development/debugging only
## Comments
- JSDoc comments for complex Playwright test suites (describe blocks)
- Comments explaining configuration choices (e.g., `export default defineConfig` comment in `playwright.config.ts`)
- Minimal inline comments — code is expected to be self-documenting
- Rarely used — code clarity prioritized over inline documentation
- Example from `playwright.config.ts`:
## Function Design
- Prefer smaller, focused functions
- Components typically 10-50 lines (including JSX)
- Utility functions very concise (e.g., `cn()` is 3 lines)
- Accept React.ComponentProps spreads for flexibility: `React.ComponentProps<"div">`, `TabsPrimitive.List.Props`
- Use destructuring with rest operator: `{ className, orientation, ...props }`
- Props grouped at end of parameters: `...props`
- JSX components return single JSX element
- Utility functions return typed values: `cn()` returns `string`
- No explicit return type annotations on React components
## Module Design
- Named exports only (no default exports per project guidelines)
- Multiple related functions exported together: `export { ButtonGroup, ButtonGroupSeparator, ButtonGroupText, buttonGroupVariants }`
- Path aliases used for clean imports
- Index files re-export from components: `export { Button } from "./button"`
- Allows `import { Button } from "@monorepo-template/ui/components/button"`
## Type Patterns
- Not heavily used in this codebase
- Test suites use clear, single-responsibility functions
- Prefer `prop?: Type` over `prop: Type | undefined`
- Example: `className?: string`, `orientation?: "horizontal" | "vertical"`
- Used extensively for component variants
- Pattern: `const variantName = cva("base classes", { variants: { ... } })`
- Variant props destructured from `VariantProps<typeof variantName>`
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- Workspace-based monorepo (pnpm) with two main workspaces: `/apps` and `/packages`
- Centralized UI component library (`@monorepo-template/ui`) providing reusable React components
- Showcase application (`apps/showcase`) demonstrates all UI components
- Build pipeline orchestrated through Turbo with task dependencies and caching
- Strict TypeScript with `noUncheckedIndexedAccess` enabled across all packages
- Component styling via Tailwind CSS + CVA (Class Variance Authority) for variants
## Layers
- Purpose: Orchestrate builds, linting, and testing across all workspaces
- Location: `/Users/pauvelascogarrofe/Documents/base-monorepo-template`
- Contains: Root `package.json`, Turbo configuration, TypeScript base config, shared tooling
- Depends on: pnpm workspaces, Turbo, shared dev dependencies
- Used by: All workspace packages through npm/pnpm resolution
- Purpose: Shared, reusable code and configurations
- Location: `/packages`
- Contains: UI component library, ESLint config, TypeScript configs
- Depends on: React, Tailwind CSS, @base-ui/react
- Used by: Apps and other packages via workspace dependencies
- Purpose: Centralized collection of accessible React UI components
- Location: `/packages/ui/src`
- Contains: 50+ components, custom hooks, utility functions
- Depends on: @base-ui/react (headless components), class-variance-authority, clsx, tailwind-merge
- Used by: `apps/showcase` and external consumers via npm exports
- Purpose: End-user applications that consume packages
- Location: `/apps`
- Contains: Showcase application
- Depends on: @monorepo-template/ui, React, Vite, Tailwind CSS
- Used by: End users and developers
- Purpose: Interactive demonstration and testing environment for all UI components
- Location: `/apps/showcase/src`
- Contains: Component category pages, example compositions, Vite/React entry points
- Depends on: @monorepo-template/ui, @base-ui/react, Vite, Playwright (E2E)
- Used by: Developers, designers, and QA for component validation
## Data Flow
- No centralized state management; components are presentational
- Props passed down from showcase category files to component instances
- Each component fully controlled by parent (showcase category pages)
- Test examples use `useCallback`, `useState` for demonstration
## Key Abstractions
- Purpose: Styled wrapper around headless primitives from @base-ui/react
- Examples: `packages/ui/src/components/button.tsx`, `packages/ui/src/components/accordion.tsx`
- Pattern: Named exports of sub-components (e.g., `Button`, `ButtonGroup` with multiple exports)
- Implementation example (Button):
- Purpose: Type-safe, maintainable component variants
- Examples: `buttonVariants` in `packages/ui/src/components/button.tsx`
- Pattern: `cva()` defines base classes and variant combinations
- Extracts variant and size from props, generates optimized Tailwind classes
- Purpose: Shared helper functions across components
- Location: `packages/ui/src/lib/utils.ts`
- Key function: `cn()` merges class names with Tailwind deduplication
- Pattern: Wraps `clsx` + `tailwind-merge` for safe class composition
- Purpose: Reusable React logic
- Location: `packages/ui/src/hooks/`
- Key hook: `useIsMobile()` - detects viewport size via media query
- Pattern: Returns boolean state synced with window resize/media query changes
- Purpose: Cleaner imports and API surface
- Location: `packages/ui/src/index.ts`
- Pattern: Re-exports all components and utilities in one file
- Allows: `import { Button } from '@monorepo-template/ui'`
## Entry Points
- Location: `turbo.json`
- Triggers: `pnpm dev` spawns Vite + watch processes for each workspace
- Responsibilities: Coordinate workspace development builds
- Location: `apps/showcase/src/main.tsx`
- Triggers: Vite bundler creates development server on dev command
- Responsibilities: Initialize React app, render App component with StrictMode
- Code: Imports global styles, mounts App to DOM
- Location: `apps/showcase/src/app.tsx`
- Triggers: Called from main.tsx
- Responsibilities: Render ComponentExample (the showcase page)
- Code: Single-line component returning ComponentExample instance
- Location: `apps/showcase/src/components/component-example.tsx`
- Triggers: Called from App
- Responsibilities: Render tabbed interface with 6 component category sections
- Pattern: Tabs control which category examples display; each category is imported separately
- Location: `packages/ui/src/index.ts`
- Triggers: Build process exports this as library entry point
- Responsibilities: Re-export all public components, hooks, utilities
- Exports handled through `exports` field in `packages/ui/package.json` with subpath exports
## Error Handling
- Test files use `expect()` assertions from Vitest to validate expected behavior
- Components assume valid props; no runtime validation (TypeScript provides compile-time safety)
- Event handlers wrapped in async `userEvent.setup()` during testing for proper async handling
## Cross-Cutting Concerns
- `tailwind.config.ts` (if present) or inherited from Tailwind defaults
- CSS reset and custom variables in `packages/ui/src/styles/globals.css`
- Component-level utility: `cn()` function for safe class merging
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

| Skill | Description | Path |
|-------|-------------|------|
| shadcn | Manages shadcn components and projects — adding, searching, fixing, debugging, styling, and composing UI. Provides project context, component docs, and usage examples. Applies when working with shadcn/ui, component registries, presets, --preset codes, or any project with a components.json file. Also triggers for "shadcn init", "create an app with --preset", or "switch to --preset". | `.agents/skills/shadcn/SKILL.md` |
| tauri-v2 | "Tauri v2+ cross-platform app development with Rust backend. Use when configuring tauri.conf.json, implementing Rust commands (#[tauri::command]), setting up IPC patterns (invoke, emit, channels), configuring permissions/capabilities, troubleshooting build issues, or deploying desktop/mobile apps. Triggers on Tauri, src-tauri, invoke, emit, capabilities.json." | `.agents/skills/tauri-v2/SKILL.md` |
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
