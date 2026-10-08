---
name: flutter-mail-project-architecture
description: Use when planning, scaffolding, or refactoring the overall Flutter Inbox One project structure in this repository, especially when deciding file placement, MVC boundaries, routing/theme foundations, or stage order. Do not use for isolated single-layer edits that clearly belong only to models, services, controllers, or views.
---

# Flutter Mail Project Architecture

## Read first

- `dev/PRD.md`
- `dev/TDD.md`
- `dev/DELIVERY_PLAN.md`
- Root `AGENTS.md`
- The closest nested `AGENTS.md` for the directories you touch

## Core architecture

- This repository follows an MVC-style Flutter structure:
  - `lib/models`
  - `lib/services`
  - `lib/controllers`
  - `lib/views`
  - `lib/other`
- Keep cross-layer responsibilities clean:
  - models define data shapes
  - services talk to APIs/local storage
  - controllers own state and actions
  - views render UI
  - other contains router/theme/utils/constants

## Delivery order

- Respect the staged flow in `dev/DELIVERY_PLAN.md`.
- Prefer this order unless the user explicitly reprioritizes:
  1. Foundation
  2. Inbox Parity
  3. Action & AI Completion

## Structural decisions

- Preserve document-defined folder names and boundaries unless the docs are intentionally updated.
- If a request would mix multiple responsibilities into one layer, split the work before coding.
- When introducing shared logic, place it in the narrowest stable layer instead of leaking it upward into views or downward into models.

## Output expectations

- When you make structural changes, mention which stage the work belongs to.
- Call out any doc conflict before silently diverging from the PRD/TDD.
