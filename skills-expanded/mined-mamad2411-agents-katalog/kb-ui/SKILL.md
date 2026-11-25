---
name: kb-ui
description: Portable UI patterns for Next.js 16+ App Router + React 19 + Tailwind + shadcn/ui — Server-by-default with `'use client'` at leaves, mobile-first 375px shell container, stacked responsive filters, Suspense+Skeleton, URL-state hook, RHF+Zod at the trust boundary, cascading-filter rule, a11y checklist. Invoke when writing new components in any App Router project regardless of design system. For kit primitives → `sk-ui`.
last-verified: 2026-04-23
---

# kb-ui — Portable UI Patterns (Next.js 16+ + React 19 + Tailwind)

> Stack: Next.js 16+ App Router, React 19, Tailwind v4, shadcn/ui.
> **Portable** — these patterns work in any Next.js project regardless of design system or kit barrels.
>
> **Pair:** [`sk-ui`](../sk-ui/SKILL.md) — kit-shipped primitives (`INVENTORY.md` SSOT, `FormField`, `DataTable`, `StatusToggle`, `useTableState`, `BreadcrumbSetter`, human-ID rule). **Orchestrator:** [`sk-crud-scaffold`](../sk-crud-scaffold/SKILL.md) — CRUD layer orchestration across DB / actions / table / form.

---

## 1. Server vs Client Components

Default is **Server**. Only add `'use client'` when a trigger applies. Push the boundary as deep as possible — a page can stay Server even when a leaf button is Client.

| `'use client'` required      | Keep Server Component              |
| ---------------------------- | ---------------------------------- |
| `useState` / `useEffect`     | Data fetch (`await db.query(...)`) |
| Event handlers (`onClick` …) | Static render                      |
| Browser APIs (`window`, DOM) | Filesystem / DB / secrets access   |
| React context with state     | Stateless presentational render    |

**Fetching lives in Server Components.** Avoid `useEffect` for data fetching — fetch in the Server Component with `await`, pass data down as props. Client leaves receive already-resolved data.

```tsx
// page.tsx (Server Component — no 'use client')
export default async function UsersPage() {
  const users = await getUsers();
  return <UsersTable rows={users} />; // Client leaf receives data
}
```

---

## 2. Layout patterns — mobile-first 375px baseline

Per `SK.md §3.2`, every screen must be 100% usable at 375px without horizontal scroll. The patterns below cover the common layout situations: protected shell, detail page, stats grids, wide tables that must scroll internally, and mobile tabs.

### 2.1 Shell container

The shell wraps the protected area and prevents horizontal overflow at 375px.

```tsx
// Protected shell (conceptual — design-agnostic)
<main className="min-w-0 pt-16 lg:ml-60">
  <div className="max-w-full p-4 lg:p-6">{children}</div>
</main>
```

| Class        | Why it matters                                                   |
| ------------ | ---------------------------------------------------------------- |
| `min-w-0`    | Flex/grid children can shrink below their intrinsic min-content  |
| `max-w-full` | Hard cap at 100% of the parent — prevents overflow from children |
| `p-4 lg:p-6` | Consistent padding that scales up on desktop                     |
| `pt-16`      | Top offset for fixed header                                      |
| `lg:ml-60`   | Left offset for desktop sidebar (collapses on mobile)            |

**Rule:** any flex/grid child that must shrink (e.g. table row cells, tab labels) needs `min-w-0` too. Without it, text with `truncate` will overflow its parent.

### 2.2 Detail page layout — centered + readable

Detail pages need a readable max-width and consistent vertical rhythm. Pair with `min-w-0` on any text container that should truncate.

```tsx
<div className="mx-auto max-w-4xl space-y-6 py-6">
  <div className="flex items-start gap-4">
    <Avatar src={entity.image} name={entity.name} size="lg" />
    <div className="min-w-0 flex-1">
      <h1 className="text-foreground text-2xl font-bold">{entity.name}</h1>
      <p className="text-muted-foreground truncate text-sm">{entity.email}</p>
    </div>
  </div>
  {/* badges, navigator, tabs */}
</div>
```

| Class       | Why it matters                                  |
| ----------- | ----------------------------------------------- |
| `max-w-4xl` | Readable line length; consistent detail width   |
| `mx-auto`   | Horizontal centering                            |
| `space-y-6` | Vertical rhythm between blocks                  |
| `min-w-0`   | Lets child text truncate inside flex containers |

