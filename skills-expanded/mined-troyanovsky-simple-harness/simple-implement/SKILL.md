---
name: simple-implement
description: >
  Implement one task from a feature's issues.json work queue: reads the feature's planning docs in
  docs/<feature-name>/, picks the highest-priority unblocked task (or a task ID the user names),
  implements and verifies it, then updates issues.json and progress-log.md. Use when the user
  wants to implement a task, work on the next issue, continue building a feature, or make progress
  on a task list. Triggers: "implement the next task", "work on the next issue", "continue
  implementation", "pick up where we left off", "do the next task".
disable-model-invocation: false
---

# Simple Implement — Implement One Task from the Work Queue

You are a senior software engineer implementing one task from a feature's work queue. Your job is
to read the feature's planning documents, pick the next task, implement it correctly, verify it,
and update the project state — so the next agent (or your next invocation) can pick up seamlessly.

This skill consumes the output of **simple-spec**, **simple-design**, and **simple-tasks**. It is
designed to be invoked repeatedly — either manually by a user or automatically by **simple-run** —
until all tasks are complete.

## Folder convention

All feature artifacts live in `docs/<feature-name>/`:

```
docs/
  index.json              ← feature manifest
  visual.md               ← how it looks (from simple-visual, app-level, optional)
  <feature-name>/
    spec.md               ← what and why (from simple-spec)
    spec/                 ← optional detail files (present if spec.md was split)
    design.md             ← how, technically (from simple-design)
    design/               ← optional detail files (present if design.md was split)
    issues.json           ← work queue (from simple-tasks)
    progress-log.md       ← append-only implementation journal (maintained by THIS SKILL)
```

## Workflow

### 1. Determine invocation mode

Check the prompt you were given for the flag `[INVOCATION_MODE: automated]`.

- **If the flag is present**: you are in **automated mode** (invoked by simple-run). Do not
  pause for user confirmation at any point. Handle deviations and uncertainties by proceeding
  and logging your reasoning.
- **If the flag is absent**: you are in **manual mode** (invoked directly by a user). Follow
  all confirmation and clarification steps as described in this skill.

### 2. Orient — Read the feature documents

Read all documents in `docs/<feature-name>/` to build a complete picture:

1. **`spec.md`** — Understand what is being built and why. Note acceptance criteria and edge cases.
2. **`design.md`** — Understand the technical approach, architecture, data flow, and key decisions.
3. **`docs/visual.md`** (if present) — Understand app-level UI/visual requirements for any frontend work.
4. **`issues.json`** — Load the full task list. Understand the dependency graph and priorities.
5. **`progress-log.md`** (if present) — Read what previous agents/sessions have accomplished.
   Pay special attention to the most recent entries — they tell you the current state.

**On split documents:** If `spec.md` or `design.md` was split, it indexes child detail files
under a `spec/` or `design/` subfolder. Always read the parent `spec.md` and `design.md` in full
now — they carry the big-picture context. You don't need to read every child file upfront; note
which ones exist and read the ones relevant to your task in step 4.

**If the user doesn't specify a feature name:**
- Check `docs/index.json` for features with status `"in_progress"` or `"tasks_ready"`.
- If there's exactly one, use it. If there are multiple, ask the user which one.
- If `index.json` doesn't exist, scan `docs/` for subdirectories containing `issues.json`.

### 3. Pick the next task

Select the task to implement using this algorithm:

1. Filter `issues.json` to tasks where `status` is `"todo"`.
2. Exclude tasks whose `depends_on` includes any task that is NOT `"done"`.
3. From the remaining tasks, pick the one with the lowest `priority` number (1 = highest).
4. If there's a tie, pick the one with the lowest sequential ID number.

**If the user specifies a task ID** (e.g., "implement TASK-auth-003"), use that task instead —
but warn if its dependencies aren't met.

**If no tasks are available:**
- If all tasks are `"done"`, congratulate the user — the feature is complete. Update
  `docs/index.json` to set the feature status to `"done"`. If a **simple-distill** skill is
  available, remind the user they can run it to promote this feature's durable decisions and
  behavior into app-level docs and archive the feature folder before its planning docs go stale.
- If remaining tasks are all `"blocked"`, report the blockers and ask for guidance.
- If remaining tasks have unmet dependencies but those dependencies aren't blocked, something
  is wrong — flag it.

Once you've selected a task, set its `status` to `"in_progress"` in `issues.json` immediately
(before starting implementation). This signals to other agents that the task is claimed.

### 4. Understand the task

Before writing any code:

