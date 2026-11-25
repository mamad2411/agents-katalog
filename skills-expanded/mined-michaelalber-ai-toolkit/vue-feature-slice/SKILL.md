---
name: vue-feature-slice
audience: team
description: >
  Scaffolds feature-based Vue / TypeScript architecture using feature folders, presentational
  + container SFCs, composables, a typed data layer, and structural CQRS (query composables vs
  mutation composables). Vue analog of dotnet-vertical-slice and react-feature-slice — no DI
  framework; uses props/provide-inject for dependency injection and a query layer for server
  state. Use when creating feature-based Vue projects, adding Vue features, organizing
  components by feature rather than by technical type, or scaffolding a feature's data layer.
---

# Vue Feature Slice Architecture

> "The best code is code that never has to be written."
> -- Jeff Atwood

> "Organize around business capabilities, not technical layers."
> -- Sam Newman, *Building Microservices*

## Core Philosophy

Feature slice architecture organizes code by feature, not by technical type. The default Vue tutorial
layout — `components/`, `composables/`, `utils/`, `services/` — spreads one feature across many
directories, so adding "checkout" means touching five folders. This skill replaces that with
self-contained vertical slices: `features/cart/`, `features/checkout/`, each owning its full stack —
components, composables, data layer, types, and tests.

Vue has no mediator and no DI container. **Dependency injection is props and `provide`/`inject`**; the
container resolves nothing for you. **CQRS is a structural and naming convention** — read composables
(`useOrdersQuery`) versus mutation composables (`useCreateOrder`) — backed by a query layer (TanStack
Query for Vue / Pinia actions) for server state, never a library contract.

> **Grounding note:** the KB has a Vue 2/3 corpus under `collection="javascript"` (alongside TS). Use
> `collection="ui_ux"` for accessible component design, and cite **vuejs.org** for composable/component
> patterns. Never invent a `vue` collection.

**Non-Negotiable Constraints:**
1. **TypeScript `strict`** — every component, composable, and prop is typed; no `any` without justification
2. **Feature isolation** — no cross-feature imports; features communicate through `shared/` or composition only
3. **Data layer owns I/O** — components do not call `fetch`; query/mutation composables do
4. **Server state in a query layer** — never `ref` + `onMounted` for server data
5. **Presentational components are pure** — they receive data and callbacks via props/emits; no data fetching inside
6. **Barrel exports define the public surface** — other features import only the feature's `index.ts`

**What this skill is NOT:**
- It is NOT a microservices or micro-frontend guide — slices live within one Vue app
- It is NOT prescriptive about a state library — a plain `provide`/`inject` context or Pinia both fit the conventions
- It is NOT a styling system — bring your own (CSS Modules, Tailwind, etc.)

The 10 domain principles (applied-as examples) and the grounding query map live in
`references/domain-principles.md`. The structural CQRS conventions live in `references/vue-cqrs-conventions.md`.
AI discipline rules, the anti-patterns catalog, and error-recovery procedures live in
`references/discipline-and-recovery.md`.

## Workflow

### Phase 1: DETECT

**Objective:** Understand the existing structure before scaffolding.

```bash
# Vue + tooling versions
grep -E '"(vue|typescript|vite|nuxt|pinia|vuex|@tanstack/vue-query)"' package.json

# TypeScript strictness
grep -n '"strict"' tsconfig*.json

# Existing layout — type-based, feature-based, or mixed
find src -type d -maxdepth 2 | head -30

# Existing data-fetching pattern
grep -rn "useQuery\|defineStore\|fetch(\|axios" src/ | head -20
```

Record: Vue version, bundler (Vite/Vue CLI/Nuxt), TS strict on/off, state/query libraries, current layout, router.

### Phase 2: SCAFFOLD

Create the feature folder. See `references/feature-folder-template.md` for file-by-file content.

```
src/features/<name>/
  components/<Name>List.vue        # container: wires composable → view
  components/<Name>ListView.vue    # presentational: props in, template out
  components/<Name>Form.vue        # form with boundary validation
  composables/use<Name>sQuery.ts    # read (query composable)
  composables/useCreate<Name>.ts    # write (mutation composable)
  data/api.ts                       # api client + zod parse; the only I/O
  data/schema.ts                    # zod schemas + inferred types
  types.ts                          # feature-local types
  index.ts                          # barrel: the feature's public surface
  <Name>List.test.ts                # component test
  composables/useCreate<Name>.test.ts  # composable test
```

### Phase 3: WIRE

Register the slice with the router and (only if shared) a `provide`/`inject` context.

```ts
// app/routes.ts
import { OrdersPage } from "@/features/orders";   // barrel import only
{ path: "/orders", component: OrdersPage }

// provide/inject only when prop-drilling earns it:
// provide(CartKey, cart) at the feature root; useCart() calls inject(CartKey).
```

### Phase 4: VERIFY

```bash
npx vue-tsc --noEmit                             # types clean (SFC-aware)
npx eslint src/features/<name>                    # incl. vue + a11y rules
npx vitest run src/features/<name>                # slice tests green
# Cross-feature import check — should print nothing:
grep -rn "features/" "src/features/<name>" | grep -v "features/<name>"
```

## State Block

```xml
<vue-feature-slice-state>
  phase: DETECT | SCAFFOLD | WIRE | VERIFY | COMPLETE
  feature_name: [name]
  vue_version: [detected]
  existing_structure: type-based | feature-based | mixed | unknown
  query_lib: tanstack-vue-query | pinia | none
  route_registered: true | false
  query_composable_created: true | false
  mutation_composable_created: true | false
  tests_scaffolded: true | false
  last_action: [description]
  next_action: [description]
</vue-feature-slice-state>
```

## Output Template

Emit a "Feature Slice Scaffold" report (Files Created / Wiring / Verification checklist) plus the
feature-folder diagram. Both full templates live in `references/output-templates.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `vue-component-scaffolder` | Component-level quality (props typing, component test, story, a11y). Use to generate the individual components inside a slice. |
| `vue-app-scaffolder` | When there is no app yet, scaffold the Vite + TS + router + Vitest skeleton first, then add slices. |
| `vue-security-review` | After scaffolding, audit the slice's boundary validation, link/URL handling, and token usage against OWASP. |
| `vue-architecture-checklist` | Architecture quality gate. Run after several slices to verify isolation, reactivity discipline, and coupling. |
| `tdd-loop` | Drive each composable and component test-first (RED → GREEN → REFACTOR) rather than scaffolding code ahead of tests. |
