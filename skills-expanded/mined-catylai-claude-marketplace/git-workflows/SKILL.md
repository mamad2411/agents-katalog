---
name: git-workflows
description: "Use when starting a branch, when a branch is behind its base or a push is rejected, when choosing rebase or merge, tagging a release, or adopting or auditing CODEOWNERS. Team rules for each."
license: MIT
---

# Git Workflows

Forge-neutral: the commands are plain `git`. Where a step is better done server-side (rebasing
an open pull request, merging, deleting a merged branch), use the forge plugin for that call.
Branch names come from `issue-tracker-core:branch-and-title-conventions` when that plugin is
installed; otherwise use `<type>/<short-description>`.

## Branching

- Trunk is the only long-lived branch. One branch per unit of work, so it can be reviewed and
  reverted on its own.
- Start from a synced trunk, because a branch cut from a stale local copy starts behind:

  ```sh
  git switch main && git pull --ff-only origin main
  git switch -c <branch-name>
  ```

  `--ff-only` refuses to create a merge commit. If it errors, local `main` has commits of its own;
  inspect them (`git log origin/main..main`) before doing anything else.
- Commit to a feature branch, not to trunk, even when trunk is not protected.

## Rebase or merge

| Situation | Route |
| --- | --- |
| Local trunk behind its remote | `git pull --ff-only origin main` |
| Feature branch not yet pushed | `git fetch origin && git rebase origin/main` |
| Feature branch pushed, review open | Rebase server-side through the forge, so nobody else's copy is rewritten locally |
| Server-side rebase reports conflicts | Rebase locally, then `git fetch` and `git push --force-with-lease` |
| Finished branch into trunk | Merge through the forge; the merge is the audit record |

Rebase onto the remote-tracking ref (`origin/main`), not local `main`, which may be stale.

**Being behind the base is not an error.** A branch behind trunk can still be pushed and
reviewed, and many forges rebase at merge time. Bring it current when you need the newer base:
to pick up a fix, clear a conflict, or get a pipeline green that depends on a trunk change.

## Force push

Use `--force-with-lease` on your own feature branch, right after `git fetch`: the lease only
protects against commits you have not fetched. Bare `--force`, and any force push to trunk or
another protected branch, are off the table. If `dev-guardrails` is installed, its Bash hook
enforces this and its message says what to run instead.

A push rejected as non-fast-forward means the remote has commits you lack: fetch, inspect them,
then rebase or merge. Overwriting the remote to make the push succeed discards them.

## After a conflict

1. Resolve each file on its merits; taking one side wholesale is a decision, not a default.
2. `git add` the resolved files, then `git rebase --continue`.
3. Re-run the full test suite. A textually clean resolution can still be semantically wrong.

## Tags

Release tags are annotated `vX.Y.Z` (`git tag -a v1.3.0 -m "<summary>"`, then
`git push origin v1.3.0`). A pushed tag is permanent: fix a wrong one by cutting the next
version, because anything that already fetched the old tag keeps the old commit.

## CODEOWNERS

The plugin ships a baseline at `${CLAUDE_PLUGIN_ROOT}/templates/CODEOWNERS`. Read it before
adopting or auditing an owners file; its comments carry the reasoning. The rules:

- **One file, one location**: repository root, `.github/`, `.gitlab/` or `docs/`. A second copy
  is dead config, because each forge reads only one.
- **Every rule names the owning group** (`@org/team`). An author cannot approve their own change,
  so a rule owned by one person requires nothing on that person's changes. Individuals are added
  alongside the group, never instead of it.
- **Catch-all first.** Only the last matching pattern applies, so a `*` rule placed below others
  silently replaces them. Add a path rule only to give that path extra owners.
- **Every rule has an owner.** A pattern with no owner marks the path as unowned.
- **An owner must be a member of the project**, and a group from another namespace must be shared
  with it. A handle that resolves to a real user outside the project gates nothing, and no tool
  reports it.

To audit, check the file against those rules. If `dev-guardrails` is installed, its session-start
hook reports the textual ones (duplicate locations, ownerless rules, sole individual owners,
malformed handles, shadowed rules). Membership needs the forge.

**Verify** on a live open request that is not the one adding the file: forges evaluate
CODEOWNERS from the target branch, so the adoption request shows no code-owner rule at all.
After it merges, open the approval state of the next request and confirm every code-owner rule
lists a non-empty set of eligible approvers. Without a forge connection, report the file as
"not yet verified" instead of passing it.

Without a checkout (web), give the user the commands above to run rather than running them, and
audit a pasted CODEOWNERS file against the rules.