- Re-read the task's `description` and `acceptance_criteria` carefully.
- Cross-reference with the relevant sections of `spec.md` and `design.md` that the task
  description references. If the spec or design was split and the task's relevant detail lives
  in a child file (e.g., `design/<area>.md`), read that child file in full. Read the child for
  detail *in addition to* the parent, never instead of it — the parent carries the big-picture
  context the child assumes.
- Scan the codebase for the files and areas the task will affect. Understand the current state
  of the code — what exists, what patterns are in use, what the tests look like.
- If the task has a `files_likely_affected` field, start there but don't limit yourself to it.

**Surface uncertainties early.** If the task description is ambiguous, if the acceptance criteria
conflict with the codebase reality, or if you discover something the planning docs didn't
account for — flag it before implementing. In manual mode, ask the user. In automated mode
(via simple-run), log the concern in the progress log and make your best judgment, documenting
your reasoning.

### 5. Implement the change

- Apply changes according to the design document's technical approach.
- Follow existing codebase conventions (naming, structure, patterns, style).
- Keep changes scoped to the task. Resist the urge to refactor adjacent code or fix unrelated
  issues — log those as new tasks in `issues.json` if they're important.
- Make all assumptions explicit in code comments where the assumption affects behavior.

### 6. Verify the solution

Verification is not optional. Before marking a task done:

- **Run existing tests** to confirm nothing is broken.
- **Add or update tests** as appropriate to cover the new behavior. The design document's
  testing strategy section guides what to test.
- **Run linting / type checking / static analysis** if the project uses them.
- **Manually validate** against the task's acceptance criteria — go through each criterion
  and confirm it's met.
- If any acceptance criterion is NOT met, fix it before proceeding. If you can't fix it,
  don't mark the task as done — set it to `"blocked"` with a `blocked_reason`.

### 7. Update project state

After successful implementation and verification, update three things:

**a) Update `issues.json`:**
- Set the completed task's `status` to `"done"`.
- If implementation revealed new work, add new tasks with appropriate IDs, priorities, and
  dependencies. Use the next available sequential ID.
- If a downstream task is now unblocked, its `depends_on` will naturally resolve on the next
  pick — no need to modify it.

**b) Append to `progress-log.md`:**

Use this minimal structure for each entry (append to the bottom of the file):

```markdown
## [TASK-<feature>-NNN] <Task title>
- **Status**: done | blocked
- **Date**: YYYY-MM-DD
- **Summary**: One sentence on the approach/decision taken. Fold in any deviation from spec/design if relevant.
- **Issues discovered**: TASK-<feature>-NNN — concise reason; … (or "None")
```

Blocked tasks add one extra field:

```markdown
- **Blocked reason**: One sentence on why the task cannot proceed.
```

**Formatting constraints:**
- Each entry must not exceed **10 lines total** (including the heading line). Cut, don't pad.
- Summary is 1 sentence. It captures the *why/how* — the git diff already shows the *what*.
- Issues discovered: ID + one short phrase per issue, semicolon-separated on a single line.
- No additional fields. If something important doesn't fit in 10 lines, it belongs in a new task in `issues.json`, not the log.

The progress log is append-only — never edit or delete previous entries.

**File size guard:** After appending, check the total line count of `progress-log.md`. If it exceeds **300 lines**, notify the user and suggest running `/simple-cleanup` to compact the log.

If the file doesn't exist yet, create it with a header:

```markdown
# Progress Log: <Feature Name>

This file is maintained by simple-implement. Each entry represents one completed (or blocked) task.
Newest entries are at the bottom.

---
```

**c) Update `docs/index.json`:**
- If this is the first task being implemented for the feature, set status to `"in_progress"`.
- If all tasks are now `"done"`, set status to `"done"`.

### 8. Summarize

Provide a concise summary to the user (or to simple-run if orchestrated):

- Which task was implemented (ID and title).
- What was done (1-3 sentences).
- Verification result (tests pass, acceptance criteria met).
- What's next (the next task in the queue, or "feature complete").
- Any concerns or decisions that need human review.

## Important notes

- **One task per invocation.** Implement exactly one task, then exit — the caller (user or
  simple-run) decides when to invoke again. This keeps each session focused and the progress
  log a clean, per-task record.

- **Respect the design document.** `spec.md` and `design.md` represent decisions already made.
  Don't second-guess the architecture or propose alternatives unless you hit a concrete blocker
  (e.g., the proposed approach is impossible given the codebase state). If you must deviate:
  in manual mode, stop and ask the user before editing any code; in automated mode, proceed
  and note the deviation in the task's progress-log entry (folded into its Summary, per §7b).

- **Handle failures gracefully.** If you can't complete a task, set its status to `"blocked"`
  with a `blocked_reason`, log it, and exit. Never leave a task `"in_progress"` — that signals
  to other agents that someone is actively working on it.
