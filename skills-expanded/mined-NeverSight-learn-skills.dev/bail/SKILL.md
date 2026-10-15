---
name: bail
description: Reflects, updates GitHub Issue, closes PR if open, cleans up worktree/branch.
---

Bail-out protocol: always reflect FIRST, then clean up.

## Inputs
- Optional reason string (if not provided, ask for one)

## Steps

1. **Detect current step** by examining what exists:
   | What exists | Estimated step |
   |------------|---------------|
   | Just an issue, no branch | Step 0 (Capture) |
   | .branch-context.md, no worktree | Step 1 (Orient) |
   | Worktree exists, no code changes | Step 2 (Isolate) |
   | Plan file on branch | Step 3-4 (Design/Review) |
   | Code changes committed | Step 5-7 (Build/Verify/Archive) |
   | PR open on GitHub | Step 8 (Ship) |

2. **Prompt for reason** if not provided.

3. **Write learnings to .branch-context.md**:
   - What was attempted
   - Why bailing (the reason)
   - What was learned
   - Any partial work worth preserving

4. **Consolidate learnings**: Read `.branch-context.md` and append relevant items to `ai-workspace/MEMORY.md` on main:
   ```bash
   git stash
   git checkout main
   # Append learnings to MEMORY.md
   git add ai-workspace/MEMORY.md
   git commit -m "docs: consolidate learnings from abandoned <branch>"
   git checkout <branch>
   git stash pop
   ```

5. **Update GitHub Issue** (if accessible):
   ```bash
   # Find issue number from branch name or PR
   gh issue comment <number> --body "Bailing: <reason>. Learnings captured in MEMORY.md."
   gh issue edit <number> --add-label "deferred" --remove-label "triage"
   ```

6. **Close PR if open**:
   ```bash
   PR_NUM=$(gh pr list --head "<branch>" --json number -q '.[0].number')
   if [ -n "$PR_NUM" ]; then
     gh pr close "$PR_NUM"
   fi
   ```

7. **Ask about branch preservation**:
   - Default: preserve the branch (user can resume later)
   - If user says delete:
     ```bash
     git worktree remove .worktrees/<name> 2>/dev/null
     git branch -D <branch> 2>/dev/null
     git push origin --delete <branch> 2>/dev/null
     ```

8. **Return to main**:
   ```bash
   git checkout main
   ```

## Edge Cases
- No worktree exists (bailing at Step 0-1) → skip worktree cleanup, just update issue
- No GitHub access → skip issue update, still do local cleanup + memory consolidation
- PR already merged → don't close, just note it in the output
- No .branch-context.md → create one with just the bail reason before consolidating

Output: Summary of what was cleaned up and where learnings were saved.
