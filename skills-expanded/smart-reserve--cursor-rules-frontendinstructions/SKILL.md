---
name: "Frontend"
description: "React component patterns, routing structure, UI components, and styling conventions for Next.js App Router"
applyTo: "app/**,src/app/**,components/**,src/components/**,hooks/**,src/hooks/**"
---

# Frontend Instructions

## Route-Based Folder Structure

Each route colocates its own private modules using the Next.js `_` prefix convention. Shared code lives in top-level directories.

```
src/
  app/
    (public)/                     # Route group for public pages
      reservations/
        page.tsx
        _components/              # Components used only by this route
          reservation-form.tsx
          reservation-list.tsx
          reservation-card.tsx
        _hooks/                   # Hooks scoped to this route
          use-reservation-filters.ts
        _lib/                     # Utilities scoped to this route
          format-reservation.ts
      tables/
        page.tsx
        _components/
          table-grid.tsx
        _hooks/
          use-table-availability.ts

    (dashboard)/                  # Route group for authenticated pages
      admin/
        page.tsx
        _components/
          admin-stats.tsx

  components/                     # Shared components used across multiple routes
    ui/                           # shadcn/ui components
    layout/                       # Layout components (header, sidebar, footer)

  hooks/                          # Shared hooks used across multiple routes

  lib/                            # Shared utilities (db, auth, helpers)

  server/                         # Backend logic (see architecture instructions)
```

### Rules

- **Route-specific code** (components, hooks, utils) goes in `_components/`, `_hooks/`, `_lib/` folders inside the route directory. The `_` prefix makes them private to Next.js (not treated as routes).
- **Shared code** used by 2+ routes goes in top-level `components/`, `hooks/`, or `lib/` directories.
- If a "private" component starts being used in another route, move it to the shared `components/` directory.
- Keep page files thin — they should compose route-specific components, not contain large JSX trees.

---

## UI Components

- Always use **shadcn/ui** components. Do not create custom components for things shadcn already provides (Button, Dialog, Input, Select, Card, etc.).
- If a required shadcn component is not yet installed, install it before using:
  ```bash
  npx shadcn@latest add <component-name>
  ```
  Example — need a dialog:
  ```bash
  npx shadcn@latest add dialog
  ```

## React Patterns

- **Do NOT use `useCallback` or `useMemo`** unless there is a clearly measured performance problem. Prefer simplicity over premature optimization.
- **Do NOT use `React.memo`**. If a component re-renders too often, fix the architecture instead of wrapping it in memo.
- **Extract parts into separate components.** Keep components small and focused on a single responsibility. If a section of JSX grows beyond ~50 lines or has its own state/logic, extract it into its own component file.

## Component Declaration

- Define components as **arrow functions assigned to a const**. Do not explicitly type the return type.
- **Define props inline** in the function signature. Do not create separate `Props` interfaces unless the props are reused across multiple components.

```tsx
// Good — inline props
export const ReservationCard = ({ name, guests }: { name: string; guests: number }) => {
  return <div>{name} — {guests} guests</div>
}

// Bad — separate type for single-use props
interface ReservationCardProps {
  name: string
  guests: number
}
export const ReservationCard = ({ name, guests }: ReservationCardProps) => { ... }

// Bad — explicit return type
export const ReservationCard = ({ name, guests }: { ... }): JSX.Element => { ... }
export const ReservationCard: React.FC<Props> = ({ name, guests }) => { ... }
```

If props grow large (5+ properties), extract to an `interface` in the same file — not a separate file.

```tsx
// Acceptable for complex props
interface ReservationFormProps {
  name: string
  date: Date
  guests: number
  tableId: string
  onSubmit: (data: FormData) => void
}

export const ReservationForm = ({ name, date, guests, tableId, onSubmit }: ReservationFormProps) => { ... }
```

## Styling

- Use Tailwind CSS utility classes. Avoid custom CSS unless absolutely necessary.
