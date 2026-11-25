---
name: todo
description: >-
  Use when generating or resuming TODO.md from PLAN.md, reporting task state,
  handling blocked, skipped, temporary, or dependent items, recording
  CHANGELOG.md, or continuing tracked work across sessions.
---

# Smart TODO Flow

Manage work through `PLAN.md` -> `TODO.md` -> `CHANGELOG.md`.
Core principle: **persistent memory, resumable, user controls the pace**.

# State Detection

On every invocation, detect state by priority:

1. User explicitly says "clear todo" -> clear `TODO.md`
2. `TODO.md` exists with unchecked items (`[ ]`) -> enter Resume Mode
3. `TODO.md` exists and all items are resolved (`[x]`, `[-]`, `[~]`; no `[ ]`) -> enter Completion Pending
4. `TODO.md` is missing or empty -> enter Generation Mode

If the user explicitly asks to write the changelog or archive work, enter the relevant changelog flow even if another state applies.

# Task States

TODO items support four states:

| Syntax | State | Meaning |
|--------|-------|---------|
| `- [ ]` | Pending | Not started |
| `- [x]` | Done | Completed |
| `- [-]` | Blocked | Cannot proceed; reason noted inline |
| `- [~]` | Skipped | Intentionally deferred |

Blocked and skipped items use inline notes:

```markdown
- [-] Deploy to production (blocked: waiting for security review)
- [~] Write integration tests (skipped: API spec not finalized)
```

# Resume Mode

## Smart Detection of Completed Work

If the project is a git repository, inspect recent commits and the current diff:

- `git log --oneline -10`
- `git diff --stat`

Compare them against unchecked TODO items. If an item appears addressed, suggest marking it done but never update it without user confirmation. Skip this step outside git repositories.

```text
Detected: recent commits may have addressed these items:
- [ ] Implement user auth -> commit a1b2c3d "add user auth middleware"
Mark as done? (y/n per item)
```

## Progress Report

Read `TODO.md` and report progress with a state breakdown. Use `TODO.md` as the primary state source. Read `PLAN.md` only when the phase marker, next-phase decision, or plan/task ambiguity requires it.

```text
Phase: 2 (from PLAN.md)
Progress: 3/7 done · 1 blocked · 1 skipped · 2 remaining

Blocked:
- [-] Task B (blocked: reason)

Skipped:
- [~] Task F (skipped: reason)

Remaining:
- [ ] Task D
- [ ] Task E

How would you like to proceed? (e.g.: do next item / finish all / do item 5 first / I'll pick)
```

Omit the Phase line when no `<!-- phase: N -->` marker exists.

## Runtime Integration

Before starting an execution item, read `references/runtime.md` when it exists.
Use that adapter only for ephemeral session progress; `TODO.md` remains the durable source of truth.
If the adapter capability is unavailable, continue without the session mirror.

# Generation Mode

## Information Gathering

Use project instructions already available in the current context.
Read the relevant instruction files only when that context is missing or insufficient.
Then gather the remaining generation context:

1. `PLAN.md` for goals and phase planning
2. Current code state, including `git status` and recent commits when git is available

## When PLAN.md Does Not Exist

Ask the user:

```text
No PLAN.md found in this project. How should we proceed?
1. I'll draft a quick one based on project instructions and current project state
2. You generate one yourself
3. No PLAN needed - just tell me what to do
```

## PLAN Guidance

When the user's input looks like it might contain planning-level content, offer a choice instead of deciding for the user:

```text
These could be planning directions or action items - you know best:
1. Write to PLAN.md first, then pick items to generate TODO
2. Directly generate TODO from these

Which way?
```

Planning-level content includes multiple directions, feature ideas, architectural options, phased goals, or vision-level discussion.

## Phase Detection

When reading `PLAN.md`:

1. Look for phase or stage structure, such as `Phase 1`, `Stage A`, `第一阶段`, or numbered sections
2. If `TODO.md` previously existed with `<!-- phase: N -->`, identify the next phase
3. If no prior phase marker exists, start from the first phase with unfinished goals
4. Present the detected phase to the user for confirmation before generating

## Generating TODO

- Break down current phase goals into concrete, actionable steps
- Default to 5-8 steps; adjust if the user asks for finer or coarser granularity
- If tasks have natural ordering dependencies, annotate with `(depends: N)` where `N` is the item number
- Present the TODO draft for confirmation; write `TODO.md` only after approval
- If the user modifies the draft, adjust and re-confirm

`TODO.md` format:

```markdown
# TODO

<!-- phase: 1 -->

- [ ] First step description
- [ ] Second step description
- [ ] Third step description (depends: 2)
```

Keep `TODO.md` as a pure checklist: no dates, section headers, or priority fields beyond the phase comment.

# Execution

## User Options

The user may:

- Specify one or several items to work on
- Say "next" to do one item
- Say "finish all" to execute all remaining items in one turn
- Pick a custom order
- Mark an item as blocked: "item 3 is blocked because..."
- Mark an item as skipped: "skip item 4"

