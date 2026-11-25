---
name: inertia-patterns
description: Build VILT apps with Inertia.js the intended way - controller-to-page data flow, form handling, partial reloads, shared data, and type sync between Laravel and Vue. Use when building or reviewing Inertia pages and controllers, deciding what data a page receives, handling forms and validation errors, or when an Inertia app over-fetches or drifts out of type sync.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [inertia, vilt, laravel, vue, spa]
---

# Inertia Patterns

Inertia's deal: **the controller is the API and the page gets exactly its props**. Honor that and you skip the whole REST/state-sync circus; break it and you get both circuses at once.

## When to use

- Building or reviewing Inertia pages and their Laravel controllers
- "What data should this page receive?" / props bloat
- Forms, validation errors, file uploads in Inertia
- Type drift between PHP and TypeScript

## Principles

- **The controller shapes the page's data.** Each page gets a deliberate, minimal prop payload — not `Order::all()` and hope.
- **No shadow API.** Don't add JSON endpoints + axios next to Inertia for page data; that reintroduces everything Inertia removed. (Dedicated APIs for third parties/mobile are a different thing.)
- **Server state stays on the server.** After a mutation, redirect and let Inertia re-render with fresh props — don't patch local copies of server data.
- **Types cross the boundary explicitly.** PHP shapes and TS types must come from one source (generated types or shared DTOs), not parallel guesswork.

## Process

### 1. Shape the page props

```php
return Inertia::render('Orders/Index', [
    'orders'  => OrderResource::collection($orders),   // explicit shape, not raw models
    'filters' => $request->only('search', 'status'),
]);
```

- API Resources (or DTOs) for every non-trivial prop — raw models leak columns and break the moment the schema changes
- Lazy-load expensive props so they're only computed when requested: closures / `Inertia::lazy()` for data used by partial reloads
- Authorization data the UI branches on (`can.update`) goes in props — computed server-side from policies, never inferred client-side

### 2. Forms — use the form helper

```ts
const form = useForm({ name: '', email: '' })
form.post(route('users.store'), {
    preserveScroll: true,
})
```

- `useForm` gives you `errors`, `processing`, `isDirty`, `reset()` — don't rebuild it with refs + axios
- Validation: throw it server-side (FormRequest); errors arrive automatically in `form.errors` — no error-shape contract to invent
- Files: the form helper handles multipart; progress via `form.progress`

### 3. Mutations — redirect, don't patch

- Controller action → validate → mutate → `return redirect()->route(...)` (or `back()`) with a flash message
- The page re-renders with fresh props: no client cache to invalidate, no stale list bug
- Flash messages: share via middleware (`HandleInertiaRequests::share`), render in the layout

### 4. Control the payload

| Need | Tool |
|---|---|
| Update one prop (filter a table) | Partial reload: `router.reload({ only: ['orders'] })` |
| Expensive sidebar stats | Lazy prop + explicit `only` request |
| Data every page needs (auth user, flash) | `HandleInertiaRequests::share` — keep it *small*, it rides every response |
| Big lists | Server-side pagination in props, never "all rows, filter in Vue" |

### 5. Keep types in sync

- Generate TS types from PHP (e.g. a types-generation package or shared DTO definitions) — one source of truth
- Page components declare `defineProps<{ orders: Paginated<Order> }>()` against the generated types
- CI check: regenerate types and fail on diff, so drift can't merge

### 6. Review pass

```bash
grep -rn "axios\.\|fetch(" resources/js/Pages    # shadow-API smell in pages
grep -rn "Inertia::render" app/Http/Controllers | wc -l   # map the pages
```

Plus: raw `$model` props (no Resource), shared-data bloat, mutations that return JSON instead of redirecting, pages with `any` props.

## Output format

```markdown
## Inertia review: <page/feature>

### Prop contract
| Prop | Shape (Resource/DTO) | Lazy? | Size concern |
|------|----------------------|-------|--------------|

### Form flows
<form>: useForm ✅/❌, server validation ✅/❌, redirect-after-mutate ✅/❌

### Findings (ranked)
1. <file:line> — <issue> → <fix>

### Type sync
Generated types: ✅/❌ — drift check in CI: ✅/❌
```

## Anti-patterns

- ❌ axios/fetch calls inside Inertia pages for data the controller should provide
- ❌ Raw Eloquent models as props — column leaks and accidental payload bloat
- ❌ Mutating then patching local state instead of redirecting for fresh props
- ❌ Hand-written TS interfaces drifting from PHP shapes
- ❌ Shared data as a junk drawer (every page pays for it on every visit)
- ❌ Client-side filtering of a full-table prop instead of partial reloads with server filtering
- ❌ Rebuilding `useForm` features by hand with refs, axios, and a custom error shape
