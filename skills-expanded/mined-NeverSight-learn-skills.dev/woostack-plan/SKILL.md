---
name: woostack-plan
description: "Use to write the implementation plan for an approved woostack spec — a comprehensive, bite-sized TDD plan structured as PR-sized increments, saved frontmatter-free to .woostack/plans/<spec-basename>.md, opening with a `**Source:**` line that joins it 1:1 to the spec, and setting the spec's status: planning. This is the plan phase of the woostack build loop (woostack-build step 4); also usable standalone via /woostack-plan <spec-path>. One plan per spec. Writes the plan and hands back — never executes, commits, or merges."
---

# woostack-plan

Write a comprehensive implementation plan from one approved spec, structured as PR-sized
increments. This is woostack's own planning phase — [`woostack-build`](../woostack-build/SKILL.md)
step 4. It keeps the discipline that makes plans worth executing (file-structure first,
bite-sized TDD tasks, no placeholders, a self-review pass) and adds the woostack conventions:
markdown plans under `.woostack/plans/`, an opening `**Source:**` line that joins the plan 1:1 to
its spec, frontmatter-free, decomposed into independently shippable increments, and a
`status: planning` transition on the spec. It writes the plan and hands back; it owns no approval
gate and never executes, commits, or merges.

It internalizes the plan-writing discipline as a native phase — the same move
[`woostack-ideate`](../woostack-ideate/SKILL.md),
[`woostack-harden`](../woostack-harden/SKILL.md), and
[`woostack-execute`](../woostack-execute/SKILL.md) made on the phases around it. With this skill
the build loop has **no external skill dependencies**. It pairs with `woostack-execute` as
produce-plan / consume-plan: `/woostack-plan <spec>` writes the plan, `/woostack-execute <plan>`
runs it.

## Commands

- `/woostack-plan <spec-path>` — write the plan for the named markdown spec under
  `.woostack/specs/`. **The spec path is required.**
- `/woostack-plan` (no argument) — do **not** guess "the current spec." Ask which spec to plan
  (optionally list `.woostack/specs/` candidates) and stop until one is named.

When `woostack-build` reaches step 4 it invokes this skill with the approved spec path from
step 2/3.

## Read and check the spec

1. Read the spec file end to end — it is the source of truth for *what* to build; the plan is
   *how*.
2. **Scope check.** If the spec covers multiple independent subsystems, suggest splitting into
   separate specs first — one per subsystem, each producing working, testable software on its own
   — then write one plan per resulting spec. Don't write a monolithic plan over a
   multi-subsystem spec.
3. **One plan per spec.** If a plan already resolves to this spec (a `.woostack/plans/` file with
   a matching `**Source:**` line or the same basename), **amend that plan in place** — never write
   a second (`spec : plan : PRs = 1 : 1 : N`; a second plan breaks the board join). Say you are
   amending.

## File structure first

Before defining tasks, map which files are created or modified and each one's single
responsibility. This locks in decomposition.

- Design units with clear boundaries; one responsibility per file. Prefer small, focused files.
- Files that change together live together. Split by responsibility, not by technical layer.
- In an existing codebase, follow established patterns; don't unilaterally restructure. If a file
  you must touch has grown unwieldy, folding a split into the plan is reasonable.

## PR-sized increments

Structure the plan as a sequence of **independently shippable increments** — preferably ≤500 LOC
each (a soft target, not a gate) — so the plan is execute-ready: `woostack-execute` runs one
increment per cycle as its own Graphite-stacked PR. Flag any slice that can't reasonably stay
under the target and propose a further split; genuinely atomic changes may exceed it. This
decomposition is part of planning (it folds `woostack-build`'s old decompose step into the plan
engine).

## Optional: independent tracks (for overnight runs)

