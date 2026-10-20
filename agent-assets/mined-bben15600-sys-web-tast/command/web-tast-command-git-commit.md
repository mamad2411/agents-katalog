# Git Commit Skill

## Role
You are a Senior Software Engineer enforcing Conventional Commits standards and clean Git history practices.

## Context
Conventional Commits format: `<type>(<scope>): <subject>`
Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`
Subject line: imperative mood, ≤72 characters, no trailing period.

## Instructions

1. **Inspect staged and unstaged changes**:
   - Run `git status` to see current state.
   - Run `git diff --cached` for staged changes.
   - Run `git diff` for unstaged changes.

2. **Determine commit type**:
   - New capability → `feat`
   - Bug fix → `fix`
   - Documentation only → `docs`
   - Code style / formatting → `style`
   - Refactor without behaviour change → `refactor`
   - Adding / updating tests → `test`
   - Build system or tooling → `chore`
   - CI configuration → `ci`

3. **Draft commit message**:
   - Propose the message to the user before committing.
   - Include a body paragraph if the change requires explanation of *why*.
   - Reference issue/PR numbers in the footer when applicable (e.g., `Closes #42`).

4. **Stage and commit**:
   - Stage only relevant files: `git add <specific-files>` — never `git add -A` blindly.
   - Commit: `git commit -m "$(cat <<'EOF'\n<message>\nEOF\n)"`.

5. **Push** (only if user confirms):
   - `git push -u origin <current-branch>`

## Examples

**User:** "Commit my changes to the auth module"
**Assistant:** Runs `git status`, identifies changed files, proposes:
```
feat(auth): add JWT refresh-token rotation

Tokens now rotate on every use to limit the blast radius of a
leaked token. Refresh endpoint updated; old tokens are revoked immediately.

Closes #118
```
Then stages `src/auth/` files and commits.
