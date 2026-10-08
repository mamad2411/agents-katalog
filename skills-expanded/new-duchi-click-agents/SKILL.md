# AGENTS.md

Guidelines for AI agents working in this repository.

## Project Overview

This is an **Astro** static site built with:

- **Framework**: Astro 5.x (static output)
- **UI**: React 19, TailwindCSS 4, DaisyUI 5
- **Language**: TypeScript (strict mode)

---

## Commands

### Development

```bash
npm run dev        # Start dev server at localhost:4321
npm run build      # Build production site to ./dist/
npm run preview    # Preview production build locally
```

### Linting & Formatting

```bash
npx eslint .                      # Lint all files
npx eslint src/pages/index.astro  # Lint specific file
npx eslint . --fix                # Auto-fix lint issues

npx prettier --write .            # Format all files
npx prettier --check .            # Check formatting
```

### Type Checking

```bash
npx astro check    # Run Astro type checker
npx tsc --noEmit   # TypeScript type check only
```

### Validation (Recommended)

```bash
npm run validate   # Full validation: typecheck → astro check → lint → format check
npm run lint:fix && npm run format  # Auto-fix all issues
```

> **Note**: Always run `npm run validate` before committing changes.

---

## Code Style

### File Headers

All code files must start with a path comment:

```typescript
// src/components/Card.astro
```

### Imports

**Order** (enforced by `eslint-plugin-simple-import-sort`):

1. External packages (react, astro, etc.)
2. Internal absolute imports (`@/...`)
3. Relative imports

**Path Aliases**:

- Use `@/*` for `src/*` imports
- Prefer absolute imports over deep relative paths

```astro
---
// ✅ Good
import BaseLayout from '@/layouts/base-layout.astro';

// ❌ Avoid
import BaseLayout from '../../layouts/base-layout.astro';
---
```

### Naming Conventions

| Type                  | Convention                  | Example                         |
| --------------------- | --------------------------- | ------------------------------- |
| Files (components)    | kebab-case                  | `base-layout.astro`             |
| Files (React .tsx)    | kebab-case                  | `theme-selector.tsx`            |
| Files (pages)         | kebab-case or `index.astro` | `about/index.astro`             |
| React Components      | PascalCase                  | `<BaseLayout />`                |
| TypeScript interfaces | PascalCase                  | `interface Props`               |
| Variables/functions   | camelCase                   | `const pageTitle`               |
| CSS classes           | TailwindCSS utilities       | `className="flex items-center"` |

### TypeScript

- **Strict mode** enabled (extends `astro/tsconfigs/strict`)
- Use `interface` for component props
- Use **type-only imports** when importing types:

```typescript
// ✅ Enforced by @typescript-eslint/consistent-type-imports
import type { CollectionEntry } from 'astro:content';
```

- Unused variables must be prefixed with `_`:

```typescript
// ✅ Allowed
const [_unused, setValue] = useState();
```

### Formatting (Prettier)

| Setting        | Value        |
| -------------- | ------------ |
| Print Width    | 100          |
| Semicolons     | Yes          |
| Quotes         | Single (`'`) |
| Tab Width      | 2 spaces     |
| Trailing Comma | ES5          |

### Astro Components

Structure of `.astro` files:

```astro
---
// 1. Imports
import Component from '@/components/Component.astro';

// 2. Props interface
interface Props {
  title: string;
  description?: string;
}

// 3. Destructure props
const { title, description } = Astro.props;

// 4. Logic/data fetching
---

<!-- 5. Template -->
<html>
  <body>
    <slot />
  </body>
</html>
```

---

## Architecture

```plain
src/
├── assets/       # CSS and static assets processed by Vite
│   └── app.css   # Global styles (Tailwind + DaisyUI)
├── layouts/      # Layout components
│   ├── base-layout.astro   # HTML shell (head, body)
│   ├── app-layout.astro    # App-level wrapper
│   └── post-layout.astro   # Blog post layout
├── pages/        # File-based routing
│   ├── index.astro
│   ├── about/index.astro
│   ├── blog/[slug].astro
│   └── showcase/[slug].astro
└── components/   # Reusable UI components (Astro/React)
```

---

## Commit Messages

Follow **Conventional Commits**:

```plain
<type>[optional scope]: <description>
```

- Keep messages under 60 characters
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

```bash
git commit -m 'feat: add responsive navbar with TailwindCSS'
git commit -m 'fix(blog): correct date formatting'
```

---

## ESLint Rules

Key rules enforced:

| Rule                                         | Setting              |
| -------------------------------------------- | -------------------- |
| `simple-import-sort/imports`                 | error                |
| `simple-import-sort/exports`                 | error                |
| `@typescript-eslint/consistent-type-imports` | error                |
| `@typescript-eslint/no-unused-vars`          | warn (ignore `^_`)   |
| `react/prop-types`                           | off (use TypeScript) |
| `react-hooks/*`                              | recommended          |

### Astro-specific

- Type-checked rules are **disabled** in `.astro` files (parser limitation)
- Config files (`*.config.*`) have type checking disabled

---

## Important Guidelines

### DO

- Use TailwindCSS for all styling (utility-first)
- Keep components modular and reusable
- Follow DRY principles
- Use path aliases (`@/`) for imports
- Add file header comments
- Write comments that describe **purpose**, not effect

### DON'T

- Use `as any` or `@ts-ignore` to suppress type errors
- Commit without running lint/format
- Use inline styles when Tailwind classes exist
- Create deeply nested relative imports

---

## VS Code Settings

The project includes VS Code settings for:

- Format on save (Prettier)
- ESLint auto-fix on save
- Astro extension as default formatter for `.astro` files

---

## External Resources

- [Astro Docs](https://docs.astro.build)
- [TailwindCSS v4](https://tailwindcss.com/docs)
- [DaisyUI Components](https://daisyui.com/components)
- [React 19](https://react.dev)
