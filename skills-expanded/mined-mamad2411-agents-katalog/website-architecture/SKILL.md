---
name: website-architecture
description: Use when planning, scaffolding, restructuring, or documenting the web app: application mode, stack, routes, data flow, frontend/backend boundary, and the design-quality gate.
---

# Website Architecture Skill

The structural phase that happens before UI code is written. It sits between repository layout
(`docs/skills/repository-structure/SKILL.md`) and visual implementation, and it owns the decisions
recorded in `docs/architecture.md`.

## Core Rule

Do not generate isolated visual pages before structure, routes, stack choices, data flow, and
design-quality requirements are defined and written down.

## This Repository's Answers

These are already decided. Read them before proposing anything; change them deliberately, not
incidentally.

| Decision | Current answer | Recorded in |
| --- | --- | --- |
| Application mode | Flask monolith — one served page + ten JSON blueprints, no build step | `docs/architecture.md` |
| Rendering | A vendored runtime hydrates an inline template in the browser | `docs/architecture.md` |
| Styling | Inline styles + per-theme CSS custom properties; no framework, no stylesheets | `docs/design-system.md` |
| Routing | Flask owns HTTP; the client hash-routes three top-level views | `docs/routes.md` |
| Data flow | Scrapers → SQLite → `/api/*` → the page | `docs/data-flow.md` |
| Boundary | Server-side validation in route handlers; JSON contracts | `docs/api-contract.md` |
| Long-running work | `POST .../start` + poll `.../status/<id>`, in-memory task stores | `docs/api-contract.md` |
| Auth | None — single user, local-first | `docs/architecture.md` |
| Code location | `utils/` + `app.py`, not `web/` (deferred migration) | `docs/structure.md` |

## When Re-Deciding (the React rebuild)

The planned React overhaul re-opens the whole table. When that work starts, make each choice
explicitly and record it — do not let a framework's defaults decide by omission:

- language (JS or TS) and rendering model (SPA, SSR, SSG, server-rendered)
- framework, styling layer, and component primitives
- data fetching/caching, forms and validation, routing, motion
- testing: unit, component, route, API, accessibility, responsive, build, lint, type-check

Rules that survive any stack choice:

- Include a library only when it has a defined job. No two routers, two form libraries, or two
  animation systems without a stated reason.
- Record every library in `docs/architecture.md`, every command in `docs/workflow.md`, and any
  structural ownership in `docs/structure.md` + `docs/component-map.md`.
- If the choice is genuinely open, propose a conservative stack and ask before installing.

## Route Map

Every route is listed in `docs/routes.md` before implementation, with: path, method, purpose,
data dependencies, the component that owns it, the backend endpoints it calls, and its loading,
empty, and error states.

## Design-Quality Gate

`docs/design-system.md` must define, before UI work is called done:

- the project-specific visual motif and the token set that expresses it
- color, typography, radius, shadow, icon, and spacing rules
- concrete domain vocabulary for UI copy
- at least one layout decision specific to this project
- required loading, empty, partial-data, error, and success states
- mobile-specific layout decisions (see `docs/skills/accessibility-mobile/SKILL.md`)

Reject generic AI-site patterns: vague productivity copy, decorative glowing gradients, fake
metrics, abstract orb imagery, and repeated identical feature-card grids.

## Required Documentation

Create or update, in the same change as the code: `docs/architecture.md`, `docs/structure.md`,
`docs/routes.md`, `docs/component-map.md`, `docs/data-flow.md`, `docs/deployment.md`,
`docs/design-system.md`, and `docs/api-contract.md`.
