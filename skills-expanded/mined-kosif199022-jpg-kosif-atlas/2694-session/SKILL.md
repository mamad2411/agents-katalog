---
name: session
description: Pick up and hand off work seamlessly across multiple agents, models, and CLI windows working on the same project. Use at session start ("what should I work on", "what's the state of this project", "resume work", "pick up where we left off", "session check-in"), mid-session ("checkpoint", "save where I am", "quick save", "save progress"), and at session end ("wrap up", "log what I did", "session check-out", "before I stop"). Reads the project's `.context/` store to orient, claims a task by routing rules, then on exit updates the board, appends a structured handoff entry, and commits. Works for any project — code, content, skill-authoring — that has a `.context/` directory at the repo root. If `.context/` is missing, offers to bootstrap it.
---

# Session — project continuity protocol

This skill runs the check-in / check-out ritual for projects with a `.context/`
store at the repo root. The store is the project's shared brain — every agent,
model, or CLI window reads it on entry and updates it on exit. The store is
the truth; open terminals are just doors into it.

## Gotchas (read first)

- **Treat every check-in as a stranger arriving.** Re-read STATE and recent
  LOG even if you (the same model) ran in this window earlier. Another agent
  may have worked between, and your private conversation history is invisible
  to other windows anyway.
- **The store is the only truth.** If a fact needs to survive into another
  session, it must be in `.context/`. Conversation history doesn't carry.
- **Lock is held for seconds, not the session.** Acquire just before mutating
  STATE or DECISIONS, release immediately after. A long-held lock blocks
  other agents.
- **Review against commits, never working trees.** When checking out a task
  as `Ready-for-Review`, you MUST have a commit SHA. Reviewers diff that SHA.
- **Multiple worktrees share ONE `.context/`.** It lives in the main repo and
  is symlinked into each worktree. Never create a parallel `.context/` in a
  worktree — you'd fork the brain.
- **Append-only files are append-only.** LOG.md and DECISIONS.md grow forever
  (with old LOG entries rolling to `archive/`). Never rewrite history there.
- **If `.context/` is missing, ask before bootstrapping.** Don't silently
  create it — it might mean you're in the wrong directory.

## When to invoke

- **Check-in** — start of any session ("what should I work on", "resume").
- **Checkpoint** — mid-session save without closing the task ("checkpoint",
  "save where I am", "quick save", "save progress").
- **Check-out** — end of any session ("wrap up", "save", "log this").
- **Status** — quick read of the board ("what's happening on this project")
  without claiming a task.
- **Bootstrap** — project has no `.context/` and Lou confirms creating one.

---

## Check-in flow

**1. Verify the store.** Confirm `.context/CHARTER.md` exists at the repo
root. If not, ask Lou whether to bootstrap. Do not proceed without a store.

**2. Check the lock.** Read `.context/lock` if it exists.
- Absent → proceed to step 3.
- Present, age <5min → another agent is mid-mutation. Wait 5–10s. Retry once.
  Still held → report to Lou and halt.
- Present, age >5min → presumed stale. Note this in your LOG entry at
  check-out. Proceed.

**3. Acquire the lock.** Write to `.context/lock`:

```json
{"agent": "<your-model-id>", "worktree": "<basename of pwd>", "started": "<ISO timestamp>"}
```

**4. Read context** in this order:
- `CHARTER.md` — full read on first ever encounter; skim on subsequent.
- `STATE.md` — full.
- `LOG.md` — top ~5 entries (newest first).
- `DECISIONS.md` — skim. Flag any `proposed-supersede` block awaiting
  ratification.

**5. Detect stale Doing tasks.** For each task in `Doing`, parse `started:`.
If >4h ago and not your own claim, add a line under "Needs Lou":

> *"T-`<N>` has been Doing for `<H>`h under `<agent>`@`<worktree>` — reclaim
> or reassign?"*

This catches crashed sessions before they block the queue.

**6. Select a task** in this priority order:

