---
name: git-recovery
description: "Recover from broken git states: detached HEAD, stale locks, divergent remotes, force-push failures."
tags: ["git", "recovery", "detached-HEAD", "force-push", "troubleshooting"]
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
version: 1.0.0
---

# Git State Recovery

Rescue repos from broken states during complex git operations. Covers detached HEAD, stale lock files, divergent remote histories, and network errors during push.

## When to Use

Load this skill when:
- User reports git repository is in a "broken" or "weird" state
- You encounter git errors like "not currently on any branch" or "unable to create index.lock"
- Force-push fails with network or filesystem errors
- A botched rebase left the repo in detached HEAD with hundreds of "deleted" files
- User asks "how do I recover my repo?" or "git is acting weird"

## Common Problems & Fixes

### 1. Stale Lock File

**Symptoms:**
```
fatal: Unable to create '.git/index.lock': File exists.
Another git process seems to be running...
Please make sure no other git process is running and remove the file manually to continue.
```

**Solution:**
```bash
# Remove the lock file
rm -f .git/index.lock

# Also clean up any incomplete rebase state
rm -rf .git/rebase-merge 2>/dev/null

# Abort any in-progress rebase
git rebase --abort 2>/dev/null

# Retry your original operation
```

**Why it happens:** Git crashed, was killed, or another git process is actually running. The lock prevents concurrent operations from corrupting the repo.

### 2. Detached HEAD After Botched Rebase

**Symptoms:**
- `git branch` shows `* (no branch)` or `(no branch, rebasing main)`
- `git status` shows 90+ deleted files (the working tree matches old remote commit while your committed work is on a separate branch)
- You can't get back to your actual work branch

**Diagnosis:**
```bash
# Where is HEAD right now?
git log --oneline HEAD -3
# What branch has our actual work?
git log --oneline main -3
# What's remote looking like?
git log --oneline origin/main -3 2>/dev/null

# Are our good commits intact on local main?
git ls-tree --name-only main | head
```

**Recovery — Local Branch Has the Right Commit:**

```bash
# 1. Clear any stuck state
rm -f .git/index.lock
rm -rf .git/rebase-merge 2>/dev/null

# 2. Stash anything blocking checkout (untracked files, modified files)
mv AGENTS.md AGENTS.md.bak 2>/dev/null  # if these exist and block checkout
mv CLAUDE.md CLAUDE.md.bak 2>/dev/null
git stash 2>/dev/null

# 3. Force-checkout the branch with our work
git checkout -f main
# If "Bus error" or "mmap failed", retry once. If still failing, use python:
# python3 -c "import os; os.remove('.git/index.lock')"

# 4. Verify we're on main with our commit
git log --oneline -1
```

**Recovery — Remote Has Divergent History That Needs Replacing:**

```bash
# After you're on the right branch with the right commits:
# Force push to replace remote history
git push --force origin main

# If network error on large repos, be explicit:
git push --force origin HEAD:main
```

### 3. Divergent Repos Being Force-Replaced

**Symptoms:**
- `git push` rejected: "Updates were rejected because the remote contains work that you do not have locally."
- But the remote history is the wrong project (different file structure, different purpose)
- You want to replace the entire remote with your local commits

**Solution:**
```bash
# Just force push — GitHub preserves old branches as refs, nothing truly lost
git push --force origin main

# For the truly nuclear option (when force-push fails repeatedly):
gh repo delete owner/repo --yes
gh repo create name --public --source=. --push
```

**When this is appropriate:**
- Repo was previously used for one project and is being repurposed
- Local has the correct, meaningful commits (your "feat:" commits from today)
- Remote has old unrelated commits that should be replaced

### 4. NFS/Network Errors During Push

**Symptoms:**
```
fatal: mmap failed: Operation timed out
fatal: mmap failed: Stale NFS file handle
error: RPC failed; result=22, HTTP code = 413
/bin/bash: line 2: <PID> Bus error: 10
```

**Recovery steps in order:**

```bash
# 1. Clear locks and incomplete state
rm -f .git/index.lock
rm -rf .git/rebase-merge

# 2. Retry the push
git push --force origin main

# 3. If still failing, try garbage collection
git gc --auto
git push --force origin main

# 4. If still failing (rare), clone fresh and cherry-pick
cd /tmp
git clone https://github.com/owner/repo.git fresh-repo
cd fresh-repo
git remote add source /path/to/original/repo
git fetch source
git cherry-pick <commit-hash-from-original>
git push origin main
```

**Pitfall — Repeated terminal() failures on the same repo:**

