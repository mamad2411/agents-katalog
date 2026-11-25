---
name: git
description: Git workflow, conventional commits, branch naming and PR conventions
license: MIT
compatibility: opencode
metadata:
  type: infra
  framework: git
  language: agnostic
---

# SKILL: Git

> **REVIEW:** This skill was generated with generic best practices.
> Adapt it to your project's conventions before using in production.
> Last review: 2026-02-24

## Tech Stack

- Git >= 2.40
- Husky >= 9.0 (git hooks)
- GitHub Flow (simplified trunk-based)
- Conventional Commits 1.0.0

## Project Patterns

### Branch Naming

Format: `<type>/<description-kebab-case>`

```
feature/add-user-auth
fix/login-redirect-loop
docs/update-api-readme
refactor/extract-payment-service
chore/upgrade-dependencies
hotfix/critical-null-pointer
```

**Rules:**
- Always in English, kebab-case
- Short but descriptive (3-5 words max)
- Base branch: `main` (never `develop` in GitHub Flow)
- Delete branch after merge

### Conventional Commits

Format: `<type>(<scope>): <description>`

```bash
feat(auth): add JWT token refresh endpoint
fix(auth): correct token refresh on expired sessions
docs(api): update OpenAPI spec for /users endpoint
test(auth): add integration tests for login flow
refactor(domain): extract ValueObject base class
perf(search): add index for user full-text search
chore(deps): upgrade symfony to 7.2
```

**Allowed types:**

| Type | When to use | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(dashboard): add drag-and-drop widgets` |
| `fix` | Bug fix | `fix(tts): handle empty text in speech synthesis` |
| `docs` | Documentation only | `docs(readme): add setup instructions` |
| `test` | Add or fix tests | `test(api): add e2e tests for auth flow` |
| `refactor` | No behavior change | `refactor(users): extract repository interface` |
| `perf` | Performance improvement | `perf(api): cache user profile responses` |
| `chore` | Maintenance, deps, CI | `chore(docker): update PHP base image` |
| `ci` | CI/CD changes | `ci(github): add deploy workflow` |

**Message rules:**
- Description in imperative, lowercase, no trailing period
- Scope optional but recommended (affected module or layer)
- First line < 72 characters
- Optional body: separated by blank line, explains the "why"
- Footer: `BREAKING CHANGE:` if it breaks compatibility, `Closes #123` for issues

```bash
feat(auth): add password reset via email

Users reported being locked out of their accounts. This adds
a password reset flow using time-limited tokens sent via email.

Closes #45
```

### GitHub Flow

```
main ─────●─────●─────●─────●─────── (always deployable)
           \                 /
            feature/xyz ────● (PR + review + merge)
```

1. **Create branch** from `main`
2. **Develop** with frequent, descriptive commits
3. **Push** and create PR when ready for review
4. **Review** — minimum 1 approval
5. **Merge** to `main` (squash or merge commit per preference)
6. **Deploy** automatically after merge
7. **Delete** feature branch

### PR Template

```markdown
## What changes

[Brief description of changes]

## Why

[Motivation, issue it solves, context]

## How to test

1. [Step 1]
2. [Step 2]

## Checklist

- [ ] Tests pass
- [ ] Lint clean
- [ ] Documentation updated (if applicable)
- [ ] No hardcoded secrets
```

### Husky (Git Hooks)

Husky runs scripts automatically on git events. Ensures no commit or push breaks the project rules.

**Installation:**

```bash
npm install --save-dev husky
npx husky init
```

This creates `.husky/` with a sample `pre-commit`. Structure:

```
.husky/
├── pre-commit       # Runs BEFORE each commit
├── pre-push         # Runs BEFORE each push
└── commit-msg       # Validates the commit message
```

**pre-commit** — Lint and format (staged files only):

```bash
#!/bin/sh
# .husky/pre-commit

# Backend: lint PHP
cd backend && composer lint 2>/dev/null

# Frontend: lint + format staged files
cd frontend && npx lint-staged
```

**commit-msg** — Validate conventional commits:

