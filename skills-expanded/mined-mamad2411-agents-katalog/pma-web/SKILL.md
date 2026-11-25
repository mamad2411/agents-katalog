---
name: pma-web
description: Frontend implementation guide for React 19 + TypeScript + Vite 8 monorepo projects. Covers tech stack, project structure (bun workspaces), state management (TanStack Query for async requests + Zustand for client state), UI (shadcn/ui + Tailwind CSS 4.2), theming (light/dark/system), i18n (react-i18next), routing (React Router 7), and coding conventions. Use when scaffolding, developing, or reviewing frontend web applications.
---

# Web Frontend Implementation Guide

Standard frontend stack and conventions for web application projects.

## Tech Stack

| Category | Technology | Version | Notes |
|---|---|---|---|
| **Core** ||||
| Framework | React | 19.2 | |
| Language | TypeScript | 5.9 | strict mode |
| Build tool | Vite | 8 | host: `0.0.0.0`, allowedHosts: `true` |
| Package manager | bun workspaces | — | monorepo |
| **Routing & State** ||||
| Router | React Router | 7 | lazy routes for code splitting |
| Async state | TanStack Query | 5.90 | request caching, refetch, sync |
| Client state | Zustand | 5.0 | UI-only state |
| **UI & Styling** ||||
| Component library | shadcn/ui + Base UI | — | |
| CSS | Tailwind CSS | 4.2 | `@theme` + CSS variables |
| Theming | shadcn/ui ThemeProvider | — | [official Vite guide](https://ui.shadcn.com/docs/dark-mode/vite), light / dark / system |
| **i18n** ||||
| Internationalization | react-i18next | — | i18next-http-backend for lazy loading |
| **Tooling** ||||
| Lint / format | ESLint + @antfu/eslint-config | 10 / 7.7 | |

## Monorepo Structure

```
bunfig.toml
bun.lock
package.json                     # workspaces: ["apps/*", "packages/*"]
apps/
  web/
    src/
      app/
        providers.tsx             # compose all Providers
        router.tsx                # React Router 7 route config
        i18n.ts                   # i18n initialization
      features/                   # organized by business domain
        auth/
          components/
          hooks/
          api.ts                  # TanStack Query hooks
          store.ts                # Zustand store (if needed)
          routes.tsx
        dashboard/
          ...
      shared/
        components/
          ui/                     # shadcn/ui components
          theme-provider.tsx      # shadcn/ui official ThemeProvider
          mode-toggle.tsx         # shadcn/ui official ModeToggle
        hooks/
        lib/
          http.ts                 # fetch wrapper
          query-client.ts         # TanStack Query client
        types/
      styles/
        theme.css                 # CSS variables & design tokens
    index.html
    vite.config.ts
    tsconfig.json
    package.json
packages/
  config/                           # @repo/config — shared configs
    tsconfig/
      base.json                     # module: NodeNext, strict: true, target: ES2022
      react.json                    # extends base, module: ESNext, jsx: react-jsx
      utils.json                    # extends base, declaration: true
    package.json
  shared/                           # @repo/shared — cross-workspace types
    src/
      index.ts                      # domain types, API types, shared constants
    package.json
eslint.config.ts
```

## bun workspaces

- Root `package.json` declares `"workspaces": ["apps/*", "packages/*"]`
- `bunfig.toml` for workspace-level options
- Use `bun install` instead of `pnpm install`
- Run scripts: `bun run --filter apps/web dev`
- Cross-package references: `"@repo/config": "workspace:*"`, `"@repo/shared": "workspace:*"`

## packages/config — Shared Configs

Shared TypeScript configs for all workspaces:

| File | Purpose |
|---|---|
| `tsconfig/base.json` | Base: `module: NodeNext`, `strict: true`, `target: ES2022` |
| `tsconfig/react.json` | Extends base: `module: ESNext`, `moduleResolution: bundler`, `jsx: react-jsx`, `noEmit: true` |
| `tsconfig/utils.json` | Extends base: `noEmit: true`, `declaration: true` |

Each app's `tsconfig.json` extends the appropriate config:

```json
{
  "extends": "@repo/config/tsconfig/react.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

## packages/shared — Cross-Workspace Types

Single entry point exporting all shared types:

- Domain types (entities, enums, constants)
- API types (`ApiResponse<T>`, request/response shapes)
- Use `import type` for type-only imports across workspaces

## State Management

| Data type | Solution |
|---|---|
| Async/request state | TanStack Query |
| Client UI state | Zustand |
| Theme | shadcn/ui ThemeProvider (single source of truth) |
| Forms | Controlled components or react-hook-form |

## Theming

- Use [shadcn/ui official Vite dark mode guide](https://ui.shadcn.com/docs/dark-mode/vite)
- ThemeProvider is the single source of truth — do not mix with Zustand
- Support light / dark / system modes
- Persist via `localStorage`
- Tailwind 4.2 `@theme` defines design tokens; `.dark` class toggles variable values

## i18n

- react-i18next + i18next-http-backend for lazy loading
- Namespace per feature: common, auth, dashboard, etc.
- Language files at `public/locales/{{lng}}/{{ns}}.json`
- Support zh-CN and en, fallback to zh-CN
- Auto-detect via i18next-browser-languagedetector

## Provider Composition Order

```
I18nextProvider
  └─ QueryClientProvider
       └─ ThemeProvider
            └─ App
```

## Conventions

| Area | Convention |
|---|---|
| API layer | Each feature exports `useXxxQuery` / `useXxxMutation` from `api.ts` |
| Routing | Feature-level `routes.tsx` defines sub-routes; `app/router.tsx` aggregates with lazy imports |
| Components | shadcn/ui → `shared/components/ui/`; business components → within each feature |
| Naming | Files: kebab-case; Components: PascalCase; Hooks: `use-xxx.ts` |
| Path alias | `@/` → `src/` |
| Imports | `import type` required for type-only imports |
| Styling | `cn()` = `twMerge(clsx(...))` from `lib/utils.ts` |

## ESLint

- `@antfu/eslint-config` with `type: 'app'`, TypeScript, React
- No Prettier — ESLint handles formatting
- Stylistic: 2-space indent, single quotes, no semicolons
- Ignore shadcn/ui generated components: `src/components/ui/**`

## Vite Config

```ts
// vite.config.ts
export default defineConfig({
  plugins: [
    tailwindcss(),        // @tailwindcss/vite
    tsConfigPaths(),      // vite-tsconfig-paths
    react(),              // @vitejs/plugin-react
  ],
  server: {
    host: '0.0.0.0',
    allowedHosts: true,
  },
})
```

## shadcn/ui Initialization

### Step 1: Init shadcn in the app directory

```bash
cd apps/web
bunx shadcn@latest init
```

Select these options:
- Style: `base-nova`
- Base color: `neutral`
- CSS variables: yes
- RSC: no (Vite, not Next.js)
- Icon library: `lucide`

This generates `components.json`:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "base-nova",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

### Step 2: Add components

```bash
# Add individual components
bunx shadcn@latest add button card dialog

# Add theme components for dark mode
bunx shadcn@latest add sonner
```

### Step 3: Theme setup (dark mode)

Follow the [official Vite dark mode guide](https://ui.shadcn.com/docs/dark-mode/vite):

1. Create `src/shared/components/theme-provider.tsx` — ThemeProvider context
2. Create `src/shared/components/mode-toggle.tsx` — theme switcher UI
3. Wrap app with `<ThemeProvider defaultTheme="system" storageKey="ui-theme">`

### Notes

- shadcn/ui components are generated into `src/shared/components/ui/` — they are **owned code**, not a dependency.
- ESLint should ignore `src/shared/components/ui/**` (generated code).
- Always use `bunx shadcn@latest add` to add new components, not manual copy.

## Tailwind CSS v4

```css
/* src/index.css */
@import 'tailwindcss';
@import 'tw-animate-css';

@custom-variant dark (&:is(.dark *));

@theme inline {
  /* map CSS variables to Tailwind color tokens */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  /* ... */
}
```
