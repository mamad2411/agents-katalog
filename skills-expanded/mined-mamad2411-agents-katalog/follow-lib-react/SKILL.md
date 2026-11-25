---
name: follow-lib-react
description: Develop React 19.3 applications with Server Components, React Compiler, and modern hooks
argument-hint: "[scope]"
related:
  - follow-tool-react-scan
  - follow-lib-animejs
  - follow-lib-arktype
  - follow-lib-unocss
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Develop React applications per best practices with React 19.2+, React Compiler, Server Components, and modern hooks

## Scope

Use for developing React 19.2+ applications with Vite or Next.js, TypeScript, and a standard folder structure

- No own CLI — used through the bundler/framework (Vite, Next.js) (thus none)
- Latest: `react@19.3.0` / `react-dom@19.3.0` (verified 2026-09-16)
- References: [apis](references/apis.md) 
## Execute

### 1. Setup Project Structure

> Goal: create a project structure per the React 19 standard

Create the project structure per the standard

1. Create `src/components/ui`, `src/components/features`, `src/hooks`, `src/lib`, `src/types`
2. Set up `package.json` with the standard scripts `dev`, `build`, `preview`, `typecheck`, `lint`
3. Configure `vite.config.ts` or `next.config.ts` and `tsconfig.json`
4. Install the dependencies `react@^19.3.0`, `react-dom@^19.3.0`, `typescript`, `babel-plugin-react-compiler` (if using React Compiler)
5. Use React 19.2+ as the minimum version

### 2. Configure Core Principles

> Goal: configure React 19's core principles correctly

Configure the core principles of React 19

1. Wrap the `App` component in `React.StrictMode`
2. Use Error Boundaries for risky sections
3. Configure UnoCSS per `/follow-lib-unocss` or use Tailwind CSS per project
4. Use React Server Components as the default and Client Components only when necessary
5. Enable React Compiler before adding manual memoization, via `babel-plugin-react-compiler` or `reactCompilerPreset` in Vite/Next.js
6. Use Server Actions for form handling and mutations in Next.js or a supporting framework

### 3. React 19 Hooks And APIs

> Goal: use React 19 hooks and APIs correctly per use case

Use React 19 hooks and APIs

1. Use `useActionState` for form actions with pending state
2. Use `useFormStatus` for form submission status
3. Use `useOptimistic` for optimistic updates
4. Use the `use()` API for unwrapping promises and context
5. Use `useTransition` for non-blocking UI updates
6. Use `useDeferredValue` for deferring expensive renders
7. Use `useEffectEvent` to separate event logic from `useEffect` dependencies (React 19.2+)
8. Use `<Activity>` when you want to hide UI while preserving state (React 19.2+)
9. Use `cacheSignal` only in React Server Components for cache lifetime (React 19.2+)
10. Use `<ViewTransition>` to animate enter/exit/update/share of elements within Transitions (stable in React 19.3)
11. Use `addTransitionType` to label the cause of a Transition (e.g. `next`/`previous`) together with `<ViewTransition>` (React 19.3+)
12. Pass a `ref` directly into a Fragment when you need DOM-level access to a group of elements (Fragment refs, React 19.3+)
13. Use `use(browser())` when a component must render only on the browser, not on the server (React 19.3+)

### 4. Implement Folder Rules

> Goal: apply rules per folder clearly

Apply rules for each folder

1. `components/ui`: Dumb components, props in, events out
2. `components/features`: Feature-specific components
3. `hooks`: Orchestration and facade patterns
4. `lib`: Pure utilities, clients, adapters

### 5. Setup Import Rules

> Goal: configure import dependencies in the correct layered order

Configure import dependencies in order

1. pages → components/features, hooks
2. components/features → components/ui, hooks
3. components/ui → no internal dependencies
4. hooks → lib, types
5. lib → types
6. types → no internal dependencies

### 6. Server Components Patterns

> Goal: use Server Components as default and Client Components only when necessary

Use Server Components correctly

1. Server Components are the default (no `useState`, `useEffect`)
2. Client Components only when interactivity is needed
3. Use the `'use client'` directive only where necessary
4. Use the `'use server'` directive for Server Actions
5. Pass data from Server → Client via props, not fetch in the Client
6. Use `loading.tsx` and `error.tsx` for streaming and error boundaries (Next.js App Router)

### 7. Optimize Performance

> Goal: configure performance optimization using React Compiler

Configure performance optimization

1. Use React Compiler before adding `React.memo`, `useMemo`, `useCallback`
2. Use the latest `eslint-plugin-react-hooks` so the linter supports React Compiler rules
3. Use code splitting with `React.lazy`
4. Use `useTransition` for priority updates
5. Use `useDeferredValue` for expensive renders
6. Avoid over-memoization when using React Compiler

### Workflows

- Render optimization — memo/useMemo/useCallback, React Compiler, profiling → `workflows/optimize-render/SKILL.md`

## Rules

### 1. Component Structure

Structure components by responsibility

- `components/ui`: Small, focused, single responsibility
- `components/features`: Feature-specific, no global state binding
- `hooks`: Orchestration, facade patterns, no UI markup
- `lib`: Pure utilities, clients, adapters, no React imports

### 2. React 19 Best Practices

Use React 19 features appropriately

- Use React Compiler before manual memoization
- Server Components as default, Client Components only when needed
- Use Server Actions for form handling and mutations
- Use `useActionState` instead of manual form state management
- Use `useOptimistic` for optimistic UI updates
- Use `useEffectEvent` when separating event logic from effect dependencies
- Use `<ViewTransition>` instead of an animation library for common enter/exit transitions (React 19.3+, DOM only)
- Avoid `useEffect` for data fetching — use Server Components instead

### 3. Performance Best Practices

Use performance optimization appropriately

- Use React Compiler instead of manual `memo`/`useMemo`/`useCallback`
- Avoid over-memoization
- Use code splitting by route or component
- Use `useTransition` for non-critical updates
- Use `useDeferredValue` for expensive renders

### 4. Code Quality

Maintain code quality

- Use TypeScript for type safety
- Use Biome or ESLint for linting
- Use strict mode for development
- Use Error Boundaries for error handling

### 5. Configuration Standards

Configure per the standard

- `package.json`: `dev`, `build`, `preview`, `typecheck`, `lint` scripts
- `vite.config.ts`: Vite configuration with the React Compiler plugin when needed
- `tsconfig.json`: TypeScript configuration
- UnoCSS configuration per `/follow-lib-unocss`

- Use `/follow-tool-react-scan` if needed
- Use `/follow-lib-animejs` if needed
- Use `/follow-lib-arktype` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A React 19.2+ application with a correct structure
- Server Components as default, Client Components only when needed
- React Compiler reduces the need for manual memoization
- Appropriate performance optimization
- Type safety with TypeScript
- Code quality via linting
