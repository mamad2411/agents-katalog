---
name: tidy-commits
description: Use when cleaning up local git commit history before review or merge, especially when a branch has WIP, fixup, review-fix, format-only, poorly ordered, unsigned, or poorly messaged commits.
---

# Tidy Commits

Tidy an existing branch into a clear, reviewable commit story while preserving the intended final tree.

## Quick start

For local branch history cleanup only — for ordinary new commits use the repo's normal commit workflow.

Inspect state → refuse unclear or unrelated working-tree changes → create a backup ref → plan `base..HEAD` (keep / squash / fixup / reword / reorder / split / drop) → show the plan and exact commands → rebase non-interactively → verify the final tree and tests before any push.

## Preflight

- Determine the base with repo evidence: PR base, `origin/HEAD`, or the user-provided base.
- Fetch first: `git fetch --prune --all`.
- Require a clean, understood state. If `git status` shows a rebase, merge, cherry-pick, or mixed unrelated changes, stop and ask.
- Record current state with `git log --oneline --decorate --stat <base>..HEAD`, `git diff --stat <base>...HEAD`, and nearby branch context.
- Create a backup ref, for example:
  - `git branch backup/tidy-commits-$(date +%Y%m%d-%H%M%S) HEAD`

## Cleanup plan

Classify each commit before rewriting.

| Commit type | Default action |
| --- | --- |
| Cohesive feature/fix/docs/test commit | Keep, maybe reword |
| `fix`, `fixup`, `review fix`, typo, format-only | Squash or fixup into the commit that introduced the need |
| Commit in the wrong layer/order | Reorder only when dependencies remain valid |
| Commit mixes unrelated concerns | Split if needed for reviewability |
| Debug, temporary, accidental, generated noise | Drop only when final behavior should not include it |

Do not blend unrelated concerns just to reduce commit count. A good stack is a readable story, not necessarily one commit.

## Rewrite

**Collapsing the whole range into one commit?** Skip the todo: `git reset --soft <base> && git commit`. This leaves the final tree staged and re-commits it as a single commit — nothing is replayed, so there are no conflicts (it signs automatically when `commit.gpgsign` is set). Use the rebase todo below only when you need selective fixup, reorder, or split.

Otherwise prefer non-interactive rebase patterns (no editor prompts). Generate the todo oldest-first (the reverse of `git log`), edit the actions and order, then feed it back:

```bash
git log --reverse --format='pick %h %s' <base>..HEAD > "${TMPDIR:-/tmp}/tidy-commits-todo"
# edit that file, then:
GIT_SEQUENCE_EDITOR="cp ${TMPDIR:-/tmp}/tidy-commits-todo" git rebase -i --update-refs <base>
```

The first column is the action; lines run top (oldest) to bottom (newest):

```
pick   a1b2c3d Add parser
fixup  f4e5d6a fix typo in parser   # folds into the pick above, discards its message
pick   7890abc Add CLI flag
edit   def1234 Wire CLI to parser   # stop to amend, then git rebase --continue
```

Avoid `reword` in todo files because it opens an editor; use `edit`, then `git commit --amend -m ...` and `git rebase --continue`. Use `GIT_SEQUENCE_EDITOR=:` with `--exec` for bulk mechanical amendments.

Recovery: mid-rebase, `git rebase --abort` restores the pre-rebase state; after a bad finish, `git reset --hard <backup-ref>`.

When a branch contains merge commits, ask whether to preserve them with `--rebase-merges` or flatten them. Do not guess.

## Stacked Branches

Before rewriting, detect local branches that point inside the rewritten range. Use `--update-refs` by default so stacked branches follow rewritten commits instead of being orphaned.

Flag branches checked out in another worktree: Git will not move those refs. Report them for manual verification before pushing.

If the repo uses a stacked-PR tool such as `gh stack`, prefer that tool's sync/rebase workflow over hand-editing branch relationships.

## Verification

After rewriting:

- Compare the final tree against the backup ref unless commits were intentionally dropped: `git diff --stat <backup-ref> HEAD` and `git diff <backup-ref> HEAD`.
- Show the new story: `git log --oneline --decorate <base>..HEAD`.
- Run relevant tests, type checks, linters, or focused reproductions.
- If branch protection requires verified signatures, check commit signatures with `git log --show-signature <base>..HEAD` or the repo's GitHub status. Re-sign rewritten commits before pushing when needed.

## Push Safety

Never use plain `git push --force`.

If the branch was already pushed, list every ref that changed and show exact commands first.

```bash
git push --force-with-lease origin HEAD:<branch>
git push --force-with-lease origin <moved-stacked-branch>
```

Ask for confirmation before force-with-lease pushes. Report any local-only backup ref and do not delete it without explicit approval.

## Stop Conditions

Stop and ask when:

- The intended base branch is ambiguous.
- A commit's purpose cannot be inferred from code, tests, or messages.
- Conflict resolution requires product judgment.
- Dropping a commit may change behavior.
- Another worktree or remote branch would be affected and cannot be verified.
