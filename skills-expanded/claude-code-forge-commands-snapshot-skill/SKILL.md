---
description: Session snapshot / reset handoff -- write a structured state file, then either (compact mode, default) present a compact message for /compact, or (clear mode) refresh the memory resume pointer, commit, and hand off to /clear + /orient. Trigger on "snapshot", "save state", "freeze session", "bank and reset", "prep for reset", or "snapshot clear/compact".
user-invocable: true
---

**MANDATORY FIRST OUTPUT -- say this before doing anything else, before any tool calls:**

> **Running /snapshot...**
>
> *Committing session state to disk before the reset.*

# /snapshot -- Session State Capture & Reset Handoff

Writes a structured `session-state.md` to the memory folder, then closes the loop for one of two reset paths. The state file persists on disk regardless of what happens to the live context -- it's the bridge across the gap.

## Step 0: Determine Mode

Two reset paths, two modes. Pick from the invocation; if ambiguous, ask which.

- **`compact` (default)** -- belt-and-suspenders before `/compact`. Live context gets summarized, not discarded; the state file backstops the summary if it loses detail. Ends by handing off to `/compact`.
- **`clear`** -- bank for a *fresh session*. Live context will be discarded by `/clear` and rebuilt by `/orient` from disk, so the state file isn't a backup -- it's the *only* bridge. Ends by refreshing the resume pointer, committing, and handing off to `/clear` + `/orient`.

Triggers: "snapshot clear" / "bank and reset" / "prep for reset" -> clear mode. Plain "snapshot" / "save state" -> compact mode.

**When to prefer clear mode.** At a work-stream boundary -- after committing a distinct piece of work when the next task is unrelated -- prefer `clear` over `compact`. A fresh session re-orienting from disk tends to be more reliable than a compacted summary carrying stale, topic-mismatched context forward. Reserve `compact` for the middle of a phase, when live working context (an in-flight investigation, an unbanked decision trail) genuinely needs to survive and re-orienting from scratch would cost more than the summary risks.

## Step 1: Detect Memory Folder

- **Home/root session:** write to the home project's memory folder, e.g. `~/.claude/projects/<home-key>/memory/session-state.md`
- **Project session** (a specific project directory): find that project's memory folder under `~/.claude/projects/` and write `session-state.md` there (project-key format: drive letter lowercased + path with separators replaced by dashes, e.g. `e--myproject` for `E:\MyProject`)

## Step 2: Gather State

Collect the following from the current session. Do not re-read files -- use what is already in context.

```yaml
state_fields:
  - id: identity
    content: "Session type (home / project / exploration) and current role"
  - id: completed
    content: "Work completed this session with commit hashes. Be specific -- file names, not categories."
  - id: approaches_tried
    content: "What was attempted this session and current status (worked / pending / partial). 1-3 bullets, terse."
  - id: approaches_abandoned
    content: "Dead ends with one-line reason each. 'None' if clean."
  - id: next_task
    content: "Current or next task with enough detail to resume without re-reading everything"
  - id: decisions
    content: "Active decisions, pending questions, unresolved issues. Omit if none."
  - id: key_files
    content: "File paths relevant to the current work, in first-to-last reading order for the resuming session."
  - id: repo_state
    content: "Clean or dirty. If dirty, which files are modified and why. If current dirty state isn't already known from session context, run `git status` once to capture it -- this is an exception to the 'do not re-read files' rule because the snapshot is worthless without accurate repo state. If genuinely uncertain, write 'dirty -- last known state before snapshot' rather than guess."
```

## Step 3: Write State File

Write `session-state.md` with this format (use the actual current date from the system/environment, not a date recalled from earlier in a long-running session):

```markdown
# Session State -- YYYY-MM-DD

## Identity
[Session type and role]

## Completed
- [Work item with commit hash]

## Approaches Tried
- [What was attempted -- worked / pending / partial]

## Approaches Abandoned
- [Dead end -- one-line reason]  ("None" if clean)

## Next Task
[What to do next, with enough context to start immediately]

## Open Issues
[Decisions, questions, blockers. "None" if clean.]

## Key Files
(In first-to-last reading order for the resuming session)
- [path] -- [why it matters right now]

## Repo State
[Clean/dirty, modified files, reason]
```

### Rules
- Overwrite the previous `session-state.md`. This is current state, not a log.
- Be terse. This is a handoff brief, not a narrative. Each field 1-3 lines.
- Commit hashes are mandatory for completed work. If work is uncommitted, say so.
- The **next task** field is the most important. A fresh instance should read it and start working. In clear mode it IS the bridge -- `/orient` reads this file back.

## Step 4: Close (mode-specific)

### compact mode
1. Present the compact message (identity, completed + hashes, current/next task, active decisions, key files, repo state).
2. Tell the user: **"State file written. Run `/compact` when ready."**
3. Do NOT trigger compaction yourself. The operator decides when.

### clear mode
1. **Refresh the resume pointer** the fresh session's `/orient` will surface -- a short "next up" line for this work stream in the project's top-level memory index. Point it at the current next-task. If no such pointer convention exists yet in this project, don't manufacture one -- `session-state.md` plus `/orient`'s read of it is the primary mechanism; a pointer line is secondary polish.
2. **Commit** `session-state.md` and any pointer change, with a lean message.
3. Present a terse handoff: identity, what's banked, next task, key files, repo state, commit hash.
4. Close: **"State banked, pointer refreshed, committed `<hash>`. Run `/clear`, then `/orient` in the fresh session -- it will pull the resume state."**
5. Do NOT trigger `/clear` yourself. The operator runs the reset keystrokes.

## When to Offer

If you're at a natural work-stream boundary -- you just committed a distinct piece of work and the next task is unrelated -- it's worth *offering* `/snapshot clear` rather than waiting to be asked. Offer once, phrased as a question ("we're at a boundary -- want to bank and reset?"); the operator decides. Never auto-clear. Natural offer points: right after a wrap-style command finishes, or any time a committed stream gives way to an unrelated one.
