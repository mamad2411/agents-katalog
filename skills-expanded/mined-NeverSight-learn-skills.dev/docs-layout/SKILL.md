---
name: docs-layout
description: >
  Use when setting up a project's `docs/` folder or deciding where a new decision,
  plan, runbook, report, handoff, wireframe, or reference document belongs and what
  to name it. Applies to both backend and frontend projects. Covers a shared spine
  plus project-type extras, with naming conventions for phased, dated, and flat files.
---

# docs-layout

## Overview

A normalized `docs/` layout with a shared spine plus project-type extras. **Folders are created on first use, never scaffolded empty.** Naming conventions encode time semantics: phased (ordered work), dated (time-anchored events), flat (living reference).

## Layout

**Shared spine** — applies to every project:

```
docs/
├── decisions/     # architectural decisions / trade-off rationale
├── roadmap/       # phased multi-step plans
├── reports/       # dated analyses, investigations, postmortems
├── runbooks/      # operational guides (deploy, rollback, recovery, routine ops)
└── reference/     # specs, schemas, API contracts, long-lived reference material
```

**Backend extras** — add on top of the spine:

```
docs/
└── handoffs/      # session-to-session handoffs (in-flight work, next steps)
```

**Frontend extras** — add on top of the spine:

```
docs/
├── brand/         # brand guidelines, visual identity
└── wireframes/    # UX wireframes (locale-suffixed: .en.md, .es.md, ...)
```

## Placement table

| I want to add… | Goes in | Naming |
|---|---|---|
| Architectural decision / trade-off rationale | `decisions/` | `YYYY-MM-DD-topic.md` |
| Phase of a multi-step implementation plan | `roadmap/` | `phase-N-topic.md` |
| Operational guide (deploy, rollback, recovery) | `runbooks/` | `topic.md` (flat kebab) |
| Dated analysis tied to a specific event | `reports/` | `YYYY-MM-DD-topic.md` |
| Session-to-session handoff (backend only) | `handoffs/` | `YYYY-MM-DD-topic.md` |
| API spec, schema, reference contract | `reference/` | `topic.md` (flat kebab) |
| Brand guidelines (frontend only) | `brand/` | `topic.md` (flat kebab) |
| UX wireframe (frontend only) | `wireframes/` | `feature-name.LOCALE.md` |

## Naming conventions

- **Phase prefix** (`phase-N-topic.md`) — `roadmap/` only. Encodes ordered work within a plan. Flat inside the folder; only split into subfolders when multiple concurrent roadmaps exist.
- **ISO date prefix** (`YYYY-MM-DD-topic.md`) — `decisions/`, `reports/`, `handoffs/`. Chronological sort is the natural sort; no registry needed to avoid collisions.
- **Flat kebab-case** (`topic.md`) — `runbooks/`, `reference/`, `brand/`. Living references; revisions happen in-place with git history as the audit trail. Date or number prefixes here imply staleness or ordering that don't apply.
- **Locale suffix** (`topic.LOCALE.md`) — `wireframes/` only. `en`, `es`, etc. Applied *after* the kebab slug, before the extension.

## Common mistakes

- **Naming the folder `adr/` with sequential `NNNN-` prefixes.** Use `decisions/` with ISO date prefix. Sequential numbering requires a registry to avoid collisions across concurrent branches; dates don't.
- **Naming the folder `plans/` instead of `roadmap/`.** `plans/` is ambiguous (evergreen plan? one-off plan? execution artifact?). `roadmap/` is unambiguously the evergreen phased plan.
- **Creating a top-level `specs/` folder.** Specs are reference material — they go in `reference/`. Keeping them in a sibling folder fragments the "where do I look up contracts?" question.
- **Nesting every plan in its own subfolder.** Flat phase files inside `roadmap/` work until you have concurrent roadmaps — only then split into subfolders. Don't pre-structure for hypothetical future plans.
- **Scaffolding empty folders with `.gitkeep`.** The pattern is documentation, not scaffolding. Folders appear when the first file of that type is created.
- **Putting wireframes in `reference/`.** Wireframes are frontend-domain-specific and locale-variant; they need their own folder with the locale-suffix naming convention.

## Scope

This covers the shared docs layout. A project may add domain-specific folders (`prompts/`, `migrations/`, `schemas/`, etc.) alongside `docs/` without touching the shared layout.