When `terminal()` keeps returning "Bus error", "mmap failed", or "Operation timed out" on the same repo across multiple calls (especially on macOS with NFS or iCloud-synced directories), the shell runtime itself may be hitting filesystem-level issues that retrying won't fix. **Switch to `execute_code` for the lock cleanup and checkout:**

```python
from hermes_tools import terminal
import os

repo = "/path/to/repo"

# Remove lock file directly (bypasses shell)
lock = os.path.join(repo, ".git/index.lock")
if os.path.exists(lock):
    os.remove(lock)

# Also clean rebase state
import shutil
rebase = os.path.join(repo, ".git/rebase-merge")
if os.path.exists(rebase):
    shutil.rmtree(rebase)

# Now checkout via terminal (or continue in execute_code)
terminal(f"cd '{repo}' && git checkout -f main", timeout=15)
```

**Why this works:** `execute_code` runs in a separate Python process with its own filesystem handles, bypassing the stuck terminal session. If even `execute_code` fails, the repo directory may have been moved/deleted by iCloud sync — clone fresh from remote as a last resort.

### 5. Rebase Conflict That Can't Be Resolved

**Symptoms:**
- You started a rebase (`git pull --rebase`)
- Conflicts appeared but you can't resolve them (stale lock, dirty working tree, or just stuck)
- You want to abort and go back to the state before the rebase

**Solution:**
```bash
# Clear any locks
rm -f .git/index.lock
rm -rf .git/rebase-merge 2>/dev/null

# Abort the rebase
git rebase --abort

# If untracked files block checkout, temporarily move them
mv AGENTS.md AGENTS.md.bak 2>/dev/null
git checkout -f main  # or whatever branch you were on
mv AGENTS.md.bak AGENTS.md 2>/dev/null
```

## Diagnostic Checklist

Use this table to quickly identify what's wrong:

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `index.lock` error | Crashed git process or concurrent git | `rm .git/index.lock` |
| `* (no branch)` in `git branch` | Detached HEAD from interrupted rebase | `git checkout -f main` |
| 90+ deleted files after checkout | HEAD on remote commit, local work on branch | `git checkout -f <our-branch>` |
| Push rejected (not fast-forward) | Remote diverged intentionally or accidentally | `--force` after confirming local is correct |
| `mmap failed: timeout/handle` | Filesystem or network issue | Lock cleanup + retry |
| Rebase refuses to abort | Stale lock OR very dirty working tree | `rm lock + rebase --abort` |

## Quick Recovery Recipes

**Recipe: "My repo is completely messed up"**

```bash
# Nuclear recovery: nuke all transient git state and force-checkout your main branch
rm -f .git/index.lock
rm -rf .git/rebase-apply
rm -rf .git/rebase-merge
rm -rf .git/CHERRY_PICK_HEAD
rm -rf .git/MERGE_HEAD
rm -rf .git/REVERT_HEAD
git checkout -f main
git log --oneline -3  # verify you're on the right commit
```

**Recipe: "I want to replace the entire repo history"**

```bash
# Start fresh locally but keep remote for PRs/issues
cd ..
mv project project-broken
git clone https://github.com/owner/project.git
cd project
# Copy your work back from project-broken/src, project-broken/README.md, etc.
# Make a single "Initial commit with work from project-broken"
git add -A
git commit -m "Initial commit: migrated from project-broken"
git push --force origin main
```

## Real-World Session Example

**Problem:** User has `/Users/patmini/Desktop/Master\ Artispreneur/artispreneur-academy/` in broken state:
- `git branch` shows `* (no branch)` 
- `git status` shows 90+ deleted files (all the `components/` and `scripts/` folders)
- But `git log --oneline main` shows a commit from today with the actual meaningful work

**Diagnosis:** HEAD is detached at old remote commit (9630e0b) while local `main` branch has the good commit (e55df4a).

**Solution applied:**
```bash
# 1. Remove stale AGENTS.md that blocks checkout
mv AGENTS.md AGENTS.md.bak

# 2. Stash the rest (if needed)
git stash

# 3. Force checkout main
git checkout -f main
# (retry if "Bus error" or lock complaints)

# 4. Restore AGENTS.md
mv AGENTS.md.bak AGENTS.md

# 5. Force push our local main to remote
git push --force origin main
```

Result: Both repos pushed successfully to GitHub.

## Related Skills

When this skill doesn't cover your issue, check:
- `github-auth` — authentication issues (expired tokens, missing credentials)
- `github-pr-workflow` — normal PR lifecycle, branch creation, merging
- `github-code-review` — review workflows, not recovery

## See Also

- Reference: [references/common-git-errors.md](references/common-git-errors.md) — expanded error catalog with specific git messages and fixes
- Reference: [references/rebase-vs-merge.md](references/rebase-vs-merge.md) — when to use each and common pitfalls
