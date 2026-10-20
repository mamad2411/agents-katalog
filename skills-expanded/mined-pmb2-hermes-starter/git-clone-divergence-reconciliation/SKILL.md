---
name: git-clone-divergence-reconciliation
description: "Reconcile divergent clones or branches of the same repository — identify what each side has, determine the canonical branch, restore missing subtrees additively, port doc-only commits across branches, and work around MSYS/cron git path failures. Use when two clones of one repo have diverged (e.g. canonical master missing files that only exist on another branch)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, divergence, clone, branch, reconciliation, restore, canonical, sync]
    triggers: [clone divergence, divergent clones, canonical branch, restore missing directory, missing docs directory, branch reconciliation, port docs across branches, cross-branch restore, git checkout origin branch, fetch by branch name, hermes-config divergence, master vs vps-hybrid, mass uncommitted deletions, retirement move, skills retired, uncommitted deletions, restore deleted files, stale clone working tree, reset damage, lost commits, git reset hard origin main, dropped commits, dangling commits, restore wiped fixes, cross-workstation reset]
    related_skills: [dynamic-upstream-merger, git-fork-divergence, windows-cron-msys-path-fix, discord-report-format]
---

# Git Clone Divergence Reconciliation

## Overview

Two clones of the same repository (or two branches pushed from them) drift apart: each side has commits and files the other lacks. The canonical clone is the one wired into active use (e.g. configured as `skills.external_dirs`); the other is stale or divergent. Reconciliation is the work of bringing the canonical tree up to the union of both sides WITHOUT full-merging code you didn't ask for.

Canonical example (recurring in the Hermes config environment): C: clone on `master` is canonical; E: clone on `vps-hybrid` has an entire `docs/` portfolio that C: lacks, while C: has `docs/findings/` and newer config commits E: lacks.

## When to Use

- A pulse/status check reports "docs/README.md does NOT exist on the canonical tree" or "clone divergence confirmed"
- Two clones on different drives (C: vs E:) show different file sets under the same repo
- You need to port documentation-only commits across branches without dragging in code/config divergence
- Any "restore missing directory from another branch" task

**Don't use for:** fork-vs-upstream divergence measurement (`git-fork-divergence`), full upstream sync with conflict resolution (`dynamic-upstream-merger`), merge-conflict resolution (`resolving-merge-conflicts`).

## Workflow

### Step 1: Establish what each side has

```bash
# Canonical clone: branch, recent commits, what's missing
cd ~/Documents/github/<repo> && git branch --show-current && git log --oneline -5
ls docs/            # what the canonical tree actually has

# Stale clone: same checks
cd ${MY_REPOS}/<repo> && git log --oneline -5
ls docs/            # what the other side has

# Check the remote — the divergent branch is usually pushed there
git ls-remote --heads origin
```

### Step 2: Fetch the divergent branch by name (cron-safe)

```bash
git fetch origin vps-hybrid:refs/remotes/origin/vps-hybrid
```

**NEVER `git fetch ${MY_REPOS}/... <branch>` in a cron session** — MSYS path translation doesn't apply to git.exe: `fatal: '/e/...' does not appear to be a git repository`. Fetching from `origin` by branch name always works because the branch is mirrored on the remote even when the local clone is stale. (Same class as `git -C /msys/path` failing — see `windows-cron-msys-path-fix`.)

**Windows-style local paths DO work for fetching between local clones** (verified Aug 4 2026): `git fetch ${MY_REPOS}/Documents/github/hermes-config` succeeds — only the MSYS `/e/...` form fails. If the two clones share no remote (or you want to compare against the other local clone directly), use the drive-letter form.

### Step 2.5: Quantify the divergence

Before restoring anything, measure how far apart the sides are — this tells you whether you're doing a small port or a large reconciliation:

```bash
# From clone A, fetch clone B (or origin branch), then count both directions:
git fetch ${MY_REPOS}/Documents/github/<repo>   # or: git fetch origin <branch>
git rev-list --left-right --count HEAD...FETCH_HEAD   # → "48  69" = A is 48 ahead, 69 behind
```

The two numbers are `HEAD`-side count first, `FETCH_HEAD`-side second. A large both-sided gap (e.g. 48/69 on hermes-config, Aug 4 2026) means each clone carries a different doc generation — verify which branch each clone is on (`git branch --show-current` + `git remote -v` on BOTH) before trusting either side's README/ECOSYSTEM counts as canonical. The two clones may be on different branches (`master` vs `vps-hybrid`) pushed to the same origin — that is branch divergence, not a corrupted clone.

### Step 3: Diff the trees to size the gap

```bash
git diff --stat origin/vps-hybrid master -- docs/ | tail -20
```

A one-sided diff (all deletions on one side) confirms the missing subtree. If both sides have unique files, the restore is pure addition.

### Step 4: Restore the missing subtree ADDITIVELY

```bash
git checkout origin/vps-hybrid -- docs/
```

Key property (verified Aug 2026 — 20-file `docs/` restore onto canonical master): `git checkout origin/<branch> -- <dir>/` copies the source tree but leaves local-only files under the same dir untouched. `docs/findings/` on master survived the restore with zero conflicts.

- Do NOT use `git checkout .` — it can overwrite/nuke local-only files
- Do NOT use a full `git merge` or rebase for this — you only want the missing subtree; a merge drags in code/config divergence you didn't ask for

