---
name: worktree-lanes
description: Establish and coordinate Git worktree lanes before repository work. Use when operating in a linked worktree, when multiple worktrees or parallel agent sessions exist, or when work may contend for project-declared shared resources. Also matches everyday phrases such as grouped workspace or main worktree. Do not use for ordinary single-checkout Git work.
---

# Worktree Lanes

Treat each worktree as an operational lane. Establish lane identity before
acting, then obey the repository's lane contract without assuming that a
branch named `main`, a container runtime, or a particular worktree manager
exists.

Read [the canonical terminology](references/terminology.md) before producing a
lane census.

Read [manager workspaces](references/manager-workspaces.md) only when a
terminal or session manager is used to inspect, create, operate, or close lane
state, or when the environment, the lane contract, or an inventory indicates
existing manager state. Read it before the first manager action or lane
closure. Git-only work with no such indication does not load it.

## Establish the lane census

Before the first repository-affecting action:

1. Read all applicable repository instructions.
2. Confirm that the current directory belongs to a Git worktree. If it does
   not, stop applying this skill.
3. List the repository's worktrees read-only. Stop applying this skill only
   when exactly one worktree exists and neither the request nor the repository
   instructions indicate worktree coordination, parallel sessions, or
   project-declared shared-resource coordination. Otherwise continue with the
   rules that apply.
4. Inspect local Git state without fetching, switching, stashing, or changing
   refs. Resolve:
   - the current worktree root and branch or detached commit;
   - the Git common directory and primary worktree;
   - every linked worktree and its branch or detached commit;
   - cleanliness and local divergence where the required refs already exist.
5. Resolve the integration branch in this order: an explicit operator choice,
   the repository's lane contract, the current pull request's base, then the
   remote default branch already recorded locally.
