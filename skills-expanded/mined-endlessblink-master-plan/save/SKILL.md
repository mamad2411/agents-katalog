---
name: save
description: Save work-in-progress and push to remote. Like /done but keeps task IN PROGRESS. Use when switching machines, ending a session, or backing up work. Triggers on "/save", "save progress", "switch machine", "end session".
---

# Save Progress

Save work-in-progress and push to remote repository. Unlike `/master-plan:done`, this keeps the task status as IN PROGRESS — perfect for:
- Switching machines
- End of session but task not complete
- Before restarting your computer
- Backing up current work

## Triggers

- `/master-plan:save` - Main command
- "save progress", "switch machine", "end session", "backup work"

## Workflow

### Step 1: Show Current State

Run these commands to show what changed:

```bash
git status
git diff --stat
```

Display a summary of modified files to the user.

### Step 2: Get Task Information

Use `AskUserQuestion` to gather:

1. **Task ID** (header: "Task")
   - Options: "Tracked task (enter ID)", "No task (just commit)"

2. **Update MASTER_PLAN?** (header: "Docs")
   - Options: "No (just commit)", "Yes (add progress note)"

Then ask in plain text: "What's a brief summary of the progress? (1-2 sentences)"

**IMPORTANT**: Wait for user to provide the summary before proceeding.

### Step 3: Update MASTER_PLAN.md (if requested)

If the user wants to add progress notes:
1. Find the task's `###` section in MASTER_PLAN.md
2. Add a progress note with timestamp

Format:
```markdown
**Progress (YYYY-MM-DD):** [summary of what was done]
```

**Keep status as IN PROGRESS** — do NOT change to DONE.

### Step 4: Stage Files

Stage all changed files EXCEPT:
- `.env*` files (secrets)
- `node_modules/`, `__pycache__/`, `target/`, `.venv/`
- Backup directories
- OS files (`.DS_Store`, `Thumbs.db`)

Prefer staging specific files by name over `git add -A`.

### Step 5: Commit

Create a WIP commit:

**With task ID:**
```bash
git commit -m "$(cat <<'EOF'
wip(TASK-XXX): progress summary

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Without task ID:**
```bash
git commit -m "$(cat <<'EOF'
wip: progress summary

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Push to Remote

```bash
git push
```

### Step 7: Output Summary

```
## Progress Saved

- **Task**: TASK-XXX (or "No task")
- **Summary**: [what was done]
- **Commit**: [short hash]
- **Status**: Still IN PROGRESS

Ready to continue on another machine:
1. `git pull`
2. Continue working on TASK-XXX
```

## Difference from /done

| Aspect | `/master-plan:done` | `/master-plan:save` |
|--------|---------------------|---------------------|
| Task Status | ✅ DONE | 🔄 IN PROGRESS (unchanged) |
| Commit prefix | `feat(TASK-XXX):` | `wip(TASK-XXX):` |
| Tests required | Yes | No (skip for speed) |
| MASTER_PLAN update | Mark complete | Add progress note only |
| Use case | Task finished | Session end, machine switch |

## Important Rules

1. **Do NOT mark task as DONE** — The whole point is to save progress without claiming completion
2. **Do NOT run tests** — Speed is the priority for session-end saves
3. **Always push** — The goal is to make work available on another machine
4. **Ask before MASTER_PLAN changes** — Some users may just want to commit/push
