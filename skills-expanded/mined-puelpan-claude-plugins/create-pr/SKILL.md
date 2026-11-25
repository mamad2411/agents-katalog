---
name: create-pr
description: >-
  Create a new branch, split changes into logical commits, push, and open a
  GitHub pull request with a proper summary and test plan. Use only when the
  user explicitly asks to open or create a pull request (e.g. "create a PR",
  "open a pull request", "submit this as a PR"). For a plain commit with no PR,
  use the commit skill instead.
---

# Create Pull Request

Create a new branch, commit changes, and submit a pull request.

## When to Use This Skill

Use this skill only when the user explicitly asks to open or create a pull
request. For committing changes without opening a PR, use the `commit` skill.

## Behavior

- Creates a new branch based on current changes.
- Analyzes changes and automatically splits into logical commits when
  appropriate.
- Each commit focuses on a single logical change or feature.
- Creates descriptive commit messages for each logical unit.
- Pushes branch to remote.
- Creates pull request with proper summary and test plan.
- Do NOT add Claude co-authorship to PR description or commit messages.
- Use the GitHub CLI (`gh`) if necessary.

## Guidelines for Automatic Commit Splitting

- Run the linter, formatting, and type-check tools for this project before
  committing your changes.
- Split commits by feature, component, or concern.
- Keep related file changes together in the same commit.
- Separate refactoring from feature additions.
- Ensure each commit can be understood independently.
- Multiple unrelated changes should be split into separate commits.
- Do NOT add Claude co-authorship to PR description or commit messages.
