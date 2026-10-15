---
name: flutter-atomic-components
category: architecture
description: Use when adding or reusing Flutter UI - organize widgets as atoms, molecules, and organisms in a shared library and never hand-roll a component that already exists
tech_stack: Flutter
---
# Flutter Atomic Components

## Overview

The same atomic-design discipline the web app follows applies to Flutter: build a shared component library organized by level and compose screens from it. This keeps the app visually consistent and makes screens small.

**Core principle:** Reuse before you build. Before writing any button/card/chip/input/list-row, search the component library — hand-rolling a duplicate is a review-blocking defect.

## The Levels

| Level | What | Flutter example |
|-------|------|-----------------|
| **Atom** | Smallest reusable UI, no app logic | `AppButton`, `AppTextField`, `StatusChip`, `Avatar` |
| **Molecule** | A few atoms forming a unit | `TaskCard` (title + chip + avatar), `SearchBar` |
| **Organism** | Section built from molecules/atoms | `TaskList`, `BoardColumn`, `AppBarWithActions` |
| **Screen** | Route wiring organisms to state | `TaskBoardScreen` |

Library lives under `lib/ui/core/{atoms,molecules,organisms}` — the official Flutter architecture layout — alongside `lib/ui/features/<feature>/` for screen-specific composition; follow the app's existing layout if it differs (e.g. a flat `lib/ui/atoms`).

## INVENTORY.md

`lib/ui/core/INVENTORY.md`: header `One line per component: level · name · purpose · variants`, one bullet per component, added in the same commit that creates or meaningfully changes it. Check it before building anything — it's faster than grepping the tree and it's the thing the next task's agent will actually read. If the repo has no component library or theme yet, load `mobile-design-system-foundation` first.

## Rules

- **Before creating a component, check INVENTORY.md / grep the library.** If an atom exists, use it. If it almost fits, extend it backward-compatibly — don't fork a near-duplicate.
- **Place new components at the correct level.** A button is an atom; a card composed of atoms is a molecule. A "component" that fetches data is not a component — split the presentation out.
- **Atoms take data + callbacks, never talk to services.** `AppButton({required this.label, required this.onPressed})`. State/data flows from the screen down.
- **Atoms carry no outer margin of their own** — spacing between atoms is the parent's job (a `Row`/`Column` with `spacing:`, or explicit `SizedBox`/padding at the call site), so the same atom composes correctly in every context without fighting a built-in margin.
- **Style through the theme** (see flutter-widget-architecture) so every instance of an atom looks identical.
- **Changing a shared atom:** grep every call site first; keep the change backward-compatible or update all callers in the same task. The build must stay green.

## Worked Example

Task: "add a priority badge to task cards." Wrong: add a `Container` with a colored label inline in `TaskCard`. Right:
1. Check `INVENTORY.md` / grep atoms → no `PriorityBadge`, but there is a `StatusChip` atom. Priority is distinct enough → add a `PriorityBadge` atom next to it, themed the same way.
2. Compose it into the `TaskCard` molecule.
3. Both the badge atom and the card get a widget test.
4. Add the `PriorityBadge` line to `INVENTORY.md` in the same commit.

Now every screen showing a task card gets the badge for free, consistently.

## Common Mistakes

- Inline `Container`/`Text` styling that reinvents an existing atom.
- A component with a network/service call inside → not a component.
- New component dumped at the wrong level (an organism where an atom belongs).
- Breaking a shared atom's constructor without updating callers.
- A new component added to the library with no `INVENTORY.md` line.
- An atom with a built-in outer margin, so it looks right in one layout and wrong in the next.

## Red Flags

- Two screens render visually identical buttons built differently.
- A "widget" imports a repository or http client.
- Copy-pasted styled `Container`s across screens.
- `lib/ui/core/` (or the repo's component folder) with no `INVENTORY.md`.
