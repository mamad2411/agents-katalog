---
name: frontend-ui-engineering
description: >
  Production-quality UI discipline. Component architecture, state decisions,
  design-system adherence (no AI aesthetic), a11y (WCAG 2.1 AA), responsive,
  meaningful empty/loading/error states. Code-side methodology paired with
  spec_board mode=ux (spec side) and code_review_board (diff side).
  Triggers when building or refactoring production UI code (build execute, frontend); NOT for UX spec review (use spec_board mode=ux) and NOT for TTY-style tokens (use frontend_design_tty).
status: active
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: frontend-ui-engineering

## Source

agent-skills at `eb07f19` (MIT License, © 2025 Addy Osmani); Forge's register of adopted methods.

## Purpose

**Build production-quality UI** that does not look AI-generated. That means: real design-system adherence, proper accessibility, considered interaction patterns, and no generic "AI aesthetic" (purple gradients, oversized cards, stock layouts).

This skill is **code-side methodology**. It complements:
- `spec_board mode=ux` — UX review of spec artefacts (spec side)
- `code_review_board` — code-diff review (diff side)

The skill is the running build instruction in between: what must be done **during** building so that what the spec side intended and what the diff side reviews come together.

## When to use

- Building new UI components / pages
- Changing existing user-facing interfaces
- Implementing responsive layouts
- Adding interactivity / state management
- Fixing visual / UX issues

### Do not invoke for

- UX spec review (reader-facing surface) -> `spec_board mode=ux`
- Code review of a frontend diff -> `code_review_board` (with UX specialist personas)
- Backend API design -> `api_and_interface_design`
- One-shot a11y audit -> `references/accessibility-checklist.md` + axe-core / pa11y / Lighthouse directly
- Performance tuning of an existing app -> separate discipline (`references/performance-checklist.md` + profiler)

## Standalone rationale

Why a separate skill rather than a mode of `code_review_board` or
`spec_board mode=ux`?

- **`spec_board mode=ux`** = spec-side review of UX artefacts (3 UX
  personas: Heuristic / IA / Interaction). A reviewer pass over the spec, not
  build instructions while code is being written.
- **`code_review_board`** = diff-side review after building. A reviewer pass
  with findings output. UX specialist personas there can load this skill as
  their methodology anchor.
- **`frontend_ui_engineering` (this skill)** = the running build
  discipline **in between**: what must happen during building so that
  spec-side intent (mode=ux) and code-side reviewability (code_review_board)
  come together. Component architecture, state decisions, design-system
  adherence, a11y in code, the 4 states.

Deleting it and integrating it into `code_review_board` as a mode would tie
the discipline to diff reviews — but frontend methodology applies **during
the build** (component file layout, container/presentation split, state-tree
decisions), not just retrospectively in review. Standalone rationale:
methodology container for the build phase, consumed by boards on both sides.

## Component architecture

When laying out a component's files, splitting container from presentation, choosing where state lives, and when
applying spacing, typography and colour: read and follow `skills/frontend_ui_engineering/structure.md` (component
architecture: colocated file structure, composition over configuration, container vs presentation; state
management decision tree; design-system adherence: avoiding the AI aesthetic, spacing scale, typography and colour).

## Accessibility (WCAG 2.1 AA)

When implementing interaction, focus, dialogs or ARIA, the loading / empty / error / populated states, transitions
and optimistic updates, responsive layout, and when loading heavy routes, components or images: read and follow
`skills/frontend_ui_engineering/states-and-a11y.md` (keyboard navigation, ARIA labels, focus management and modal
dialogs, empty / loading / error states; responsive design; loading and transitions; performance).

## Red flags

- Components > 200 lines (split)
- Inline styles or arbitrary px values
- Missing empty / loading / error states
- No keyboard test performed
- Colour as sole indicator
- Generic AI look in production UI
- `<dialog open>` without `showModal()` (non-modal, no focus trap)
- Optimistic updates without onError rollback + onSettled refresh

## Common rationalisations

| Rationalisation | Reality |
|---|---|
| "Accessibility is nice-to-have" | Legal requirement in many jurisdictions + an engineering quality standard |
| "We'll do responsive later" | Retrofitting is 3x more expensive than building it from scratch |
| "Design isn't final yet, no styling" | Use design-system defaults — unstyled UI = broken first impression |
| "It's just a prototype" | Prototypes ship to production. Build the foundation properly. |
| "AI aesthetic is OK for now" | Signals low quality. The project's design system from day 1. |

## Contract

### INPUT

- **Required:** UI component / page / layout spec or an existing UI diff. When the change has a look and an experience contract (`skills/ux_authoring/contracts.md`), they are required input: tokens and component visuals from `look.md`; surfaces, states, component behaviour, wording and the accessibility floor from `experience.md`
- **Optional:** design-system reference (Storybook / Figma / tokens file), brand colours, spacing scale
- **Context:** repo component conventions (`src/components/` layout), style system (Tailwind / CSS Modules / styled-components), `references/accessibility-checklist.md`, `references/performance-checklist.md`

### OUTPUT

