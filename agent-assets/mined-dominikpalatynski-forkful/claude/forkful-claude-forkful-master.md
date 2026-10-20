# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- **Astro 5** - SSR-enabled web framework (server output mode)
- **React 19** - UI library for interactive components
- **TypeScript 5** - Type-safe JavaScript
- **Tailwind CSS 4** - Utility-first CSS framework
- **Shadcn/ui** - Accessible UI components
- **Node.js** - v22.14.0 (see `.nvmrc`)

## Development Commands

```bash
npm run dev          # Start dev server on port 3000
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run lint:fix     # Auto-fix ESLint issues
npm run format       # Format code with Prettier
```

**Git Hooks**: Husky + lint-staged automatically run linters on pre-commit for `*.{ts,tsx,astro}` files and Prettier for `*.{json,css,md}` files.

## Project Architecture

### Directory Structure

```
src/
├── layouts/           # Astro layout templates
├── pages/            # Astro pages (file-based routing)
│   └── api/          # API endpoints (set prerender = false)
├── middleware/       # Astro middleware (index.ts)
├── components/       # UI components
│   ├── ui/           # Shadcn/ui components
│   └── hooks/        # Custom React hooks
├── lib/              # Services and utilities
├── db/               # Supabase client and types
├── types.ts          # Shared types (Entities, DTOs)
├── assets/           # Internal static assets
└── styles/           # Global styles
public/               # Public static assets
```

### Path Aliases

TypeScript is configured with `@/*` alias pointing to `./src/*`:

```typescript
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
```

### Component Strategy

- Use **Astro components** (`.astro`) for static content and layouts
- Use **React components** (`.tsx`) only when interactivity is needed
- Never use Next.js directives like `"use client"` - this is Astro + React, not Next.js

### API Routes

- API endpoints live in `src/pages/api/`
- Use uppercase HTTP method exports: `GET`, `POST`, etc.
- Always set `export const prerender = false`
- Use Zod for input validation
- Extract business logic to `src/lib/services`

### Supabase Integration

- Access Supabase via `context.locals.supabase` in Astro routes (not direct imports)
- Use the `SupabaseClient` type from `src/db/supabase.client.ts`, not from `@supabase/supabase-js`
- Validate all data with Zod schemas

## Code Style Guidelines

### Error Handling Pattern

- Handle errors and edge cases at the beginning of functions
- Use early returns for error conditions (avoid deep nesting)
- Place the happy path last for readability
- Avoid unnecessary else statements; prefer if-return pattern
- Use guard clauses for preconditions

```typescript
function processData(data: unknown) {
  if (!data) return { error: "No data provided" };
  if (!isValid(data)) return { error: "Invalid data" };

  // Happy path here
  return { success: true, result: transform(data) };
}
```

### React Best Practices

- Use functional components with hooks (no class components)
- Wrap expensive components with `React.memo()` when appropriate
- Use `useCallback` for event handlers passed to children
- Use `useMemo` for expensive calculations
- Use `useId()` for accessibility ID generation
- Consider `useOptimistic` for optimistic UI updates
- Use `useTransition` for non-urgent state updates
- Code-split with `React.lazy()` and `Suspense`

### Tailwind CSS

- Use `@layer` directive to organize styles (components, utilities, base)
- Use arbitrary values with square brackets: `w-[123px]`
- Use responsive variants: `sm:`, `md:`, `lg:`
- Use state variants: `hover:`, `focus-visible:`, `active:`
- Use `dark:` variant for dark mode

### Accessibility

- Use semantic HTML before adding ARIA attributes
- Apply ARIA landmarks for page regions
- Use `aria-expanded` and `aria-controls` for expandable content
- Implement `aria-live` regions for dynamic updates
- Use `aria-hidden` for decorative content
- Add `aria-label`/`aria-labelledby` for elements without visible labels
- Use `aria-current` for navigation states
- Avoid redundant ARIA that duplicates native HTML semantics

## Shadcn/ui Components

Components are installed in `src/components/ui/` with:

- **Style**: new-york
- **Base color**: neutral
- **Icon library**: lucide-react

### Installing New Components

```bash
npx shadcn@latest add [component-name]
# Example: npx shadcn@latest add accordion
```

**Note**: Use `npx shadcn@latest`, not the deprecated `npx shadcn-ui@latest`

### Usage

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

<Button variant="outline">Click me</Button>;
```

## Astro-Specific Features

- **View Transitions**: Use ClientRouter for smooth page transitions
- **Content Collections**: Use type-safe content collections for structured content
- **Image Optimization**: Use Astro Image integration
- **Hybrid Rendering**: Server-side rendering enabled (output: "server")
- **Environment Variables**: Access via `import.meta.env`
- **Cookies**: Manage server-side with `Astro.cookies`
- **Middleware**: Implement request/response modification in `src/middleware/index.ts`

## Configuration Files

- `astro.config.mjs` - Astro config (server mode, Node adapter, port 3000)
- `components.json` - Shadcn/ui configuration
- `tsconfig.json` - TypeScript config (strict mode, path aliases)
- `package.json` - lint-staged configured for pre-commit checks
