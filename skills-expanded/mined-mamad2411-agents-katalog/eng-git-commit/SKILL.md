---
name: eng-git-commit
description: Manage atomic Git commits, conventional commit messages, branch synchronization, and safe upstream pushing. Use when staging changes, committing code, and pushing branches.
---

# Git Workflow

A disciplined workflow for staging changes, crafting conventional commits, and safely pushing to remote repositories.

## Commit Readiness Checklist (Pre-Stage Gate)

Run this checklist before any `git add`:

- [ ] **Atomicity self-check**: All pending changes decompose into single-logical-unit commits; mixed concerns are split first.
- [ ] **Staging purity**: Only files belonging to the current logical unit get staged; inspect with `git status` and `git diff --staged`.
- [ ] **No forbidden artifacts**: No secrets, credentials, debug prints, temp files, or editor droppings in the staged diff.
- [ ] **Message conformance**: Type prefix valid (`feat|fix|refactor|test|docs|chore`), subject imperative and under 72 chars, body explains why when non-obvious.
- [ ] **Hook respect**: Pre-commit hooks run clean; never bypass with `--no-verify`.

## Principles & Safety Rules

- **Atomic Commits**: Each commit must represent one logical unit of change (feature, bugfix, refactor).
- **Conventional Commits**: Format messages with standard type prefixes (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`).
- **Never Force-Push to Protected Branches**: Strict guard against `--force` on `main`, `master`, `release`, or `production`.
- **Verify Staged Diff**: Always inspect staged changes (`git diff --staged`) before creating the commit.

---

## Workflow Steps

### 1. Status & Diff Inspection
```bash
git status --short
git diff
```

### 2. Stage Changes Atomically
Stage only the relevant files for the current logical change:
```bash
git add <file1> <file2>
# Or stage all tracked modifications if all belong to one change:
git add -u
```

### 3. Create Conventional Commit
Formulate a descriptive, imperative commit message:

```bash
git commit -m "<type>(<scope>): <concise summary>" -m "<optional detailed body explaining rationale>"
```

**Types**:
- `feat`: New feature or user-facing capability
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `docs`: Documentation updates
- `chore`: Maintenance, dependencies, or configuration updates

### 4. Push to Upstream
Verify the active branch and push safely:
```bash
git push -u origin $(git branch --show-current)
```
---

## Checkable Completion Criteria

- [ ] Staged diff contains only files belonging to the current logical unit.
- [ ] Commit message uses a valid conventional type prefix with imperative subject under 72 chars.
- [ ] No secrets, debug artifacts, or forbidden files in the committed tree.
- [ ] Pre-commit hooks ran clean; branch pushed only per user instruction.
