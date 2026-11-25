---
name: git-blame-explain
description: Explains why specific lines of code were written using git blame and commit history
argument-hint: <file-path> [line-range e.g. 40-60]
user-invocable: true
allowed-tools: Bash(git *) Read
effort: low
---

## Explain Code History

File: **$1**
Lines: **$2** (or full file if not specified)

1. Run git blame on the specified range:
```bash
git blame -L ${2:-1,50} $1 2>/dev/null || git blame $1
```

2. For each distinct commit found, get the full message:
```bash
git show <hash> --stat --format="%H%n%an%n%ad%n%s%n%b"
```

3. Correlate code lines with commit messages.

4. Produce a narrative explanation:
   - Who wrote each section and when
   - What the commit message says about the intent
   - Any related issue/PR references in the commit
   - Notable patterns (e.g., "this was a hotfix", "this was a refactor from X")

This helps understand *why* code exists, not just *what* it does.
