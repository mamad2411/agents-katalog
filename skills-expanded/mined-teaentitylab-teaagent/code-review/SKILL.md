---
name: code-review
description: Use when reviewing code changes, pull requests, or performing systematic code analysis and quality assessment.
tags: code-review, quality, analysis, pr
---

# Code Review Skill

Use this skill when reviewing code changes, PRs, or performing quality assessment.

## Workflow

1. Gather context: understand the scope of changes, related files, and dependencies.
2. Run static analysis: execute linters, type checkers, and security scanners.
3. Check test coverage: verify existing tests and identify gaps.
4. Analyze patterns: look for code smells, security issues, and performance concerns.
5. Provide actionable feedback: specific suggestions with severity levels.

## Key Tools

- `workspace_read_file` - Read files to review
- `git_diff` - View changes
- `grep` - Search for patterns
- `shell` - Run linting/testing tools

## Rules

- Always verify changes compile before flagging issues as "bugs"
- Distinguish between style preferences and actual issues
- Check for security vulnerabilities in external inputs
- Verify test coverage for critical paths
- Reference specific lines when providing feedback

## References

- See the main workflow and rules sections above for detailed review checklists and common patterns.