---
name: architect-impl-grounding
description: Grounds the grill's settled decisions in the codebase — annotates impl.md with file paths, signatures, reference files, test specs, and LOC; re-grounds the next epic after each landing.
usedBy: [architect]
version: 0.2.2
lastUpdated: 2026-09-12
---

## Purpose

The grill settles the decisions. This skill makes them concrete. It grounds the plan artifacts in the codebase and annotates `impl.md` with the details the coder implements from. The refresh procedure handles what lands: it verifies the shipped epic's discoveries, classifies them, and re-grounds the next epic against the codebase as it now stands.

## Procedure

- **Ground** — the grill is done. Annotate `impl.md`.
- **Refresh** — an epic has landed. Classify its discoveries, then re-ground the next epic.

1. **Ground mode.** Annotate `impl.md`:
   a. Read the plan artifacts:
      - `plan.md` — acceptance criteria.
      - `arch.md` — directory structure, layer separation, reference projects.
      - `impl.md` — epics grouped at one day of work.
   b. Ground the artifacts in the codebase:
      - Read `.context.md` files in affected directories.
      - Read `docs/FEATURE-MAP.md` if it exists.
      - Read the project's architecture skill, if one exists.
      - Run `ls` on affected directories.
      - Verify assumptions — check library docs for capability claims, inspect handler code for API contracts, validate environment references against config files.
   c. Annotate `impl.md` with the annotation set for each epic.
   d. Respect current layer boundaries and dependency direction (follows: `rules/code/general.md`). For each file in the epic, verify its imports do not violate dependency direction.
   e. Write the annotated `impl.md` back to disk. The coder works from this file.
2. **Refresh mode.** Handle the landed epic's discoveries, then re-ground:
   a. Read `impl.md` and the coder's handoff for the epic that landed.
   b. Verify each discovery against the changed files. Use `git diff --stat` to see what shipped, then read the files the discovery claims to affect. Discard a discovery that does not match the implementation — note the mismatch.
   c. Classify each verified discovery:
      - **adjust** — changes how the remaining work is built, not what the user wants. Fold it into the remaining epics inline. No user gate.
      - **escalate** — contradicts a settled decision, or reveals a decision the user should make. Flag it for the Maestro. Do not guess.
   d. Re-ground the next pending epic with step 1 against the current codebase. Verify its file paths, method signatures, and reference files. Re-annotate what drifted.
   e. Write the updated `impl.md` back to disk.

## Annotation Set

Each epic in `impl.md` carries:

- File paths to create or modify.
- Method signatures following `rules/code/` naming conventions.
- Reference files for style matching.
- Test specifications (Good, Bad, Ugly) for each method.
- Information flow tracing the request path through layers.
- Estimated LOC, within the 600 soft cap and the 900 hard cap.

## Handoff

Ground mode delivers the annotated `impl.md`. Refresh mode delivers the re-grounded `impl.md`:

```
## Summary
[One sentence: what was done]

## Grounding (ground mode)
- Epic N: [files identified, methods named, references listed]

## Discoveries (if any)
- [discovery] — action: adjust | escalate — [effect on remaining epics, or the question for the user]

## Re-grounding (refresh mode)
- [what drifted, what was re-annotated]
```

## Guardrails

- Never write code. You ground the plan. The coder implements.
- Never skip re-grounding the next epic in refresh mode.
- Never fold an escalate-class discovery as an adjust. The user's gate is not yours to close.