1. **Explicit assignee match.** Any Todo with `@<your-role>` → take the top one.
2. **Focus match.** Any Todo whose `#focus` matches your specialty → take the
   top one.
3. **User override.** If Lou's prompt explicitly names a task or scope, that
   wins.
4. **Else report idle.** Release the lock, tell Lou there's nothing matching
   your specialty in the queue, do not invent work.

**7. Mutate STATE.** Move the task from `Todo` to `Doing` and stamp it:

```markdown
- [~] T-014 <description> — @<your-role> #<focus>
      worker: <agent-id>@<worktree>
      started: <ISO timestamp>
```

Update the "Last updated" line at the top of STATE.md.

**8. Release the lock.** Delete `.context/lock`.

**9. Report to Lou** in 2–4 lines:
- Task taken (ID and one-line description).
- Current active objective from STATE.
- Any `Needs-Lou` items that surfaced.
- Any `proposed-supersede` decisions awaiting them.

**10. Begin work.** The protocol is done until check-out.

---

## Checkpoint flow

Run when Lou says "checkpoint", "save where I am", "quick save", or "save
progress" mid-session. Saves current state without closing the task.

**1. Acquire the lock.**

**2. Update the task's `Doing` entry in STATE** — replace or append a
`progress:` note summarising where things stand:

```markdown
- [~] T-014 <description> — @<role> #<focus>
      worker: <agent>@<worktree>
      started: <ISO>
      progress: <one line — what's done, what's next, any blocker>
```

**3. Append a checkpoint block to the TOP of LOG.md:**

```markdown
## <ISO date> · <agent-id> · checkpoint

**Task:** T-<N>
**Progress:** <what's been done so far>
**Next:** <exactly where to resume — file:line if applicable>
**Blockers:** <if any; else "none">

---
```

**4. Release the lock.**

**5. Commit `.context/`:**

```bash
git add .context/
git commit -m "context: <agent> checkpoint T-<N>"
```

**6. Confirm to Lou** in one line: "Checkpointed T-<N> — <progress summary>."

Do NOT change task status. Do NOT append to DECISIONS (checkpoints are
progress notes, not decisions). The task stays `Doing`; the session continues.

---

## Check-out flow

Run when the user signals wrap-up, when you hit a natural stopping point, or
when you're about to end the session for any reason.

**1. Commit code changes first** (separate from `.context/`). If you touched
source files, stage and commit them with a normal message. Note the SHA —
you'll need it if the task is `Ready-for-Review`.

**2. Determine task outcome:**

| Outcome | Status |
|---|---|
| Done and verified locally | `Done` |
| Done, needs another set of eyes | `Ready-for-Review` (requires commit SHA) |
| Started but not finished | leave in `Doing`, update note with where to resume |
| Discovered the approach was wrong | `Needs-Rework` with reason |

**3. Acquire the lock.** Same protocol as check-in step 3.

**4. Mutate STATE:**
- Move the task to its new status.
- If `Ready-for-Review`: append a paired review task to Todo:

  ```
  - [ ] T-<N>-R Review T-<N> @ <SHA> — #review
        parent: T-<N>
        commit: <SHA>
  ```

- Add `commit: <SHA>` to the moved task if applicable.
- Update the "Last updated" line.

**5. Append to LOG.md** at the top (newest first), using this template:

```markdown
## <ISO date> · <agent-id> · session

**Worked:** T-<N>
**Did:** <2–4 sentences of what happened>
**Changed:** <files/areas touched; include commit SHA>
**Learned:** <anything surprising; otherwise "nothing notable">
**Handoff / next:** <if mid-task: exactly where to resume, file:line; if done: what the next reasonable task is>
**Raised:** <any new DECISIONS, proposed-supersedes, or Needs-Lou items>

---
```

**6. Promotion prompt.** Before releasing the lock, ask yourself:

> *"Did this session produce any durable decision worth recording?"*

If yes, append to DECISIONS.md using this template:

