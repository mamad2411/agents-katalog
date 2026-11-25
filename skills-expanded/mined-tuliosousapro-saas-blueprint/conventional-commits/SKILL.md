---
name: conventional-commits
description: Enforces Conventional Commits format for git commit messages. Use when formatting commits or validating message structures. For git commands, see git-control.
---

# Conventional Commits Skill

## When to Use
- Every time a git commit is made
- When the user asks to "commit this" or "save progress"
- When auto-committing after task completion

## Reference
[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

## Instructions

### 1. Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 2. Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `style` | Formatting, missing semicolons, etc. (no code change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system or external dependency changes |
| `ci` | CI configuration changes |
| `chore` | Other changes that don't modify src or test files |

### 3. Scope (Optional)

Use the BRAINIAC phase or module name:
- `feat(idea): add competitor analysis playbook`
- `docs(planning): update tech stack playbook`
- `feat(skills): add market-research skill`
- `fix(landing-page): correct CTA link`

### 4. Breaking Changes
Add `!` after type/scope for breaking changes:
```
feat(api)!: change authentication flow to OAuth2
```

Or use footer:
```
feat(api): change authentication flow

BREAKING CHANGE: JWT tokens are no longer accepted.
```

### 5. Examples

```
feat(idea): add structured competitor analysis playbook

docs(skills): create market-research skill with Firecrawl integration

fix(landing-page): correct hero section gradient on mobile

chore(tasks): reset todo.md for foundations sprint

refactor(playbooks): rewrite idea phase to match new template
```

### 6. Rules
- Description: lowercase, imperative mood, no period at end
- Max 72 characters for the first line
- Body wraps at 100 characters
- One logical change per commit
- Reference issue numbers in footer when applicable: `Refs: #123`

## Quality Gates
- First line matches `<type>[scope]: <description>` format
- Type is from the approved list
- Description is imperative mood ("add" not "added", "fix" not "fixed")
- No commits with generic messages like "update", "fix stuff", "wip"