**Anti-pattern:** ad-hoc widths per page (`max-w-2xl` here, `max-w-6xl` there) — picks a detail-page standard and stick to it.

### 2.3 Responsive grid — stats cards & card rows

Content grids are 2-column on mobile (keeps cards legible) and expand on desktop.

```tsx
<div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
  <StatCard />
  <StatCard />
  <StatCard />
  <StatCard />
</div>
```

| Breakpoint        | Columns |
| ----------------- | ------- |
| Mobile (<640px)   | 2       |
| Desktop (≥1024px) | 4       |

**When to diverge:** 3-up featured cards use `grid-cols-1 md:grid-cols-3`. 1-up hero cards skip the grid entirely.

### 2.4 Internal scroll — wide tables inside a bounded container

Wide tables cause page-level horizontal scroll unless you contain them. The pattern: scroll internally inside a rounded border, so the page layout never shifts.

```tsx
<div className="scrollbar-auto w-full overflow-x-auto rounded-xl border">
  <DataTable className="min-w-125" />
</div>
```

| Class               | Why it matters                                    |
| ------------------- | ------------------------------------------------- |
| `overflow-x-auto`   | Enables horizontal scroll on the wrapper          |
| `scrollbar-auto`    | Thin scrollbar that appears on scroll             |
| `rounded-xl border` | Visible bounds that contain the scrolling region  |
| `min-w-125`         | Minimum table width — triggers scroll when needed |

**Required CSS** (`globals.css`, touch-aware scrollbar):

```css
.scrollbar-auto {
  scrollbar-width: thin;
}
@media (pointer: coarse) {
  .scrollbar-auto::-webkit-scrollbar {
    height: 4px;
  }
  .scrollbar-auto::-webkit-scrollbar-thumb {
    background: var(--muted-foreground);
    opacity: 0.5;
  }
}
```

**Anti-patterns:** `overflow-x-hidden` (truncates data), `whitespace-nowrap truncate` on every cell (data loss). Scroll the container, not the cell.

### 2.5 Tab content layout — mobile-wrapping tabs

Tabs must wrap at 375px when they don't fit inline. Override default height so multi-row triggers stay touch-friendly.

```tsx
<Tabs defaultValue="datos" className="w-full">
  <TabsList className="h-auto! w-full flex-wrap p-1.5">
    <TabsTrigger value="datos" className="h-auto py-2.5">
      <User className="h-4 w-4" /> Datos
    </TabsTrigger>
    <TabsTrigger value="actividad" className="h-auto py-2.5">
      <Activity className="h-4 w-4" /> Actividad
    </TabsTrigger>
  </TabsList>
  <TabsContent value="datos">
    <EntityDataTab />
  </TabsContent>
</Tabs>
```

| Class               | Why it matters                           |
| ------------------- | ---------------------------------------- |
| `w-full`            | Tabs span the container width            |
| `h-auto! flex-wrap` | Multi-row allowed; override fixed-height |
| `p-1.5`             | Padding inside the tab bar               |
| `h-auto py-2.5`     | Taller touch targets per trigger         |

---

## 3. Stacked filter pattern — responsive mobile-first

Problem: filter rows with search + 2-3 selects + primary action overflow at 375px.

Solution: **stack vertically on mobile, inline on desktop** using `sm:contents` to dissolve the grid wrapper on `sm+`.

```tsx
<div className="space-y-3 sm:flex sm:flex-wrap sm:items-end sm:gap-4 sm:space-y-0">
  {/* Search — full width on mobile, flexible on desktop */}
  <div className="w-full sm:w-auto sm:min-w-48 sm:flex-1 lg:max-w-xs">
    <SearchInput />
  </div>

  {/* Filters — 2-col grid on mobile, inline on desktop */}
  <div className="grid grid-cols-2 gap-3 sm:contents">
    <RoleFilter />
    <StatusFilter />
  </div>

  {/* Spacer — desktop only, pushes action right */}
  <div className="hidden lg:block lg:flex-1" />

  <div className="flex justify-end sm:justify-start">
    <Button>+ Add</Button>
  </div>
</div>
```

