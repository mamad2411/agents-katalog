---
name: triage-repo-cleanup
description: "Triage and clean up a repo's leftovers — stale git worktrees, merged and abandoned local branches, stale remote-tracking refs, and old stashes — by classifying each one by whether deleting it would destroy work. Triggers on: clean up my branches, clean up leftover worktrees, prune stale branches, delete merged branches, remove old worktrees, clear my stashes, repo cleanup, tidy up this repo, what branches can I delete, landing the plane cleanup."
when_to_use: "Use when the user wants leftovers removed — after a branch merges, when ending a work session, or on 'clean up any leftover trees/branches'. Also use before answering 'can I delete this branch/worktree?', because the answer depends on reachability, not on what `git branch -d` says. Creating a worktree is the companion create-git-tree skill; this one tears them down."
allowed-tools:
  - "Bash(bash */scripts/repo-cleanup-triage.sh*)"
  - "Bash(git worktree*)"
  - "Bash(git branch*)"
  - "Bash(git remote prune*)"
  - "Bash(git stash list*)"
  - "Bash(git push*)"
  - "Bash(git log*)"
  - "Bash(git merge-base*)"
  - "Bash(git rev-list*)"
  - "Bash(git for-each-ref*)"
---

# Triage Repo Cleanup

Cleanup is not a delete list. It is a **reachability question asked four times** —
of worktrees, local branches, remote-tracking refs, and stashes. Answer it first
and most of the cleanup turns out to be free; skip it and you eventually delete
the one commit that existed nowhere else.

## Run the triage

Codex: this path resolves under Claude Code; substitute the directory containing
this `SKILL.md`.

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
bash "$SKILL_DIR/scripts/repo-cleanup-triage.sh"
```

Flags: `--base <ref>` (default: `origin/HEAD`, else `main`, else `master`),
`--remote <name>` (default `origin`), `--json`, `--apply-safe`.

Exit status is `1` when anything landed in WOULD LOSE WORK or NEEDS A DECISION,
so it reads as "a human still has to look at this," not as a failure.

## The four tiers

| Tier | Meaning | Your move |
|---|---|---|
| **SAFE** | Deleting destroys no commit | Do it, report it after |
| **RECOVERABLE** | Not in base, but a remote still holds it | Do it, name the refetch command |
| **NEEDS A DECISION** | Holds state nothing else has (dirty tree, stash) | Ask |
| **WOULD LOSE WORK** | Commits on no remote and not in base | Ask, and offer to push first |
| **KEEP** | In use, or owned by another tool | Leave alone |

Apply the free tier without a round-trip:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
bash "$SKILL_DIR/scripts/repo-cleanup-triage.sh" --apply-safe
```

`--apply-safe` runs the SAFE tier and stops there. It never drops a stash, even a
SAFE-classified one, because a stash is the one artifact with no second copy
anywhere — confirm those individually.

## What makes a verdict trustworthy

**Do not classify with `git branch -d`.** It answers against your *current HEAD*
and against the branch's *own upstream*, so a branch fully merged into `main`
gets refused as "not fully merged" whenever you are standing on a third branch,
and a rebased branch gets refused because its stale remote counterpart diverged.
Both read as "unmerged work here" when nothing is at risk. Ask reachability
directly instead:

```bash
git merge-base --is-ancestor <branch> <base> && echo "every commit is in base"
git rev-list --count <upstream>..<branch>    # 0 = a remote still has all of it
git for-each-ref --contains <sha> refs/remotes   # empty = no remote has it
```

**Removing a worktree is not deleting a branch.** A clean worktree's commits live
on its branch ref, which survives the removal untouched — so a stale worktree is
almost always free to remove while its branch stays put. Triage the two
separately; treating them as one decision is what makes cleanup feel risky when
it is not.

**A detached worktree is the exception.** Its HEAD may be on no branch at all, in
which case removal orphans that commit. Check before removing, and if nothing
contains it, branch it first: `git branch rescue/<name> <sha>`.

**Leave tool-managed worktrees alone.** Anything under `.git/` belongs to the tool
that made it (`beads-sync`, for one). Its owner creates and reaps it on its own
schedule; removing it by hand breaks that tool rather than tidying the repo.

## Reporting

Lead with what you deleted, then the single decision you need. Name what each
deletion could not have cost — "every commit already in `main`", "identical to
`origin/<branch>`" — because that is the sentence that makes the cleanup
auditable. End on the open question only when the triage actually produced one.

Do not present the whole table back when a tier is empty. A repo with nothing in
WOULD LOSE WORK gets one line saying so.
