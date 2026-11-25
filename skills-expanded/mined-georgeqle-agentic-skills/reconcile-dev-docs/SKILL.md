---
name: reconcile-dev-docs
description: Reconcile development docs by auditing roadmap, todo, history, phase archives, specs, git history, and code reality
type: analysis
version: v0.2
required_conventions: [alignment-page]
argument-hint: "[audit|fix] [tasks|specs|all]"
---

# Reconcile Dev Docs

Invoke as `$reconcile-dev-docs`.

Audit or repair development documentation so the roadmap, current work, history, specs, and evidence from git/code all tell the same story.

## Process

### 1. Determine Mode and Scope

Parse `$ARGUMENTS`:

- **Mode**: `audit` (default, read-only) or `fix` (update development docs only)
- **Scope**: `all` (default), `tasks`, or `specs`

Resolve the canonical development docs:

- `tasks/roadmap.md`
- `tasks/todo.md`
- `tasks/manual-todo.md` (if it exists)
- `tasks/record-todo.md` (if it exists)
- `tasks/recurring-todo.md` (if it exists)
- `tasks/history.md`
- `tasks/phases/*.md`
- `tasks/ideas.md` (if it exists)
- `specs/*.md` and `specs/*/*.md`
- `docs/specifications/*.md` (fallback specs location)

If no task docs exist, report that there is nothing to reconcile and recommend `$roadmap` or `$plan-phase` based on available specs.

### 2. Gather Evidence

Read the development docs and collect:

- Roadmap phases, milestone checkboxes, acceptance criteria, manual tasks, record tasks, recurring tasks, and deferred items
- Current todo phase, checked/unchecked steps, blockers, and review/results sections
- Manual task blockers and `_(blocks: ...)_` / `_(after: ...)_` annotations
- Record task conditions, non-blocking reasons, evidence paths, and promotion rules
- Recurring task cadence, last run, next due, evidence paths, and escalation conditions
- History entries with dates, completed phases/steps, commit SHAs, and claimed outcomes
- Phase archives and their completion summaries
- Spec titles, statuses, acceptance criteria, and major implementation claims

Read git/code evidence:

- `git status --short`
- `git log --oneline -50`
- `git log --name-only --since=<latest relevant doc date>` when timestamps suggest docs may be stale
- Targeted file existence and `rg` checks for claims marked complete

### 3. Reconcile Rules

Classify findings:

| Severity | Examples |
|----------|----------|
| **Error** | Docs contradict each other: roadmap marks a phase done while todo has unchecked required steps; history claims completion but no matching roadmap/todo/archive/git evidence exists |
| **Warning** | Likely drift: recent commits changed areas covered by specs but history/todo were not updated; completed phase has no archive; manual blockers remain for completed steps |
| **Info** | Cleanup opportunities: stale handoff notes, missing links between history entries and commits, specs that should be checked by `$spec-drift` |

Use these specific checks:

- `tasks/todo.md` checked steps should be reflected in `tasks/history.md` after shipping.
- Completed roadmap phases should have corresponding `tasks/phases/phase-N.md` archives.
- The active `tasks/todo.md` phase should match the first incomplete roadmap phase.
- `tasks/manual-todo.md` should not contain unchecked blockers for completed todo steps unless the user explicitly overrode them.
- `tasks/todo.md` should not contain condition-gated baseline measurements or future records unless they are current execution work; move clear cases to `tasks/record-todo.md`.
- `tasks/manual-todo.md` should not contain non-blocking records unless they require human-only external action tied to a `blocks` or `after` step; move clear cases to `tasks/record-todo.md`.
- `tasks/manual-todo.md` should not contain agent-executable work such as repo edits, SDK wiring, generated assets, local commands, tests, audits, or authenticated CLI/API operations; move clear cases to `tasks/todo.md`.
- `tasks/recurring-todo.md` due items should remain advisory unless explicitly promoted into `tasks/todo.md`.
- Recent commits that complete user-facing work should have a matching history entry.
- Specs whose described areas changed after their last modification date should be flagged for `$spec-drift`.
- Claimed completed work should have either git evidence, file evidence, test evidence, or an explicit note explaining why evidence is unavailable.

### 4. Fix Mode

In `fix` mode, apply only unambiguous development-doc changes:

- Append missing factual entries to `tasks/history.md`.
- Check roadmap milestones only when todo/archive/git evidence all support completion.
- Create missing `tasks/phases/phase-N.md` archives from completed `tasks/todo.md` content.
- Move the next roadmap phase into `tasks/todo.md` only when the current phase is clearly complete.
- Move clearly misclassified non-blocking condition-gated records from `tasks/todo.md` or `tasks/manual-todo.md` into `tasks/record-todo.md`.
- Move clearly misclassified cadence-based obligations from `tasks/todo.md` or `tasks/manual-todo.md` into `tasks/recurring-todo.md`.
- Move clearly misclassified agent-executable work from `tasks/manual-todo.md` into `tasks/todo.md` with enough file/command detail for `$exec`.
- Add unresolved contradictions to `tasks/todo.md` under `## Development Docs Reconciliation`.
- Archive existing `specs/` or `docs/specifications/` files before replacing or substantively rewriting them.
- Write `tasks/reconciliation-report.md` with resolved, deferred, and remaining findings.

Ask before applying any ambiguous change. If already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask plainly in chat.

## Output

### Audit Mode

```
## Dev Docs Reconciliation

### Errors (N)
- **tasks/todo.md** - [problem]. Evidence: [roadmap/history/git reference].

### Warnings (N)
- **specs/foo.md** - [problem]. Recommended action: $spec-drift.

### Info (N)
- **tasks/history.md** - [cleanup opportunity].

### Summary
- Roadmap/todo alignment: [ok|issues]
- History coverage: [ok|issues]
- Phase archives: [ok|issues]
- Spec freshness: [ok|issues]
- Recommended next action: [specific skill or fix plan]
```

### Fix Mode

Report the same sections plus:

```
### Fixed
- [x] [file] - [change made]

### Deferred
- [ ] [finding requiring user judgment]
```

## Constraints

- Read-only by default.
- In `fix` mode, modify only development docs under `tasks/`, `specs/`, or `docs/specifications/`; archive existing spec documents before replacement per the Archive-First Replacement Policy.
- Do not modify code, research docs, kanban cards, git history, or deployment state.
- Do not rewrite or delete old `tasks/history.md` entries; append corrections or superseding notes.
- Do not uncheck completed work automatically. Report unsupported completion claims unless the user approves the correction.
- Treat `tasks/roadmap.md` as the strategic source of truth, `tasks/todo.md` as the active execution contract, `tasks/manual-todo.md` as human-only external step-linked work, `tasks/record-todo.md` and `tasks/recurring-todo.md` as advisory surfaces, and `tasks/history.md` as append-only evidence.

## Alignment Page

By default, this skill reports results inline and writes only its normal durable artifacts (for example `tasks/*.md`, reports, queues, benchmark notes, status docs, or other skill-specific files). Do not build an alignment page automatically. Create `alignment/reconcile-dev-docs-{topic}.html` only when the user explicitly requests an alignment page or when you explicitly identify a concrete clarification/review need that cannot be handled cleanly inline; when you create one, follow `ALIGNMENT-PAGE.md` in this skill's directory.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
