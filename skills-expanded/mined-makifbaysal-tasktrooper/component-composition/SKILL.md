---
name: component-composition
category: frontend
description: Use on every UI change - Atomic Design levels, reuse-before-build, correct placement, and import direction through the shared component library.
---
# Component Composition (Atomic Design)

## Overview

All web UI follows Atomic Design on top of a shared component library. The quality bar is reuse and correct placement: a new screen is assembled from existing atoms and molecules, and anything genuinely new is added at the right level so the next screen reuses it too.

**Core principle:** Reuse before you build, and place new components at the level the import-direction rule expects — `ui → atoms → molecules → organisms → templates → pages`.

No design system yet in this repo (no tokens, no `components/` levels, no `INVENTORY.md`)? Lay the foundation with `web-design-system-foundation` first — this skill assumes it already exists.

## The Levels

| Level | What | Web examples |
|-------|------|------|
| `ui/` | Vendor layer: generated/wrapped Radix-shadcn primitives | Dialog, Popover, Tabs, Tooltip |
| **Atom** | Smallest reusable UI, no app logic, variants only | Button, Input, Label, Badge, Icon, Heading, Text, Container, Stack, Link |
| **Molecule** | A few atoms as one reusable unit | FormField (label+input+error), NavLink, PriceTag, Rating, SearchBar |
| **Organism** | A page section composed of molecules/atoms (may contain another organism) | SiteHeader, MobileNav, PricingTable, ContactForm, SiteFooter |
| **Template** | Page skeleton: owns the grid + breakpoints, no data | MarketingLayout, DashboardLayout |
| **Page** | Route component: data + state wiring, composes templates/organisms | `PricingPage`, `ProjectBoardPage` |

## The reuse procedure (every time, before writing a component)

1. Read `src/components/INVENTORY.md`.
2. Grep the level folders for the noun (`grep -ri button src/components`).
3. Found a close match → reuse it, or extend it with a new variant **backward-compatibly** (add a `cva` variant, don't change an existing one's output).
4. Nothing close → create it at the right level (see placement below) and add its `INVENTORY.md` line in the same commit.

## Placement decision list

- Does it fetch data or own app state? → **page** (or a container that wraps a page-level hook).
- Is it a page skeleton with no content, owning only the grid/breakpoints? → **template**.
- Several molecules/atoms forming a page section (pricing grid, contact form, header)? → **organism**.
- Label + input + error, or icon + text pairing — two or three atoms as one reusable unit? → **molecule**.
- A single element with variants and no composition (one button, one badge)? → **atom**.
- A generated/wrapped Radix or shadcn primitive with no app-specific variants of its own? → **`ui/`**.

## Import direction

`ui ← atoms ← molecules ← organisms ← templates ← pages`. A level imports only from levels to its left, plus `lib/`. Same-level imports are allowed ONLY for organisms (an organism may contain another organism). `hooks/` and `api/` are imported only by `pages/`. Where the repo runs `ui-guard` (from `web-design-system-foundation`), it enforces this on every build — a violation fails `npm run build`, it isn't a style note.

## Atom API rules

- No outer margin or absolute positioning — the parent lays out with `gap-*`; an atom that sets its own margin breaks every layout that reuses it.
- Variants through `cva`, never a pile of boolean props; `className` is merged **last** via `cn()` and callers use it for layout only (width, grid placement, alignment) — never to restyle the atom; a new look is a new variant.
- Every interactive state is styled: hover, `focus-visible`, active, disabled, `aria-invalid`, loading where relevant.
- Accepts `ref` as a plain prop (React 19) or `forwardRef` (React 18) — a shared atom that can't take a ref breaks the first caller that needs to measure or focus it.

## Composition over prop explosions

Three or more `isX` booleans on one component is a sign it's actually two components, or that it needs `children`/named slots instead. Prefer:
```tsx
// ❌ boolean-prop explosion
<Card isHighlighted isCompact hasFooter footerText="Save" />

// ✅ composition: the variant is a real prop, content is children/slots
<Card variant="highlighted" size="compact">
  <Card.Footer>Save</Card.Footer>
</Card>
```
An explicit variant component (`PrimaryCard` vs `<Card variant="primary">`) is fine when the two really don't share markup — don't force one component to branch internally just to avoid two small ones.

## Templates and organisms are container-aware

A template owns the grid and the breakpoints (`sm:`/`md:`/`lg:` live here) — organisms placed inside it should not assume a specific viewport width. Where an organism's internal layout depends on the space it's given rather than the screen, use a `@container` query or let the parent grid/flex sizing drive it, so the same organism works in a full-width template and a narrower sidebar slot.

## Existing repos

Map the repo's own folders onto these levels (e.g. `components/common/` ≈ atoms+molecules) and follow them as found. Never restructure an existing repo's component layout inside a feature task — if the mapping is genuinely broken, propose a follow-up task instead of doing it inline.

## Changing a shared component

Grep every caller first (`grep -r "from '@/components/atoms/Button'" src`). Keep the change backward-compatible (new optional prop, new variant) or update every caller in the same task — never leave some callers on an old, incompatible shape. Update `INVENTORY.md` if the component's variants/props changed. `npm run build` must stay green.

## Worked Example

Task: "add a pricing section to the marketing site."

1. Read `INVENTORY.md`, grep `components/atoms` → `Button`, `Badge`, `Heading` already exist. Reuse them.
2. Nothing in `molecules/` prices a plan → new **molecule** `PriceTag` (amount + interval) and **molecule** `PlanCard` (`Heading` + `PriceTag` + `Text` + `Button`, props in, `onSelect` callback out).
3. Nothing in `organisms/` lists several plans → new **organism** `PricingTable` (grid of `PlanCard`, `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`, container-aware, no data fetching).
4. `PricingPage` (page) loads the plan list, wires `onSelectPlan`, and composes `MarketingLayout` (template, already exists) around `PricingTable`.
5. Add three `INVENTORY.md` lines (`PriceTag`, `PlanCard`, `PricingTable`) in the same commit, each with a co-located RTL test (see `component-testing`).

Only `PriceTag`, `PlanCard`, and `PricingTable` are new; `Button`, `Badge`, `Heading`, and `MarketingLayout` are pure reuse.

## Common Mistakes

- Rebuilding an existing atom/molecule inline instead of importing it (always grep first).
- A component that fetches data or reads a global store below the page level — split presentation from data.
- An atom with its own `margin-*` or `position: absolute`.
- Boolean-prop explosions (`isX`, `isY`, `isZ`) instead of a variant prop or composition.
- An organism that hardcodes `md:`/`lg:` assuming it's always full-width — breaks the day it's reused in a sidebar.
- Changing a shared component's props without grepping every caller.
- A component file long enough that you scroll to read it (~150 lines is the point to split).

## Red Flags

- Two screens render visually identical controls built two different ways.
- A hex color or raw Tailwind palette class (`bg-blue-500`) inside a component — `ui-guard`, where it runs, fails the build on this.
- A molecule or organism importing a hook from `hooks/` or a client from `api/`.
- A new component added with no `INVENTORY.md` line.
- A file over ~150 lines that's still growing.
