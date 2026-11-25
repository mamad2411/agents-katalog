---
name: continue-work
description: >
  Resumes a stalled task by resetting its remediation loop counter and relaunching a
  `code` agent. A task becomes `stalled` when the code skill exhausts its loop budget
  (default 10 iterations) without satisfying all Definition of Done criteria. This skill
  shows the user the last failing criteria, lets them add optional guidance, resets the
  counter (with an optional new budget), and triggers a fresh implementation session.
  Optionally accepts `--max-loops N` to set a custom loop budget for the new session.

  Trigger on: "continue-work TASK-NNN", "/continue-work", "resume TASK-NNN",
  "retry TASK-NNN", "unblock TASK-NNN", "restart work on TASK-NNN",
  "reset loops for TASK-NNN", "give TASK-NNN more loops",
  or any request to resume a task that is in `stalled` status.
---

# Continue Work

Resume automated implementation for a task whose remediation loop budget was exhausted.
This skill resets the counters, optionally accepts new user guidance, and relaunches a
fresh `code` session with the full original context.

---

## Sentinel — acquire before writing TASK cards

A PreToolUse hook (`tasks-folder-guard.py`) rejects every Write/Edit/MultiEdit/
NotebookEdit call targeting `tasks/<CAP>/TASK-*.md` unless the shared
task-pipeline sentinel `/tmp/.claude-task-pipeline.active` is present and
≤30 min old. This skill is on the allowlist (together with `/task`,
`/task-refinement`, `/launch-task`, `/code`, `/fix`, and
`/pr-merge-watcher`). The `code` session this skill relaunches acquires
its own sentinel inside its session — `/continue-work` only needs the
sentinel for its own counter-reset edits.

Before the first TASK-card write (resetting `loop_count`, `stalled_reason`,
status):

```bash
touch /tmp/.claude-task-pipeline.active
```

At the very end (success or graceful abort):

```bash
rm -f /tmp/.claude-task-pipeline.active
```

A stale sentinel grants write access to the next agent — explicit `rm -f`
on exit is preferred. The hook treats sentinels older than 30 minutes as
expired.

---

## Usage

```
/continue-work TASK-NNN
/continue-work TASK-NNN --max-loops 15
/continue-work TASK-NNN --max-loops 20 "Look for #consent-gate not #gate-consentement"
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `TASK-NNN` | yes | — | Task identifier to resume |
| `--max-loops N` | no | same as previous `max_loops` | New loop budget for the session |
| `"guidance text"` | no | — | Optional hint injected into the remediation context |

---

## Step 1 — Locate and Validate the Task

1. Find the task file at `/tasks/{capability-id}/TASK-NNN-*.md`.
   If not found, scan all `tasks/*/` directories and report a list of stalled tasks.

2. Verify the task status is `stalled`:
   - If `status: done` → tell the user: "TASK-NNN is already done — nothing to resume."
   - If `status: in_progress` → tell the user: "TASK-NNN is already running."
   - If `status: in_review` → tell the user: "TASK-NNN is awaiting PR merge, not stalled."
   - If `status: todo` → tell the user: "TASK-NNN has not been started yet. Use `/code TASK-NNN`."

3. Read from the task frontmatter:
   - `loop_count`: number of loops used before stalling
   - `max_loops`: the budget that was exhausted
   - `stalled_reason`: multi-line failure summary written by the code skill

---

## Step 2 — Show the Stall Context

Present the situation clearly before asking the user to confirm:

```
⚫ TASK-[NNN] — [Title]
Capability: [ID] — [Zone]

Stalled after [loop_count] loop(s) / budget was [max_loops].

Last failing criteria:
  ❌ [Criterion 1]: [failure description from stalled_reason]
  ❌ [Criterion 2]: [failure description from stalled_reason]

Loop budget for new session: [new_max_loops]
  (pass --max-loops N to change — current default: [max_loops])

Optional guidance to inject into the first remediation prompt:
  [guidance if provided, or "(none — will retry with the same context)"]

Shall I reset and relaunch? [yes / no / --max-loops N "guidance"]
```

Wait for the user's confirmation (or adjustment) before proceeding.

---

## Step 3 — Reset the Loop Counters

Determine the new `max_loops` value:
- If `--max-loops N` was provided: use `N`
- Otherwise: reuse the previous `max_loops` value (not 10 — respect the setting already in the file)

Update the task file frontmatter:

```yaml
status: todo
loop_count: 0
max_loops: [new_max_loops]
# stalled_reason field: keep it for history but prefix with "# (resolved attempt):"
```

Write the updated frontmatter. Do not touch any other field (preserves `depends_on`,
`priority`, `pr_url` history, etc.).

---

## Step 4 — Notify the Board

Invoke `/sort-task` to refresh `/tasks/BOARD.md` and reflect the `todo` status
(→ will transition to `in_progress` once the code agent starts). `/launch-task`
will pick it up reactively when its Step 6 fires.

Report:
```
Board updated: TASK-[NNN] moved from ⚫ stalled → 🟢 ready.
```

---

## Step 5 — Relaunch via Code Skill

Invoke the `code` skill for TASK-NNN with the following additional context prepended:

```
── CONTINUE-WORK CONTEXT ──
This task was previously stalled after [loop_count] remediation loop(s).

Stall reason (last failing criteria):
[stalled_reason content]

[IF guidance provided]:
User guidance for this session:
"[guidance text]"

New loop budget: [new_max_loops] iterations.
Loop counter has been reset to 0.
── END CONTINUE-WORK CONTEXT ──
```

The code skill will:
- Read the updated `loop_count: 0` / `max_loops: [new_max_loops]` from the frontmatter
- Detect the zone and route to the correct implementation path
- Skip the initial implementation step if artifacts already exist and only re-run tests +
  remediation (the code skill handles this via the Stall Procedure check in Step 3)
- Run the matching test skill — `/test-business-capability` for non-CHANNEL tasks (test-business-capability agent) or `/test-app` for CHANNEL tasks (test-app agent) — and loop up to `new_max_loops` times

Say:
> "Relaunching code skill for TASK-[NNN] with [new_max_loops] loop(s) available..."

---

## Step 6 — Report

After the code skill completes (pass or new stall):

**If all tests pass:**
```
✅ TASK-[NNN] resumed and completed.
All DoD criteria validated after [loop_count] additional loop(s).
PR: [PR_URL]
```

**If the budget is exhausted again:**
```
⚫ TASK-[NNN] stalled again after [new_loop_count] additional loop(s).

Failing criteria (new run):
  ❌ [Criterion 1]
  ❌ [Criterion 2]

Suggestions:
  - Increase the budget: /continue-work TASK-NNN --max-loops [N+10]
  - Add targeted guidance: /continue-work TASK-NNN "specific hint about the failure"
  - Review the FUNC ADR or task definition — the criterion may be ambiguous
  - Run /task-refinement TASK-NNN to clarify the acceptance criteria before retrying
```

---

## Skill Boundaries

- This skill **only** resumes `stalled` tasks — it does not modify design decisions or task
  definitions. To change what a task must produce, use `/task-refinement TASK-NNN` first.
- The `stalled_reason` written by the code skill is preserved in the file for traceability.
  Each new `/continue-work` run annotates it with `# (resolved attempt N):` prefix rather
  than deleting it.
- This skill does not create new branches — it resumes work on the existing
  `feat/TASK-NNN-{slug}` branch where the previous implementation left off.