Default pacing: after completing each item, pause, report progress, and wait for user input before continuing. "finish all" opts into a longer continuous turn with higher token usage.

## Dependency Check

When the user selects a task, check for `(depends: N)`. If a dependency is not `[x]`, warn the user and ask whether to proceed anyway or do the dependency first.

## Starting a Task

When the user selects a task:

1. Re-read relevant project instructions when needed
2. Read `references/runtime.md` when it exists
3. Use the runtime adapter to mark the selected item in progress when that capability is available
4. Implement the task

If the user marks an item blocked or skipped instead of implementing it, update `TODO.md`, append changelog when appropriate, and reflect the resolved state in the ephemeral session mirror when available.

## Temporary Tasks

When the user wants to do something else mid-flow, insert temporary tasks as indented sub-items under the furthest-progressed main item:

```markdown
- [x] Completed task A
- [x] Completed task B
  - [ ] [temp] User's temporary request
  - [ ] [temp] Another temporary task
- [ ] Original task C
- [ ] Original task D
```

- Temporary tasks remain visually distinct from main-line items
- After all temporary tasks are done, resume the next main-line item
- Main-line order is never disrupted
- Include active `[temp]` sub-items in the ephemeral session mirror when available

## Completing an Item

After completing an item:

1. Mark it done in `TODO.md`: `- [x] task description`
2. Mark it completed through the runtime adapter when available
3. Append to `CHANGELOG.md` under the current batch
4. Refresh the session mirror from remaining pending TODO items when continuing in the same turn
5. If all actionable items are done, notify the user and offer Completion Pending options
6. Unless the user requested "finish all", pause and wait for "next" or "continue"

Do not include completion dates in `TODO.md`.

# Changelog Rules

Follow three rules:

1. **Immediate:** append an entry whenever a TODO item is completed
2. **Batched:** with git, one batch is one commit and is sealed on commit; without git, one batch is one TODO round and is sealed on clear or new round
3. **Style-adaptive:** match the existing changelog; otherwise use the default format

```markdown
# CHANGELOG

## YYYY-MM-DD (batch summary)
- <verb> <description>
```

- Keep newest batches at the top
- Keep heading summaries to 2-8 Chinese characters or 3-5 English words
- Use `- <verb> <description>` entries, one line per change
- Before appending, determine whether the latest batch is still open
- Create a new top heading when the previous batch is sealed
- When appending to an open batch, read only the latest heading and do not reread the full changelog

# Completion Pending

When all actionable items are resolved, report done, blocked, and skipped counts and offer independent next actions:

```text
All TODOs resolved! (N done, M blocked, K skipped)
Changes have been recorded in CHANGELOG.md.

Remember to update PLAN.md - mark Phase N as completed if appropriate.

You can:
1. Review or edit blocked and skipped items
2. Review or revise CHANGELOG.md
3. Clear TODO.md
4. Commit to git
5. Generate the next phase TODO from PLAN.md
```

Show the commit option only in git repositories. Show the next-phase option only when `PLAN.md` has a subsequent phase. Never auto-chain these operations.
Show the PLAN update reminder only when `TODO.md` contains a `<!-- phase: N -->` marker and `PLAN.md` exists.

# Clear TODO

Clear only when the user explicitly asks. Keep the heading:

```markdown
# TODO
```

# Git Commit

Commit only when the user asks. Read recent git history first and follow the existing convention; otherwise use **Conventional Commits**:

```text
<type>(<scope>): <description>

- <module or theme>: <high-level summary>
- <module or theme>: <high-level summary>
```

- Keep the first line at 72 characters or fewer
- Use `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `style`, or `perf`
- Use an optional scope such as `skill`, `hooks`, or `plugin`
- Add body bullets when two or more modules or user-visible surfaces changed
- Keep bullets high-level and modular rather than listing every file edit
- Include quantified results when available

# Reference

## PLAN.md Interaction

Only read `PLAN.md`. Never generate or modify it.
Focus on the current phase, its goals, constraints, prerequisites, and progression. If it needs adjustment, remind the user to update it.

## Project Instruction Integration

Use project instructions already supplied by the current runtime for always-on rules such as writing changelog entries after changes and routing planning content to `PLAN.md`. Read the underlying instruction files only when the supplied context is missing or insufficient. This skill handles on-demand generation, status, resume, and phase flow.

# Important Rules

- `TODO.md` is an execution checklist, not documentation
- "continue", "keep going", and "next step" mean resume, not regenerate
- After all items are resolved, wait for user instructions and do not auto-clear
- Guide planning-level content toward `PLAN.md` first
- Smart git detection only suggests; never auto-mark without confirmation
- Track blocked and skipped items separately even though they count as resolved
- Write the changelog immediately when each item completes
- Keep durable state in project files; session mirrors are ephemeral
