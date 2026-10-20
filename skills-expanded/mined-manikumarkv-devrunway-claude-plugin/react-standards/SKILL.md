---
name: react-standards
description: React best practices, performance rules, and anti-patterns. Load when writing, reviewing, or discussing any React/TypeScript frontend code, components, hooks, or state management.
user-invocable: false
stack: frontend/react
paths:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/hooks/**"
---

Full rules in [react.md](react.md). Always-on summary:

**Follow the project's existing choices first.** These are the defaults only where the project hasn't chosen:
- React 18+ with TypeScript strict
- UI components: the project's component library (shadcn/ui, MUI, Chakra, Ant Design…). Check what exists before building anything. Library-specific rules load from their own `ui-components/*` layers
- Server state: React Query (TanStack Query) v5 — `useQuery(` for reads, `useMutation` for writes — never `fetch` in `useEffect`
- Forms: React Hook Form with `zodResolver(schema)` when the project uses Zod
- i18n: if the project is localised, every user-visible string goes through its translation function (`t()` with react-i18next). Don't add i18n unprompted
- Testing: Vitest or Jest + React Testing Library + MSW

**Single sources of truth:**
- One constants module (e.g. `src/lib/constants.ts`) for magic values: numbers, limits, timeouts
- One API routes module (e.g. `src/lib/api-routes.ts`) for every endpoint path, including parameterised ones
- Never inline a URL string, page size or debounce delay in a component

**Components:**
- Functional only · explicit `interface` props · max ~150 lines
- Named exports · co-located `.test.tsx` · a feature's `index.ts`, if any, exports only its public API; inside the app, import from the file directly

**URL accessibility — every view must be deep-linkable:**
- Every feature has a dedicated route — create → `/resource/new`, edit → `/resource/:id/edit`, detail → `/resource/:id`
- All list state (filters, search, sort, cursor) lives in URL search params via `useSearchParams()` — never in `useState`
- Tab selection → `?tab=` in URL. Browser back button must restore previous state
- After create/edit mutations, `navigate()` to the detail page — never stay on the same page and show a modal

**UI patterns — modals and notifications:**
- **Modals (the library's alert dialog) only for destructive confirmations** — "Delete?" / "Archive all?" — never for create/edit forms
- **All feedback via the library's toast/snackbar** (Sonner with shadcn: `toast.success()` · `toast.error()` · `toast.promise()`)
- Field-level validation errors inline under the field, not in a toast
- Mount the toast container once at the app root, never per component

**Never:**
- `any` type
- Raw `console.*` in production code — use the project's logger or error reporter (e.g. Sentry)
- `useEffect` for data fetching
- Components defined inside components
- Default exports inside feature folders
- Inline `style={{}}` for static values
- Business logic in component body (belongs in a hook)
- Server state stored in Zustand/Redux
- Build a button, input, dialog, select, table or badge from scratch when the project's component library has one
- Open a create/edit form in a modal — give it its own page/route
- Show success/error/warning in a modal alert — use `toast` instead

**Re-render rules (see react.md for full examples):**
- Hoist static JSX and non-primitive defaults outside components
- Functional `setState` for stable callback refs
- Primitive useEffect dependencies, never objects
- `useMemo` only for genuinely expensive computations
- `startTransition` for non-urgent updates
- `useRef` for values that change without needing re-renders

**Performance rules (see react.md for full examples):**
- `Promise.all()` for independent async operations — never sequential awaits
- `React.lazy` + `Suspense` for heavy components
- Import library modules directly (`lodash-es/debounce`), never whole-package barrels that defeat tree-shaking
- Map/Set for O(1) lookups instead of array.find/includes
- Hoist RegExp to module scope
- `{ passive: true }` on touch/wheel listeners


**Related skills — apply together:**
- `typescript-patterns` — type all props, events, and hook return values
- `composition-patterns` — compound components, context shape, children over render props
- `testing-standards` — every component needs loading/success/empty/error test states
- `accessibility` — semantic elements, focus management, aria attributes
- `error-handling` — error boundaries around every async feature, ApiError in mutations