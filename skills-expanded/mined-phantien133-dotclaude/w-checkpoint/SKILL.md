---
description: Create a standardized TDD checkpoint commit (RED or GREEN) during w-task Phase 4. Updates state.yaml with checkpoint timestamp.
argument-hint: RED|GREEN <task-slug>
allowed-tools: Bash, Read, Write, Edit
---

# w-checkpoint

Create a checkpoint commit marking the current TDD state.

**RED** — tests written and failing, implementation not started.  
**GREEN** — tests passing, refactor done.

`git diff RED..GREEN` shows the full implementation delta.

---

## Step 1 — Parse arguments

Format: `RED <task-slug>` or `GREEN <task-slug>`

Validate:
- First token must be `RED` or `GREEN` (case-insensitive, normalize to uppercase).
- Second token is the task slug.
- If either missing: say "Usage: `/w-checkpoint RED|GREEN <task-slug>`" and stop.

---

## Step 2 — Load config

```bash
cat .claude/workflow.yaml 2>/dev/null
```

Extract `workflow.state_root` → default `.workflow`.

---

## Step 3 — Check working tree

```bash
git status --short
```

If no changes (clean working tree): say "Nothing to commit — working tree is clean." Stop.

---

## Step 4 — Stage changes

Show the developer what will be staged:

```bash
git diff --stat HEAD
```

Ask:
```
Stage all changes for checkpoint? (y) or stage interactively? (i)
[y]:
```

- `y`: `git add -A`
- `i`: `git add -p` (interactive patch)

---

## Step 5 — Commit

```bash
git commit -m "chore(workflow): [RED] <task-slug> — tests written, impl pending"
# or
git commit -m "chore(workflow): [GREEN] <task-slug> — tests passing, refactor done"
```

Capture commit hash.

---

## Step 6 — Update state.yaml

```bash
cat <state_root>/<task-slug>/state.yaml
```

Append to the `notes` field (or add it):
- RED: `checkpoint_red: <hash> at <timestamp>`
- GREEN: `checkpoint_green: <hash> at <timestamp>`

Update `last_updated: <now>`.

---

## Step 7 — Output

```
Checkpoint [RED|GREEN] created: <short-hash>

  git diff <red-hash>..<green-hash>   — view full TDD delta (once both exist)
```

If both RED and GREEN checkpoints now exist in state.yaml, show the diff command.
