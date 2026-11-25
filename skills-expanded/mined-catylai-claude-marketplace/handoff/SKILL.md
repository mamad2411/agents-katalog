---
name: handoff
description: "Writes a self-contained handoff document another engineer or a fresh session can resume from: the goal, branch and working-tree state, open threads anchored at file:line, the next step, and what was already tried and ruled out. Use at the end of a session, when handing work to someone else, when switching machines, or when the context window is running long. Not for summarizing a finished change for review (use your forge plugin's PR description), and not for executing the remaining work."
when_to_use: "hand this off, write a handoff, end of day summary, fresh session prompt, continue this tomorrow, context is getting long, pass this to someone else"
argument-hint: "[resume|fix] [optional focus note or issue key]"
allowed-tools: Read, Grep, Glob, Bash(git status *), Bash(git log *), Bash(git diff *), Bash(git rev-parse *), Bash(git worktree list *), Bash(date *), Edit(docs/handoffs/**)
license: MIT
---

# Handoff

Produce one document that a reader with none of this conversation's history can act on
immediately. Everything the next session needs goes in the document, because the context it
depends on is about to be lost.

Arguments: $ARGUMENTS

## Modes

- **`resume`** (default) — "here is where the work stands; continue it."
- **`fix`** — "here are the open problems; the next session should plan and execute the
  remediation." This session only writes the plan's starting point.

If the first word of the arguments is exactly `resume` or `fix`, it selects the mode. Everything
else is a focus note: free text, or an issue key like `PROJ-123`.

## Procedure

1. **Read the repository state.**
   - `git rev-parse --abbrev-ref HEAD` and `git worktree list` — branch, and the worktree path if
     this is not the primary checkout.
   - `git status -sb`, `git log --oneline -8`, `git diff --stat`, `git diff --cached --stat`.
   - Take an issue key from the branch name if the convention carries one; a key in the focus note
     wins.
2. **Recover the task context from this conversation** rather than re-deriving it from the
   repository:
   - the goal, stated as an outcome;
   - what was tried and ruled out, with why. This is the section a fresh session cannot
     reconstruct, and without it the first several turns go back down the same dead ends;
   - a file:line anchor for every open thread;
   - the current blocker and the single most useful next action.
3. **Issue tracker.** If one is in scope and a tracker tool is connected (for example through
   `issue-tracker-core`), fetch the issue's key, summary and status. If the lookup fails, write
   "tracker lookup failed — verify manually" rather than filling it in from memory.
4. **Re-check every anchor** against the current tree with Read or Grep. A line number that has
   moved is worse than a bare file name, because it is trusted and wrong.
5. **Write it.** Print the document in a fenced block, and save it to
   `docs/handoffs/<YYYY-MM-DD>-<branch>.md` (date from `date +%F`; replace `/` in the branch
   with `-`). A per-date, per-branch file keeps earlier handoffs instead of overwriting them. Tell
   the user the path, and that the new file shows as untracked in `git status`: they can commit it
   deliberately, or add `docs/handoffs/` to `.gitignore` to keep handoffs out of the repository.

**Outside a git repository:** skip the git steps, build the handoff from the conversation alone,
and state that repository state was unavailable.

**Without a checkout (Cowork/web):** print the document only; ask the user to paste `git status`
and recent commits if they want the state section filled.

## Template

```markdown
# Handoff — <repo> @ <branch> — <YYYY-MM-DD>

Mode: resume | fix

## Goal
<one paragraph: the outcome being pursued and why it matters>

## Current state
- Branch / worktree: <branch> (<worktree path, if not the primary checkout>)
- Issue: <KEY> <summary> — <status>     (omit if none)
- Working tree: <status summary, or "clean">
- Recent commits: <top three, one line each>

## Open threads
1. <what is unfinished> — `path/to/file.ext:LINE`

## Already tried and ruled out — skip these
- <approach> → <what happened, and why it is a dead end>

## Immediate next step
<the single most useful first action, specific enough to start on>

## Constraints
<repository rules that bear on this work: conventions, required checks, things to leave alone>
```

In `fix` mode the ruled-out section is required: a remediation plan without it spends the next
session's opening turns rediscovering it.

## Rules

- This skill writes only the handoff file. Code edits, commits, pushes and ticket transitions are
  the next session's job.
- Write for a stranger. Rewrite any sentence that only makes sense to someone who watched this
  session.

## Verify

Before finishing: every `path:LINE` in the document was re-read in step 4, the ruled-out section
is non-empty (or says "nothing ruled out yet"), and the saved file exists at the path you gave.
