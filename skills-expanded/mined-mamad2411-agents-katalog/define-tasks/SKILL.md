---
name: define-tasks
description: Break a project definition or briefing into actionable task files and update _OVERVIEW. Use when ready to create implementable task files from an overview.
---

# Define tasks

Emit **implementable-one-session** markdown tasks + hydrate **`_OVERVIEW`** work-package grid.

**Context:** **`project-workflow.mdc`**, **`workpkg-hygiene.mdc`** (filenames `NN[ABC]-task-slug-project.md`; parallel sibling streams share prerequisites → `02A/02B`).

---

## Preconditions

`_OVERVIEW` exists (otherwise stub Mission/Goals/Constraints minimally, then proceed).

## Task file blueprint (~≤1.5 pages)

1. **Agent instructions (START HERE)** — obedience preamble (“follow sections in order”, “respect dependencies”, etc.).
2. **Overview**, **Scope** (`In`, `Out`, boundaries), **Dependencies** (`Provides`, `Blocks`).
3. **Implementation tasks** — numbered, observable outcomes.
4. **Technical notes** — integration hooks only when non-obvious.
5. **Completion** — **single** acceptance + Final Steps block (no duplicated “definition of done” headings).

Reuse project-level bullets from **`_OVERVIEW`** by reference—not copy/paste novels per task.

## Steps

1. Decompose logically ordered work; fan-out parallel lanes only when dependency graph allows.
2. Author each Markdown file + synchronize `_OVERVIEW` table entries + progress tracker.
3. Validate every task declares one completion chokepoint satisfying WP hygiene.

## Quality

Tasks stay narrow. Dependencies explicit. Acceptance testable (“build”, “scenario X”, instrumentation expectations).
