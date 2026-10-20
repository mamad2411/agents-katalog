---
name: sequence-plans
description: Use when a project has more than one plan and you need to know which is runnable next — reads a committed manifest, runs a Kahn topological ready-set, and dispatches one plan at a time. Do NOT use for intra-plan step order (that is `write-plan` and `sdd`) or for greenfield spec work (that is `iterate`).
---

# Sequencing Plans

## Overview

`write-plan` produces one plan. `sdd` (SDD) executes
one plan and ledgers its own tasks. Neither models the space above one plan.
This skill does — with one committed file per project, one CLI, and one loop.

Use it when brainstorming split a spec into more than one plan and each plan
depends on the previous one (or on a diamond of previous ones) landing. The
first version of this problem is deterministic and cheap. Nothing here holds
state across sessions except the manifest, and the manifest is a git-tracked
markdown file — a fresh session on another machine reads the same answer.

**Announce at start:** "I'm using the sequence-plans skill to run this plan
set."

## When NOT to use this

- **One plan.** `write-plan` covers it. This skill exists for the
  cross-plan case.
- **Intra-plan step order.** SDD's per-task ledger already handles that inside
  one plan.
- **Greenfield spec work over a large surface.** `iterate` is
  the right cluster for that; its state model is per-iteration, and this skill
  will not help.
- **Parallel plan dispatch.** Not covered here (`parallel-execution-option`
  owns the write-ban lift). Run one plan at a time.

## The manifest

One file per plan set, committed alongside the plans it names:
`docs/moe/plans/<project>-MANIFEST.md`. It is a markdown wrapper around one
fenced YAML block. Fields:

- `plan_set_id` — optional stable id unique across the manifests in this
  repository. It must match `[A-Za-z0-9][A-Za-z0-9._-]*` so qualified
  `<plan-set-id>/<plan-id>` references round-trip without ambiguity. When
  omitted for a legacy manifest, the CLI derives it from the filename by
  removing `-MANIFEST.md` and validates the derived id with the same grammar.
- `depends_on_plan_sets` — optional list of plan-set ids that must be wholly
  `done` before any plan in this set is runnable. Defaults to `[]`. A blocked
  prerequisite blocks every dependent set transitively.
- `id` — short label unique in this manifest. Used by `plan-set done` and by
  every `depends_on` reference. Recommend the plan slug.
- `plan` — path to the plan markdown, from the repository root.
- `depends_on` — list of ids that must be `done` before this plan is ready. `[]`
  when nothing precedes it.
- `status` — one of `pending`, `running`, `done`, `blocked`. New entries start
  as `pending`. `blocked` is terminal and propagates: every dependent of a
  `blocked` node is treated as blocked too, so a plan whose foundation stopped
  by design is never handed back as "ready".
- `commits` — set by `plan-set done`, not by hand. `<base7>..<head7>` for the
  range of commits the finished plan produced.

A manifest must contain at least one plan. Empty plan sets are rejected rather
than treated as vacuously complete prerequisites.

Example:

````markdown
# <Project> Plan Set

Prose describing the project. `plan-set` reads only the yaml block below.

```yaml
plan_set_id: example-project
depends_on_plan_sets: []
plans:
  - id: schema
    plan: docs/moe/plans/2026-01-01-schema.md
    depends_on: []
    status: pending
  - id: reader
    plan: docs/moe/plans/2026-01-02-reader.md
    depends_on: [schema]
    status: pending
  - id: writer
    plan: docs/moe/plans/2026-01-03-writer.md
    depends_on: [schema]
    status: pending
  - id: server
    plan: docs/moe/plans/2026-01-04-server.md
    depends_on: [reader, writer]
    status: pending
```
````

## The CLI

Resolve {resource:skills/sequence-plans/scripts/plan-set.mjs} relative to this
loaded document. It is a plugin-owned Node launcher, not a global executable:
invoke the resolved resource with `node`, never as a bare `plan-set` command.
It locates the plugin's scheduler independently of the project working
directory and ships in the `moe` plugin alongside this skill.

Verbs:

- `plan-set next [--manifest <path>]` — Print every id whose plan and plan-set
  dependencies are all `done` and whose own status is `pending`. With multiple
  discovered manifests, output is qualified as `<plan-set-id>/<plan-id>`.
  Scoped output remains the legacy bare id. Blocked nodes, sets, and their
  transitive dependents never appear.
- `plan-set done <id> <base>..<head> [--manifest <path>]` — Mark `<id>` as
  `done` and record its commit range. In aggregate mode with multiple manifests,
  `<id>` must be qualified as `<plan-set-id>/<plan-id>`. Fails if the id is
  unknown, if any plan or plan-set dependency is not `done`, or if the range is
  not two 7+-char hex SHAs joined by `..`.
