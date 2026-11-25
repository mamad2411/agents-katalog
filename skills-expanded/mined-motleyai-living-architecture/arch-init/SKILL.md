---
name: arch-init
description: Build a repo's first living-architecture model — write the language sections of architecture/index.yaml, scaffold the as-is model from the measured imports (la-arch-scaffold), choose the wedge with the user, draft the principles from the repo's own instructions, map the specs, and get la-arch-check green. Syntax and maintenance are in the la:living-architecture reference.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory> --require-config` once per session before using any `la-*` or `dr-*` command. If it reports the missing-config finding (the one naming `/la:init`), run the fast path of the `la:init` skill, then re-run this preflight; stop and show the user its output on anything it still reports, or on any other failure.

# Build the first architecture model

The syntax of the model, `index.yaml`, views and arc42 files, and every check `la-arch-check` runs, are in
the `la:living-architecture` skill; read it first. Everything this skill writes is normative, like tests:
show each model, arc42 and `index.yaml` edit and get the user's OK before landing it.

## 1. Preconditions

- `architecture/index.yaml` does not exist (otherwise this is maintenance: use `la:living-architecture`).
- `openspec: true` in the config means `openspec/` is healthy; if not, run `la:openspec-init` first.
- A type check with a baseline: run `dr-typecheck`. If it checks a language that has no baseline, offer
  `dr-typecheck --write-baseline` (the one legitimate recording; afterwards the baseline only shrinks). If it
  prints "nothing to check", tell the user that `la:arch-cleanup` cannot verify moves without one, and offer
  to set `commands.typecheck` first.

## 2. Language sections

Write `architecture/index.yaml` with one section per language the repo has: `root_package` (or
`root_packages` when the language's code sits in several sibling directories under one `source_root`), and
`source_root` / `tsconfig` where needed. Confirm them with the user. From now until step 8 `la-doctor`
reports `architecture: false` against the new index; that is expected.

## 3. Scaffold

Run `la-arch-scaffold`. It writes, atomically, the as-is model in `architecture/model.c4` (one node per
top-level unit, one arrow per measured runtime import edge), one view per language in `architecture/views.c4`,
`system.arc42.md` with the generated diagrams and TODO sections, and `legacy_arrows` / `diagrams` in
`index.yaml`. It refuses (exit 2, writing nothing) when any LikeC4 file (`.c4`, `.likec4`) or arc42 file
already exists under `architecture/`. Show the user the model and the arrow list.

## 4. Choose the wedge

Offer only genuine options: less work is never a pro and more work never a con unless the amount is ridiculously large,
and an option that breaks something working today is not offered without a very good reason.

Interview the user, one question at a time, each with PROS/CONS and a RECOMMENDATION:
- which nodes are **precise** (usually the subsystem about to be worked on plus its neighbours) and which
  are swept into **virtual buckets**;
- the node titles;
- which measured arrows are wrong and slated to die: tag them `#legacy` and set `legacy_arrows.baseline` to
  their exact count;
- where the import law must hold child-level: nest elements under that node.

The model stays true at every step: every arrow is a measured edge, and grandfathered ones are `#legacy`,
never omitted.

## 5. Principles

Draft `system.arc42.md` from the repo's own `CLAUDE.md` / `AGENTS.md` and the structure you measured:
Purpose and context, numbered Principles (each with a status tag: `[enforced: …]`, `[review]` or
`[target: …]`), and Rationale. Present the principles ONE BY ONE and land each only on the user's OK. Write an
element arc42 file (`architecture/<element id>.arc42.md`) only for the 1–3 elements that earn prose now.

If the repo has an ADR or decisions file, fold its present-tense rules into the owning elements' principles,
then, with the user's OK, delete it (history stays in git and the OpenSpec archive).

## 6. Spec mapping

The scaffold maps no specs. Map every `openspec/specs/<id>` exactly once: in one element's metadata `specs` (at any depth), or
in `cross_cutting_specs` with its `touches:` list. Decide each with the user.

## 7. Green

Run `la-arch-diagrams`, LikeC4 model validation (`npx likec4 validate`, or the lightest command that parses
the model) and `la-arch-check`, and fix until all are green.

## 8. Flip the gate

Set `architecture: true` in `living-architecture.yaml` and run `la-doctor --plugin <this skill's base directory> --require-config`
until it passes. Do not wire CI. The user commits.
