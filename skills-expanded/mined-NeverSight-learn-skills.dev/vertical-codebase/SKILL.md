---
name: vertical-codebase
description: >
  Apply vertical (domain-first) codebase architecture to any project. Use this skill whenever
  a user asks where to put a file, how to structure a codebase, how to organize code by feature
  or domain, how to refactor a "horizontal" structure (components/, hooks/, utils/, types/),
  or asks about code colocation, monorepo boundaries, shared code, or module ownership.
  Also trigger when the user creates a new module and needs to decide where it belongs, or
  when reviewing a PR that touches file organization. Works for any language or framework
  (Python, TypeScript, Go, Rust, etc.) — not just React or frontend.
---

# Vertical Codebase Architecture

## Core Mental Model

**Code that changes together lives together.**

The fundamental question when placing any file is:

> _"What does this code DO, not what TYPE of thing is it?"_

Two structures to recognize:

### ❌ Horizontal (organize by technical type)

```
src/
  components/   ← all UI components mixed together
  hooks/        ← all hooks mixed together
  utils/        ← everything else
  types/        ← all types
  services/     ← all API calls
```

Problem: to understand or change one feature, you jump across 4+ folders.

### ✅ Vertical (organize by domain/functionality)

```
src/
  dashboard/    ← everything related to the dashboard
  billing/      ← everything billing-related
  auth/         ← everything auth-related
  design-system/ ← truly generic, reusable across projects
  shared/       ← shared business logic (not generic enough for design-system)
```

Benefit: one feature = one folder. Easy to find, easy to own, easy to delete.

---

## The Placement Decision Tree

When deciding where a file goes, work through these questions in order:

```
1. Is it tied to a specific feature or domain?
   YES → put it in that vertical (e.g. src/billing/)
    │
    └── Is it used by multiple features?
        YES → does it contain business logic specific to this app?
               YES → make it its own vertical or put in /shared
               NO  → put it in /design-system (or /lib)
        NO  → keep it private inside the feature vertical

2. Is it purely generic with zero business logic?
   (could live in any project, any company)
   YES → /design-system or /lib

3. Is it infrastructure / cross-cutting concern?
   (logging, config, error handling, i18n, routing)
   YES → /infrastructure or /core
```

---

## Vertical Structure (inside a vertical)

Inside each vertical, organize however makes sense — flat is often fine:

```
src/billing/
  billing-service.ts
  billing-types.ts
  billing-utils.ts
  invoice-list.tsx      (if frontend)
  use-invoice.ts        (if frontend)
  invoice.test.ts
```

**Flat > nested** inside a vertical. Only add sub-folders when the vertical grows large enough to justify it (50+ files).

No barrel/index files. Boundaries are enforced by the linter, not by what you choose to export.

---

## Enforcing Boundaries with the Linter

Declaring verticals is not enough — **enforce the dependency direction with lint rules**.

The generic rule is:

> A feature vertical can only import from `shared`, `infrastructure`, and `design-system`. Never from another feature vertical.

```
feature vertical  →  shared          ✅
feature vertical  →  infrastructure  ✅
feature vertical  →  design-system   ✅
feature vertical  →  feature vertical ❌ lint error
shared            →  feature vertical ❌ lint error
design-system     →  anything        ❌ lint error
```

If two verticals need to communicate, the answer is to **extract the shared code into `/shared`**, not to create an exception in the linter.

### TypeScript / JS — `eslint-plugin-boundaries`

```js
// eslint.config.js
import boundaries from "eslint-plugin-boundaries";

export default [
  {
    plugins: { boundaries },
    settings: {
      "boundaries/elements": [
        {
          type: "feature",
          pattern: "src/!(shared|infrastructure|design-system)/*",
        },
        { type: "shared", pattern: "src/shared/*" },
        { type: "infrastructure", pattern: "src/infrastructure/*" },
        { type: "design-system", pattern: "src/design-system/*" },
      ],
    },
    rules: {
      "boundaries/element-types": [
        "error",
        {
          default: "disallow",
          rules: [
            {
              from: "feature",
              allow: ["shared", "infrastructure", "design-system"],
            },
            { from: "shared", allow: ["infrastructure", "design-system"] },
            { from: "infrastructure", allow: ["design-system"] },
            { from: "design-system", allow: [] },
          ],
        },
      ],
    },
  },
];
```

### Other languages

| Language       | Tool                                                                         |
| -------------- | ---------------------------------------------------------------------------- |
| Python         | `import-linter`                                                              |
| Go             | `internal/` package — compiler-enforced, no cross-package imports by default |
| Rust           | Cargo workspaces + `pub` / `pub(crate)` visibility                           |
| Java/Kotlin    | Package-private + ArchUnit                                                   |
| Monorepo (any) | `nx` dependency rules, `pnpm` workspaces                                     |

---