6. Discover the repository's lane contract in its applicable agent
   instructions, development documentation, task runner, or worktree tooling.
   Identify only resources and ownership checks that the project explicitly
   declares. Do not infer that Docker, secrets, databases, ports, or caches are
   shared merely because they exist. When no contract is found, report
   `none-found`, treat every shared resource as `unknown`, and follow
   [lane contract](references/lane-contract.md) only if the operator asks for
   one. When running a declared ownership check would execute branch code,
   read the same fact read-only instead (a container's mounts, a lock file)
   and name that source in the census. When the contract's own checks fail
   before any lane action (an unsupported tool version, missing hook
   approvals), stop and report them.
7. Report the lane census before proposing a lane-sensitive action.

```text
Lane census
- Current lane: <branch-or-detached> at <worktree-root>
- Primary lane: <branch-or-detached> at <primary-worktree-root>
- Integration branch: <branch-or-unknown>
- Other linked lanes: <list-or-none, each with its commits not on the integration branch and whether they are pushed>
- Current tree: <clean-or-summary>
- Shared resources: <owners-and-state, none-declared, or unknown>
- Lane contract: <source-or-none-found>
```

The lane census is complete only when every field is filled, using `unknown`
or `none` rather than a guess or an omission. Keep the current lane, primary
lane, and integration branch on separate lines even when they are equal. Use
the full template every time, including after the conversation has been
summarised: a one-line census is incomplete.

## Operate within the lane

- Perform writes only in the current lane unless the operator explicitly
  directs work elsewhere.
- Treat another lane's branch, files, processes, and resource claim as active
  work. Read across lanes only when needed to establish state or compare a
  contract; do not clean up or repair another lane opportunistically.
- Opening another pane or starting another agent in the same worktree creates
  neither a new lane nor write isolation. Default to one writing agent per
  lane, and use separate worktree lanes for parallel writers. When every
  writer's checks need one shared resource that only one lane can own at a
  time, prefer one lane and run the writers in sequence.
- Keep same-lane helpers to bounded read-only investigation or review; name
  each one's lane, role, working directory, authority, prohibitions, and stop
  condition.
- A **scratch helper** may also run beside the lane's writer. It changes
  nothing in the worktree, its Git metadata, or a declared shared resource,
  and writes only to its own scratch path outside the worktree, named in its
  instructions and read by none of the writer's builds, tests, or tools. State
  its authority as "scratch writes to `<path>`", not as read-only. Start it in
  a read-only mode with only that path writable when its harness allows, and
  confirm the worktree is unchanged after it stops.
- Run multiple writers in one lane only with explicit operator direction and
  non-overlapping file and process scope, and state each one as a writer. An
  agent that runs the lane's branch code against a shared resource or external
  system counts as a writer, even when it changes no file in the worktree.
- Run a lane's Git commands one at a time: a `git fetch` and a `git pull` run
  in parallel race on the same ref lock.
- Serialize operations that can affect a shared resource or external system
  across all agents in a lane, including read-only helpers.
- Treat worktree lanes as concurrency isolation, not security sandboxes.
  Branch code in a lane can access every credential and service available to
  its process.
- Before executing branch-controlled code that can affect a shared resource,
  verify that the current lane contains the lane contract governing that
  resource. If the contract may be stale, compare it read-only with the
  integration branch and stop on a material mismatch.
- Use only project-declared ownership checks and claim commands. A busy,
  unreachable, ambiguous, or differently owned resource is a refusal, not an
  invitation to kill processes or override ownership.

## Authorization boundaries

- A claim transfers ownership, which is a mutation. Perform one only when the
  operator or a lane contract explicitly authorizes agents to perform it; a
  lane census or closure readiness never implies it.
- A claim does not authorize rebuilds, refreshes, migrations, deployments, or
  server access.
- Installing worktree managers, plugins, or other tools is outside this skill.
  It belongs to the project's own installer and needs explicit operator
  approval. So does changing a tool's configuration outside the worktree,
  such as recording a worktree manager's hook approvals.
- Rebase, force-push, merge, deploy, credential movement, worktree or branch
  removal, other destructive cleanup, and external mutations require explicit
  operator authorization, which covers only the lane it names.
- To update another author's branch from the primary lane, with operator
  authorization, check it out detached, create no local branch, push only as
  a fast-forward (`git push origin HEAD:refs/heads/<branch>`), then switch
  back to the integration branch.

## Hand off a shared resource

Merging a pull request performs no handoff. Before the primary lane receives
a shared resource after integration, establish that its checked-out commit
contains the integrated work and that its tree is clean. If either is false
or cannot be established without fetching, stop and report; updating the
primary lane is a separate action requiring operator authorization. Then
follow these steps, stopping at the first one that is unsupported, ambiguous,
or fails.

1. Identify the shared resource, its resource owner, and the receiving lane
   from the lane contract and the lane census.
2. Verify with the project-declared ownership check that the owner is idle or
   that the resource has no owner.
3. Perform the project-declared claim.
4. Repeat the ownership check. The handoff is complete only when it names the
   receiving lane as resource owner; run no dependent work before then.

## Close a lane

A lane is ready to close only when each item is observed:

- **Work preserved:** choose a named evidence ref that every authorized action
  will retain, including action side effects. For ancestry-based integration,
  observe that the lane HEAD is an ancestor of the ref's resolved commit, then
  record the lane HEAD, ref, and resolved commit. For squash, rebase, or another
  non-ancestry method, use patch-equivalence evidence against a named ref that
  meets the same retention rule, or record the operator's verification. A ref
  is not retained when remote-branch deletion will also remove its local
  remote-tracking ref. A push result, pull request, or CI status alone does not
  prove preservation.
- **Tree clean:** status is clean, and ignored files that removal would
  discard are reported.
- **No running process:** a project-declared process or manager inventory
  shows none launched from the lane. Without such an inventory, report
  unknown.
- **No shared resource owned:** hand off any it owns first.

Report each item. If any is unmet or unknown, stop before removing an existing
worktree. When the checkout path is already absent, no path remains to remove:
report the items that cannot be observed, and clean up only stale records that
are separately inventoried and authorized. If manager state exists, follow
[manager workspaces](references/manager-workspaces.md).

## Work with other coordination skills

When another coordination skill is active, include the intended worktree lane
in every actionable prompt and handoff. Do not duplicate this skill's lane
rules in that coordination skill.
