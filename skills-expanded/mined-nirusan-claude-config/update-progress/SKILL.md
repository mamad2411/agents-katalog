---
name: update-progress
description: Update progress tracking files (progress.md and implementation plan). Use after completing tasks, implementing features, or when the user wants to record progress.
triggers:
  - "/update-progress"
  - "update progress"
  - "mettre à jour le progrès"
  - "mettre à jour l'avancement"
  - "maj progrès"
allowed-tools: Read, Edit, Write, Glob, Bash
user-invocable: true
args:
  - name: feature
    description: Feature name to update (updates memory-bank/features/{name}/progress.md)
    required: false
disable-model-invocation: true
---

# Update Progress Files

Keep tracking files synchronized with completed work.

## Step 0: Determine Context

1. **Check for --feature parameter**:
   - If `--feature=X` provided, set `feature_name = X`
   - Otherwise, check if `memory-bank/features/` exists

2. **If features exist and no param specified**:
   - Check recent git changes to infer which feature was worked on
   - Or ask: "Which feature did you work on? (or 'main' for the main project)"

3. **Set paths based on context**:
   ```
   If feature_name and feature_name != 'main':
     plan_file = memory-bank/features/{feature_name}/plan.md
     progress_file = memory-bank/features/{feature_name}/progress.md
   Else:
     plan_file = memory-bank/plan.md
     progress_file = memory-bank/progress.md (or progress.txt)
   ```

## Step 1: Find Files

Search for the plan and progress files at the determined paths.

Fallback search (in priority order):
- Plan:
  1. `memory-bank/*-implementation-plan.md` or `memory-bank/implementation-plan.md`
  2. `*-implementation-plan.md` or `implementation-plan.md` (project root)
  3. `docs/*-implementation-plan.md` or `docs/implementation-plan.md`
  4. First `**/*implementation-plan*.md` found elsewhere
- Progress:
  1. `progress.txt`, `progress.md`, `PROGRESS.md` (project root)
  2. `memory-bank/progress.txt`, `memory-bank/progress.md`

**If multiple matches**: Ask the user which file to use.

If no implementation plan exists, skip plan updates and only update progress.

## Step 2: Read Current Files

Read:
- The implementation plan file (if found)
- The progress file

## Step 3: Analyze Recent Changes

If no description provided, analyze:
```bash
git diff HEAD~1 --name-only
git log -1 --oneline
```

Identify:
- What files were changed
- What was implemented
- Which story this corresponds to (match against plan)

## Step 4: Update progress.md

Follow this format:

```markdown
# Progress: {Feature/Product Name}

## Status: In Progress

## Current Story
Story {N}: {title}

## Completed
- [x] Story 1: {title} (2025-01-20)
- [x] Story 2: {title} (2025-01-20)

## In Progress
- [ ] Story 3: {title}

## Remaining
- [ ] Story 4: {title}
- [ ] Story 5: {title}

## Notes
- {date}: {observation or decision made}
```

**Update rules**:
- Move completed stories from "Remaining" → "Completed" with date
- Add `(date)` suffix to completed items
- Update "Current Story" to reflect what's being worked on
- Add notes for important decisions or blockers

## Step 5: Update Implementation Plan (if exists)

Update checkbox status in `{plan_file}`:
- `- [ ]` to `- [x]` for completed **implementation** tasks
- Keep `- [ ]` for **validation** tasks (require manual testing)

**Important distinction**:
- **Implementation tasks** = Code exists → Can be checked
- **Validation tasks** = Requires human testing → Stay unchecked

## Step 6: Confirmation

Output:
```
## Progress Updated

### Context
- Feature: {feature_name or 'main'}

### Progress file
- Updated: {progress_file}
- Completed: Story {N} - {title}
- Next: Story {M} - {title}

### Implementation plan
- File: {plan_file or "Not found - skipped"}
- Tasks checked: {X items}
- Still pending: {Y items}

### Summary
{X}/{Y} stories complete for {feature_name or 'main project'}
```

## Feature Flag Examples

```bash
/update-progress                          # Asks which feature or infers from git
/update-progress --feature=dark-mode      # Updates dark-mode progress
/update-progress --feature=main           # Updates main project progress
```

## Auto-Detection

When no feature is specified, try to auto-detect:
1. Check `git diff --name-only` for paths containing `features/{name}/`
2. Check recent file modifications in `memory-bank/features/`
3. If unclear, ask the user