- `plan-set check [--manifest <path>]` — Validate: unique ids, all plan files
  exist, all plan and plan-set dependencies resolve, neither DAG contains a
  cycle (Kahn), plan-set ids are unique, and no plan path is listed twice even
  across manifests. Exits non-zero on any failure. A cycle names its nodes on
  stderr.

If `--manifest` is omitted, `plan-set` discovers every matching
`docs/moe/plans/*-MANIFEST.md` in sorted filename order and operates on the
aggregate. If `--manifest` is present, it loads only that manifest and its
transitive prerequisite closure. Unrelated malformed siblings therefore do not
poison a scoped command, while prerequisite completion is still enforced.

## The SessionStart hook

`plan-set-notice` is a bash SessionStart hook that fires on `startup|clear|compact`.
It looks in the session's cwd for `docs/moe/plans/*-MANIFEST.md`, and if one or
more exist and have runnable plans, it prints the bare or aggregate-qualified
ids and a `plan-set next` command as SessionStart `additionalContext`. Fully
deterministic — no model in the loop. Every failure path exits 0; a broken
notice must never break a session.

The hook exists so the cold-start case ("new session, four plans exist, which
are done?") is caught even when the transcript has no history and no skill
description is triggering. `plan-set-notice` announces; this skill carries the
loop.

## The loop

1. **Confirm the manifest set.** Resolve
   {resource:skills/sequence-plans/scripts/plan-set.mjs} relative to this
   loaded document, then invoke it as
   `node "<resolved-plan-set.mjs>" check`
   before anything else. A cycle, a missing plan file, or a duplicate id is a
   dead end before the first plan runs, and `check` says which one at once. Use
   `--manifest docs/moe/plans/<project>-MANIFEST.md` only when intentionally
   scoping to that set and its prerequisites.

2. **Pick the next plan.** Invoke the resolved launcher as
   `node "<resolved-plan-set.mjs>" next`. `next`
   returns a set; the loop takes the first line of it.

   ```bash
   NEXT=$(node "<resolved-plan-set.mjs>" next | head -n 1)
   ```

   If the output is empty, either everything is `done` (the project is
   finished) or everything ready is `blocked` (a foundation stopped by design
   and its dependents cannot run). Do not dispatch in either case.

3. **Dispatch.** Read the plan path for `$NEXT` out of the manifest and hand
   the plan off to `sdd` (the recommended executor) or
   `execute-plan` (the no-subagents fallback). Both skills already own
   their own per-task ledger, so this skill does not track task-level state.

4. **Record completion.** When the plan finishes cleanly, capture the branch's
   base and head SHAs and mark it done:

   ```bash
   node "<resolved-plan-set.mjs>" done "$NEXT" \
     "$(git merge-base main HEAD | cut -c1-7)..$(git rev-parse --short HEAD)"
   ```

   Add `--manifest` only for a scoped, bare-id workflow.

   `done` refuses to run if `$NEXT`'s dependencies are not all `done` — a
   safeguard against marking things done out of order.

5. **Loop.** Return to step 2.

## When to mark a plan `blocked`

`blocked` is terminal and propagates. Use it when a plan has stopped by
design — the spec changed, the approach is being reconsidered, an external
dependency is not going to land. Do NOT use it as a synonym for "in progress"
or "waiting for review": those are `running`.

The reason `blocked` matters is that its dependents are still `pending` in the
file. A naive "artifact exists = done" reader hands the agent a plan whose
foundation was never built. `plan-set next` never returns a dependent of a
`blocked` node.

Edit the manifest by hand to mark a plan `blocked`; there is no CLI verb for
it, on purpose — it is a decision, not a state transition.

## Design notes

- **`next` returns a ready set, not a single id.** The loop takes the first of
  it. The set is the seam a later cross-plan scheduler would read, once the parallel-write
  ban is lifted. Nothing here requires that ban lifted.
- **The CLI lives under `hooks/`, not this skill's directory.** SessionStart
  invokes the adjacent notice before any skill body is loaded. Keeping both
  runtime pieces together also gives every generated harness the same stable
  plugin-relative path.
- **`plan-set` is Node, not bash.** Kahn's algorithm plus per-line YAML
  parsing over a mutable file is short in JS and painful in bash. Node ships
  with every harness this fork targets.
- **The manifest is a markdown wrapper around one YAML block, not a bare YAML
  file.** The wrapper is where humans write the prose that says what the
  project is for. `plan-set` reads the yaml block and ignores everything
  outside it.
