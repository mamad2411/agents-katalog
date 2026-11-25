---
name: commit-conventions
description: "Conventional-commit message format and pull-request description conventions. Apply when writing a git commit message or PR description."
---

# Skill: Commit Conventions

## Format
```
type(scope): concise description

[optional body — explain WHY, not WHAT]

[optional footer — references, breaking changes]
```

## Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `docs`: Documentation only
- `chore`: Build, CI, tooling changes
- `style`: Formatting, no code change

## Rules
- Subject line: imperative mood, lowercase, no period, max 72 chars
- Body: wrap at 72 chars, explain motivation and context
- Reference the plan/phase when applicable: `Part of plan: [feature-name] Phase 2`
- One logical change per commit — don't mix refactoring with features

## PR Description
```markdown
## What
Brief description of the change.

## Why
Context and motivation.

## Phase
[Plan name] — Phase N: [Phase title]

## Changes
- Key change 1
- Key change 2

## Testing
How this was tested.

## Integration Notes
Any cross-repo impacts or integration summary updates.
```

## Multi-Repo Projects

When the project uses separate git repos per stack (e.g., `server/` and `web/` are each their own repo):

- **Check which repo you're in** before committing: `git -C <dir> rev-parse --show-toplevel`
- **Commit from within the stack directory**: `git -C server add . && git -C server commit -m "..."`
- **Never combine changes across repos** in a single commit — they are independent histories
- **If a phase touched multiple repos** (it shouldn't), make separate commits in each
