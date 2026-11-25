---
name: create-draft-pr
description: Commit, push, and create a draft PR using the pr-description format, with UX flow context when relevant.
user-invocable: true
---

# Create Draft PR

Commit all changes, push to remote, and create a draft pull request with a focused generated description.

## Steps

1. Run `git status` to see changes
2. Run `git diff` to understand what changed
3. Run `git log` to see commit message style
4. If on `main`, create a new branch in the format `<initials>/<feature>` or the project's branch naming convention, then switch to it
5. Stage and commit changes with a concise message
6. Push branch to remote with `-u` flag
7. Generate the PR description using the `pr-description` skill's description format.
8. If the change is user-facing, workflow-oriented, or architectural, include a concise UX flow section using the `ux-flow-plan` style.
9. Create draft PR using `gh pr create --draft`
10. If you created the branch (were on `main`), switch back to `main` after the PR is created

## PR Body Format

Use the `pr-description` skill's format as the base:

```markdown
## Summary

<One sentence describing the overall change>

- Additional note if needed
- Another note if needed

## Problem

Describe the issue being addressed. What was broken, missing, or suboptimal? Be specific about the root cause.

## Solution

Explain the approach taken to fix the problem. Include code snippets only when they clarify the core approach.
```

When relevant, add this section between `Problem` and `Solution`:

````markdown
## UX Flow

```text
Current flow
└─ ...

Desired flow
└─ ...
```
````

Only include `UX Flow` when it helps explain the product behavior, user journey, or architecture boundary. Keep it short and use the `ux-flow-plan` tree style.

## Rules

- PR title should be succinct (no "feat:" prefix, but "fix:" is ok for bug fixes)
- Use `pr-description` as the source of truth for PR body structure.
- Include `UX Flow` from `ux-flow-plan` only when relevant; omit it for mechanical, dependency, or tiny internal changes.
- Do NOT include a file-by-file summary of code changes.
- Do NOT include a test plan with checkboxes.
- Do NOT include "Generated with Claude Code" or similar footers
- Keep the PR description concise and focused on intent and approach
- Use HEREDOC for the PR body to preserve formatting