### Step 5: Update index docs + CHANGELOG, then commit

After restoring a docs directory:
1. Update the directory's index (`docs/README.md`) — add any new subdirectories the other side didn't know about, bump the file/dir counts
2. Add a CHANGELOG entry describing the restoration
3. Commit with a descriptive message listing what was restored and from which branch

### Step 6: Decide what remains

- **Docs-only commits on the divergent branch** can be cherry-picked onto canonical later if needed (check each one only touches docs: `git show --stat <sha> | grep 'files? changed'`)
- **Code/config divergence** (feature commits on one side only) is a merge decision — defer to the development lead; document it as the remaining Next Action rather than deciding unilaterally

## Reset-Damage Recovery (lost local-only commits)

A sibling failure mode: `git reset --hard origin/main` on a shared clone silently drops EVERY local-only commit (fixes, tests, features that were never merged upstream). Recurring on the Hermes Agent repo (5th+ occurrence, 2026). Detection is a 30-second reflog check; recovery is possible because reset does not delete objects:

```bash
git reflog -8 --oneline        # "reset: moving to origin/main" = the wipe
git merge-base --is-ancestor <known-fix-sha> HEAD || echo DROPPED
git fsck --no-reflogs --unreachable | grep commit   # dangling objects survive
git cherry-pick -x <dangling-sha>                   # -x records provenance
```

Full workflow — including the staged-cherry-pick false-positive trap (a conflicted cherry-pick's STAGED content in the working tree can look like "the fix is already upstream"; always check `git status` before concluding that) and the namespace-package shadowing recurrence — in `references/cross-workstation-reset-recovery-2026-08-04.md`.

## Pitfalls

- **Mass uncommitted deletions on one clone are often a RETIREMENT MOVE, not data loss** (verified Aug 2026): `git status` shows 76+ ` D` files (17K lines) in the working tree, but the "deleted" files actually live in an untracked `skills.retired-YYYY-MM-DD/`-style directory — someone `mv`'d the subtree out of the tracked tree and never committed. Before restoring or committing anything, check: (1) is this the canonical clone or the stale one? The canonical `external_dirs` clone may be completely clean — the incident is only on the stale side; (2) does an untracked retirement/backup dir exist (`git status --short | grep '^??'`)? If yes, nothing is lost and restore is safe; (3) do the deleted files have NO local copy elsewhere (`find ${USER_HOME}/AppData/Local/hermes/skills -name <skill> -type d`)? Unique live skills (no local copy, not stale archived names) deleted uncommitted = the Jul 31 loader-failure class — restore them.
- **Restore ONLY the deleted tracked files, leave untracked work alone**: `git diff --name-only --diff-filter=D | xargs git checkout --` restores exactly the ` D` files (verified Aug 2026 — 76 files / 17K lines restored on the E: clone) and does NOT touch untracked dirs (the retirement archive, in-flight docs). Do NOT use `git checkout .` — it would also revert legitimate ` M` modified files and risk clobbering in-flight work. Verify after: `git status --short | grep -c '^ D'` → 0, and spot-check key files exist.
- **`git fetch /msys/path <branch>` fails in cron** (`fatal: does not appear to be a git repository`) — always fetch from `origin` by branch name; the branch is on the remote even if the local clone is stale
- **`git checkout origin/<branch> -- <dir>/` is additive** — local-only files under the restored dir survive. Verify with `ls <dir>/` after restoring before committing
- **Don't full-merge a divergent branch to restore one subtree** — you inherit every unrelated code/config change
- **Verify pre-flight skill files** (Scribe pulse pattern): if the job's skills are served from the repo's `skills/` tree, confirm the SKILL.md files exist before trusting the job ran with full context
- **PULSE.md append**: read the full file before `write_file` (partial reads silently truncate) — see `discord-report-format`

## Verification Checklist

- [ ] `git fetch origin <branch>:refs/remotes/origin/<branch>` succeeded
- [ ] `git diff --stat origin/<branch> master -- <dir>/` showed the one-sided gap
- [ ] `git checkout origin/<branch> -- <dir>/` restored the subtree
- [ ] Local-only files under the dir survived (`ls <dir>/` shows both sides)
- [ ] Index doc updated (file counts, subdirectory table)
- [ ] CHANGELOG entry added
- [ ] Commit created; remaining code/config divergence documented for the lead

## Reference Files

- `references/hermes-config-docs-restore-2026-08-01.md` — Full worked example: 20-file `docs/` portfolio restored from `vps-hybrid` onto canonical master (commit 7c9ebc7), including the commands that failed (MSYS path fetch, python `/e/...`) and the one-sided-diff signature that makes a restore zero-risk.
- `references/e-clone-skills-retirement-restore-2026-08-02.md` — Full worked example: 76-file / 17K-line uncommitted skills retirement on the stale E: clone detected and restored (`git diff --name-only --diff-filter=D | xargs git checkout --`), incl. the unique-live-skill test and the decision to leave the retirement archive + in-flight docs untouched.
- `references/cross-workstation-reset-recovery-2026-08-04.md` — Full worked example: `git reset --hard origin/main` wiped 8 local-only fix groups on the Hermes Agent repo; detection via reflog, discovery via `git fsck`, restoration via `git cherry-pick -x`, plus the staged-cherry-pick false-positive trap and namespace-hijack recurrence.
