---
name: "commit-writer"
description: "Write conventional commit messages from staged diff — type, scope, subject, body, breaking changes"
---

# Commit Writer Skill

## When to activate
- You have staged changes and need a well-structured commit message
- Writing commit messages across a team that uses Conventional Commits
- Generating commit messages that will feed into automated changelogs
- You want Claude to analyse the diff and propose the right commit type

## When NOT to use
- Work in progress / draft commits — use `git commit -m "wip"` and squash later
- Merge commits — let git generate these
- Revert commits — `git revert` generates the message automatically

## Instructions

### Conventional Commits format
```
<type>(<scope>): <subject>

[body]

[footer]
```

**Types:**

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability visible to users |
| `fix` | Bug fix |
| `docs` | Documentation only — no code change |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code restructuring with no behaviour change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build, tooling, dependency updates |
| `ci` | CI/CD configuration changes |
| `revert` | Reverts a previous commit |

**Rules:**
- Subject: imperative mood, lowercase, no full stop, max 72 chars — "add user auth" not "Added user auth"
- Scope: optional, in parentheses — the module, package, or file area affected
- Body: explain *why*, not *what* (the diff shows the what)
- Breaking changes: add `BREAKING CHANGE:` in the footer, or `!` after the type (`feat!:`)

### Workflow

Run this before invoking the skill:
```bash
git diff --staged   # see what you're about to commit
```

Then prompt Claude:
```
Write a conventional commit message for these staged changes:

[paste git diff --staged output, or describe what changed]
```

Claude will:
1. Identify the primary change type
2. Infer the scope from files changed
3. Draft a subject line (imperative, ≤72 chars)
4. Add a body if the change needs explanation
5. Flag breaking changes if present

### Multi-change commits
If the diff contains multiple logical changes, Claude will either:
- Write one commit that covers the primary change (mentioning others in the body)
- Suggest splitting into separate commits with `git add -p`

### Output format
Claude outputs the commit message ready to copy-paste:
```bash
git commit -m "feat(auth): add JWT refresh token rotation

Implement sliding session windows by rotating refresh tokens on each use.
Previous tokens are invalidated immediately after rotation.

Closes #234"
```

## Example

**Staged diff includes:**
- `src/auth/tokens.py` — new `rotate_refresh_token()` function
- `tests/test_tokens.py` — tests for the new function
- `CHANGELOG.md` — updated

**Expected output:**
```
feat(auth): add refresh token rotation

Rotate refresh tokens on each use to implement sliding session windows.
Previous tokens are invalidated immediately, reducing the window for
token theft after a session is compromised.

Closes #234
```

---