**Key:** `sm:contents` makes the grid wrapper's children behave as if unwrapped on `sm+`, so they join the flex row directly.

---

## 4. Filter cascading — derive, do not hardcode

Per `SK.md §3.1`: when a table has **2+ filters**, each filter's options must be derived from the subset filtered by the **other** filters. Never hardcode static option lists next to a live dataset.

```tsx
// ❌ WRONG — static options regardless of data
const ROLE_OPTIONS = ['admin', 'staff', 'super_admin'];

// ✅ RIGHT — each filter sees options from rows surviving the OTHER filters
const rowsForRole = rows.filter((r) => matchStatus(r, statusFilter)); // skip role filter
const roleOptions = unique(rowsForRole.map((r) => r.role));

const rowsForStatus = rows.filter((r) => matchRole(r, roleFilter)); // skip status filter
const statusOptions = unique(rowsForStatus.map((r) => r.status));
```

**Rule:** only disable cascading if the issue declares it explicitly (e.g. `static filter options — see AC-3`).

---

## 5. URL state hook — the cheapest persistent store

Prefer URL state over client state for anything **bookmarkable or shareable**: filters, pagination, tab selection, sort direction, search query. The URL is durable across refresh, works with back/forward, and supports deep-linking.

```tsx
'use client';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import { useCallback } from 'react';

export function useQueryState(key: string) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const value = searchParams.get(key);
  const setValue = useCallback(
    (next: string | null) => {
      const params = new URLSearchParams(searchParams);
      if (next === null || next === '') params.delete(key);
      else params.set(key, next);
      router.push(`${pathname}?${params.toString()}`, { scroll: false });
    },
    [key, pathname, router, searchParams]
  );

  return [value, setValue] as const;
}
```

**When to use client state instead:** ephemeral UI state (dialog open, hover, focus), controlled form inputs before submit, animation state.

---

## 6. Suspense + Skeleton — mirror the real layout

Skeletons must mirror the **final layout's dimensions** — otherwise the real content lands and causes CLS (Cumulative Layout Shift).

```tsx
// app/users/page.tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<UserListSkeleton />}>
      <UserList />
    </Suspense>
  );
}
```

```tsx
// Skeleton mirrors the real row — same heights, same gaps
export function UserListSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="flex items-center gap-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="space-y-2">
            <Skeleton className="h-4 w-40" />
            <Skeleton className="h-4 w-36" />
          </div>
        </div>
      ))}
    </div>
  );
}
```

**Anti-pattern:** a generic spinner for a data-heavy page. Users perceive it as slower than a correctly-sized skeleton.

---

## 7. Tailwind — predefined scale over arbitrary values

Prefer the scale over `w-[150px]` / `p-[16px]`. Arbitrary values bloat bundle, break design consistency, and skip IDE autocomplete.

| ❌              | ✅         | Value          |
| --------------- | ---------- | -------------- |
| `w-[150px]`     | `w-40`     | 10rem = 160px  |
| `max-w-[400px]` | `max-w-md` | 28rem ≈ 448px  |
| `gap-[20px]`    | `gap-5`    | 1.25rem = 20px |
| `p-[16px]`      | `p-4`      | 1rem = 16px    |

**Exception:** a precise design value with no nearby class (e.g. `w-[37px]` for an icon). Always document the exception in an adjacent comment.

**Responsive direction:** mobile-first. Base = 375px. Add `sm:` / `md:` / `lg:` for larger. Never `max-lg:` / `max-md:` as the primary axis.

**Interactive states:** always cover `hover`, `focus-visible` (ring), `disabled` (pointer-events + opacity).

---

## 8. React — avoid common pitfalls

### 8.1 Derived state vs managed state

```tsx
// ❌ props → state copy drifts
const [items, setItems] = useState(props.items);
useEffect(() => setItems(props.items), [props.items]);

// ✅ derive from props (or use directly)
const items = useMemo(() => processItems(props.items), [props.items]);
```

### 8.2 Stable list keys

```tsx
// ❌ keys can collide (two "Ana")
items.map((item) => <Item key={item.name} />);

// ❌ index-only keys break on reorder/insert
items.map((item, i) => <Item key={i} />);

// ✅ stable domain ID, index as last resort
items.map((item, i) => <Item key={item.id ?? `item-${i}`} />);
```

### 8.3 Stale closures — function updaters

