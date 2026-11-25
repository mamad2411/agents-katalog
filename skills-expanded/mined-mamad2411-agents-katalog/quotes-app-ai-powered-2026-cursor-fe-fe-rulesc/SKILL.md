---
description: Frontend Rules (scoped to fe)
globs:
  - "fe/**"
alwaysApply: false
---
# cursor-rules.mdc
# Cursor rules for building a ReactJS application using TypeScript, Shadcn, Tailwind, and TanStack Query

## 1. Project Setup
- Use **Vite** or **Create React App** with TypeScript template.
- Initialize TailwindCSS using `tailwind.config.ts`.
- Install Shadcn components via `@shadcn/ui`.
- Setup TanStack Query (v5) using a global `QueryClientProvider`.

## 2. Folder Structure
src/
  app/                   # Entry point, main App component
  components/            # Reusable components
  features/              # Feature-specific modules
    <featureName>/       # Each feature has its own folder
      api.ts             # Feature-specific API functions
      hooks.ts           # Feature-specific hooks
      components/        # Feature-specific components
  hooks/                 # Global hooks
  pages/                 # Page-level components / routes
  styles/                # Global styles and Tailwind overrides
  types/                 # TypeScript type definitions
  utils/                 # Utility functions

## 3. TypeScript Rules
- Strict mode enabled in `tsconfig.json`.
- Use explicit types for props and state.
- Avoid `any`; prefer generics or `unknown` with proper checks.
- Use type aliases for API response objects.
- Consistent interface naming (`I<FeatureName>` optional but consistent).

## 4. React Rules
- Functional components only, using hooks.
- Components should be **pure** where possible.
- Use `React.memo` for heavy components.
- Prefer composition over prop drilling.
- All state must use `useState` or `useReducer`.

## 5. TanStack Query Rules
- All API calls go through feature-specific `api.ts`.
- Use `useQuery` and `useMutation` hooks in `hooks.ts`.
- Cache keys must be constants in `types.ts` or `constants.ts`.
- Implement optimistic updates for mutations.
- Handle loading and error states in the UI.

## 6. Shadcn + Tailwind Rules
- Always use Shadcn components for consistent UI.
- Tailwind classes should follow BEM-like naming if needed.
- No inline styles.
- Responsiveness via Tailwind (`sm:`, `md:`, `lg:`).
- Dark mode supported via Tailwind class strategy.

## 7. Naming Conventions
- Files & folders: `kebab-case`.
- Components: `PascalCase`.
- Hooks: `useCamelCase`.
- Constants: `SCREAMING_SNAKE_CASE`.
- API functions: `camelCase`.

## 8. Linting & Formatting
- **Biome** for linting and formatting (replaces ESLint & Prettier)
  - Fast, all-in-one toolchain: format, lint, and check all at once
  - 366+ rules with excellent error messages and auto-fixes
  - Run with: `biome check --write ./src`
  - Configuration via `biome.json` in project root
- Tailwind class order managed via Biome's built-in CSS support
- Use git hooks to lint and format code on commit (via Biome)

## 9. Testing Rules
- Use React Testing Library + Vitest/Jest.
- Tests in `__tests__/` folder inside each feature.
- Components must have snapshot and functional tests.
- Mock API calls using `msw` or similar.

## 10. Version Control
- Use Git with feature branches.
- Branch naming: `feature/<feature-name>` or `bugfix/<issue>`.
- Commit messages follow Conventional Commits.
- Merge PRs only after code review and passing CI checks.

## 11. Additional Rules
- Use environment variables for API URLs (`.env`).
- Avoid console logs in production.
- Use lazy loading for large components with `React.lazy`.
- Prefetch important queries using TanStack Query `prefetchQuery`.