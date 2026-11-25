---
name: commit-message
description: Generates concise, intent-driven Git commit messages in imperative mood. Use when the user asks to create, write, draft, make, generate, or suggest a commit message, says "commit these changes" or "what should I commit?", or asks for help with a Git commit.
allowed-tools: Bash(git status:*), Bash(git diff:*)
metadata:
  author: Lucas Yang
  version: "2026.08.20"
---

# Git Commit Message Generator

Generate concise, descriptive and intent-driven Git commit messages in English.

## Process

1. Run `git diff --cached` directly to check for staged changes
2. If staged changes exist: generate commit message based on staged changes only
3. If no staged changes: run `git diff` directly to review unstaged changes and `git status --long` directly to list untracked paths
4. For untracked files, intelligently assess which need content review (code/config files) vs which can be inferred from filename (assets, dependencies)
5. Combine the diff with the intent supported by the conversation context; do not invent motivation that is not evident
6. Generate a single-line commit message that prioritizes known intent, then observable outcome, then the concrete change

## Output

Output ONLY the commit message — a single line, no explanation, no code block fencing.

## Format

- In English, imperative mood, under 72 characters
- Prefer the intended outcome over the edited file or implementation detail. If the intent is unknown, describe the concrete behavioral change.
- No type prefix (e.g., `feat:`, `fix:`) unless the user explicitly requests Conventional Commits format

## Examples

```
Add JWT authentication to protect account access
Add payment edge-case tests to prevent regressions
Validate login input before submitting credentials
Make search accessible from the navbar
Clarify installation requirements in README
Remove deprecated endpoints to simplify the API surface
Rename userService to clarify account responsibilities
Handle missing users during authentication
Fix database deadlock when updating concurrent balances
Preserve authentication behavior with regression tests
Return actionable errors when payment processing fails
Reduce page load time by batching database queries
Decouple user persistence with a repository pattern
Keep CI builds portable by migrating to GitHub Actions
Upgrade Vue to resolve hydration errors
```
