---
name: vertical-slice-splitter
description: Decompose a destination doc or spec into vertical-slice issue cards with a dependency DAG
type: planning
version: v0.1
---

# Vertical Slice Splitter

Invoke as `$vertical-slice-splitter`.

Decompose a destination doc or spec into independently grabbable vertical-slice issue cards.

## Process

1. Read input document from `$ARGUMENTS`.
2. Explore codebase: file structure, layers, modules, test boundaries.
3. Identify layers the work crosses (DB, service, API, UI, infra, etc.).
4. Decompose into vertical slices — each crosses all relevant layers for its scope.
5. Reject horizontal-only slices. Slice 000 must be a tracer bullet: visible and testable end-to-end.
6. For each slice: title, description (2-5 sentences), testable acceptance criteria, dependency edges (`blocks`/`blocked-by`), label (`afk` | `human-review` | `pair`).
7. Build DAG, validate acyclic, identify parallel groups.
8. If `issues/` has existing content, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/issues/`.
9. Write `issues/DAG.md` (mermaid graph + summary table + parallel groups) and `issues/000-[slug].md` through `issues/NNN-[slug].md`.

## Issue File Format

```markdown
# [Title]

**Label:** afk | human-review | pair
**Blocks:** 001, 003
**Blocked by:** none

## Description
[2-5 sentences]

## Acceptance Criteria
- [ ] ...

## Notes
[Optional implementation hints]
```

## Constraints

- Every slice independently grabbable (one agent or session)
- No slice larger than one focused session
- First slice (000) is always the tracer bullet
- DAG must be acyclic
- `afk` slices must have unambiguous acceptance criteria (no taste judgment)

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/vertical-slice-splitter-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
