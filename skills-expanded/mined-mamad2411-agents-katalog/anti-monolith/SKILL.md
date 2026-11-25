---
name: anti-monolith
description: >
  Anti-monolith standard for React/Next.js projects. Enforces modular component architecture,
  file size limits, single-responsibility components, custom hook extraction, data-layer separation,
  barrel exports, and strict layer dependency rules. Activate whenever the user is creating
  React components, building Next.js pages, refactoring large files, setting up a component library,
  writing page.tsx or layout.tsx files, or mentions "monolith", "too long", "refactor",
  "component library", "design system", "modular", "split", "extract component", "file too big",
  "too many useState", or any situation where a React/Next.js file is growing beyond manageable size.
  Also use proactively when scaffolding new projects to ensure the architecture is modular from the start.
---

# Anti-Monolith Standard for React/Next.js

## Why this matters

Monolithic components are the #1 cause of unmaintainable React code. A single 1000+ line page.tsx with 15+ useState hooks, inline sub-components, and direct data fetching makes the code impossible to test, reuse, or reason about. This skill prevents that pattern from ever forming.

---

## The 5 Rules

### Rule 1: Line Limits

Hard boundaries that force decomposition:

| Unit | Maximum | Action if exceeded |
|------|---------|-------------------|
| Single component function | 150 lines | Extract sub-components |
| Single file | 200 lines | Split into multiple files |
| Custom hook | 100 lines | Split into smaller hooks |
| Barrel index.ts | 50 lines | Group into sub-barrels |

**How to count:** Lines of code excluding blank lines and comments. If a component exceeds 150 lines, that is a signal that it is doing too much.

**Exceptions:** Configuration objects, large type definitions, and generated code may exceed limits. Move them to separate files.

### Rule 2: Maximum 3 useState per Component

When a component needs more than 3 useState calls, the state logic belongs in a custom hook.

```
// BAD: 8 useState in one component
function Dashboard() {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('all')
  const [favorites, setFavorites] = useState([])
  const [selected, setSelected] = useState(null)
  const [sortBy, setSortBy] = useState('name')
  const [viewMode, setViewMode] = useState('grid')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  // ... rendering
}

// GOOD: State extracted into hooks
function Dashboard() {
  const filters = useDashboardFilters()    // query, category, sortBy, viewMode
  const { items, isLoading, error } = useDashboardData(filters)
  const { favorites, toggleFavorite } = useFavorites()
  const [selected, setSelected] = useState(null)  // only local UI state
  // ... clean rendering
}
```

**Why:** Each useState is a potential source of re-renders and bugs. Grouping related state into hooks makes the logic testable, reusable, and readable.

### Rule 3: Components Do Not Fetch Data

A component should never call fetch, axios, or any data-loading function directly. Data arrives through props or custom hooks.

```
// BAD: Component fetches its own data
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers)
  }, [])
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}

// GOOD: Data comes from outside
function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}

// GOOD: Data comes from a hook
function UserPage() {
  const { users, isLoading } = useUsers()
  if (isLoading) return <Skeleton />
  return <UserList users={users} />
}
```

**Why:** Separating data loading from rendering makes components testable (pass mock data), reusable in different contexts, and eliminates useEffect-related bugs.

**Server Components exception:** In Next.js App Router, Server Components can fetch data directly. This is the recommended pattern. But Client Components ('use client') must never fetch directly.

### Rule 4: Barrel Exports (index.ts)

Every directory that contains components or hooks must have an index.ts barrel file. The project must have a single master export.

```
packages/react/src/
├── ui/
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   └── index.ts          ← export { Button } from './button'
├── sections/
│   ├── hero-section.tsx
│   ├── footer-section.tsx
│   └── index.ts          ← export { HeroSection } from './hero-section'
├── hooks/
│   ├── use-theme.ts
│   └── index.ts          ← export { useTheme } from './use-theme'
└── index.ts              ← MASTER EXPORT
```

Master export (index.ts at root):
```typescript
export * from './ui'
export * from './sections'
export * from './hooks'
export * from './providers'
```

Consumer imports from a single source:
```typescript
import { Button, HeroSection, useTheme } from '@my-org/ui'
```

**Why:** Barrel exports create a clean public API, enable tree-shaking, and prevent consumers from depending on internal file paths.

### Rule 5: Layer Separation

Components are organized in layers. Dependencies flow strictly downward:

```
tokens/       ← Colors, spacing, typography (no React, no logic)
  ↑
ui/           ← Button, Card, Input (pure presentation, no business logic)
  ↑
sections/     ← HeroSection, NavigationSection (compose ui/ components)
  ↑
features/     ← FlowCanvas, AgentHierarchy (complex, may have local state)
  ↑
hooks/        ← useTheme, useMediaQuery (stateful logic, no JSX)
  ↑
providers/    ← ThemeProvider, ErrorBoundary (wrap the app)
```

**Rules:**
- `tokens` imports nothing from other layers
- `ui` imports only from `tokens`
- `sections` imports from `ui` and `tokens`
- `features` imports from `sections`, `ui`, and `tokens`
- `hooks` imports only from `tokens` (or external libraries)
- `providers` imports from `hooks`, `ui`, and `tokens`
- No upward imports. Ever. If `ui/button.tsx` imports from `features/`, the architecture is broken.

**Why:** Layer violations create circular dependencies, make testing impossible, and lead to the "everything depends on everything" problem that makes monoliths intractable.

---

## Practical Checklist

Before submitting any React/Next.js file, verify:

- [ ] File is under 200 lines
- [ ] No component function exceeds 150 lines
- [ ] No more than 3 useState in any single component
- [ ] No direct fetch/axios calls in Client Components
- [ ] Every component directory has an index.ts barrel
- [ ] No upward layer imports (features → ui is fine, ui → features is forbidden)
- [ ] Each component has a single responsibility (one reason to change)
- [ ] Complex state logic is extracted into custom hooks

---

## Refactoring Strategy

When encountering an existing monolith (e.g., a 1200-line page.tsx), follow this sequence:

1. **Identify sub-components** — Find all functions starting with uppercase that return JSX. Extract each into its own file.
2. **Identify state clusters** — Group related useState calls. Extract each group into a custom hook.
3. **Identify data loading** — Move all useEffect + fetch patterns into custom hooks or Server Components.
4. **Create barrel exports** — Add index.ts files for each directory.
5. **Verify layer separation** — Check that no upward imports exist.
6. **Test** — Ensure the refactored code works identically to the original.

The result: a 40-line page.tsx that composes well-named, testable, reusable components.

---

## File Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Component | kebab-case | `hero-section.tsx` |
| Hook | camelCase with use- prefix | `use-theme.ts` |
| Provider | PascalCase | `ThemeProvider.tsx` |
| Barrel | index.ts | `index.ts` |
| Types | kebab-case with .types | `button.types.ts` |
| Utils | kebab-case | `format-date.ts` |

---

## What This Skill Does NOT Cover

- Styling methodology (CSS Modules, Tailwind, styled-components — all compatible)
- State management libraries (Zustand, Redux, Jotai — use what fits, but still extract hooks)
- Testing frameworks (Vitest, Jest — but the modular structure makes testing easy)
- Build tools (Vite, Webpack, Turbopack — architecture is tool-agnostic)