```tsx
// ❌ reads `count` at the time the callback was created
const handleClick = () => setCount(count + 1);

// ✅ function updater — always reads latest
const handleClick = useCallback(() => setCount((prev) => prev + 1), []);
```

---

## 9. Forms — layout + RHF + Zod at the trust boundary

### 9.1 Form layout — elevated card + 2-col grid

Wrap forms in an elevated surface card to give them visual hierarchy against the page background. Use a 2-column grid on desktop for paired fields (first/last name, email/phone), collapsing to 1 column on mobile.

```tsx
<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
  <div className="bg-background rounded-xl p-6 shadow">
    {/* surface elevation — in the TimeKast kit use `neo-outset` (see `sk-tokens-neomorphism`) */}
    <h3 className="text-foreground mb-4 font-semibold">Datos generales</h3>
    <div className="grid gap-6 md:grid-cols-2">
      <FormField name="name" label="Nombre" />
      <FormField name="email" label="Email" type="email" />
    </div>
  </div>

  <div className="flex items-center justify-end gap-3">
    <Button type="button" variant="outline" size="lg">
      Cancelar
    </Button>
    <Button type="submit" size="lg">
      Guardar
    </Button>
  </div>
</form>
```

**Rules:**

- One elevated card per logical section (`Datos generales`, `Permisos`, `Notificaciones`). Don't stack raised-on-raised — break into siblings with `space-y-6`.
- `md:grid-cols-2` for paired fields; full-width on mobile. Fields that accept long input (address, textarea) stay full-width via `md:col-span-2`.
- Actions (`Cancelar` / `Guardar`) live outside the card, right-aligned, with `gap-3`.

> In the TimeKast Starter Kit use the `neo-outset` utility as the card wrapper — see [`sk-tokens-neomorphism`](../sk-tokens-neomorphism/SKILL.md) §1.2.1 for the elevation system.

### 9.2 RHF + Zod validation

Validate at the edge: schema on the server action, same schema for the client form via `@hookform/resolvers/zod`. Zod is the single source of truth — the form derives its rules from it.

```tsx
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email'),
});
type UserInput = z.infer<typeof UserSchema>;

export function UserForm({ onSubmit }: { onSubmit: (data: UserInput) => Promise<void> }) {
  const form = useForm<UserInput>({
    resolver: zodResolver(UserSchema),
    mode: 'onBlur', // validate on blur, re-validate on change after first submit
    defaultValues: { name: '', email: '' },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <input {...form.register('name')} aria-invalid={!!form.formState.errors.name} />
      {form.formState.errors.name && (
        <p role="alert" className="text-destructive text-sm">
          {form.formState.errors.name.message}
        </p>
      )}
      {/* … */}
    </form>
  );
}
```

**Controlled vs uncontrolled:** RHF is **uncontrolled by default** (`register`). Only reach for `Controller` when wrapping a component that controls its own value (Radix Select, custom date picker). Don't mix — it creates double-binding bugs.

**At the boundary:** the server action **re-parses** the same schema. Client validation is UX; server validation is the contract.

---

## 10. CRUD UI wiring — handlers, bulk, highlights, optimism

### 10.1 Table row handlers

A row's click target depends on the primary action:

| Primary action | Pattern                                                 |
| -------------- | ------------------------------------------------------- |
| View detail    | Whole row `<tr onClick>` navigates + `cursor-pointer`   |
| Edit inline    | Only the edit icon cell handles click                   |
| Select (bulk)  | Checkbox cell handles `onChange`; row click selects too |

**Rule:** whatever you make row-clickable, also make keyboard-accessible (`tabIndex={0}`, `onKeyDown` Enter/Space).

### 10.2 Bulk-action toolbar visibility

```tsx
// ❌ toolbar always rendered — empty space when nothing is selected
<BulkActions count={selected.length} />;

// ✅ conditional mount with animation-friendly height reservation
{
  selected.length > 0 && (
    <div className="bg-background sticky top-0 z-10 flex items-center justify-between py-2">
      <span>{selected.length} selected</span>
      <Button variant="destructive" onClick={onBulkDelete}>
        Delete
      </Button>
    </div>
  );
}
```

### 10.3 Row-highlight semantics

Highlights are a semantic channel. Reuse these consistently:

