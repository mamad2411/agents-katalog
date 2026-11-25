---
name: conventional-commits-draft
description: 'Draft a conventional commit message from the staged diff.'
disable-model-invocation: true
---

# Drafting a Conventional Commit Message

## Overview

Draft a standardized, semantic git commit message using the Conventional Commits specification. Analyze the staged diff to determine appropriate type, scope, and message.

## Conventional Commit Format

```
# Single line, no body, no footer
<type>[optional scope]: <description>
```

## Commit Types

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `docs`     | Documentation only             |
| `style`    | Formatting/style (no logic)    |
| `refactor` | Code refactor (no feature/fix) |
| `perf`     | Performance improvement        |
| `test`     | Add/update tests               |
| `build`    | Build system/dependencies      |
| `ci`       | CI/config changes              |
| `chore`    | Maintenance/misc               |
| `revert`   | Revert commit                  |

## Breaking Changes

```
# Exclamation mark after type/scope
feat!: remove deprecated endpoint
```

## Workflow

### 1. Analyze Diff

```bash
# Only use staged diff
git diff --staged
```

### 2. Match Repo Conventions

Reference recent commits to align type, scope, and language with the repository's existing style:

```bash
git log --format="%s" -20
```

- **Language**: write the description in the same language as recent commits.
- **Scope/type**: reuse the wording and abbreviations already used in the repo.

### 3. Generate Commit Message

Analyze the diff to determine:

- **Type**: What kind of change is this?
- **Scope**: What area/module is affected?
- **Description**: One-line summary of what changed (present tense, imperative mood, <72 chars)
- **Breaking change**: if so, append `!` after the type/scope.

## Best Practices

- Present tense: "add" not "added"
- Imperative mood: "fix bug" not "fixes bug"
- Keep description under 72 characters

## Constraints

- NEVER update git config
- NEVER run git commit command
