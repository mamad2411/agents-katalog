---
name: rc-tickets
description: "Breaks a spec into independent tickets with blocking edges, enriched from the code. Use after a spec exists. Not for implementing one."
argument-hint: "[feature-name]"
model: sonnet
effort: high
---

# Tickets

Decompose a spec into tickets an executor can implement **in isolation**, each carrying enough context
that nobody has to grep the repo to start. A roadmap is the same object at a coarser grain — a list of
phases, each of which later decomposes into tickets — so both live here.

Read `$CLAUDE_PLUGIN_ROOT/skills/promoted/rc/references/conventions.md` first.

Field definitions are in `references/task-context-schema.md`; the ticket body structure is
`references/task-template.md`; the roadmap format is `references/roadmap-format.md`.

## 1 — Load context

The allowed `type` values are `frontend`, `backend`, `docs`, `test`, `infra`, `refactor`, `chore`,
`bugfix`. (These used to be overridable from `.rc/config.toml`, which was the retired CLI's config
file — nothing reads it now. A project needing a different set edits this list.)

Read `_prd.md`, `_techspec.md` and the ADRs under `.rc/tasks/<slug>/adrs/`. Then:

- **No `_techspec.md`** — warn that tickets will be coarser, derive them from the PRD's functional
  requirements and user stories, lean harder on codebase exploration for implementation detail, and
  **call out the gaps explicitly in the ticket body instead of inventing specifics**.
- **Neither document** — stop and ask the user to create at least one first.

Spawn read-only subagents to explore the codebase for the files to create or modify, the test patterns
and the coding conventions in play.

## 2 — Challenge scope, then decompose

The spec already applied YAGNI to the architecture; here the guard is ticket *scope*. Before turning a
requirement into a ticket, ask whether it needs to exist in **this** delivery or is speculative, and
whether step 1's exploration already found something that covers it. Drop speculative tickets; merge
ones that only scaffold "for later". If the spec deliberately cut a component, do not reintroduce it as
a ticket. **Never silently remove work the PRD explicitly requests** — when something looks like YAGNI
but sits inside PRD scope, keep it and flag it at the approval gate.

Then decompose, under these constraints:

- **A ticket touches at most 7 files and carries at most 7 subtasks.** Past that, split it and declare
  the edge between the halves.
- **Each ticket is independently implementable once its declared dependencies are met.** The executor
  runs tickets in isolation, so undeclared coupling is precisely what makes one fail mid-run. If two
  tickets are tightly coupled, either merge them or extract the shared piece into a ticket both depend
  on.
- **No circular edges.** If A depends on B, B must not depend on A directly or transitively — neither
  could ever start.
- **Test requirements are embedded in every ticket.** Never create a ticket whose only job is testing.

Complexity is assigned by real shape, not by feel:

| | Means |
| --- | --- |
| `low` | single file, no new interface, no concurrency, straightforward logic |
| `medium` | 2–4 files, may introduce an interface or type, limited integration points |
| `high` | 5+ files, new subsystem or significant refactor, several integration points, concurrency |
| `critical` | cross-cutting across packages, high regression risk, needs coordination with other tickets |

## 3 — Approval gate

Present every ticket with its title, description, complexity and dependency chain. **Wait for the
user.** Revise and re-present until they explicitly approve. This is the last cheap moment to fix a
wrong decomposition.

## 4 — Write the files

`_tasks.md` is the master list:

```markdown
# [Feature Name] — Task List

> PRD: [_prd.md](_prd.md) · TechSpec: [_techspec.md](_techspec.md)

## Tasks

| # | Title | Status | Complexity | Dependencies |
|---|-------|--------|------------|--------------|
| 01 | [Task title] | pending | [low/medium/high/critical] | [task_NN, ... or —] |
```

Then `task_01.md` … `task_N.md` (the `task_` prefix carries no leading underscore). Each starts with
YAML frontmatter holding `status`, `title`, `type`, `complexity` and `dependencies` — use
`dependencies: []` when there are none, never omit the field. Numbering is sequential and consistent
between the master list and the files.

## 5 — Enrich each ticket

Skip a ticket that already has `## Overview`, `## Deliverables` and `## Tests`. Otherwise map it to its
PRD requirements and spec guidance, spawn a read-only subagent to discover the relevant files,
dependent files, integration points and project rules **for that ticket**, and fill every section of
`references/task-template.md`. The executor reads these as its contract; a missing section leaves it
guessing:

- `## Overview` — what and why, 2–3 sentences.
- `<requirements>` — numbered technical requirements in MUST/SHOULD language.
- `## Subtasks` — 3–7 checklist items describing **what**, not how.
- `## Implementation Details` — the paths to create or modify, the integration points.
- `### Relevant Files` / `### Dependent Files` — discovered paths, each with a one-line reason.
- `### Patterns to Mirror` — 1–3 snippets of **real code already in this repo** the implementation
  should imitate: the existing error-wrap style, the table-test shape, the handler pattern. Copy the
  actual lines (≤10 each) and tag each `// SOURCE: <path>:<start>-<end>`. Capture it now, while you
  have the codebase loaded — if the executor would have to grep for "how we do X here", that knowledge
  belongs in the ticket. Omit only when the ticket genuinely has no precedent.
- `### Related ADRs` — links, or omit the subsection.
- `## Deliverables` — concrete outputs, including the test items.
- `## Tests` — specific cases as checklists, split unit and integration. Name the input, condition or
  behaviour verified: "POST /job/done with an unknown job ID returns 404", never "test the happy path".
- `## Success Criteria` — measurable outcomes.

Reassess complexity against what the exploration found and update it if it changed.

**The no-prior-knowledge test.** Before finalizing each ticket: *could a competent developer with no
prior context implement this correctly from the ticket plus the referenced spec sections, without
grepping the repo to discover how things are done here?* If not, the gap is missing context — add the
file paths, the Patterns to Mirror snippet, or the specific spec/ADR reference that closes it. A ticket
only its author could implement is under-enriched.

If enrichment fails on one ticket, continue with the rest and report every failure at the end.

## 6 — Validate

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/validate-tasks.mjs" --slug <feature>
```

Fix what it reports and re-run. Not done until it exits 0.

## Roadmap mode

A roadmap is the human-owned list of phases a long build walks one at a time, at a grain coarser than a
ticket: each phase is a chunk that fits one executor window and ends in a checkable state.
`references/roadmap-format.md` holds the format. Three operations:

- **create** — author or extend `.rc/ROADMAP.md`, then **confirm the phase list and order with the
  user**. The roadmap encodes intent; never invent it.
- **next** — resolve the next unchecked actionable phase.
- **status** — summarize progress: done, current, remaining.

A phase becomes tickets by running this skill's phases 1–6 against it when its turn comes. Do not
pre-decompose the whole roadmap: later phases are re-planned with what the earlier ones taught.

## Error handling

- Contradiction between the PRD, the techspec and an ADR → stop and report it; never pick a side.
- A ticket that cannot be made independent → merge it or extract the shared dependency; do not ship an
  undeclared edge.
