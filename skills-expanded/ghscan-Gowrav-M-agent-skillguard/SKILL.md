---
name: safe-code-reviewer
description: Read-only code review workflow for local repositories.
version: 0.1.0
capabilities: [filesystem-read, git-read]
---

# safe-code-reviewer

Review local source files and git diffs. Report correctness, security, and test gaps.

## Rules

- Read files and git history only.
- Do not write files, run installers, or contact external services.
- Keep findings grounded in file paths and line references.
