---
name: expo-bulletproof-structure
description: Bulletproof Expo project structure pattern for React Native apps. Enforces thin routing layer, feature-based modules, dependency direction rules, and Expo Router conventions. Use when creating files, scaffolding features, or making architectural decisions in any Expo/React Native project.
metadata:
  author: voitz
  version: "1.0.0"
---

# Bulletproof Expo Structure

Project structure pattern for Expo/React Native apps. Adapted from Bulletproof React for the mobile ecosystem with Expo Router's file-based routing.

## Core Principle

The `app/` directory is a **thin routing layer**. All business logic lives in `features/`. Shared code lives in top-level directories. The dependency graph flows one direction only.

## Directory Structure

```
app/                    # ROUTING ONLY — maps URLs to screens
  (tabs)/               # Tab group layout
    index.tsx           # Home tab route
    explore.tsx         # Explore tab route
    _layout.tsx         # Tab navigator config
  (auth)/               # Auth flow group
    sign-in.tsx
    sign-up.tsx
    _layout.tsx
  _layout.tsx           # Root layout (providers, theme, navigation container)
  modal.tsx             # Modal routes

features/               # BUSINESS LOGIC — one folder per feature domain
  home/
    components/         # UI specific to this feature
    hooks/              # Hooks specific to this feature
    api/                # Data fetching (queries, mutations)
    utils/              # Feature-specific utilities
    store/              # Feature-local state (Zustand slice, context)
    types.ts            # Feature types
    index.ts            # Public API — REQUIRED

components/             # SHARED UI — used across multiple features
  ui/                   # Primitives: button, input, card, icon
  layout/               # Screen wrappers, safe area, containers

lib/                    # GLOBAL UTILITIES — API client, storage, analytics
hooks/                  # GLOBAL HOOKS — use-color-scheme, use-theme-color
constants/              # GLOBAL CONSTANTS — theme, colors, config
types/                  # GLOBAL TYPES — navigation types, API types
providers/              # CONTEXT PROVIDERS — auth, theme, app-providers
assets/                 # Static files — images, fonts
```

### What Goes Where

| Code | Location | Example |
|------|----------|---------|
| Route/screen entry point | `app/` | `app/(tabs)/index.tsx` |
| Feature screen UI + logic | `features/<name>/components/` | `features/home/components/home-screen.tsx` |
| Feature data fetching | `features/<name>/api/` | `features/home/api/use-get-stamps.ts` |
| Feature hooks | `features/<name>/hooks/` | `features/home/hooks/use-stamps.ts` |
| Reusable button/card/input | `components/ui/` | `components/ui/button.tsx` |
| Layout wrappers | `components/layout/` | `components/layout/screen-wrapper.tsx` |
| API client setup | `lib/` | `lib/api-client.ts` |
| Global hooks | `hooks/` | `hooks/use-color-scheme.ts` |
| Theme config | `constants/` | `constants/theme.ts` |

## Dependency Rule

```
app/ --> features/ --> components/, lib/, hooks/, constants/, types/, providers/
```

- `app/` imports from `features/` (and shared code for layouts)
- `features/` imports from shared code
- **Shared code NEVER imports from `features/`** — this is the most critical rule
- Cross-feature imports go through `index.ts` only

## Route Files Must Be Thin

Route files in `app/` exist only to connect a URL to a screen:

```tsx
// app/(tabs)/index.tsx — CORRECT
import { HomeScreen } from '@/features/home';

export default function HomeRoute() {
  return <HomeScreen />;
}
```

NEVER put in route files:
- Data fetching
- Business logic
- Complex component trees
- State management
- Styled components beyond basic wrappers

## Feature Module Anatomy

Every feature MUST have an `index.ts` barrel file. Subfolders are created on-demand.

### Required

- `index.ts` — public API. Other code imports ONLY from here.

### On-Demand (create when needed)

- `components/` — feature-specific UI
- `hooks/` — feature-specific hooks
- `api/` — data fetching (React Query hooks, fetch wrappers)
- `utils/` — feature-specific helpers
- `store/` — feature-local state (Zustand slice or context)
- `types.ts` — feature types

### Public API Pattern

```tsx
// features/home/index.ts
export { HomeScreen } from './components/home-screen';
export { useStamps } from './hooks/use-stamps';
export type { Stamp } from './types';
```

Other features and `app/` files MUST import from `@/features/home`, never from `@/features/home/components/home-screen`.

## Expo Router Conventions

### Layouts

- `_layout.tsx` — defines the navigator for a directory (Stack, Tabs, Drawer)
- Every route group MUST have a `_layout.tsx`

### Route Groups

- `(tabs)/` — bottom tab navigator
- `(auth)/` — auth flow (sign-in, sign-up)
- `(app)/` — authenticated app shell
- Groups with `()` don't affect the URL path

### File Naming

- `index.tsx` — default route for a directory
- `[id].tsx` — dynamic route parameter
- `[...rest].tsx` — catch-all route
- `modal.tsx` — presented as modal (configured in parent layout)
- `+not-found.tsx` — 404 handler

### Settings

```tsx
// app/_layout.tsx
export const unstable_settings = {
  anchor: '(tabs)', // Initial route group
};
```

## Decision Guide

**"Where do I put this code?"**

1. Is it a screen that maps to a URL? → `app/` (thin, imports from features)
2. Is it business logic for one feature? → `features/<name>/`
3. Is it a UI component used by 2+ features? → `components/`
4. Is it a primitive UI element (button, input)? → `components/ui/`
5. Is it a utility used by 2+ features? → `lib/`
6. Is it a hook used by 2+ features? → `hooks/`
7. Is it a type used by 2+ features? → `types/`
8. Is it a context provider? → `providers/`

**"Should this be in `features/` or `components/`?"**

- If it contains business logic or data fetching → `features/`
- If it's pure UI with props and no domain knowledge → `components/`
- If in doubt, start in `features/`. Move to `components/` when a second feature needs it.

## File Naming Conventions

- **kebab-case** for all files and directories
- Component files: `stamp-card.tsx`
- Hook files: `use-stamps.ts`
- Type files: `types.ts`
- Barrel files: `index.ts`
- Test files: `stamp-card.test.tsx` (colocated with source)
- Platform-specific: `icon-symbol.ios.tsx`, `icon-symbol.tsx` (default)
