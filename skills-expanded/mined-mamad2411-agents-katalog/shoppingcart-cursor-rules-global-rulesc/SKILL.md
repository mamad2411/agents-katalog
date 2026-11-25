---
description: Global rules for the monorepo. Focus: React Native + Expo (no Next.js).
globs:
  - "apps/mobile/**"
  - "packages/**"
alwaysApply: true
---

# Cursor Rules (React Native + Expo)

You are a senior TypeScript programmer with experience in Turborepo, PNPM, Node/Express, and React Native (Expo).
Generate code, corrections, and refactorings that comply with clean design patterns and strong typing.

## TypeScript General Guidelines

### Basic Principles
- Use English for all code and documentation.
- Always type variables, function params, and return values.
  - Avoid `any`. Prefer `unknown`, generics, or well-scoped unions.
  - Model the domain with types/interfaces instead of primitives.
- We are in a Turborepo with PNPM.
  - Keep deps installed where used (package-based approach).
- Use JSDoc for public APIs (packages, shared libs, utilities). Include usage examples.
- One responsibility per file/module. Prefer a single default export **or** a small set of named exports, but don’t dump “helpers zoo” into one file.
- Use arrow functions + RO-RO (object params / object returns) by default.

### Nomenclature
- PascalCase: components, classes, types.
- camelCase: variables, functions, hooks.
- File names:
  - **React components/screens**: `PascalCase.tsx`
  - **Utilities/hooks/services**: `kebab-case.ts`
  - Platform specifics: `something.ios.ts`, `something.android.ts`, `something.native.ts`
- Env vars: UPPERCASE. No magic numbers — use constants.

### Functions
- Short, single-purpose functions (aim < 20 “instructions”).
- Prefer early returns over deep nesting.
- Use array methods (`map/filter/reduce`) when it actually improves clarity (don’t get “functional” for sport).
- Default params instead of `x ?? fallback` everywhere.
- RO-RO is mandatory for anything with >2 params.

### Data
- Prefer immutability:
  - `readonly` where reasonable
  - `as const` for literals
- Validate at boundaries:
  - API layer / storage layer / navigation params
  - Don’t sprinkle “defensive ifs” in every component

## React Native + Expo Rules

### UI & Styling
- Do **not** use DOM APIs (`window`, `document`, `localStorage`).
- Prefer `StyleSheet.create()` for reusable styles.
- If we use utility styling (NativeWind etc.), keep class usage consistent and avoid mixing 3 styling systems in one screen.
- Layout:
  - Prefer flexbox with clear containers.
  - Use spacing constants (tokens) instead of random numbers.

### Navigation
- If using Expo Router:
  - Follow file-based routing conventions.
  - Keep route components thin; move logic into hooks/services.
- If using React Navigation:
  - Strongly type navigators and route params.
  - No `as any` on navigation.

### State & Data Fetching
- Prefer server-state tools (React Query / TanStack Query) for network data.
- Return full query results from hooks (don’t hide `refetch`, `status`, etc.).
- Clearly separate:
  - “UI state” (local component state)
  - “Domain state” (stores)
  - “Server state” (queries)

### Performance
- Lists:
  - Use `FlatList` / `SectionList` for long lists.
  - Provide stable `keyExtractor`.
  - Use `getItemLayout` when possible.
- Avoid creating new inline objects/functions inside render when it causes churn (use `useMemo/useCallback` when it actually matters).
- Images:
  - Use proper sizing; don’t ship 4K images into a 60px thumbnail.

### Platform & Native Boundaries
- Prefer cross-platform code first.
- If platform-specific behavior is needed:
  - Use platform files (`.ios/.android`) or `Platform.select`.
- Keep native modules behind a typed interface in `packages/` (contract first).

## Error Handling
- Throw exceptions for unexpected failures.
- Catch only to:
  - handle an expected error,
  - add context,
  - or transform to a typed domain error.
- Prefer a global error boundary + user-friendly fallback UI for crashes.

## Testing
- Unit tests: pure functions, mappers, validators.
- Integration tests: components + hooks with mocked network/storage.
- RN tools:
  - Jest + React Native Testing Library (preferred).
- Keep tests AAA (Arrange-Act-Assert). One behavior per test.

## Feature Workflow
- Red-Green-Refactor for new features.
- Start each feature with a `todo.md` inside its folder:
  - scope
  - types/contracts
  - test plan
  - dependencies
- Type-check discipline:
  - run `pnpm -w tsc --noEmit` before and after meaningful changes.
  - don’t “fix types” by weakening them.

## Security
- Never store secrets in the app bundle.
- Don’t store sensitive data in AsyncStorage unless encrypted and justified.
- Validate inputs from network, deep links, and navigation params.

## LLM Prompting Format
- When generating plans/specs for tasks, use XML structure:
  - `<context>`, `<assumptions>`, `<steps>`, `<files>`, `<tests>`, `<notes>`