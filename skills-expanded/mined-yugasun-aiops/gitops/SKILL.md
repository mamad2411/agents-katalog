---
name: gitops
description: >
  Git operations wrapper: sync, stage, commit, push. Generates Conventional Commits
  messages with .scratch artifact references. Use when the user says gitops,
  commit, push, sync code, or needs version control operations.
---

# Gitops

Git version control operations for the aiops delivery chain.

## Operations

### sync

Pull latest from remote. Default strategy: rebase.

```
git pull --rebase
```

If merge conflict: report to user, do not auto-resolve.

### status

Show current working tree state.

```
git status
git diff --stat
```

### stage

Stage files for commit. Supports selective staging.

```
git add <files>
```

### commit

Create commit with Conventional Commits message.

**Format:**
```
<type>(<scope>): <subject>

<body>

Refs: .scratch/<feature-slug>/
```

**Types:** feat | fix | refactor | test | docs | chore

**Message generation:**
- Read `.scratch/<feature>/NOTES.md` for design context
- Read `.scratch/<feature>/REVIEW.md` to confirm review passed
- Scope = feature-slug or module name
- Subject = imperative, lowercase, no period
- Body = reference upstream artifacts for traceability

**Pre-commit checks:**
- All blocking REVIEW.md findings resolved
- No untracked .scratch files in commit (add to .gitignore if needed)

### push

Push to remote. Requires user confirmation.

```
git push origin <branch>
```

### branch

Branch management: create, switch, list.

```
git checkout -b <branch>   # create + switch
git checkout <branch>      # switch
git branch                 # list
```

## Flow

1. `sync` — pull latest
2. `status` — review changes
3. `stage` — select files
4. `commit` — with generated message
5. `push` — after user confirms

## Constraints

- Never modify code files
- Never auto-resolve merge conflicts
- Always confirm with user before push
- Commit message must reference .scratch artifacts when available
- If `.scratch/<feature>/REVIEW.md` exists and verdict is REQUEST_CHANGES, block commit and report