**DELIVERS:**
- Component implementation with colocated tests + stories (when Storybook is used)
- A11y-compliant (WCAG 2.1 AA) UI with all 4 states (loading/empty/error/populated)
- Responsive layout (mobile-first, breakpoint-tested)
- Design-system-compliant spacing/typography/colour (no off-scale values, no AI aesthetic)

**DOES NOT DELIVER:**
- **No UX spec review** -> `spec_board mode=ux`
- **No code review** -> `code_review_board` (the frontend diff goes through the board, not this skill)
- **No a11y audit tool run as a mandatory verify gate** -> dedicated tooling (axe-core, pa11y, Lighthouse) provides that. A dev-time spot check during the build (axe-core devtools extension manually or jest-axe in unit tests) is part of the discipline and referenced in DONE — that is not a full audit, it is a smoke test during implementation.
- **No performance profiling of an existing app** -> profiler tooling + `references/performance-checklist.md`
- **No design-system authoring** (token definition, colour-palette selection) -> the look contract (`ux_authoring`) or the project's design system

**ENABLES:**
- Build-workflow verify phase: the frontend diff passes through `code_review_board` with UX specialist personas that use this skill as their methodology anchor
- spec_board mode=ux: a UX spec references this skill as the "how is this implemented" reference
- shipping_and_launch: the pre-launch checklist has a11y state coverage as an item

### DONE

- 4 states covered (loading, empty, error, populated) with `role="status"` / `aria-busy` / etc.
- Keyboard navigation works (Tab through the page, no click trap)
- ARIA labels on icon-only buttons / form inputs without a visible label
- Spacing/typography/colour from the design system (no arbitrary px / hex)
- Responsive tested at 320 / 768 / 1024 / 1440 px
- Empty / error / loading states have meaningful content (no blank screen)
- Console has 0 errors / 0 a11y warnings (axe-core in dev)

### FAIL

- **Retry:** a11y tool warnings -> component edit, re-test
- **Escalate:** design-system conflict (spec demands off-scale spacing or a new colour) -> spec_board mode=ux or Council. A contract slot the build needs that is `open` or missing (a state, a label) -> back to `ux_authoring`, which asks the person; the build does not fill it
- **Abort:** not provided — UI build continues, findings are surfaced

## Boundary

- **Reviews (spec side / code side):** `spec_board mode=ux` + `code_review_board`. This skill provides the methodology that the boards review.
- **Other methodology layers:** `api_and_interface_design` (backend boundary), `security_and_hardening` (auth/input/secrets).
- **Tooling, not a skill:** axe-core / Lighthouse (a11y audit run), Storybook (component workshop), Figma/Tokens Studio (design-token authoring).

## Anti-patterns

- **DO NOT** use `<div onClick=...>` (with or without `role="button"`) as a click target. **INSTEAD** use `<button>` — natively keyboard-focusable + screen-reader affordance + Enter/Space behaviour. If `<button>` does not work for layout reasons: `role="button" tabIndex={0}` PLUS keyboard handler for Enter/Space (without it, `role` is a broken promise).
- **DO NOT** use colour as the sole state indicator (e.g., red border = error). **INSTEAD** icon + text + colour. Why: colour-blind users + reader modes lose the signal.
- **DO NOT** skip heading levels (`h1 -> h3`). **INSTEAD** real hierarchy. Why: screen readers use headings for navigation, skipping = disorientation.
- **DO NOT** ship images without `alt`. **INSTEAD** descriptive alt or `alt=""` if decorative. Why: blank alt = the screen reader reads the filename.
- **DO NOT** auto-play video / animated auto-carousels without pause. **INSTEAD** user control or respect `prefers-reduced-motion`. Why: vestibular disorders, ADHD, plus respect for user attention.
- **DO NOT** return `null` for an empty state. **INSTEAD** a meaningful empty message + action. Why: blank screen = unclear whether loading, error, or empty.
- **DO NOT** prop-drill >3 levels. **INSTEAD** Context or restructure the component tree. Why: every intermediate level must carry the props through, refactoring becomes painful.
- **DO NOT** use AI aesthetic (purple gradients, oversized cards, stock layouts). **INSTEAD** the project's actual design system. Why: signals "low effort", erodes trust + brand.
- **DO NOT** keep components > 200 lines with nested branch logic. **INSTEAD** split container/presentation + custom hook (`use-<name>.ts`) for state + sub-components. Why: monolithic components are unmockable, untestable, refactor-resistant. Red-flag counterpart.

## References

| Topic | SoT |
|-------|-----|
| UX contracts (look, experience) | `skills/ux_authoring/SKILL.md` |
| Spec-side UX review | `skills/spec_board/SKILL.md` (mode=ux: 3 UX personas) |
| Code-side diff review | `skills/code_review_board/SKILL.md` (UX specialists load this skill) |
| A11y detail checklist | `references/accessibility-checklist.md` |
| Performance detail checklist | `references/performance-checklist.md` |
| Pre-launch | `skills/shipping_and_launch/SKILL.md` |
| Cross-boundary with backend | `skills/api_and_interface_design/SKILL.md` |
