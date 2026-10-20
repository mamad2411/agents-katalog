---
name: validate-update-push
description: Complete workflow to validate build, update documentation, update progress, and push changes. Use when finalizing work, before ending a session, or when the user says "finalize", "wrap up", or "ship it".
allowed-tools: Bash, Read, Write, Edit, Glob, Skill
user-invocable: true
disable-model-invocation: true
---

# Validate, Update & Push

Sequential workflow to validate, document, and push changes.

## Step 1: Validate

Run `/validate` to check available validations:
- Lint (if configured)
- Build (if configured)
- Tests (if configured)

The validate skill automatically detects which scripts are available in `package.json` and skips those that aren't configured.

**If validation fails:**
1. Report the error clearly
2. Ask: "Validation failed. Do you want me to fix this issue?"
3. Wait for user response
4. If user agrees, fix and re-run validation
5. If user declines, stop the workflow

## Step 2: Update Documentation

Run `/update-docs` to update:
- `CLAUDE.md` (if meaningful changes exist)
- `memory-bank/` files (except `brainstorm.md`)

If no updates needed, continue.

## Step 3: Update Progress (Conditional)

**Check if applicable:**
- Search for implementation plan (in priority order):
  1. `memory-bank/plan.md` or `memory-bank/*-implementation-plan.md`
  2. `*-implementation-plan.md` or `implementation-plan.md` (project root)
  3. `docs/*-implementation-plan.md`
- If NO plan exists, skip this step

**If plan exists:**
- Determine if work relates to a task in the plan
- If yes, run `/update-progress`
- If unrelated, skip

## Step 4: Git Add, Commit & Push

Run `/git-add-commit-push` to:
- Stage all changes
- Create commit with appropriate message
- Push to current branch

## Error Handling

At any step, if something unexpected happens:
1. Explain what went wrong
2. Ask the user how to proceed
3. Never force through errors silently

## Output

```
## Summary
- Validation: [Passed / Fixed N issues]
- Documentation: [Updated X files / No updates needed]
- Progress: [Updated / Skipped (no plan) / Skipped (unrelated work)]
- Git: [Committed and pushed / Skipped]
```
