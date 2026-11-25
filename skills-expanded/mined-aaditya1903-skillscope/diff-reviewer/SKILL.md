---
name: diff-reviewer
description: Review a code diff for correctness, missing tests and unintended behaviour changes, and leave specific line-level comments. Use when reviewing a pull request or a set of staged changes.
license: MIT
compatibility: Works on any unified diff.
allowed-tools: Read Grep Bash
metadata:
  category: software-engineering
---

# Diff review

Review what the change does, not what the description says it does.

## Reading order

1. Read the tests first. They state the intended behaviour.
2. Read the diff hunks in dependency order rather than file order.
3. Re-read any hunk that changes a condition, a boundary or an error path.

## What to comment on

- Behaviour the change alters without saying so.
- Error paths that are now unreachable or newly reachable.
- Missing coverage for a branch the diff introduces.
- Names that no longer describe what the code does.

## What not to comment on

Formatting a linter already enforces, and preferences that would not change the
behaviour or the reader's understanding.
