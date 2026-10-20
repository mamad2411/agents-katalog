# Phase: Complete

**Purpose**: Merge the PR, sync project aggregation files, run post-merge cleanup, and display completion summary.

**Entry conditions**: `current_phase: complete`

---

## Finalization Steps

### Step 1: Ask About Merge

```
COMPLETION

PR is approved. Options:
1. [merge] - Merge the PR now
2. [manual] - I'll merge manually

Your choice:
```

### Step 2: Merge (if selected)

- Merge PR: `gh pr merge [number] --squash`
- Update state: `phases.complete.merged_at: [timestamp]`
- Add history entry: `pr_merged`

### Step 3: Sync Project Aggregation Files

- **Invoke**: `/project:sync CLO-XX --complete "Summary of what was accomplished"`
- This automatically updates:
  - PROJECT.md: Moves task from "Active Work" to "Recently Completed"
  - ROADMAP.md: Changes task status to "Done", updates phase completion counts
  - DEPENDENCIES.md: Removes blocking relationships, adds newly unblocked tasks
- Update state: `phases.complete.aggregation_files_updated: true`
- Add history entry: `project_sync_complete`

### Step 4: Checkout Main

```bash
git checkout main
git pull origin main
```

### Step 5: Post-Merge Cleanup

- **Invoke**: `/pr:finalize CLO-XX`

### Step 6: Final State Update

- `phases.complete.status: complete`
- `workflow.current_phase: complete`
- `workflow.status: complete`
- Add history entry: `workflow_complete`

### Step 7: Display Completion Summary

Render the canonical summary defined in `.claude/templates/completion-summary.md`.

- Load `docs/status/clo-XX-workflow.yaml`.
- Resolve every placeholder using the field-mapping table in the template (`Source of Data` section).
- Apply the phase-skip rules for the current `task_type`.
- Print the rendered block exactly as specified — preserve box-drawing characters, indentation, emojis, and separator widths. Add no commentary above or below the bottom separator.

The footer line `Status: ✅ DONE` is the single authoritative completion signal — emit it only when `workflow.current_phase == complete` AND `workflow.status == complete`.

---

## YAML Checkpoint (Required before transition)

Before marking workflow complete, verify:
- `phases.complete.aggregation_files_updated: true`
- `phases.complete.merged_at` is set (non-null)
- History contains `pr_merged`, `project_sync_complete`, and `workflow_complete`
