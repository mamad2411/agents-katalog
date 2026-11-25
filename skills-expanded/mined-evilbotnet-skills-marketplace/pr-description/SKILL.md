---
name: pr-description
description: Draft a pull request description from the branch's commits and diff. Use when the user asks to write or update a PR description.
---

# PR Description

1. Run `git log --oneline @{upstream}..HEAD` (or against the default
   branch) and `git diff @{upstream}...HEAD --stat` to understand the
   branch's changes.
2. Draft a description with sections: **Summary** (what and why, 2-4
   sentences), **Changes** (bullet list grouped by area), **Testing**
   (how it was verified).
3. Show the draft. Only create or edit the PR via `gh` if the user asks.