## Shared vs Design-System vs Feature

This is the most common point of confusion. Use this table:

| Code                                      | Where it goes               | Why                                                        |
| ----------------------------------------- | --------------------------- | ---------------------------------------------------------- |
| Generic button, input, modal              | `/design-system`            | No business logic, reusable anywhere                       |
| `useMediaQuery`, `useDebounce`            | `/design-system` or `/lib`  | Pure utility, zero business logic                          |
| `useCurrentUser`                          | `/auth` or `/user` vertical | Business logic, even if used everywhere                    |
| `PageFilters` component (used on 5 pages) | `/page-filters` vertical    | Shared but product-specific                                |
| `formatCurrency`                          | `/shared` or `/billing`     | Depends: generic math → shared, billing-specific → billing |
| Error boundary wrapper                    | `/infrastructure`           | Cross-cutting concern                                      |

**The test for design-system:** _"Could this exist unchanged in a completely different product?"_

- Yes → design-system / lib
- No → it's a vertical or shared business logic

---

## Language-Specific Examples

### TypeScript / Node.js

```
src/
  auth/
    auth-service.ts
    auth-middleware.ts
    auth-types.ts
    auth.test.ts
  users/
    user-repository.ts
    user-service.ts
    user-types.ts
  billing/
    stripe-client.ts
    billing-service.ts
    billing-types.ts
  shared/
    pagination.ts
    date-utils.ts
  infrastructure/
    logger.ts
    config.ts
    database.ts
```

### Python

```
src/
  auth/
    __init__.py
    service.py
    middleware.py
    models.py
    test_auth.py
  billing/
    __init__.py
    stripe.py
    service.py
    models.py
  shared/
    __init__.py
    pagination.py
    date_utils.py
  infrastructure/
    logger.py
    config.py
    database.py
```

### Go

```
internal/
  auth/
    handler.go
    service.go
    repository.go
    types.go
  billing/
    handler.go
    service.go
    stripe.go
  shared/
    pagination.go
    timeutil.go
pkg/           ← truly public/reusable packages (like design-system)
  middleware/
  validator/
```

### Frontend (React, Vue, Svelte...)

```
src/
  dashboard/
    DashboardPage.tsx
    dashboard-store.ts
    use-dashboard-data.ts
    dashboard-types.ts
  widgets/
    WidgetCard.tsx
    use-widget.ts
    widget-types.ts
    widget-api.ts
  design-system/
    Button.tsx
    Modal.tsx
    useMediaQuery.ts
    tokens.css
  shared/
    use-current-user.ts
    format-currency.ts
  infrastructure/
    router.ts
    i18n.ts
    error-boundary.tsx
```

---

## Common Mistakes to Avoid

**1. Placing by type reflex**

> "It's a hook/service/util, so it goes in /hooks /services /utils"

→ Always ask WHAT it does first, not WHAT it is.

**2. Over-sharing**

> "I might need this elsewhere, so I'll put it in /shared"

→ Keep things in their vertical until you actually need to share them. YAGNI.

**3. Under-splitting**

> "It's used in billing AND dashboard, so it goes in /shared"

→ If the shared code is substantial, give it its own vertical (`/invoices`, `/reports`...).

**4. Confusing "used everywhere" with "generic"**

> "`useCurrentUser` is used in 10 places, so it's design-system material"

→ Popularity ≠ genericity. It has business logic → vertical or shared.

**5. Nesting too deep**

> `src/features/billing/components/invoice/list/items/InvoiceItem.tsx`

→ Flat is better. Add one level of nesting only when a vertical truly warrants it.

---

## Refactoring a Horizontal Codebase

When the user has an existing horizontal structure to migrate:

1. **Audit first** — list all files and identify natural clusters (what "talks to" what)
2. **Start with leaf domains** — pick a self-contained feature with no dependents
3. **Move, don't copy** — create the vertical, move files, fix imports
4. **Add a lint rule** — enforce the boundary before moving on
5. **Repeat domain by domain** — never do a big-bang rewrite

> 💡 Read `references/refactoring-guide.md` for a step-by-step migration plan.

---

## Quick Reference Card

| Question                             | Answer                                                               |
| ------------------------------------ | -------------------------------------------------------------------- |
| Where does X go?                     | In the vertical that OWNS the functionality                          |
| What's a vertical?                   | A folder grouping code by what it does, not what it is               |
| What goes in design-system?          | Zero business logic, could exist in any project                      |
| What goes in shared?                 | Business logic used by multiple verticals                            |
| What goes in infrastructure?         | Cross-cutting concerns (logging, config, DB)                         |
| How do verticals talk to each other? | Direct imports, but direction enforced by linter                     |
| Two verticals need to share code?    | Extract to /shared — never create a linter exception                 |
| When to create a new vertical?       | When a concept is big enough to own, or when shared code warrants it |
