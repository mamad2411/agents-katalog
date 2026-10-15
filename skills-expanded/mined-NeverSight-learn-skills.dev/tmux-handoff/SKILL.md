---
name: tmux-handoff
description: Spins up a parallel Claude Code session in a new tmux pane or window, with its own git worktree and a focused handoff document as context.
disable-model-invocation: true
---

# tmux-handoff

Spin up a new tmux pane or window with a fresh git worktree and a Claude Code session, carrying just enough context for the next agent to hit the ground running — no more.

## Terminology

- **Source worktree** — where this skill is running (the user's current directory)
- **Destination worktree** — the new git worktree created by `claude -w`
- **Source pane** — the tmux pane where the user invoked this skill
- **Destination pane** — the new tmux pane or window this skill opens

---

## Step 1: Parse the prompt

**Focus** — what the next session will work on. Everything else is filtered through this lens.

**Target ref** — branch or commit to base the worktree on. Look for "from master", "against main", "based on develop", "off feature-x". Default: none (use whatever `claude -w` defaults to).

**Branch name** — use an explicit name if provided (e.g. `feat/quick-fix`). Otherwise slugify the focus: lowercase, spaces/special chars → hyphens, trim to ~40 chars.

**Files to move** — files mentioned with "move X", "move file X", "take X with me".

**Destination type** — vertical pane split by default. New window if the user says "new window" or "new tab".

**Skill base dir** — the directory this skill was loaded from (shown at the top of the skill invocation). You need this to locate `scripts/set-base.sh`.

---

## Step 2: Verify prerequisites

```bash
echo $TMUX                       # empty → stop, skill requires tmux
git rev-parse --show-toplevel    # not a repo → stop
```

Store the repo root.

---

## Step 3: Write the handoff document

Write this before opening the new pane — you have full session context now.

The handoff doc lives in the source worktree to avoid temp directory permission issues:

```bash
HANDOFF_PATH="<repo-root>/.claude/handoff.md"
```

First check it doesn't already exist — a leftover file means a previous handoff didn't clean up:

```bash
[ -f "$HANDOFF_PATH" ] && echo "ERROR: $HANDOFF_PATH already exists. Remove it before running a new handoff." && exit 1
```

Read the file before writing (it will not exist at this point — this is just the required pattern).

Structure:

```markdown
# Handoff: <focus>

## Context
<why this session was spun up and what it is starting from — purely informational>

## Files moved
<files that were copied into this worktree, with their paths relative to the worktree root>

## Background
<only what's directly relevant and not discoverable from git log or the files themselves>

## Artifacts
<references by path or URL — no content duplication>

## Suggested skills
<any skills the next session should use, with a brief reason>
```

Omit sections with nothing in them. Keep it under ~25 lines.

**Important:** the handoff doc is orientation, not a task list. Do not tell the next session to commit, push, open a PR, or take any specific action. State what exists and why — let the next Claude decide what to do from there.

---

## Step 4: Open the destination pane or window

**Pane (default):**
```bash
tmux split-window -h
DEST_PANE=$(tmux display-message -p "#{pane_id}")
```

**Window:**
```bash
tmux new-window
DEST_PANE=$(tmux display-message -p "#{pane_id}")
```

---

## Step 5: Launch Claude with `-w` in the destination

```bash
tmux send-keys -t $DEST_PANE "claude -w <branch-name>" Enter
```

Nothing else on this line — `claude -w` takes only the branch name.

---

## Step 6: Reset the worktree base and move files

Poll for the worktree to appear, then handle the base reset and file moves from the source — no Claude prompts needed for either:

```bash
WORKTREE="<repo-root>/.claude/worktrees/<branch-name>"
until [ -d "$WORKTREE" ] || [ $SECONDS -gt 30 ]; do sleep 0.5; done
[ ! -d "$WORKTREE" ] && echo "ERROR: worktree never appeared" && exit 1
```

**If a target ref was specified**, reset the worktree to it:
```bash
<skill-base-dir>/scripts/set-base.sh <target-ref> "$WORKTREE"
```

**Then move any files:**

For each file to move:

1. Copy `<source-worktree>/<relative-path>` → `<worktree>/<relative-path>` (create intermediate dirs as needed).
2. In the source worktree:
   - Tracked by git (`git ls-files --error-unmatch <file>` succeeds): `git checkout HEAD -- <file>` to restore committed state.
   - Untracked: `rm <file>`.

If a file doesn't exist in the source, warn and skip it.

---

## Step 8: Deliver the handoff document

Copy the doc from the source worktree into the destination and tell Claude where to find it:

```bash
mkdir -p "$WORKTREE/.claude"
cp "$HANDOFF_PATH" "$WORKTREE/.claude/handoff.md"

tmux send-keys -t $DEST_PANE "Read .claude/handoff.md for context about this session." Enter
```

---

## Step 9: Clean up the source handoff doc

Remove the handoff doc from the source worktree now that it has been copied to the destination:

```bash
rm "$HANDOFF_PATH"
```

---

## Step 10: Report back in the source pane

```
Handoff complete
  Branch:      <branch-name>
  Based on:    <target-ref or "claude -w default">
  Layout:      <pane or window>
  Files moved: <list or "none">
  Handoff doc: .claude/worktrees/<branch-name>/.claude/handoff.md
```

---

## Error handling

- **Not in tmux**: stop immediately with a clear message.
- **Not in a git repo**: stop immediately with a clear message.
- **Handoff doc already exists**: stop and tell the user to remove `.claude/handoff.md` first.
- **File to move not found**: warn and skip; list skipped files in the report.
- **`git checkout HEAD -- <file>` fails**: fall back to deleting the file from source.
- **Worktree never appears** (timeout ~30s): stop and tell the user `claude -w` may have failed.