```bash
#!/bin/sh
# .husky/commit-msg

message=$(cat "$1")
pattern="^(feat|fix|docs|test|refactor|perf|chore|ci)(\(.+\))?: .{1,68}$"

if ! echo "$message" | head -1 | grep -qE "$pattern"; then
  echo "ERROR: Commit message does not follow Conventional Commits"
  echo "Format: type(scope): description"
  echo "Example: feat(auth): add login endpoint"
  exit 1
fi
```

**pre-push** — Tests before push:

```bash
#!/bin/sh
# .husky/pre-push

# Backend tests
cd backend && ./vendor/bin/pest --bail 2>/dev/null || exit 1

# Frontend tests
cd frontend && npm run test -- --bail 2>/dev/null || exit 1
```

**lint-staged** (Husky complement for efficient pre-commit):

```json
// package.json
{
  "lint-staged": {
    "*.{ts,vue}": ["eslint --fix", "prettier --write"],
    "*.php": ["php-cs-fixer fix"]
  }
}
```

**Rules:**
- `.husky/` hooks are committed to the repo (shared by the whole team)
- Use `lint-staged` in pre-commit to avoid relinting the entire project
- Pre-push runs tests — the last barrier before remote
- Never use `--no-verify` except in justified emergencies

### .gitignore Patterns

Keep organized by sections:

```gitignore
# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Dependencies
/vendor/
/node_modules/

# Environment
.env
.env.local

# Build
/dist/
/build/
/var/

# Session state (local per developer)
.ai/.local/*
!.ai/.local/.gitkeep

# Generated (AI tools — regenerate with .ai/sync.sh)
.claude/agents/
.claude/rules/
.claude/skills
.opencode/agents
.opencode/skills
.opencode/decisions.md
.cursorrules
.windsurfrules
GEMINI.md
.github/copilot-instructions.md
```

## Known Errors and Solutions

- **Problem:** Commit with wrong type (e.g.: `fix` when it's `refactor`)
  **Cause:** Not distinguishing between behavior change and restructuring
  **Solution:** If the user sees a different behavior, it's `fix` or `feat`. If they notice nothing, it's `refactor`

- **Problem:** Orphan branches not deleted after merge
  **Cause:** Auto-delete not configured in GitHub or not deleted manually
  **Solution:** Enable "Automatically delete head branches" in Settings > General of the repo

- **Problem:** Frequent merge conflicts in long-lived branches
  **Cause:** Feature branch open too long without syncing with main
  **Solution:** Run `git rebase main` or merge main frequently. Keep branches short (< 3 days)

- **Problem:** Commits with secrets (API keys, passwords)
  **Cause:** .env or config files not excluded in .gitignore
  **Solution:** Pre-commit hook with secrets detection. If already committed, rotate the secret immediately (git history retains it)

- **Problem:** Husky hooks not running after `git clone`
  **Cause:** Husky 9+ requires `npm install` to activate hooks via the `prepare` script
  **Solution:** Verify `package.json` has `"prepare": "husky"` in scripts. After clone: `npm install`

- **Problem:** Slow hooks blocking development flow
  **Cause:** Pre-commit runs lint/tests on the entire project
  **Solution:** Use `lint-staged` for pre-commit (staged files only). Full tests only in pre-push

## Checklist

- [ ] Branch created from `main` with correct naming (`type/description`)
- [ ] Commits follow Conventional Commits (`type(scope): description`)
- [ ] Commit message < 72 characters on first line
- [ ] No secrets in the commit (`grep -r "password\|secret\|api_key"`)
- [ ] PR has description, motivation and how to test
- [ ] Branch deleted after merge
- [ ] Husky installed (`npx husky init`) with `"prepare": "husky"` in package.json
- [ ] Pre-commit: lint with `lint-staged` (staged files only)
- [ ] Commit-msg: validates Conventional Commits format
- [ ] Pre-push: runs tests before pushing to remote

## References

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-git/github-flow)
- [Husky](https://typicode.github.io/husky/)
- [lint-staged](https://github.com/lint-staged/lint-staged)
- [Git Best Practices](https://git-scm.com/book/en/v2)
