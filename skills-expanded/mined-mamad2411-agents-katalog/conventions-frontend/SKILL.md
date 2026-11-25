---
name: conventions-frontend
description: Load when coding the web frontend (TS/React/TailwindCSS).
---

# Frontend Conventions

## TypeScript

- Never use `any` - use `unknown` with type narrowing
- Favor TypeScript types over interfaces, unless extending is needed.
- Use named exports, avoid default exports. Only export functions/types that are referenced by another file (e.g., don't export `type ButtonProps` unless another file actually needs to reference it - private by default)

## Libraries

- Use pnpm for package management.
- Use vite 8+ for bundling.
- Use oxlint for linting.
- Use oxfmt for formatting.
- Use TypeScript 6+ with strict mode.
- React 19+.
- Tailwind CSS v4+ - inline styles must be justified - no CSS modules.
- shadcn/ui - import from @/components/ui/ only.
- Zod for schema validation.
- TanStack Query + @hey-api for API interactions. OpenAPI specs will be provided.
- Use the latest versions of libraries when adding libraries to the project.

When adding libraries to the project, find and use the latest version of the package.

## React

- Use functional components, never class components.
- Favor one component per file.

## Structure

The frontend project uses this structure:

```text
src/
  app/
    routes/           # Route-level page components
    providers.tsx     # All context providers composed here
    router.tsx
  components/
    ui/               # shadcn/ui re-exports - shared primitives only
  features/
    auth/
      api/            # Raw API calls + TanStack Query options
      components/     # UI scoped to this feature
      hooks/          # Hooks scoped to this feature
      types.ts
      utils.ts
    dashboard/
      ...             # Same pattern
  hooks/              # Truly global hooks only
  types/              # Global TypeScript types
  clients/            # REST clients
    storage-api/      # Clients for different areas in different folders
  utils/              # Global utilities
```

- One exported component per file.
- One exported function per file.
- Never use index barrel files, e.g., `index.ts`.
- For frontend projects, the entrypoint should be `index.html`.

## Naming

- Components: `PascalCase.tsx`
- Hooks: `useUser.ts`
- Utilities/API: `kebab-case.ts`
- Booleans: `isLoading`, `hasError`, `canSubmit`
- Event handlers: `onSubmit`, `handleClick`
- Constants: `UPPER_SNAKE_CASE`

## Testing

- Use vitest 4+.
- Co-locate test files, e.g., `LoginForm.tsx` + `LoginForm.test.tsx` in the same directory.
- Use the format `<filename>.test.<ext>` for test file names.
- Mock APIs with MSW v2.
- Use React Testing Library 16+ for testing components.
- Test Behavior, not Implementation.
- Use `When then should` style for test descriptions, e.g., `When the user clicks the button, then the modal should open`.

## Setup

Use these as baseline configurations for new and existing projects.

The TypeScript configuration (`tsconfig.json`):

```json
{
  "compilerOptions": {
    "target": "es2024",
    "module": "esnext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "isolatedModules": true,
    "skipLibCheck": true
  }
}
```

The project.json scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "oxlint",
    "fmt": "oxfmt"
  }
}
```

The oxlint configuration (`oxlint.config.ts`):

```js
import { defineConfig } from "oxlint";

export default defineConfig({
  plugins: [
    "react",
    "react-perf",
    "typescript",
    "jsx-a11y",
    "promise",
    "vitest",
  ],
  env: {
    browser: true,
    es2020: true,
  },
  ignorePatterns: ["dist"],
  categories: {
    correctness: "warn",
  }
});
```

The oxcfmt configuration (`oxfmt.config.ts`):

```js
import { defineConfig } from "oxfmt";

export default defineConfig({
  ignorePatterns: ["*.md"],
  sortImports: {
    newlinesBetween: false,
  },
  sortTailwindcss: {
    functions: ["twMerge", "twJoin"],
  },
  sortPackageJson: true,
});
```
