---
name: git-recovery
description: Recovers lost git work and undoes mistakes safely. Use whenever the user says they lost commits, ran git reset --hard, deleted a branch, dropped a stash, committed on the wrong branch, broke a merge or rebase, force pushed, wants to undo a commit or a push, or asks how to get a file back from history, even if they only say "git ate my changes". Diagnoses with the reflog first, restores onto a new branch and never rewrites history without confirmation.
---

# git-recovery

Git rarely loses committed work. The reflog and unreachable objects hold almost everything, so the job is to find the right commit and put a branch on it before anything cleans it up.

```
git-recovery/
├── SKILL.md
├── scripts/
│   └── find_lost.sh        list reflog, unreachable commits and stashes; restore onto a new branch
└── references/
    └── undo-cookbook.md    situation to command table, reset modes, safe habits
```

## When to use

- Commits disappeared after `reset`, `rebase`, `checkout` or a branch delete
- A stash was dropped or never applied
- Work was committed on the wrong branch
- A merge, rebase or pull went wrong
- Someone force pushed
- Something must be undone, locally or after a push

## Workflow

1. **Stop**: do not run `gc`, `prune`, further `reset --hard` or more experiments. Check `git status` so uncommitted changes are not overwritten.
2. **Look**: `bash scripts/find_lost.sh` (add `--grep "message words"` to narrow). It lists the reflog, unreachable commits and stashes with dates and subjects.
3. **Identify**: match by time and message, then `git show --stat <sha>` to confirm it is the right work.
4. **Restore onto a new branch**: `bash scripts/find_lost.sh --restore <sha> rescued-work`. It only creates a branch, so nothing is overwritten.
5. **Verify**: `git log --oneline rescued-work`, check the files, run the tests.
6. **Then fix the original problem** with the cookbook (`references/undo-cookbook.md`), using `revert` instead of `reset` on anything pushed.

## Decision guide

| Question | Answer leads to |
|----------|-----------------|
| Was the work ever committed? | Yes: reflog or unreachable commits. No: editor history, backups, or `git fsck --lost-found` for staged blobs |
| Is the bad commit pushed? | Yes: `git revert`. No: `reset`, `amend` or `rebase` is acceptable |
| Is the branch shared? | Yes: never rewrite history without agreement |
| Is a secret involved? | Rotate it first (`secrets-hygiene`) |

## Rules

- Create a backup branch before any risky command: `git branch backup-before-fix`
- Prefer commands that add a new commit or branch over commands that delete
- Say what each command changes before running it, and run destructive ones only after the user confirms
- Use `--force-with-lease`, never plain `--force`
- Recovery windows are finite: reflog entries expire, unreachable objects are garbage collected. Act soon.
- If nothing is found, say so honestly and list what else to check, instead of guessing

## What to report back

| Field | Content |
|-------|---------|
| What happened | the command or event that lost the work |
| Found | sha, date, subject of the recovered commit |
| Restored to | branch name, verified how |
| Remaining risk | uncommitted files, pushed history, expiring entries |
| Prevention | backup branch habit, `revert` on shared branches |

## Related skills

- `systematic-debugging`: reflog, bisect and blame for investigation
- `secrets-hygiene`: when the mistake pushed a credential
- `termux-setup`: git problems specific to a phone
