---
name: openspec-to-beads
description: >
  Turns an approved OpenSpec change (openspec/changes/<slug>/) into a bd (beads) task graph:
  an epic labelled change:<slug>, one child task per tasks.md phase (label phase:<K>, the tracker ID
  as external ref), dependencies, acceptance, owner questions.
  Use when a change is approved for implementation: "convert the spec to beads", "create tasks from
  the change", "put voice-input into the queue", "implement this change".
allowed-tools: "Read,Bash(bd:*),Bash(git status:*),Bash(git log:*)"
version: "3.0.0"
license: "MIT"
---

# openspec-to-beads — approved change → bd queue

> Canonical template (templates/base). Needs no configuration.
> Inspired by the `openspec-to-beads` skill in [lucastamoios/celeiro](https://github.com/lucastamoios/celeiro);
> this version is written from scratch for the factory layout.

> **Seam:** execution queue = beads (`bd`). To use another tool, rewrite "What to create", "Procedure" and `allowed-tools`.

OpenSpec says **what** is agreed; bd holds the **state of execution**. This skill moves an approved
change into the queue once, so that `bd ready` shows exactly the next phase to work on and nothing
from the proposal is lost on the way.

## When to run

- The change is approved: proposal, design (if any) and `tasks.md` are reviewed, and the
  **Interaction surfaces** section is confirmed (`openspec/README.md` §0). No confirmed surfaces —
  stop and say so; the change is not ready.
- Not for drafting or editing proposals, and not for a change that already has an epic in bd
  (search first: `bd list --all -t epic -l "change:<slug>" -n 0 --json`; if it exists, update it).

## Inputs

- `openspec/changes/<slug>/` — `proposal.md` (its header holds the tracker ID, if any), `design.md` (optional), `tasks.md`.
- There is no OpenSpec CLI: a change is a folder of Markdown files (the `openspec` skill).

### The store (check first)

The queue is the project's local bd store in the main checkout's `.beads/`, shared by every worktree
(`.beads/README.md`); nothing about it is committed. Check that it answers before creating anything:

```bash
bd where && bd list | head            # the project's store, with its tasks
```

No store — stop and say so (`bd init` is a setup step of the main checkout, not of this skill).

## What to create

| bd object | From | Notes |
|---|---|---|
| **Epic** (`--type=epic`), one per change | the change | title `[<slug>] <outcome>`; label `change:<slug>`; `--acceptance` = the proposal's acceptance scenarios as observable facts; with a tracker and no phases, `--external-ref <tracker ID>` |
| **Phase task** (`--type=task --parent <epic>`) | each phase in `tasks.md` | title `Phase <K>: <what>`; label `phase:<K>`; `--external-ref <tracker ID>` of the phase's own sub-card when there is a tracker; description ends with the marker line `OPENSPEC: openspec/changes/<slug> PHASE: <K>` |
| **Dependency** (`bd dep add <later> <earlier>`) | phase order and real data/API needs | sequential phases block the next one; independent phases stay parallel |
| **Owner question** (`--type=decision`, or `task` with label `needs-owner`) | "Open questions" in the proposal | description says "needs a human decision — not for the agent"; blocks the phases it affects |
| **Gap task** (`--type=task`, `discovered-from` the epic) | things the change needs but `tasks.md` misses: migration, docs/user guide, config, rollout | only real gaps; mention each in the report |

Rules:

- **One task card = one branch = one PR** (`AGENTS.md` §Operating contract): a phase task is a branch; a change
  without phases is the epic itself. The branch is `<type>/<ID>-<slug>` with a tracker (the phase's own
  sub-card ID), `<type>/<slug>-p<K>` without one (`<type>/<slug>` for a change without phases).
  `merge-feature.sh` finds the task to close by that key: the tracker ID against `external_ref`, or the
  slug against the epic label and `-p<K>` against the child's `phase:<K>` label — so the labels and the
  external ref below are what makes the close automatic.
- **Labels are case-sensitive**, and `bd list` hides closed tasks without `--all` and stops at 50 without `-n 0`.
- **Phases stay phases.** Do not split a phase into micro-tasks or merge phases; if a phase is clearly
  too big (`openspec/README.md`: not buildable and checkable in one sitting), say so in the report instead of re-planning.
- **Priorities.** Default P2. The critical path of the epic gets P1. If the proposal has a cut order
  ("drop first if short on time"), later cuts get lower priority. Do not mark everything P0.
- **Language.** Titles and descriptions in the project language (`CODING_STANDARDS.md` §Project
  language); ids, labels and markers in English.
- **Keep the why.** Each phase task's description carries one or two lines of rationale from the
  proposal or design, not just the checklist line.

## Procedure

1. Read the change; list phases, acceptance criteria, open questions, cut order.
2. Check for an existing epic; run the worktree check.
3. Show the planned graph to the human as a table (epic → phases → deps → questions → gaps) and
   wait for "yes". Use `bd create --dry-run` if unsure about a command.
4. Create: epic, then phase tasks with `--parent`, then `bd dep add`, then questions and gaps.
   Use `--silent` to capture ids for the next commands.
5. Verify: `bd show <epic>` lists all phases; `bd ready` shows the first phase (or the blocking question).
6. Report: ids created, the first ready task, gaps found, phases that look too big.

```bash
epic=$(bd create "[csv-export] CSV export of reports" --type=epic -p 1 --silent -l change:csv-export \
  --acceptance "A user downloads the monthly report as CSV from the Reports page; totals match the screen")
p1=$(bd create "Phase 1: CSV serializer for report rows" --parent "$epic" -p 1 --silent \
  -l phase:1 --external-ref DMP-124 \
  -d "Rows → CSV with the same rounding as the UI (design.md: rounding).
OPENSPEC: openspec/changes/csv-export PHASE: 1")
p2=$(bd create "Phase 2: download endpoint" --parent "$epic" -p 1 --silent \
  -l phase:2 --external-ref DMP-125 \
  -d "GET /reports/{id}.csv streams the serializer output.
OPENSPEC: openspec/changes/csv-export PHASE: 2")
bd dep add "$p2" "$p1"
bd create "Owner: include archived rows in the export?" --type=decision --silent \
  -d "Open question from proposal.md — needs a human decision, not for the agent." | xargs -I{} bd dep add "$p2" {}
```

Without a tracker, leave `--external-ref` out; the branches are `feat/csv-export-p1` and `feat/csv-export-p2`.

## Don'ts

- Don't create tasks before the human has seen the graph.
- Don't copy `tasks.md` line by line into dozens of tasks.
- Don't drop tests: if a phase has no test step, flag it in the report.
- Don't commit or push: the queue is a local store, there is nothing to commit (`.beads/README.md`).
