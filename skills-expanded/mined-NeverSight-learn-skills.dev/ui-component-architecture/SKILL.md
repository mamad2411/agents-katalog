---
name: ui-component-architecture
description: >
  Keep React screens thin and the monorepo's shared UI package (packages/ui,
  imported as @repo/ui) the home for reusable components. Triggers when
  authoring or restyling a page, route, screen, or component in an app that's
  part of a monorepo with a shared UI package — especially when a file is
  trending toward walls of plain <div className="..."> Tailwind markup. Bias
  toward reusing existing @repo/ui primitives and graduating new reusable units
  out of screens into @repo/ui, while avoiding premature over-extraction. Do NOT
  trigger for non-React code, for single-package apps with no shared UI package,
  or for editing the internals of one existing component.
---

# UI component architecture

The failure mode this corrects: an agent authors a screen as a few hundred lines
of `<div className="...">` Tailwind soup — reimplementing a `Button`, `Card`, or
`Badge` that already exists in `@repo/ui`, and never graduating the genuinely
reusable pieces back into the shared package. The result is duplicated styling,
drifting visual language, and screens nobody can read.

The fix is two habits: **reuse before you author**, and **keep screens thin by
extracting reusable units into `@repo/ui`** — without over-extracting one-off
layout glue. In these monorepos the shared package lives at `packages/ui` and is
imported as `@repo/ui`.

## When to use

- Authoring a new page/route/screen in an app under a monorepo with `packages/ui`.
- Restyling or refactoring an existing screen that's heavy with inline divs.
- Building a component that looks like a reusable primitive (button, card,
  badge, input, dialog, empty state, stat, skeleton, avatar).
- The user says "build the X page", "add a Y view", "create a Z component".

## When NOT to use

- Non-React code, or a single-package app with no shared UI package to reuse into
  (still keep components small, but there's nothing to graduate to).
- A genuinely one-off layout wrapper used exactly once — extract on the _second_
  use, not speculatively.
- Editing the internals of one existing component, not adding a new surface.

## Principles

### Reuse before you author

Before writing JSX, inventory what already exists so you don't reinvent it:

- `@repo/ui` — read its barrel (`packages/ui/src/index.ts`) or `package.json`
  `exports` to see what primitives are available. Grep for the thing you need.
- External registries — for blocks not yet in `@repo/ui`, see the
  `shadcn-registry-first` skill. The flow is registry → app screen → graduate the
  stable pieces into `@repo/ui`.

Don't reimplement a `Button`, `Card`, `Badge`, `Input`, `Dialog`, or
`EmptyState` that already exists.

### Keep screens thin

A screen should read as _composition_: a handful of named components plus data
wiring. If a route file is a wall of Tailwind, that's the smell. The target is
that a page's JSX is mostly `<NamedThing .../>` calls and the visual detail lives
inside those components. The moment you're writing the same cluster of divs a
second time, stop and name it.

### Graduate reusable units into `@repo/ui`

The load-bearing heuristic for what moves into the shared package:

- **Graduates:** reused 2+ times (in this app or another), **or** a self-contained
  visual primitive — `Button`, `Card`, `Badge`, `Avatar`, `EmptyState`, `Stat`,
  `Skeleton`, `Input`, `Dialog`.
- **Stays in the app:** app-specific composition (a particular dashboard's
  layout), one-off glue, and anything carrying data-wiring or business logic.
- **When unsure, leave it local.** Extract on the _second_ use, not the first.
  An `@repo/ui` full of single-use components with app-specific props is its own
  smell (see "Avoiding over-extraction").

### Style with tokens and variants, not scattered magic values

- Use theme tokens (CSS variables, the Tailwind theme) — not raw hex literals
  sprinkled through `className`.
- For components with variants, use a `cn` + variant map (or `cva`) rather than
  conditional class-string soup.
- Centralize a repeated cluster of classes into a component, don't copy-paste it.

## Workflow

### 1. Inventory the shared UI package

List what `@repo/ui` already exports (read the barrel / `package.json` exports;
grep for candidates). Note the primitives you'll reuse so you don't rebuild them.

### 2. Sketch the screen as composition

Before writing detail, outline the page as a tree of named components. Tag each
node: _exists in `@repo/ui`_ / _app-specific composition_ / _new but looks
reusable_. This tells you what to import, what to inline, and what to extract.

### 3. Author the screen thin

Compose existing primitives. Inline only app-specific layout. Keep the route file
readable — if it's growing past a screenful of divs, you're missing a component.

### 4. Extract the reusable pieces

For each piece that meets the graduation heuristic:

- Put it under `packages/ui/src/<component>.tsx`.
- Export it from the barrel (`packages/ui/src/index.ts`) or `package.json`
  `exports`.
- Keep props **generic** — no app-specific types, routes, stores, or API clients
  leaking into a UI primitive. A `@repo/ui` component should be dumb and
  presentational; data comes in as props.
- Co-locate variants with `cn`/`cva`.

### 5. Verify

- The screen imports primitives from `@repo/ui` rather than redefining them.
- No app-specific imports (`@/...`, app routers, stores, API clients) inside any
  `@repo/ui` component.
- Types and build pass (`lsp_diagnostics`, `check-types`, build).

## What graduates vs what stays

| Stays in the app                         | Graduates to `@repo/ui`                   |
| ---------------------------------------- | ----------------------------------------- |
| The `/dashboard` page layout             | `StatCard`, `Badge`, `EmptyState`         |
| Route-specific data fetching and wiring  | `Button`, `Input`, `Dialog`, `Skeleton`   |
| A hero used once on one marketing page   | A hero variant reused across 3+ pages     |
| Business logic, feature flags, app state | Presentational primitives that take props |

## Avoiding over-extraction

Over-extraction is the opposite failure and just as costly. Signs you extracted
too eagerly:

- `@repo/ui` components with props named after one specific screen.
- A "reusable" component used exactly once.
- UI primitives importing app stores, routers, or API clients.

Fix: pull the app-specifics back up into the app and keep the primitive dumb. If
it can't be expressed as presentational props, it isn't a shared primitive yet.

## Reference

- `reference/agents-md-rule.md` — a short, paste-able always-on rule for a
  consuming repo's `AGENTS.md`. This is the highest-leverage lever: skills are
  loaded on demand and can under-trigger on "every UI edit," whereas an
  `AGENTS.md` rule is always in context. Drop it into each monorepo that has a
  `packages/ui`.
- `reference/eslint-guardrails.md` — lint rules that enforce the boundaries
  mechanically (no raw hex in app JSX, capped JSX depth, and — most importantly —
  a boundary rule banning app imports inside `@repo/ui`).

## Relationship to other skills

- `shadcn-registry-first` — sources _external_ blocks from registries. This skill
  governs _internal_ reuse and extraction. They compose: registry → app screen →
  graduate stable pieces into `@repo/ui`.
- `coding-standards` — general DRY, file-size, and module-boundary guidance. This
  is the React + monorepo specialization of those principles at component
  granularity.
- `repository-organization` — where directories and packages live. This operates
  one level down, at the component-reuse granularity.
- `vercel-react-best-practices` — performance patterns for the components you
  write and compose.
