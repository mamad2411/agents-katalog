---
name: commit-messages
description: Shape commits, branches and their messages. Use when staging or splitting changes, writing a commit message, committing for a delegated run, creating, naming or syncing a branch, resolving merge conflicts, merging a pull request and cleaning up its branch, backporting a fix, or writing a pull request description.
---

# Commit messages

## What goes in a commit

- **Atomic**: one logical change per commit, buildable on its own where the project expects that. Split unrelated edits; keep a change and its tests together. One commit holds one whole seam, not one file or one edit, so neither split a seam into fragments nor merge unrelated seams into one.
- Stage explicit paths. Leave out secrets, env files, credentials, and incidental build, cache or tool output. Generated files that the repository tracks are regenerated and verified the way the repository prescribes.
- Dependency changes pin versions and include the lockfile.
- Preserve other people's uncommitted work: commit only what this task changed.

## The message

- **Subject**: imperative and verb-led (`Add`, `Fix`, `Remove`, `Rename`), about 50 characters, no trailing period. It completes "This commit will …".
- **Attribution**: a commit holding another agent's accepted work says so in its body, for example "Written by <agent> from a coordinator brief; checked by the coordinator."
- **Body** when the why is not obvious: the reason, the consumer impact, and any follow-up, in about six lines or fewer, wrapped at about 72 columns; never a list of the files changed or a retelling of the diff. Reference task or issue IDs the project tracks.
- Follow a convention the repository already uses (for example Conventional Commits) over this default.
- End with the attribution trailer the host asks for, exactly as given, and only that one.

## Interrupted work

When committing a stopped run's work on its behalf, mark it in the subject (`WIP: <task label> …`) so the next writer sees the state.

## Branches

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

Trunk-based: the default branch stays releasable, and every change reaches it through a short-lived branch and a pull request; a branching scheme the repository already documents wins. Read [references/branches.md](references/branches.md) before creating, naming, syncing, pushing or merging a branch, resolving conflicts, backporting a fix or cleaning up after a merge. In short:

- **Main checkout** stays on the default branch and clean; every branch, a coordinator's own small fix included, gets a worktree of its own: `git worktree add -b <name> <path> origin/<base>`. Advisory (agent judgment); the session start warns when the main checkout is off its default branch.
- **Sync**: rebase a branch you have not pushed onto `origin/<base>`; merge the base into a pushed one. Rebasing a pushed branch needs authority ("Authority" below).
- **Default branch**: changes arrive by pull request; an agent never uses a branch-protection bypass, even when its login holds one, and a rejected direct push means: open a pull request.
- **Merge** through the pull request after the merge check (`review-gate` "Pull requests"), pinned to the reviewed head: `gh pr merge <number> --merge --match-head-commit <sha>` on GitHub.
- **Worktree sweep**: right after a successful merge, run `python3 -I <this skill's folder>/scripts/worktree_sweep.py list` (read-only); only for the worktree of the pull request just merged, when it is a candidate this agent or its runs created, run exactly the two git commands it prints, and tell the user the rest of the list with sizes (advisory, agent judgment; git enforces its own checks).

## Authority

Committing locally is part of the task when the task calls for it: commit when a seam is done and its targeted tests pass, always on a branch of your own and never on the default branch, and without pushing. Pushing, force-pushing, rewriting published history, merging and opening or merging pull requests need explicit authority.

## Pull request descriptions

When `pr` from [mattpocock/skills](https://github.com/mattpocock/skills) is installed, let it shape the body and keep the verification and review-status lines and the router marker line below.

Summary of the change, how it was verified (commands and results), what was not verified, and the review status (`review-gate`), each in one to a few lines. When `coding-router` routed the work, add its marker on a line of its own, exactly `<!-- fnl-router depth=<MIN|NORMAL|DEEP> trigger=<trigger> -->` with the depth and trigger of its receipt (`coding-router` "3. Choose the depth"); a repository that adopted `review-gate` blocks the merge without it (enforcer: its `merge_check.py`). Do not copy the changelog entry: `CHANGELOG.md` is the one place that records a public change. End with the attribution line the host asks for.
