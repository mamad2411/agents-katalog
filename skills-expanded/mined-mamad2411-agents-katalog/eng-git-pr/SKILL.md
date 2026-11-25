---
name: eng-git-pr
description: Create GitHub Pull Requests with comprehensive change summaries, testing evidence, and linked issues. Use when submitting feature or fix PRs for team review.
---

# Git Pull Request

Prepare and create a GitHub Pull Request for the current branch.

## Push Readiness Policy

Default mode is **readiness-only**: prepare the branch, verify all checks, and present a push-readiness report. Actual `git push` runs only on explicit user instruction.

**Readiness report items (all must be green before offering to push):**
- [ ] Branch rebased or merged cleanly onto the latest base.
- [ ] Full validation suite green on the final state.
- [ ] Commit history conforms to conventional commits with no fixup/noise commits.
- [ ] PR description drafted with change summary, test evidence, and linked issues.
- [ ] No force-push required; if the branch diverged, reconcile via merge/rebase discussion, never force.

**Hard rules:** Never force push to `main`, `master`, or protected branches under any instruction. Pushing without an explicit user request is prohibited even when readiness is green.

## Prerequisites
- Branch pushed to remote.
- GitHub CLI (`gh`) available and authenticated, or generate markdown for manual submission.

## Process

### 1. Diff & Commit Analysis
1. Review all commits included on this branch compared to base branch:
   ```bash
   git log origin/<base-branch>...HEAD --oneline
   git diff origin/<base-branch>...HEAD --stat
   ```

### 2. Draft PR Description

```markdown
## Summary
- High-level overview of what changes are introduced.

## Key Changes
- **Module A**: <Key modification>
- **Module B**: <Key modification>

## Testing & Verification
- [x] Unit tests passing
- [x] Manual verification performed

## Related Issues
- Closes #<issue-id>
```

### 3. Create PR
```bash
gh pr create --base <base-branch> --title "<title>" --body "<markdown-body>"
```
---

## Checkable Completion Criteria

- [ ] Readiness report shows every gate green: clean rebase state, validation green, conventional history, drafted description.
- [ ] PR body includes summary, key changes, test evidence, and linked issues.
- [ ] Push and PR creation happened only on explicit user instruction; zero force-pushes to protected branches.