| Intent          | Class                                 |
| --------------- | ------------------------------------- |
| Destructive row | `bg-destructive/10`                   |
| Warning row     | `bg-warning/10` (or amber equivalent) |
| Selected row    | `bg-primary/10`                       |
| Hover           | `hover:bg-muted`                      |

Never invent a new color for "this row is special" — pick from the semantic palette.

### 10.4 Optimistic delete pattern

```tsx
async function handleDelete(id: string) {
  const prev = rows;
  setRows(rows.filter((r) => r.id !== id)); // optimistic
  try {
    const result = await deleteUser(id);
    if (!result.ok) throw new Error(result.error);
    toast.success('Deleted');
    router.refresh(); // re-fetch from server
  } catch (error) {
    setRows(prev); // rollback
    console.error(error);
    toast.error('Could not delete. Try again.');
  }
}
```

**Rule:** optimistic only for idempotent low-risk actions (delete, toggle). Never optimistic for money movement or irreversible writes.

---

## 11. Dialogs — never use native browser dialogs

`alert()` / `confirm()` / `prompt()` / `window.confirm()` are forbidden. They break style, theme, and accessibility.

| ❌                 | ✅                                        |
| ------------------ | ----------------------------------------- |
| `alert('Error')`   | `toast.error(...)` (Sonner or equivalent) |
| `confirm('Sure?')` | `AlertDialog` (shadcn/ui)                 |
| `prompt('Name:')`  | `Dialog` + form component                 |

### Destructive confirmation pattern

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Delete this item?</AlertDialogTitle>
      <AlertDialogDescription>This action cannot be undone.</AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={() => deleteItem(id)}>Yes, delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Messages are always human-readable

| ❌ Shown to user       | ✅ Shown to user                             |
| ---------------------- | -------------------------------------------- |
| `Error: ECONNREFUSED`  | "We couldn't connect. Try again."            |
| `TypeError: undefined` | "Something went wrong. Please reload."       |
| Stack trace            | Friendly toast + `console.error` for the log |

```tsx
try {
  await deleteUser(id);
  toast.success('User deleted');
} catch (error) {
  console.error('Delete user failed:', error);
  toast.error("Couldn't delete the user. Try again.");
}
```

---

## 12. Accessibility checklist

- [ ] `<img>` has `alt` (empty `alt=""` for decorative images)
- [ ] Every input has an associated `<label htmlFor>` or `aria-label`
- [ ] Interactive elements are `<button>`, not `<div onClick>`
- [ ] Navigation uses `<a>` or `<Link>`, not `<div onClick>` + `router.push`
- [ ] `focus-visible` ring on every interactive element (keyboard users)
- [ ] Contrast meets WCAG AA (4.5:1 text, 3:1 large text / UI)
- [ ] Keyboard navigation works end-to-end (Tab, Shift+Tab, Enter, Space, Esc)
- [ ] Dialogs trap focus and restore it on close
- [ ] Live regions (`role="alert"`, `aria-live`) announce async errors
- [ ] Icon-only buttons have `aria-label` or a tooltip with visible text

---

## 13. Portable anti-patterns

| ❌                                | ✅                                     |
| --------------------------------- | -------------------------------------- |
| `<div onClick>`                   | `<button onClick>`                     |
| Inline styles                     | Tailwind classes + `cn()`              |
| CSS modules (in Tailwind stacks)  | Tailwind + `cn()`                      |
| Deep prop drilling                | Context or composition                 |
| `useEffect` to fetch data         | Server Component with `await`          |
| Global store for everything       | URL state when bookmarkable            |
| Arbitrary Tailwind values         | Predefined scale                       |
| `alert` / `confirm` / `prompt`    | Toast / `AlertDialog` / `Dialog`       |
| Raw technical errors to user      | Human-readable messages                |
| Naked icon buttons                | Wrap in `Tooltip` with a label         |
| Hardcoded filter option lists     | Cascading derivation from filtered set |
| Optimistic writes on money        | Server-first with spinner + success    |
| Props-to-state copy + `useEffect` | Derive with `useMemo` or use directly  |

---

Cross-reference: [`sk-ui`](../sk-ui/SKILL.md) — kit-shipped primitives. [`sk-crud-scaffold`](../sk-crud-scaffold/SKILL.md) — CRUD orchestration.
