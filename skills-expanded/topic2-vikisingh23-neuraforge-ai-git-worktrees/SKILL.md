# Git Worktrees — Isolated Feature Development

## When This Activates

Before starting any feature implementation (after architecture approval), create an isolated worktree so the main branch stays clean.

## Workflow

```bash
# 1. Create worktree on a new branch
git worktree add ../feature-${feature_name} -b feature/${feature_name}

# 2. Move into it
cd ../feature-${feature_name}

# 3. Install dependencies (verify clean baseline)
npm install  # or dotnet restore, etc.

# 4. Run existing tests (must pass before any changes)
npm test     # or dotnet test

# 5. Develop in isolation — main branch untouched
# ... all changes happen here ...

# 6. When done — merge or create PR
git push -u origin feature/${feature_name}
# Create MR/PR from this branch

# 7. Clean up worktree
cd ..
git worktree remove feature-${feature_name}
```

## Rules

1. **Never develop on main/master** — always create a worktree
2. **Verify clean baseline** — tests must pass BEFORE you write any code
3. **One feature per worktree** — don't mix concerns
4. **Clean up after merge** — remove worktree once PR is merged

## When to Skip

- Single-file hotfix (< 10 lines)
- Documentation-only changes
- Config changes that don't affect code

## For Agents

When `forge`, `react-forge`, or `fullstack-orchestrator` starts implementation:

```bash
# Check if we're on main
CURRENT=$(git branch --show-current)
if [ "$CURRENT" = "main" ] || [ "$CURRENT" = "master" ]; then
  git worktree add "../wt-${FEATURE}" -b "feature/${FEATURE}"
  cd "../wt-${FEATURE}"
  echo "Working in isolated worktree: $(pwd)"
fi
```

After completion:
```bash
git add -A
git commit -m "feat: ${FEATURE_DESCRIPTION}"
git push -u origin "feature/${FEATURE}"
# Return to original directory
cd -
```
