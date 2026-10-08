---
name: resume-from-pr
description: Resume work on a pull request by loading its context, diff, CI status, and review comments
---

# Resume from PR

## Name

github:resume-from-pr - Resume work on a pull request

## Synopsis

```
/resume-from-pr <pr-number-or-url>
```

## Description

Load full context for a pull request to resume work. Fetches PR details, diff, CI check status, and review comments to provide complete context for continuing development.

This maps to Claude Code's `--from-pr` flag which creates a PR-linked session.

## Implementation

1. Parse the PR number or URL from arguments
2. Use `gh pr view <number> --json title,body,headRefName,baseRefName,state,reviewDecision,statusCheckRollup,comments,reviews` to fetch PR metadata
3. Use `gh pr diff <number>` to get the current diff
4. Use `gh pr checks <number>` to get CI status
5. Check out the PR branch: `git checkout <headRefName>`
6. Summarize:
   - PR title and description
   - Current CI status (passing/failing)
   - Review comments and requested changes
   - Files changed
7. Present a plan for what needs to be done based on the PR state

## Example Interaction

```
User: /resume-from-pr 42

Claude: Loading PR #42 context...

**PR #42: Add user authentication**
- Branch: `feature/auth` -> `main`
- Status: Changes requested
- CI: 2/3 checks passing (lint failing)

**Review Comments:**
- @reviewer: "Please add input validation for email field"
- @reviewer: "Missing test for password reset flow"

**Plan:**
1. Fix ESLint errors in auth module
2. Add email input validation
3. Add password reset test
```

## Arguments

- `pr-number-or-url` (required): A PR number (e.g., `42`) or full GitHub URL (e.g., `https://github.com/owner/repo/pull/42`)

## Tips

- Works best when you have `gh` CLI authenticated
- The PR branch will be checked out automatically
- Combines well with `/review-pr` for a detailed code review before resuming work
- If the PR has failing CI, the plan will prioritize fixing those failures first

## Related Commands

- `/load-pr-context`: Load PR context without checking out the branch
- `/review-pr`: Get a comprehensive code review of a PR
- `/create-pr`: Create a new pull request
