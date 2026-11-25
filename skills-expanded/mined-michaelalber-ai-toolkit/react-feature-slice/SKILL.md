---
name: react-feature-slice
audience: team
description: >
  Scaffolds feature-based React / TypeScript architecture using feature folders, presentational
  + container components, custom hooks, a typed data layer, and structural CQRS (query hooks vs
  mutation hooks). React analog of dotnet-vertical-slice and python-feature-slice — no DI
  framework; uses props/context for dependency injection and a query cache for server state. Use
  when creating feature-based React projects, adding React features, organizing components by
  feature rather than by technical type, or scaffolding a feature's data layer.
---

# React Feature Slice Architecture

> "The best code is code that never has to be written."
> -- Jeff Atwood

> "Organize around business capabilities, not technical layers."
> -- Sam Newman, *Building Microservices*

## Core Philosophy

Feature slice architecture organizes code by feature, not by technical type. The default React tutorial
layout — `components/`, `hooks/`, `utils/`, `services/` — spreads one feature across many directories,
so adding "checkout" means touching five folders. This skill replaces that with self-contained vertical
slices: `features/cart/`, `features/checkout/`, each owning its full stack — components, hooks, data layer,
types, and tests.

React has no mediator and no DI container. **Dependency injection is props and context**; the container
resolves nothing for you. **CQRS is a structural and naming convention** — read hooks (`useOrdersQuery`)
versus mutation hooks (`useCreateOrder`) — backed by a query cache (TanStack Query / RTK Query) for server
state, never a library contract.

> **Grounding note:** the KB has no React corpus. Use `collection="javascript"` for TS, `collection="ui_ux"`
> for accessible component design, and cite **react.dev** for hooks/component patterns. Never invent a `react` collection.

**Non-Negotiable Constraints:**
1. **TypeScript `strict`** — every component, hook, and prop is typed; no `any` without justification
2. **Feature isolation** — no cross-feature imports; features communicate through `shared/` or composition only
3. **Data layer owns I/O** — components do not call `fetch`; query/mutation hooks do
4. **Server state in a query cache** — never `useState` + `useEffect` for server data
5. **Presentational components are pure** — they receive data and callbacks via props; no data fetching inside
6. **Barrel exports define the public surface** — other features import only the feature's `index.ts`

**What this skill is NOT:**
- It is NOT a microservices or micro-frontend guide — slices live within one React app
- It is NOT prescriptive about a state library — Context, Zustand, or RTK all fit the conventions
- It is NOT a styling system — bring your own (CSS Modules, Tailwind, etc.)

The 10 domain principles (applied-as examples) and the grounding query map live in
`references/domain-principles.md`. The structural CQRS conventions live in `references/react-cqrs-conventions.md`.
AI discipline rules, the anti-patterns catalog, and error-recovery procedures live in
`references/discipline-and-recovery.md`.

## Workflow

### Phase 1: DETECT

**Objective:** Understand the existing structure before scaffolding.

```bash
# React + tooling versions
grep -E '"(react|typescript|vite|next|@reduxjs/toolkit|zustand|@tanstack/react-query)"' package.json

# TypeScript strictness
grep -n '"strict"' tsconfig*.json

# Existing layout — type-based, feature-based, or mixed
find src -type d -maxdepth 2 | head -30

# Existing data-fetching pattern
grep -rn "useQuery\|createApi\|fetch(\|axios" src/ | head -20
```

Record: React version, bundler (Vite/CRA/Next), TS strict on/off, state/query libraries, current layout, router.

### Phase 2: SCAFFOLD

Create the feature folder. See `references/feature-folder-template.md` for file-by-file content.

```
src/features/<name>/
  components/<Name>List.tsx        # container: wires hooks → view
  components/<Name>ListView.tsx    # presentational: props in, JSX out
  components/<Name>Form.tsx        # form with boundary validation
  hooks/use<Name>sQuery.ts          # read (query hook)
  hooks/useCreate<Name>.ts          # write (mutation hook)
  data/api.ts                       # api client + zod parse; the only I/O
  data/schema.ts                    # zod schemas + inferred types
  types.ts                          # feature-local types
  index.ts                          # barrel: the feature's public surface
  <Name>List.test.tsx               # RTL test
  hooks/useCreate<Name>.test.ts     # hook test
```

### Phase 3: WIRE

Register the slice with the router and (only if shared) a context provider.

```tsx
// app/routes.tsx
import { OrdersPage } from "@/features/orders";   // barrel import only
{ path: "/orders", element: <OrdersPage /> }

// Provider only when prop-drilling earns it:
// <CartProvider> wraps the subtree that needs it, at the feature root.
```

### Phase 4: VERIFY

```bash
npx tsc --noEmit                                 # types clean
npx eslint src/features/<name>                    # incl. hooks + a11y rules
npx vitest run src/features/<name>                # slice tests green
# Cross-feature import check — should print nothing:
grep -rn "features/" "src/features/<name>" | grep -v "features/<name>"
```

## State Block

```xml
<react-feature-slice-state>
  phase: DETECT | SCAFFOLD | WIRE | VERIFY | COMPLETE
  feature_name: [name]
  react_version: [detected]
  existing_structure: type-based | feature-based | mixed | unknown
  query_lib: tanstack | rtk-query | none
  route_registered: true | false
  query_hook_created: true | false
  mutation_hook_created: true | false
  tests_scaffolded: true | false
  last_action: [description]
  next_action: [description]
</react-feature-slice-state>
```

## Output Template

Emit a "Feature Slice Scaffold" report (Files Created / Wiring / Verification checklist) plus the
feature-folder diagram. Both full templates live in `references/output-templates.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `react-component-scaffolder` | Component-level quality (props typing, RTL test, story, a11y). Use to generate the individual components inside a slice. |
| `react-app-scaffolder` | When there is no app yet, scaffold the Vite + TS + router + Vitest skeleton first, then add slices. |
| `react-security-review` | After scaffolding, audit the slice's boundary validation, link/URL handling, and token usage against OWASP. |
| `react-architecture-checklist` | Architecture quality gate. Run after several slices to verify isolation, hooks discipline, and coupling. |
| `tdd-loop` | Drive each hook and component test-first (RED → GREEN → REFACTOR) rather than scaffolding code ahead of tests. |
