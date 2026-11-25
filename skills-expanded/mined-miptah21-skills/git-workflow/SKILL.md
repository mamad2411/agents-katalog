---
name: git-workflow
description: Git conventions for commits, branches, and PRs. Use when performing git operations or preparing changes for review.
---

# Git Workflow

> Conventions for git operations: commits, branches, PRs.
> Read when performing git operations or preparing changes for review.

---

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]
[optional footer]
```

### Types

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build process, dependencies, tooling |
| `ci` | CI/CD changes |

### Rules
- Use imperative mood: "add feature" not "added feature"
- First line ≤ 72 characters
- Reference ticket if applicable: `fix(auth): handle expired tokens (#123)`
- No period at the end of the subject line

## Branch Naming

```
<type>/<short-description>
```

Examples:
- `feat/user-authentication`
- `fix/login-redirect-loop`
- `chore/update-dependencies`
- `docs/api-reference`

## Pull Requests

### PR Title
Same format as commit messages: `type(scope): description`

### PR Description Template
```markdown
## What
Brief description of what changed.

## Why
Context on why this change is needed.

## How
Key implementation details (if non-obvious).

## Testing
How this was tested. Include commands run.

## Checklist
- [ ] Tests pass
- [ ] Lint passes
- [ ] No new type errors
- [ ] Breaking changes documented (if any)
```

## Merge Strategy
- **Squash merge** for feature branches (clean history)
- **Merge commit** for release branches (preserve history)
- **Rebase** for keeping branches up-to-date with main
- **Never force-push** to shared branches
