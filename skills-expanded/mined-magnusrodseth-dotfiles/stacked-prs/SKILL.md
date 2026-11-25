---
name: stacked-prs
description: Manage a stack of dependent pull requests (a chain where each PR's base is the branch below it, up to main). Covers GitHub's native stacked pull requests via the gh stack CLI extension, and hand-rolled stacks built with plain git + gh. Use when creating or planning a stack of dependent PRs, merging the bottom of a stack, retargeting a PR's base to main, propagating main or a review fix up a chain of branches, rebasing or restructuring a stack, resolving conflicts across a PR stack, or recovering a stacked PR that was auto-closed when its base branch was deleted.
---

# Stacked PRs

A **stack** is a chain of PRs where each PR's base branch is the **head** branch of the one below it, down to a PR whose base is the **trunk** (usually `main`):

```
main  ←  A (branch a)  ←  B (branch b)  ←  C (branch c)
         PR #A            PR #B            PR #C
         base: main       base: a          base: b
         bottom                            top
```

Each PR's diff shows only **its own layer** because it is compared against the branch below. The bottom is closest to trunk; the top is furthest. Foundational work (schema, shared types) goes low; things that depend on it (API routes, UI) go high. The invariant: **if code in one layer depends on code in another, the dependency must live in the same branch or a lower one.**

## Route first: native stack or hand-rolled chain

GitHub shipped **native stacked pull requests** on 30.07.2026 (public preview, rolling out to all repos). A native stack is a first-class object on GitHub with its own number, a stack map in the merge box, webhook/REST/GraphQL surface, and server-side cascading rebase. A hand-rolled chain is just a set of PRs whose bases happen to point at each other; GitHub has no idea they are related.

**They behave differently in ways that will bite. Establish which one you have before touching anything.**

```bash
# 1. Is the CLI extension available locally?
gh extension list | grep gh-stack

# 2. Is this PR part of a native stack?  `null` means it is not.
gh api repos/<owner>/<repo>/pulls/<n> --jq '.stack'

# 3. What stacks exist in this repo at all?
gh api repos/<owner>/<repo>/stacks
```

|  | Native stack | Hand-rolled chain |
|---|---|---|
| Created by | `gh stack init/add/submit`, github.com, or `gh stack link` | `gh pr create --base <branch>` by hand |
| Merge with | `gh stack merge --yes` (**`gh pr merge` fails**) | `gh pr merge` |
| Retarget on merge | automatic | **manual, and skipping it closes the PR above** |
| Rebase up the chain | `gh stack rebase` (cascading) | by hand, branch by branch |
| Reviews, checks, CODEOWNERS | evaluated against the **stack base** for every layer | evaluated against the branch directly below |
| Visible to reviewers as a unit | yes, stack map in the merge box | no |

**If the repo supports native stacks, use them.** The hand-rolled section below is the fallback for repos where the preview has not landed, and the repair manual for chains that already exist.

## Native stacks (`gh stack`)

### Setup

```bash
gh extension install github/gh-stack        # needs gh >= 2.90.0 and git >= 2.20
gh skill install github/gh-stack            # optional: GitHub's own agent skill
git config rerere.enabled true              # remember conflict resolutions across rebases
git config remote.pushDefault origin        # only if the repo has more than one remote
```

### Run every command non-interactively

Bare `gh stack view`, `submit`, `init`, `add`, `checkout` and `merge` open a prompt or a full-screen TUI. In an agent session that **hangs forever**; it does not fail. Always pass the argument or flag that skips the interaction:

| Never | Always |
|---|---|
| `gh stack view` | `gh stack view --json` |
| `gh stack submit` | `gh stack submit --auto` |
| `gh stack init` | `gh stack init <branch> [<branch>...]` |
| `gh stack add` | `gh stack add <branch>` |
| `gh stack checkout` | `gh stack checkout <pr-number \| stack-number \| branch>` |
| `gh stack merge` | `gh stack merge --yes` |

Two more traps. Commands that resolve a remote but have **no `--remote` flag** (`checkout`, `modify`, `trunk`) error out non-interactively when several remotes exist and `remote.pushDefault` is unset. And a branch belonging to two stacks makes commands exit with code **6**; check out a non-shared branch first.

### Plan the layers before writing code

Stack shape is a design decision and expensive to change later. Split by dependency first, then by reviewer attention:

```
main
 └── data-model      shared types, migration
  └── api-endpoints  routes that use the model
   └── frontend      components that call the routes
    └── integration  tests exercising the whole thing
```

Start a new branch when the concern changes (backend to frontend, logic to tests), when the reviewer audience changes, or when the current layer is already a full read on its own. Unrelated work gets its **own stack**, not a spare layer on this one.

### Build

```bash
gh stack init data-model                  # creates the branch, checks it out, trunk = default branch
# ... write code ...
git add <paths> && git commit -m "..."    # stage deliberately: this is what keeps layers clean
gh stack add api-endpoints                # next layer, on top of the current one
git add <paths> && git commit -m "..."
gh stack submit --auto                    # push every branch, open a PR per branch, link them as a stack
```

`gh stack init --base release/2.1 <branch>` targets a trunk other than the default branch. `gh stack submit --auto` opens PRs as **drafts**; add `--open` for ready-for-review. Existing branches are adopted rather than recreated, so `gh stack init a b c` works on work already in progress.

### Change a lower layer

Never patch around a missing lower-layer change from the top: the fix lands in the wrong PR and both diffs stop making sense. Go down, fix it where it belongs, cascade up:

```bash
gh stack down                       # or: gh stack checkout <branch>, gh stack bottom
git add <paths> && git commit -m "..."
gh stack rebase --upstack           # replay every branch above onto the fix
gh stack push                       # force-with-lease, handled for you
gh stack top                        # back to where you were
```

`gh stack rebase` alone rebases the whole stack from trunk up; `--downstack` does trunk to current only, `--no-trunk` rebases branches onto each other without fetching trunk. On conflict it stops and lists the files: resolve, `git add`, then `gh stack rebase --continue` (or `--abort` to restore every branch). Hand the conflicts themselves to the `merge-resolver` skill.

### Sync after someone else moves

```bash
gh stack sync --prune
```

Fetch, mirror the remote stack locally, fast-forward trunk, cascading rebase, push, refresh PR state, delete local branches for merged PRs. A remote that is simply *ahead* (teammates added PRs on top) is pulled down without prompting, so this is safe in automation. Genuine **divergence** (you added a branch locally while different PRs were added to the same stack on GitHub) aborts non-interactively; resolve by unstacking and recreating.

### Restructure

`gh stack modify` is an interactive TUI (drop, fold up/down, insert, reorder, rename) and therefore **not agent-operable**. Non-interactively:

```bash
gh stack unstack            # dissolve on GitHub + drop local tracking (--local keeps the remote stack)
gh stack init a c b         # recreate with the structure you want; existing branches are adopted
gh stack submit --auto      # re-link on GitHub, replacing the old stack
```

Merged or merge-queued PRs cannot be unstacked and stay in the stack.

### Merge

> **`gh pr merge` does not work on a stacked PR.** It is the single most likely way to break a stack from muscle memory.

```bash
gh stack merge --yes --squash        # whole current stack, bottom-up, atomically
gh stack merge 42 --yes              # everything up to and including PR #42
gh stack merge 7 --yes               # stack #7, no local checkout needed
```

Rules that follow:

- **Bottom-up only, always contiguous.** Merging a mid-stack PR brings everything below it with it. You cannot land a middle layer in isolation.
- **All-or-nothing.** If any PR in the selected group cannot merge, none of them do, and the reason is reported.
- **Merging is the retarget.** After the group lands, the next unmerged PR is automatically rebased to target the stack base. That is exactly the failure the hand-rolled cardinal rule exists to prevent, and native stacks remove it.
- **Auto-merge is not supported** for stacked PRs. Merge queues are, and take over the merge method (any `--squash`/`--rebase`/`--merge` you pass is ignored with a warning); a stack may then land across consecutive merge groups.
- Only basic PR state (open, not draft) is checked client-side. Merge requirements are enforced server-side and **cannot be bypassed** for stacks.
- Once every PR in a stack has merged, the stack is **complete and cannot be extended**. `gh stack submit` on new branches starts a fresh stack rooted at trunk.

Merging is outward-facing and irreversible. Confirm first, and say which PRs will land.

### Rules and CI

Every PR in a stack is evaluated as if it targets the **stack base** (`main`), not the branch directly below it. Required reviews, required checks, CODEOWNERS and code scanning all apply to mid-stack PRs, so existing branch protections need no changes.

The cost is that a `pull_request` workflow runs **once per PR in the stack**, so an n-layer stack multiplies CI. Gate expensive jobs on the stack metadata, which is present only when the PR belongs to a stack:

```yaml
# only on the lowest unmerged PR (its base is the stack base)
if: github.event.pull_request.stack != null &&
    github.event.pull_request.stack.base.ref == github.event.pull_request.base.ref

# only on the top PR (the full set of changes)
if: github.event.pull_request.stack != null &&
    github.event.pull_request.stack.position == github.event.pull_request.stack.size
```

Fields: `stack.number`, `stack.size`, `stack.position` (1 = bottom), `stack.base.ref`, `stack.base.sha`. The same `stack` object appears on `pull_request` webhook payloads (with a dedicated `stacked` action when a PR joins a stack) and on the REST API, and is `null` for standalone PRs, so existing integrations keep working.

### Limits to check before committing to a stack

- **Same repository only.** Cross-fork stacks are not supported.
- **Linear chains only.** No branching structures.
- **Merging requires the Stacks API.** In-house merge bots and ChatOps calling the legacy merge endpoint cannot merge a stack, and need updating before a rollout.
- **Reordering requires the CLI.** There is no way to reorder a stack from github.com.
- **Server-side rebase produces unsigned commits.** If the repo requires signed commits, run `gh stack rebase` locally instead of clicking **Rebase stack**.
- **Not supported in GitHub Desktop.**

### Coming from jj, Sapling or git-town

Keep managing branches with your own tool and use GitHub only for the stack object:

```bash
gh stack link change1 change2 change3          # bottom → top; pushes, opens draft PRs, links them
gh stack link 123 124 125 change4 change5      # extend: pass the FULL list, existing PRs by number
```

`link` creates no local tracking, so `rebase`, `sync` and navigation are unavailable. For full local tracking use `gh stack init <branches...>` then `gh stack submit --auto` instead.

## Hand-rolled stacks (plain git + gh)

For repos without native stacks, and for chains that already exist. **Map the chain before touching it:**

```bash
gh pr list --repo <owner/repo> --state open \
  --json number,title,headRefName,baseRefName,mergeable,reviewDecision
```

Chain them by `baseRefName == headRefName` down to the PR whose base is `main`. That order is the stack, bottom→top. Anything based on `main` is a bottom.

### The cardinal rule (read before merging anything in a hand-rolled chain)

> **GitHub closes, it does NOT reliably retarget, a PR whose base branch is deleted.** With `delete_branch_on_merge` enabled (common), merging the bottom PR deletes its branch, which silently **closes** the PR sitting on it.
>
> **So retarget the next PR up to `main` BEFORE you merge/delete the branch it sits on:**
> ```bash
> gh pr edit <next-up-PR> --repo <owner/repo> --base main
> ```

Retarget-before-merge makes the auto-close impossible: the dependent now sits on `main`, which never gets deleted. Do not rely on GitHub's documented auto-retarget; it does not fire when the branch is auto-deleted on merge (verified). Check the repo's setting with `gh api repos/<owner/repo> --jq .delete_branch_on_merge`.

**This failure mode does not exist in a native stack**, where merging retargets the layer above automatically. It is the strongest single argument for adopting the chain (see **adopt** below) rather than nursing it.

### Operations

Pick by what the user is doing. Every destructive step (merge, force-push, branch delete, retarget) is **outward-facing**: confirm before each, and never force-push a branch someone else may be reviewing without saying so.

#### status: map and report
Read-only. Run the `gh pr list` map above; print the chain bottom→top with each PR's base, `mergeable`, `reviewDecision`, and whether it is behind `main` (`git rev-list --count origin/main..origin/<branch>`). Surface any PR whose base is a branch that no longer exists (orphaned, see **recover**).

#### sync: bring the chain current with main
`main` moved; propagate it up **bottom-up** with merges (not rebase, since merging avoids force-pushing branches under review):
```bash
git fetch origin
# bottom first, then each branch into the next up the chain:
git checkout a && git merge origin/main   && git push      # bottom ← main
git checkout b && git merge a             && git push      # next  ← bottom
git checkout c && git merge b             && git push      # ...up the chain
```
Resolve each conflict **once, at the lowest layer where it arises**; the merge upward carries the resolution. Hand conflicts to the `merge-resolver` skill. Done when every branch is `behind=0` vs `main`.

#### land: merge the bottom and propagate, safely
For `main ← a ← b`, to land the bottom `a` without closing `b`:
```bash
git fetch origin
ATIP=$(git rev-parse origin/a)                       # 1. capture bottom tip FIRST
gh pr edit <PR-b> --base main                        # 2. retarget dependent to main (cardinal rule)
gh pr merge <PR-a> --squash --delete-branch          # 3. merge bottom (branch deletion now can't close b)
git fetch origin
git rebase --onto origin/main "$ATIP" b              # 4. drop a's commits → b's diff = just b's layer
git push --force-with-lease                          # 5. (force needed: rebase rewrote b)
```
Then repeat from the new bottom up the chain. Rebase (step 4) is what keeps the landed PR's diff scoped to its own layer; the squash-merge of `a` is already in `main`, so replaying only `b`'s commits is correct. Hand any rebase conflicts to `merge-resolver`.

#### recover: a stacked PR was closed or orphaned
The base branch was deleted, so GitHub closed the PR. The **head branch survives** (auto-delete only removes the *merged* PR's head). Recreate against `main` and clean the diff:
```bash
gh pr create --repo <owner/repo> --head <orphaned-branch> --base main --title "..." --body "..."
git fetch origin && git checkout <orphaned-branch>
git rebase --onto origin/main <former-base-tip-sha> <orphaned-branch>   # if the old base SHA is known
git push --force-with-lease
```
If the former base SHA is unknown, `git rebase origin/main` and drop the already-merged commits during the rebase. This is the cure; **land** is the prevention.

#### adopt: turn the chain into a native stack
Worth offering whenever the repo has the preview and the chain still has unmerged layers, because it retires the cardinal rule entirely:
```bash
gh stack link <bottom-pr-or-branch> <...> <top>   # PRs only, no local tracking
# or, for full local tracking:
gh stack init <bottom-branch> <...> <top-branch>  # adopts the existing branches
gh stack submit --auto                            # links them into a stack on GitHub
```
`link` corrects any PR whose base does not match the expected chain, and existing PRs keep their reviews and threads.

## Cross-repo dependencies are not stacks

When the dependency spans repos (a schema PR in repo X must merge before a consumer PR in repo Y works at runtime), there is no shared branch to retarget and no stack to create: stacks require every branch in one repo. Treat it as **merge ordering only**: sequence the merges bottom-up across repos, and gate the consumer's deploy on the dependency. None of the retarget, rebase or `gh stack` mechanics apply.

## Worked example

A two-PR hand-rolled chain and the exact auto-close it caused (plus how the cardinal rule prevents it) are in [EXAMPLES.md](EXAMPLES.md). Read it for a concrete walk-through of the failure native stacks now remove.
