---
name: task-file-format
description: "Use when creating, validating, or updating a task file in docs/tasks/. Defines the canonical TASK-XXX file template, naming convention, status rules, blocker handling, and which roles may edit which sections. Keywords: task file, TASK-XXX, docs/tasks, acceptance criteria, Gherkin, blocker, Completion."
---

# Task file format

Every task lives in `docs/tasks/<TASK-ID>-short-description.md`, where the
TASK-ID is `TASK-<NNN>` with NNN zero-padded to 3 digits. Assign the next ID
by scanning `docs/tasks/` for the highest existing one. The matching branch
is `task/<NNN>-short-description`.

## Canonical template

Use this template exactly:

```markdown
# <TASK-ID> Short description

## Status
todo | in-progress | blocked | done

## Requirements
**Binding:** REQ-XXX, REQ-YYY
**BDD mode:** BDD-ACTIVE | BDD-PLANNED | BDD-ABSENT
**Depends on:** TASK-MMM or "none"
**Precedence:** The requirements above are the binding definition of this task.
The story and scenarios below are derived from them. On any discrepancy, the
requirements document wins. Stop and report discrepancies; do not build from
the story.

## Story (context, not binding)
As a <role>, I want <capability>, so that <benefit>.

## Description
What needs to be done and why.

## Branch
**Branch name:** `task/<NNN>-short-description`
**Switch/create:** `git checkout -b task/<NNN>-short-description`
**Make target:** `make branch-task f=<TASK-ID>`

## Acceptance criteria (Gherkin)
**Feature files:** tests/bdd/features/<TASK-ID>-*.feature (BDD-ACTIVE only; omit or write "None" otherwise)

- [ ] 1. Scenario: <name derived from the requirement's trigger and effect>
      Given <precondition / state from the requirement's WHILE/IF clause>
      When <trigger from the requirement's WHEN clause>
      Then <observable effect with the requirement's measurable values>
- [ ] 2. Scenario: <error/boundary case>
      See `tests/bdd/features/<TASK-ID>-<slug>.feature`: Scenario "<name>"

Each numbered criterion carries either an inline Gherkin scenario or a
reference to the feature file + scenario name that covers it (e.g.
`See tests/bdd/features/TASK-XXX-example.feature: Scenario: <name>`). Use
inline scenarios for BDD-PLANNED/BDD-ABSENT tasks; use feature file
references for BDD-ACTIVE tasks. Both forms may appear in the same task
file without ambiguity — each criterion picks exactly one.

Map each requirement clause to its Gherkin step: precondition -> Given,
trigger -> When, obligation/measurable value -> Then.

## Out of scope
- <explicit exclusions, including negative/scope-exclusion requirements>

## Blockers
- [ ] REQ-XXX carries [VALUE TBD] for <parameter>: must be resolved before implementation
- (write "None" if empty)

## Completion
**Date:** YYYY-MM-DD
**Summary:** What was done, any decisions made, and what was left out and why.
**Files changed:**
- `path/to/file` - created / modified
**Branch:** `git checkout task/<NNN>-short-description`
**Stage:** `path/to/file1 path/to/file2 CHANGELOG.md`
**Commit:** `git commit -m "Short imperative summary of what was done"`
```

## Rules

- Every task references at least one REQ-ID, and every referenced REQ-ID must
  exist verbatim in the requirements document.
- The Precedence section (requirements binding, story is context) must be
  present verbatim in every task file.
- Every measurable value from the referenced requirements (time, threshold,
  capacity) appears verbatim in a Then step.
- A `[VALUE TBD]` or `[TRIGGER TBD]` in a referenced requirement appears as
  `<TBD: parameter>` in the scenario AND as an open item under Blockers.
- A task with any open Blocker has Status `blocked` and must not be
  implemented. Only the user can waive a blocker.
- The `**Commit:**` line is the message used by `make commit-current-task` -
  keep it a single short imperative sentence.
- The `**Stage:**` line is a whitespace-separated list of file paths only -
  never a command line. `butler task stage` always runs `git add <paths>`
  itself; it never executes the field's text as a shell command. Never write
  `make ...`/`butler ...`/`git ...` there - doing so does not run that
  command, it is treated as literal (and almost certainly invalid) file
  paths (see REQUIREMENTS_TASK_WORKFLOW.md Requirement 15, and the
  TASK-069/TASK-082/TASK-083 incidents this closes off).
- `CHANGELOG.md` must always be in the Stage list.
- Acceptance criteria are numbered (1, 2, 3, ...); each criterion keeps the
  checkbox marker (`- [ ]`/`- [x]`) at the start of the line — the number is
  part of the criterion text, not a separate list level — so
  `butler task check --criterion N` keeps working against the existing
  `- [ ]` parser.
- Each numbered criterion is followed by exactly one of: an inline Gherkin
  scenario (`Given`/`When`/`Then`), or a reference to the feature file and
  scenario name that covers it (`See <path>.feature: Scenario "<name>"`).
  Use inline scenarios for BDD-PLANNED/BDD-ABSENT tasks; use feature file
  references for BDD-ACTIVE tasks. Both forms may appear in the same task
  file, one per criterion, without ambiguity.
- When BDD mode is BDD-ACTIVE, the task file includes a `**Feature files:**`
  field (placed under the `## Acceptance criteria (Gherkin)` heading) listing
  the `.feature` files belonging to the task. Omit it or write "None" for
  BDD-PLANNED/BDD-ABSENT tasks.
- Requirement clauses map to Gherkin steps: precondition -> Given, trigger ->
  When, obligation/measurable value -> Then.

## Status transitions and role boundaries

- Drafting roles (Task Drafter, Bug Triage, Dependency Auditor, Test Design
  Reviewer) fill in every section except Completion, and set Status only to
  `todo` or `blocked`.
- The Workflow Guardian owns the `in-progress` and `done` transitions and is
  the only role that edits Status and Completion on an existing task. It
  never hand-edits stories, scenarios, or blockers.
- Acceptance criteria checkboxes are checked off only by the Workflow
  Guardian, one by one, after it has verified with its own tool calls that
  the corresponding automated test exists and passes.
