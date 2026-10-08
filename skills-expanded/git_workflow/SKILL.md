---
name: git-workflow
description: Advanced Git workflows, branching strategies, and repository management.
---

# Git Workflow

Advanced Git operations and branching strategies.

## Branching Strategies

### Trunk-Based Development
- Single `main` branch, short-lived feature branches
- Fast feedback, continuous integration
- Feature flags for incomplete work

### Git Flow
- `main` (production), `develop` (integration), `feature/*`, `release/*`, `hotfix/*`
- Structured but heavier process
- Good for versioned releases

### GitHub Flow
- `main` + feature branches, PR-based
- Simple, deploy on merge
- Good for continuous deployment

## Advanced Operations

### Interactive Rebase
```bash
git rebase -i HEAD~5  # Clean up last 5 commits
# Commands: pick, squash, fixup, reword, drop
```

### Cherry-Pick
```bash
git cherry-pick <commit-hash>  # Apply specific commit to current branch
```

### Bisect (Debugging)
```bash
git bisect start
git bisect bad          # Current state is broken
git bisect good <hash>  # This commit was working
# Git binary searches to find the offending commit
```

### Reflog Recovery
```bash
git reflog             # Show all HEAD movements
git reset --hard <ref> # Recover "lost" commits
```

### Submodules vs Subtrees
- **Submodules**: Separate repos, .gitmodules tracking, version-pinned
- **Subtrees**: Merged into parent, simpler workflow, larger repo

## Conflict Resolution
1. Understand both sides of the conflict
2. Reconcile logically, not just textually
3. Test after resolving
4. Communicate with the other contributor if needed

## Best Practices
1. **Commit messages**: Imperative mood, descriptive subject + body
2. **Atomic commits**: One logical change per commit
3. **PR size**: Keep reviews manageable (under 400 lines when possible)
4. **Hooks**: Pre-commit for lint/format, pre-push for tests
5. **Tags**: Annotated tags for releases (`git tag -a v1.0.0 -m "..."`)
6. **.gitignore**: Keep it comprehensive, ignore build artifacts and secrets
