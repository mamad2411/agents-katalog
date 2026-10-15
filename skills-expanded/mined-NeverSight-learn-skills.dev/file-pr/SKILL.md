---
name: file-pr
description: File a concise pull request. Use when the user asks to file, open, or create a PR.
---

Create a pull request for the current branch using a clear title and a concise body.

Before filing, check whether the current branch already has a PR. Review its diff against the default branch on `origin` and confirm it matches the requested change.

**Title**
- Prefer a short imperative summary, <= 72 chars, with no trailing period.
- If the repo uses Conventional Commits, reuse that style for the PR title when it still reads naturally.
- Keep the title aligned with the actual diff, not the branch name.

**Body**
- Keep the body brief and reviewer-oriented.
- Mention affected user behavior, important implementation decisions, and anything a reviewer should inspect closely.
- Include `Closes #123` or equivalent only when the linked issue is known.
- If the base branch or testing status cannot be determined locally, ask the user.
