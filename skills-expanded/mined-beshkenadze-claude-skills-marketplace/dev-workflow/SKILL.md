---
name: dev-workflow
description: Orchestrate full development workflow. Use when implementing features, starting structured development, or user mentions "workflow" or "implement issues".
---

# Development Workflow

## Overview

Orchestrates complete feature development from issue to merge: Issue → Branch → Worktree → Implement → Test → Review → PR → Merge → Close.

## Prerequisites

1. Git repository initialized
2. Issue tracker MCP available (Gitea: `mcp__gitea__*`, GitHub: `mcp__github__*`)
3. Codex CLI installed (`codex --version`)
4. Repository owner/name confirmed

## Workflow Steps

### 1. Get Issue Details

**Gitea MCP:**
```
mcp__gitea__get_issue_by_index(owner, repo, index)
```

**GitHub MCP:**
```
mcp__MCP_DOCKER__get_issue(owner, repo, issue_number)
```

**GitHub CLI:**
```bash
gh issue view {issue_number} --repo {owner}/{repo}
```

### 2. Create Branch
```bash
git checkout main && git pull origin main
git checkout -b feature/{issue-number}-{slug}
```

### 3. Create Worktree
```bash
git worktree add ../worktrees/feature-{issue}-{slug} feature/{issue}-{slug}
```

Copy vendor dependencies if present:
```bash
cp -R Vendor ../worktrees/feature-{slug}/
```

### 4. Implement Feature
Work in worktree. For complex tasks, use Task tool with sub-agents.

### 5. Write Integration Tests
Add tests for new functionality. See [TESTING.md](TESTING.md) for testing patterns.

### 6. Run Tests
Project-specific test command (e.g., `xcodebuild test`, `npm test`).

### 7. Code Review

**Ask user which tool to use** if not specified:
- **Codex CLI**: `codex review --base main`
- **Gemini CLI**: `gemini -p "/code-review"`
- **GitHub Copilot**: `gh copilot` (interactive, ask for review)
- **OpenCode**: `opencode -p "review changes"` (provider-agnostic)

Run **exactly once** per review cycle:
```bash
# Codex (detailed P1-P4 findings)
codex review --base main

# OR Gemini (quick quality analysis)
gemini -p "/code-review"

# OR GitHub Copilot (interactive)
gh copilot  # then ask: "review my changes against main"

# OR OpenCode (works with any LLM provider)
opencode -p "review my code changes against main branch"
```

**IMPORTANT:** Wait for the full output. Do NOT run a second review unless you've made code changes to fix issues.

**If critical/high issues found:**
1. Fix all issues in code
2. Commit fixes
3. THEN run review again (this is a new review cycle)

**If no critical issues:** Proceed to commit.

See [CODE-REVIEW.md](CODE-REVIEW.md) for handling specific findings.

### 8. Commit & Push
```bash
git add . && git commit -m "feat(scope): description"
git push -u origin feature/{issue}-{slug}
```

### 9. Create Pull Request

**Gitea MCP:**
```
mcp__gitea__create_pull_request(owner, repo, title, body, head, base="main")
```

**GitHub MCP:**
```
mcp__MCP_DOCKER__create_pull_request(owner, repo, title, body, head, base)
```

**GitHub CLI:**
```bash
gh pr create --title "title" --body "body" --base main --head feature/{issue}-{slug}
```

### 10. Merge to Main
```bash
git checkout main && git pull origin main
git merge feature/{issue}-{slug} --no-ff && git push origin main
```

### 11. Close Issue

**Gitea MCP:**
```
mcp__gitea__edit_issue(owner, repo, index, state="closed")
```

**GitHub MCP:**
```
mcp__MCP_DOCKER__update_issue(owner, repo, issue_number, state="closed")
```

**GitHub CLI:**
```bash
gh issue close {issue_number} --repo {owner}/{repo}
```

### 12. Cleanup
```bash
git worktree remove ../worktrees/feature-{issue}-{slug}
git branch -d feature/{issue}-{slug}
```

## Parallel Workflow

For multiple independent issues, see [PARALLEL.md](PARALLEL.md).

## Error Recovery

See [ERRORS.md](ERRORS.md) for handling build failures, Codex P1 issues, and merge conflicts.

## Examples

### Example: Implement Feature from Issue

**Input:**
"Implement issue #42 - Add user authentication"

**Process:**
1. Get issue details via MCP
2. Create branch `feature/42-user-auth`
3. Create worktree
4. Implement authentication feature
5. Write tests
6. Run code review
7. Create PR and merge

**Output:**
```
✅ Issue #42 implemented
✅ PR #15 created and merged
✅ Issue #42 closed
```

## Guidelines

### Do
- Confirm repository owner/name before starting
- Create worktree for isolation
- Run code review before PR
- Close issue after merge

### Don't
- Skip the code review step
- Work directly on main branch
- Leave worktrees after merge
- Forget to push before creating PR
