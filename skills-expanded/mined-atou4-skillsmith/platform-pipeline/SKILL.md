---
name: platform-pipeline
description: >
  Staged workflow for building a platform from scratch: PRD, design
  refinement on real artboards, a hard approval gate, visual and UX
  research only, then an autonomous build verified against the running
  app. Runs once for the whole platform (Platform init), then repeats per
  feature (Feature cycle). Use for "start a PRD for X", "kick off
  building X from scratch", "new platform", "next feature for this
  platform", or /platform-pipeline. For integrating an external service
  across repos that already exist, use feature-forge instead.
---

# Platform pipeline

Two entry points, same five stages. **Platform init** runs the full
sequence once, at whole-platform scope, to lay down the PRD and a shared
design system. **Feature cycle** re-runs it per feature afterward, at
narrower scope, reusing what init produced.

## Which entry point, and which pipeline

Check the project before choosing:

- No platform PRD or no approved design system yet: **Platform init**.
- Both exist: **Feature cycle**. Rerun Platform init only when the
  platform's foundational scope changes, not for a single feature.
- The hard part is a shared contract between several existing repos
  and an external service (payments, auth, messaging): stop and use
  `feature-forge`. This pipeline assumes one product being built up from
  its own PRD.

Say which entry point you chose and why before Stage 1.

## Project state

Keep one file, `docs/platform-pipeline.md` in the project (create it in
Platform init). It records:

- where the master PRD lives,
- where the approved design system lives (canvas link, file or folder),
- the feature-PRD convention (section of the master PRD, or one doc per
  feature),
- one line per completed cycle: feature, approved artboard version,
  date, verification evidence location.

Read it at the start of every run. It is how a Feature cycle knows what
init produced, and how a convention chosen once is not asked again.

## Dependencies and fallbacks

Each stage names a skill. None ships with this pack, and the pipeline
works without them: the fallback is what the stage must still produce.
Check which are installed before Stage 1 and tell the user which
fallbacks are in play.

| Stage | Skill | Where to get it | Fallback when it is missing |
|---|---|---|---|
| 1 | `to-spec` | mattpocock/skills | A PRD written by hand: goals, users, core modules, non-goals, open questions |
| 2 | a design-canvas skill or tool (for example Claude Design's `design`) | your design tool of choice | Wireframes or screenshots the user can look at and react to. A text description of screens is not a fallback |
| 4 | web search and a browser tool | built into most agents | Ask the user for 3-5 reference products or screenshots |
| 5 | `create-verification-skill` | cursor/plugins | A script that launches the app, drives the feature the way a user would and saves evidence |
| 5 | `blast-radius` | cursor/plugins | Trace every caller of what changed and run real code to prove it still works |
| 5 | `tdd` | mattpocock/skills | Write the failing test first by hand |
| 5 | `code-review`, `simplify` | mattpocock/skills; `simplify` is built into Claude Code | Any careful review pass over the diff |

Read each installed skill in full when its stage comes up. Do not
reconstruct its steps from memory.

## Stage 1: PRD

- **Platform init:** capture the whole-platform vision with `to-spec`:
  goals, users, core modules, explicit non-goals. This is the master PRD.
  Create `docs/platform-pipeline.md` and record where it lives.
- **Feature cycle:** a scoped mini-PRD for just this feature. The first
  time, ask whether it is a section of the master PRD or its own doc,
  record the answer in `docs/platform-pipeline.md`, and never ask again.

## Stage 2: Design refinement

- Draft actual artboards, not a text description of screens.
- **Platform init:** the design-system foundations: navigation shell,
  core screens, component and style primitives, so every later feature
  inherits one look.
- **Feature cycle:** only the new screens and flows for this feature,
  reusing the approved design system rather than introducing new
  primitives. If a new primitive is unavoidable, say so and why.
- Iterate with the user. Do not move to Stage 3 until they have looked
  at and reacted to the artboards themselves.

## Stage 3: Approval gate (hard stop, every time)

- Stop and wait for explicit approval of the specific artboards and
  version, in Platform init and in every Feature cycle.
- An ambiguous or off-topic reply is not approval. "Looks fine" said
  about something else is not sign-off. If the user asks for changes,
  go back to Stage 2.
- Once approved, Stages 4 and 5 run without asking again: the gate was
  the one planned stop for this cycle. Two exceptions still stop and
  ask: anything destructive or hard to reverse (deleting data, force
  pushes, migrations on shared databases), and anything outward-facing
  (deploying, publishing, sending messages, spending money). Decisions
  that are only judgment calls are made, written down, and reported at
  the end, not asked.

## Stage 4: Visual and UX research (inspiration only)

- Scope is strictly visual and UX reference for the screens and flows
  just approved: layout patterns, interaction idioms, visual style. Not
  technical or architectural research; the build stage decides if it
  needs any.
- Look at design galleries, pattern libraries and direct competitors
  for the specific approved elements.
- Write a short note: a handful of concrete references, and exactly
  what to borrow from each, tied to named approved elements. Not a mood
  board.
- Feed a finding back into the artboards only if it is a concrete,
  worthwhile tweak, and show the user the change. Otherwise it is input
  to Stage 5 for details the design did not pin down (spacing, motion,
  empty, loading and error states).

## Stage 5: Build

- First time in this repo: run `create-verification-skill` once to
  create a project-local way to drive the real app end to end.
- Every feature after that: add the feature to that verification
  skill's feature map, then drive it for evidence before calling the
  feature done. "Looks right in the canvas" is not done.
- Test-first with `tdd` if the user wants it for this feature.
  Otherwise: scaffold, a checkpoint that the skeleton runs, implement,
  verify.
- If the user works with a build-discipline skill (for example
  `poteto-mode`), use it only when they ask for it; some such skills are
  explicit-invocation only.
- Before merging any change you are not fully sure of: run
  `blast-radius` on the diff.
- Close with a `code-review` and `simplify` pass.
- Add the cycle's line to `docs/platform-pipeline.md` with where the
  evidence is.

## Verification

A cycle is done when all of these hold. Report each with its evidence:

1. The approved artboard version is recorded in `docs/platform-pipeline.md`.
2. The feature was driven in the real running app through the
   verification skill, and the evidence (screenshots, transcripts,
   state before and after) exists at the recorded location.
3. Review findings were fixed or listed as accepted with a reason.
4. Any judgment calls made after the gate are listed in the final
   report.

## Loop

After Stage 5, the next feature re-enters at Stage 1 as a Feature cycle,
not Platform init.
