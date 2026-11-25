---
name: to-plan
description: Turn a PRD, decision document, or conversation into the smallest independently verifiable vertical tasks under plans/tasks/, append them to the project's single local master plan, and wait for user approval before writing. Use to plan features, tracer-bullet work, or agreed decisions for implement-next-task.
---

# To Plan

Turn the source into self-contained local task files and register them in the project's single
master plan. Each task is the smallest complete behavior that can be implemented, verified, and
merged independently on its own branch.

## Process

### 1. Confirm the source

Use a PRD, decision document, or the current conversation. If the source is unclear, ask the user
to identify it. The source type never determines the number of tasks.

### 2. Locate or bootstrap the master plan

Find the master plan through the most specific `AGENTS.md` `Active plan` entry, falling back to
`CLAUDE.md`.

- If it exists, append tasks to it. Do not create another plan.
- Change an architectural-decision bullet only when the source contains a new durable decision.
- If no plan exists, explore the codebase first, create the master plan from the template below,
  and register it in `AGENTS.md` and in `CLAUDE.md` when that file exists.
- On an existing codebase, describe the current architecture and begin the task list with work
  planned now. Do not backfill shipped work.

### 3. Explore the codebase

Inspect the current architecture, domain vocabulary, patterns, integration layers, tests, and
relevant decision records.

Before drafting any task that reads or writes existing data, open the schema or model spec of
every entity the task names and note:

- fields that identify a person, owner, parent, or resource, and whether the same identity is
  recorded on more than one record (a chat and its trip each carrying an owner);
- lifecycle flags the selection may need to respect (deleted, deletion requested, archived, demo,
  test, staff);
- rough volumes, and any access cost the repository already documents in comments or docs.

