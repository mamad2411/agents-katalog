---
name: orbyn-worktree
description: "Manage local task branches, private contribution storage when supported and Git worktree isolation; use sibling <repo>-wt directories, purpose-based names and preservation before cleanup."
---

# Worktree ownership and lifecycle

Use this skill when a task needs checkout isolation, the user requests a worktree,
or a worktree needs reconciliation/cleanup. The [workflow](../orbyn-workflow/SKILL.md)
selects it from the ordinary request. Follow the consuming project's instructions,
requested checkout and host permissions.

## Create a worktree by work mode

Read the repository's `work mode` from `harness.py resolve` first and follow the
[mode table](../orbyn-workflow/references/harness-settings.md#the-work-mode):
`simple` no worktree, `isolated` one per task, `parallel` one per active task with
at most `max_active`, the rest queued. A small clear edit stays in the current
checkout in every mode, and "just do it here" overrides the mode for that task.
In `parallel`, run the cleanup report at every closeout.

## Resolve the repository and owner first

Inspect the current checkout, branch, HEAD, changes and `git worktree list --porcelain`.
Resolve the primary clone from Git registration; the current directory may be a
linked worktree (its `.git` is a pointer), so derive no other `-wt` root from it.

Preserve unrelated changes and outputs; do not stash, reset, switch another owner's
checkout, copy dirty files or move worktrees to enforce this convention.

## Reuse before cloning or replacing

Before creating a checkout, inspect registered trees, remotes, host attachments and
any reference cache. Reuse a worktree only when repository, owner, branch,
source and local work fit and no active session holds it. Continue a task/PR in its
owned branch; start independent work from the verified default branch and a stack
from its exact reviewed dependency; never reuse a historical branch because it is
current or create a clone per agent/day/retry.

## Sibling location and names

The default root is the primary clone's sibling `<parent>/<repo-slug>-wt/`, with one
direct child per worktree named for its purpose slug, not the branch path; a target in the library's `repo/` workspace uses `repo/<target>-wt/<purpose>/`. An explicit user location or an
established project policy wins. Use neutral branch prefixes, no agent/vendor/model branding. Inspect collisions first; never overwrite a directory, reuse a
foreign branch or force past Git's already-checked-out protection; keep legacy paths
intact. Slugs, reuse and creation steps: [naming and creation](references/naming-and-creation.md).

## Keep task branches local and publish deliberately

A worktree and its branch are local Git state and need no remote branch. Reuse one
owned branch and worktree through review, never one per agent, phase or retry; never
push every delegate branch. Serialize operations on shared Git refs, remotes
and configuration under one owner. Before any push, follow
[contribution storage](references/contribution-storage.md). Preserve valuable
unpushed work before cleanup; a local branch survives only with its checkout.

## Create and verify the selected checkout

Resolve the base before writes: continue a task/PR from its actual branch, start new
work from the verified default branch (not a stale local `main`). Fetch only when
available and authorized; label an offline/cached base as such. Create a branch with
`git worktree add -b <branch> <path> <base>`; reuse an existing branch only after
ownership inspection; avoid `-B`, `--force` and duplicate branch checkouts. Verify
path, branch, base/HEAD and status before editing, then use that worktree for every
edit/check. After selecting or switching checkout, reread nested instructions and
re-resolve search roots there ([action scope](../orbyn-setup/references/action-scope.md)).
Preserve project environment files; never copy secrets or run setup hooks from
source; assign shared databases, ports and services separately.
If the host denies Git metadata writes, preserve the patch and report delivery as
blocked; never rewrite `.git`, supply an alternate index or bypass the sandbox.

## Designate task verification

Before expensive runs, name focused checks, exclusions and widening conditions in the
task brief ([feature-worktree gates](../orbyn-ci-design/references/change-scope.md#designate-gates-for-the-feature-worktree)).
A new worktree adds no entire-app suite, hosted CI or deployment.

## Preserve before cleanup

At delivery, follow [task closeout](references/task-closeout.md): reconcile source,
commit, push, PR and resources, record retention reasons/review triggers and assess
exact-path retirement separately from permission to remove it (Windows:
[native retirement](references/task-closeout.md#windows-retirement)).

Never delete another owner's work; unknown ownership means hold. A squash merge or
clean status alone does not clear a tree for removal. Retire a tree only through
`worktree_retire.py` (whole folder to the system Trash, then that one Git registration
cleared). Its `apply` proves only landing, a clean tree, no hidden changes, nothing open and no hold; the owner still
judges the rest ([retirement gate](references/task-closeout.md#retirement-gate-for-an-exact-path-or-ref)).
A refusal has no automatic force fallback; ref deletion and tracking prune stay separate.

After a merge, [retire the worktree in the same closeout](references/task-closeout.md#retire-at-delivery)
when you have cleanup authority; never hand-run `git worktree remove` on a live tree,
which deletes ignored files. Keep a merged tree only with a named reason and review
event in a `HOLD.json`. At closeout, before creating a worktree and on low disk, [run workspace cleanup](references/task-closeout.md#clean-the-workspace)
(`worktree_retire.py report`, then `apply`). It trashes only finished worktrees,
rebuildable caches and idle output, archive and references; everything else in
`repo/` is report-only.

### Worked failure

PR 17 merged by squash, but its tree has a later local commit, ignored review
captures and a live preview. Treating the merged badge, a clean status or ancestry as
proof it is disposable cache is the failure: keep the later source and a verified
evidence package, check dependent work and get the owner's release first
([closeout example](references/task-closeout.md#synthetic-closeout-example)).

Return the path/base/head, verified delivery state, retained resources, recovery
pointers and closeout disposition.

## Read when needed

- Push, fork, private storage, backup or public PR: [contribution storage](references/contribution-storage.md).
- Reclone, replace a checkout or empty partial cache: [checkout replacement](references/checkout-replacement.md).
- Layouts other than nested, delegate branches, unattended runs, dirty primary changes, host worktree tools, another checkout's search results, delivery statuses, a worked command: [checkout setup](references/checkout-setup.md).
- Preview/evidence storage, servers, retention classes: [artifact lifecycle](../orbyn-workflow/references/artifact-lifecycle.md).