By default the increments form **one linear `gt` stack** — each stacks on the previous, the shape
`woostack-execute` runs. A plan **may** instead group increments under top-level **`## Track:`
headings**; each track is an independent linear stack branched off the common base (the spec+plan
PR). This is **author-driven and optional**: write tracks only when increments are genuinely
independent and you want an unattended overnight run to **isolate failures** across them — a
blocker ends only its own track, not the whole run. Tracks run **sequentially** (one session, no
concurrency); the benefit is fault isolation, not speed. Do **not** auto-partition — default to one
implicit track (no headings = today's behavior).

Only [`woostack-execute-overnight`](../woostack-execute-overnight/SKILL.md) consumes tracks (it
runs each track off the base and, on a blocker, ends only that track and advances to the next).
[`woostack-execute`](../woostack-execute/SKILL.md) ignores the headings and runs every increment
as one linear stack.

## Bite-sized tasks (TDD)

Within each increment, decompose into bite-sized tasks; each **step** is one action
(~2-5 minutes): write the failing test → run it, confirm it fails → minimal implementation → run
it, confirm it passes → commit. Use checkbox (`- [ ]`) syntax for every step so
`woostack-execute` ticks them in place as the live progress record. DRY, YAGNI, TDD, frequent
commits throughout.

In a target without a test runner (e.g. a docs/skills repo), "the failing test" becomes a
concrete **verification command** — a `grep`, a `bash -n`, a link check, or an existing script's
test — with exact expected output. Never a vague "verify it works."

The output shape (header, `**Source:**` line, task/step structure) is captured in
[references/plan-template.md](references/plan-template.md) — populate it; don't reinvent it.

## No placeholders

Every step carries the actual content an engineer needs. These are plan failures — never write
them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add error handling" / "add validation" / "handle edge cases" — write the actual test instead; error and edge cases belong in the spec's §7 Acceptance criteria, enumerated there as happy/error/edge cases
- "Write tests for the above" without the actual test
- "Similar to Task N" — repeat the code; tasks may be read out of order
- A step that says *what* without showing *how* (code/command blocks required)
- References to types/functions/methods defined in no task

Exact file paths always. Complete code in every code step. Exact commands with expected output.

## Board join: Source line, frontmatter-free, filename

- **Filename:** save to `.woostack/plans/<spec-basename>.md` — the **same** `YYYY-MM-DD-<slug>`
  basename as the spec (reuse the spec's date; **not** today's). The shared basename is the
  slug-match fallback join.
- **Opening line:** the plan's first line is `**Source:** .woostack/specs/<file>.md` — the
  primary spec→plan join the `/woostack-status` board reads.
- **Frontmatter-free:** plans carry no YAML frontmatter and no `REQUIRED SUB-SKILL` banner. The
  header is the `**Source:**` line plus Goal / Architecture / Tech Stack.

The phase enum and join contracts are defined once in
[`../woostack-status/references/conventions.md`](../woostack-status/references/conventions.md) —
link, never restate.

## Self-review

After writing the plan, check it against the spec with fresh eyes — a checklist you run yourself,
not a subagent dispatch:

1. **Spec coverage** — every section/requirement maps to a task. List and fill any gap.
   **AC coverage:** when the spec's §7 Acceptance criteria lists ACs, every AC — and each
   filled (non-N/A) happy/error/edge case — maps to a task/test; when §7 is whole-section
   `N/A`, confirm the spec body has no behavioral requirement (else flag the `N/A` as suspect).
2. **Placeholder scan** — search for the red flags above; fix them.
3. **Type consistency** — types, signatures, and property names match across tasks (a method
   called one name in Task 3 and another in Task 7 is a bug).

Fix issues inline; no re-review needed.

## Status: planning

When the plan file exists, set the spec's `status: planning` (the conventions.md value for "plan
exists, 0 boxes done"). Doing it here means a standalone `/woostack-plan` also advances the board.
Do not tick any plan checkbox yet — execution owns checkbox progress.

## Terminal state: plan written, handed back

Stop when the plan is written, self-reviewed, and the spec is `planning`. Then hand back and name
the next step:

- Inside `woostack-build`: return to **step 6** (harden the plan).
- Standalone: tell the user the plan is ready and offer `/woostack-execute <plan-path>`. Stop.

Chain nothing yourself.

## Gate boundary

This skill owns **no approval gate**. The spec-approval gate (`woostack-build` step 3) is
upstream; the execution-handoff gate (step 8) is downstream. It does not present-for-approval,
execute, commit, or merge. It writes the plan and hands back — preserving `woostack-build`'s
"inherit gates, add none."

## Hard constraints

- **Spec path required.** Never guess "the current spec"; ask when no argument is given.
- **One plan per spec.** A plan already resolves to the spec → amend it; never write a second
  (breaks the 1:1 board join).
- **Markdown plan under `.woostack/plans/`, basename = spec basename.** Frontmatter-free, opening
  `**Source:**` line.
- **PR-sized increments.** Decompose into independently shippable slices (≤500 LOC soft target);
  flag and split oversized ones.
- **Bite-sized TDD tasks, no placeholders.** One action per step; complete code, exact commands,
  expected output.
- **Set `status: planning`; tick no checkbox.** Execution owns checkbox progress.
- **Own no gate; never execute, commit, or merge.** Write the plan and hand back.