```markdown
## D-<N> · <one-line decision> · <ISO date> · <agent-id> · accepted

**Context:** <what problem this answers>
**Decision:** <what we're doing>
**Why:** <1–3 reasons>
**Tradeoffs accepted:** <what we're giving up>
**Alternatives considered:** <other options weighed and why rejected>
```

If overturning a prior decision, use `proposed-supersede of D-<N>` in the
title and add a Needs-Lou line in STATE flagging the proposal.

**7. Release the lock.** Delete `.context/lock`.

**8. Commit `.context/`** as a separate commit:

```bash
git add .context/
git commit -m "context: <agent> check-out T-<N> <status>"
```

**9. Report to Lou** in 2–3 lines: what landed, where, any open questions.

---

## Status flow (no mutation)

When Lou just wants a read of the board:

1. Read STATE.md and top 3 LOG entries.
2. Report:
   - Current active objective.
   - What's Doing (and who, in which worktree).
   - Top of Todo.
   - Any `Needs-Lou` items or `proposed-supersede` decisions awaiting them.
3. Do **not** acquire the lock. Do **not** mutate anything.

---

## Reviewer discipline (#review tasks)

This is the discipline that protects against multi-model anchoring:

1. Read the **parent task's** definition in STATE first.
2. Run `git show <SHA>` to read the diff **blind** — do not read the doer's
   LOG entry yet.
3. Form findings using the template in CHARTER.
4. **Then** read the doer's LOG entry. If it changes your reading, note
   "anchoring check: shifted view on X after reading LOG" in your review.

Findings format (also in CHARTER, repeated here so the reviewer doesn't need
to context-switch):

```markdown
**Finding:** <one-line claim>
**Severity:** blocker | major | minor | nit
**Location:** <file:line or section>
**Evidence:** <what the code/text actually does>
**Suggested fix:** <if obvious; else "needs discussion">
```

Outcome:
- All findings minor/nit → mark T-`<N>` `Done`, T-`<N>-R` `Done`.
- Any major or blocker → mark T-`<N>` `Needs-Rework`, append findings to a
  new task T-`<N+1>` with `@<original-doer-role>`, mark T-`<N>-R` `Done`.

---

## Bootstrapping a fresh project

Only after Lou confirms. Then:

1. Create `.context/` with these files (copy from this skill's template, or
   from another project's `.context/`):
   - `CHARTER.md` — the protocol (copy verbatim, edit only the project name).
   - `STATE.md` — single Todo: "Define the active objective."
   - `LOG.md` — header only.
   - `DECISIONS.md` — single decision D-001 capturing why the store exists.
   - `archive/.gitkeep`
   - `README.md` — short pointer to CHARTER.
2. Add `.context/lock` to `.gitignore`.
3. Commit the scaffold.
4. Suggest Lou wire SessionStart and Stop hooks in `.claude/settings.json`
   (template in this skill's `assets/hooks.json` if present).

---

## Failure modes and how to handle them

- **Lock present and you can't tell if it's stale.** Read the timestamp; if
  >5min, break it and log the break in your LOG entry. If you can't parse
  it, ask Lou.
- **STATE.md has a merge conflict** (concurrent workdirs hit a race).
  Resolve by accepting both task moves — both agents did real work.
  Acknowledge the race in LOG.
- **You realize mid-session you're working on the wrong task.** At check-out,
  move the original task back to Todo with a note, create a new task for what
  you actually did, mark the new one `Done` (or `Ready-for-Review`).
- **You finish a task but can't commit (dirty unrelated changes).** Stash the
  unrelated changes, commit your task, restore the stash. Note the stash in
  LOG so Lou knows what's pending.

---

## Why this design (short)

- Markdown is agent-native — no parsers, no schema drift.
- Git provides versioning, attribution, and diff-as-explanation for free.
- One canonical source (STATE.md) means no inter-system drift.
- Append-only journals (LOG, DECISIONS) are conflict-free under concurrent
  appends.
- Short-held locks mean near-zero contention in practice.
- The check-in / check-out ritual makes continuity a property of the store,
  not of any agent's memory.

The full architecture and known limitations are in each project's
`.context/CHARTER.md`.