Write what you learn as semantics in `What to build` or `Decided` ("the exported user id is the
chat's owner; a chat owner can differ from the trip owner"; "members who requested deletion are
excluded") and as landscape in `Context`. Never as steps, field names, or file paths: the task
tells the implementer what is true and what must hold, not how to get there. The implementer builds
forward from the task and will not discover a second owner field or a lifecycle flag on its own;
the reviewer will.

Before naming anything in a task, check it against the base branch:

- **Existence.** Every file, script, command, or skill the task names exists on the base branch
  (`git ls-tree -r <base>`, not the working tree). Gitignored or local-only tools are named as
  operator-supplied, never as repository files the implementer can open.
- **Prior art.** When the task points the implementer at existing code or a prototype to borrow
  from, state which parts you verified correct and mark the rest "unverified: do not reuse its
  logic". A `Context` line such as "the prototype already does X" is read as fact and copied,
  defects included.
- **External data.** When the task parses another system's data (API payloads, traces, exports),
  a real anonymised sample must be committed before implementation, or the task opens with a
  human checkpoint to provide one. Synthetic fixtures only encode the planner's assumptions.

### 4. Draft the smallest vertical tasks

Break the source into tracer-bullet tasks.

<vertical-slice-rules>

- Create one task for each smallest complete, independently verifiable behavior.
- Cross every layer relevant to that behavior, including its tests or verification. Do not invent
  schema, API, or UI work when the behavior does not require it.
- Keep tests and verification in the task whose behavior they prove. Never defer them to a later
  horizontal task.
- Make every completed task demoable or verifiable on its own.
- Apply the split test repeatedly: list the task's observable behaviors. If one can be delivered
  and verified independently, split it into another vertical task. Continue until removing any
  behavior would make the remaining task incomplete.
- Keep each task small enough to understand, implement, verify, and review in one fresh
  implementation context. If it does not fit comfortably, apply the split test again. Do not split
  by technical layer to satisfy this limit.
- Give every task its own `feature/<kebab-slug>` branch and one PR. One PR is a ceiling, not a
  sizing target.
- Do not include volatile file names or line numbers. Include durable decisions such as routes,
  schema shapes, public contracts, and domain model names.

</vertical-slice-rules>

#### Size gate

Review findings scale with task size, and oversized tasks are where implementers guess and
reviewers disagree. Before proposing a task, check it against every line below; one failure means
split again. This is a hard stop: never present or write a task that fails a line. Measure the
word count with a command over the drafted sections; do not estimate it.

<size-gate>

- The binding sections (`What to build`, `Implementation work`, `Acceptance criteria`) fit in
  roughly 600 words. Context and rationale live in the non-binding `Context` section and do not
  count, but a task whose context is longer than its contract is usually two tasks.
- One primary output: one new command, flow, screen, model, or report. A task that fetches from
  several sources *and* analyses them *and* adds an optional mode is at least three tasks.
- At most two external integration points (APIs, services, third-party packages) touched.
- `Implementation work` has at most eight items, and every item names a behavior the acceptance
  criteria can observe.
- Optional flags, alternative modes, and "while we're here" capabilities are not part of the first
  task. Put them in a follow-up task or in `Non-goals`.

</size-gate>

#### What belongs in a task, and what does not

A task is a contract about observable behavior, not an implementation plan. The implementer does its
own reconnaissance from the current code; details written into the task go stale, over-constrain
the implementation, and turn into review findings when the reviewer takes them literally.

<task-detail-rules>

Write these in, precisely:

- observable behavior: inputs, outputs, and the effect on the user or system;
- public contracts: names of flows, routes, CLI commands and their flags, schema fields, events,
  environment variables the operator must set;
- decision semantics: whenever the output is a classification, verdict, status, or score, give a
  decision table (`conditions → result`) covering every result, including the "cannot decide" case.
  Every input column of the table needs its own "absent / not present" row: a table that covers
  "no reply in output" but not "reply present in output, absent from history" is where the
  implementer guesses and the reviewer files a `major`. When a column identifies a person, owner,
  or resource (trip owner, chat owner, `resourceId`, uid) and the data reaches that identity by
  more than one path, the table also needs a row for the paths disagreeing (chat owner differs
  from trip owner; thread `resourceId` differs from the user id) and names which path is
  authoritative for every exported or compared field;
- runtime guarantees the implementation may lean on ("X is always persisted before Y runs"): write
  them in `Decided` as an explicit assumption with its evidence, never only in `Context`. Context
  binds nobody, so the implementer cannot rely on it and the reviewer must treat the case as
  reachable;
- the data source of every output field or list ("the calls made at step N" says which records
  they come from), not only identity fields;
- when behavior must mirror another system ("send what production sends"), the authority to read
  (a package, module, or service) rather than values transcribed from it. Transcribed values are
  partial and go stale; the implementer builds them literally. Name the exact file production
  loads, as a resolved path, and the production call site that uses it, checked by reading that
  call site: a package can exist twice in `node_modules` (a top-level install and a copy vendored
  inside another package), and the two can differ in the very behavior the task mirrors. Name what
  the authority is known not to record, so the implementer supplies it deliberately instead of
  discovering it at the first live call;
- edge cases with their expected outcome (missing source, empty input, partial failure);
- `Non-goals`: adjacent behavior deliberately excluded, so the implementer does not build it and the
  reviewer does not demand it;
- `Decided`: durable design constraints the user has already chosen (trust model, data boundaries,
  what must never happen). Each entry is one line with its reason. Reviewers treat these as
  accepted, so record only genuine decisions, not preferences;
- for scripts and tools: who runs it, with what credentials, against what environment, and what it
  must never do. Reviewers cannot calibrate security severity without this;
- scale budget and access pattern, in `Decided`, whenever the code reads or writes a shared or
  production store beyond a handful of documents: the expected volume (rows, documents, chats) with
  its source, the read shape the implementer must keep (one batched query per table, filter before
  fetching, skip already-processed items before any remote read), and any index or table the plan
  knows to be expensive. Without it the implementer writes one query per item and the reviewer
  files cost findings the task never priced.

Leave these out:

- file paths, function names, and line numbers of existing internals (a public export the task
  depends on may be named once, without a line number);
- prescribed cache layouts, paging strategies, data-structure choices, helper reuse, or algorithm
  steps;
- test mechanics: which assertion to write, which methods to check for, which property to inspect,
  which fake to build, how many pages a fake returns, which command to run inside the test.
  A work item states the guarantee ("the exporter issues no writes to Postgres or Firestore") and
  names the test file; the implementer chooses the proof. A prescribed assertion shape ("test
  asserts no write method is reachable") gets built literally and becomes a tautology, and every
  prescribed mechanic the implementer skips becomes a spec finding that has nothing to do with
  whether the behavior works. The allowed form is `— proven in <test file>`; a clause that
  mentions a fake, a fixture shape, a page count, an assertion, or a shell command is struck;
- lists of data sources or fields to collect that no acceptance criterion consumes;
- the implementer's future reconnaissance ("X exposes no exports, so do Y");
- speculative limits, caveats, and follow-ups that are not requirements. State a known limit once,
  in `Context`, and do not turn it into work.

If a detail is necessary for correctness, it is a contract or a decision: write it in `What to
build` or `Decided`. If it is merely helpful, it is context: write it in `Context`. If you cannot
tell, leave it out; the implementer will find it in the code.

</task-detail-rules>

#### Traceability

Every behavior sentence in `What to build` must map to at least one `Implementation work` item and
one acceptance criterion, and every work item that changes behavior must name the test that proves
it. The implementer builds from the work items; the reviewer reviews against `What to build`. A
sentence present in one and absent from the other is exactly where they diverge. Before presenting
the breakdown, walk `What to build` sentence by sentence and confirm each one is either covered or
moved to `Context`.

Acceptance criteria must be executable by the implementing agent in the repository with local
resources, or be declared as a `[verify]` human checkpoint. Do not cite a command or a production
dataset as a criterion without confirming that the command works on the current base branch and the
data is reachable without production access.

#### Right-sized engineering

Plan genuinely good code at the smallest size that delivers the source. These rules bar
unrequested machinery, not craftsmanship: repository conventions, cohesive structure, clear
naming, real error handling for reachable failures, and tests remain mandatory in every task.

<right-sizing-rules>

- Plan the simplest well-factored design that satisfies the acceptance criteria. Prefer the
  code's existing structure when the change fits there cohesively; a new module for a genuinely
  new responsibility is good engineering, not overengineering.
- Do not plan a new abstraction — interface, base class, wrapper, registry, config option,
  env var, feature flag — for a single consumer unless it demonstrably improves testability or
  readability now. Never justify structure by a future the plan does not contain.
- No speculative generality: no extensibility hooks, no parameterizing what the source treats
  as fixed, no "while we're here" restructuring.
- Handle failures the planned code path actually encounters and validate at trust boundaries;
  that is normal craft. Do not plan recovery machinery — retries, fallbacks, circuit breakers,
  caching, graceful degradation — unless the source requires it.
- Phrase implementation work items as behavior, not architecture. A work item that introduces
  new structure must name the source requirement or concrete design pressure that forces it.

</right-sizing-rules>

#### Wide mechanical refactors

Use a non-vertical refactor task only when a cross-cutting mechanical change cannot land green as
a vertical slice. Plan it as expand, migrate, and contract tasks:

1. Add the new form alongside the old.
2. Move callers in the smallest green batches the blast radius permits.
3. Remove the old form after every caller has migrated.

Each intermediate task must be mergeable and green. Do not create cleanup or prefactoring tasks
merely because they would be convenient.

#### Dependencies

Give each task the minimal set of direct predecessors whose merged output it needs. Use `none` when
it needs no predecessor. Eligibility comes from dependencies, not list position: every dependency
must be `[x]` before the task can start.

- Serialize tasks that change the same durable shared artifact by adding a direct dependency and
  naming the artifact in the dependent task.
- If a new task becomes a prerequisite of an unfinished existing task, update the existing task's
  `Depends on` field and master-plan pointer. Do not renumber stable task identifiers.

### 5. Confirm the breakdown before writing

Present every proposed task as a numbered list. For each task show:

- title;
- the independently verifiable outcome;
- adjacent behavior deliberately excluded;
- direct dependencies;
- automated verification, or the required manual verification;
- why another split would make the task incomplete;
- the size-gate result (word count of the binding sections, primary output, integration points).

Ask whether tasks should be split, merged, reordered, or re-scoped. Wait for explicit approval
before creating or modifying any plan or task file, including when only one task is proposed.

### 6. Separate implementation work from human checkpoints

- **Implementation work** is everything the agent can implement and verify autonomously. Use the
  `tdd` skill and phrase behavior work test-first where appropriate.
- **Human checkpoints** are limited to:
  - `[decision]` for an unresolved product, architecture, or scope choice, handled through
    `talk-it-through`;
  - `[verify]` when the result cannot be verified automatically;
  - `[confirm-db]` for real, shared, destructive, persistent, or ambiguous database or data work;
  - `[confirm-security]` for changes to authentication, authorization, sessions, secrets,
    cryptography, dependency trust, CI, sandboxing, or another trust boundary.

Automate verification whenever possible. A `[verify]` item must state why automation is impossible,
the exact steps the user must perform, the expected result, and what indicates failure. Manual
verification blocks task completion until the user confirms it passed.

### 7. Write the approved task files

Use the next ordinal after the maximum ordinal in `plans/tasks/` and `plans/tasks/done/`, padded to
four digits. Write `plans/tasks/NNNN-<kebab-slug>.md`.

Each task must contain the relevant source requirements and acceptance criteria so a fresh
implementer does not need the PRD or neighboring tasks. Point to durable decisions instead of
duplicating them.

The sections `What to build`, `Decided`, `Clarifications`, `Non-goals`, `Implementation work`,
`Human checkpoints`, and `Acceptance criteria` are **binding**: the implementer builds them and the reviewer reviews
against them. `Context` is **non-binding**: background, evidence, and known limits that explain
the task but create no requirement and no finding.

<task-file-template>
# Task NNNN: <Title>

**Branch**: `feature/<kebab-slug>`
**Depends on**: <direct predecessor ordinals, or `none`>
**Source**: <PRD, decision document, or conversation date> · **User stories**: <list>

## What to build

<One smallest complete, independently verifiable behavior described end to end: inputs, outputs,
effect. For a classification, verdict, or status output, include the decision table.>

## Decided

- <durable constraint the user chose> — <one-line reason>
- <for scripts/tools: who runs it, with what credentials, against what, and what it must never do>

(Omit when the task carries no decision beyond the master plan's architectural decisions.)

## Clarifications

(Leave empty. `implement-next-task` appends each question the worker had to ask and the user's
answer here, dated. Entries bind like `Decided`.)

## Non-goals

- <adjacent behavior deliberately excluded, and where it goes if anywhere>

## Context

<Non-binding. Why the task exists, evidence, known limits. No requirements here.>

## Implementation work

- [ ] <work item stated as behavior or guarantee, naming the test file that proves it; never the assertion>

## Human checkpoints

- [ ] [decision] <question requiring shared understanding> (`talk-it-through`)
- [ ] [verify] <manual steps> · Expected: <result> · Failure: <failure signal> · Reason:
      <why automation is impossible>
- [ ] [confirm-db] <database or data action requiring approval>
- [ ] [confirm-security] <trust-boundary action requiring approval>

(Omit `Human checkpoints` when none apply.)

## Acceptance criteria

- [ ] <criterion proving the behavior, runnable by the agent locally, or moved to a [verify] item>
</task-file-template>

Before writing each file, re-check it against the size gate (measured), the base-branch checks in
step 3, the task-detail rules, and traceability. Fix the task, not the check. Two checks are
mechanical and run every time:

- read every `Implementation work` item's test clause; it names a test file and nothing else.
  Strike any mention of a fake, a fixture shape, a page count, an assertion, or a command;
- when the user carried planning-feedback lines from a `task-review` result into this pass, each
  line is either reflected in a binding section of the new task or answered in one sentence in
  the breakdown. A planning-feedback line that is silently dropped repeats the same review
  finding on the next task.

### 8. Append task pointers

Append one pointer per approved task to the master plan. Mirror direct dependencies in an
`(after ...)` suffix and omit the suffix for `none`:

```markdown
- [ ] NNNN · <Title> → tasks/NNNN-<slug>.md
- [ ] NNNN · <Title> (after NNNN[, NNNN]) → tasks/NNNN-<slug>.md
```

Tell the user which task files were created and where they sit in the plan.

## Master-plan template

<master-plan-template>
# Plan: <Project Name>

> Source: <brief identifier or link>

This is the project's local master plan. Task bodies live in `plans/tasks/`; merged tasks move to
`plans/tasks/done/`.

## Workflow

- `to-plan` adds approved self-contained task files and pointers.
- `implement-next-task` takes the first eligible task, claims it as `[~]`, and implements it through
  `tdd-worker` and `tdd`, using `talk-it-through` when the task or an unexpected obstacle requires a
  decision. The user then runs `task-review` and `review-fix-worker` manually until the review is
  clean, and `finish-task` updates the README, proves the behavior, and invokes `create-pr` after
  user approval.
- `[ ]` means ready, `[~]` in progress, `[>]` complete with a CI-green PR awaiting merge, and `[x]`
  merged into `main`.
- After the PR merges, the user synchronizes local `main`, cleans the merged branch, changes
  `[>]` to `[x]`, and moves the task to `tasks/done/`.
- A task is eligible only when every ordinal in its `(after ...)` list is `[x]`.
- Run one `implement-next-task` workflow at a time in the current checkout.

## Architectural decisions

- **Routes**: ...
- **Schema**: ...
- **Key models**: ...

---

## Tasks

- [ ] 0001 · <Title> → tasks/0001-<slug>.md
- [ ] 0002 · <Title> (after 0001) → tasks/0002-<slug>.md
</master-plan-template>
