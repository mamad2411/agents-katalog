---
name: intent-plan
description: Decompose a multi-contract or unclear implementation into dependency-ordered Git work units, stabilize shared contracts first, and optionally create local branches, worktrees, plans, and claims under the repository execution mode.
---

# intent-plan

Turn uncertainty about implementation order into a bounded execution graph. Do not ask the human
merely because the build path is unclear.

## Invocation

```text
/intent-plan <goal> [--scope dotted.scope] [--execute]
```

Use this skill when work crosses multiple contracts, contains independently buildable units, has
unclear sequencing, or is likely to create later integration conflicts. Skip it for one obvious
unit.

## Plan

1. Compile `intent-check` for the overall goal.
2. Inspect the narrow routed contracts and current repository structure. Do not inventory the
   repository or load unrelated intent state.
3. Define one node per independently verifiable output. Every node needs:

   - a narrow goal and semantic scope;
   - inputs and promised outputs;
   - governing brief rows;
   - owned paths or named interfaces;
   - verification and rollback;
   - dependencies and consequence classification.

4. Add dependency edges for produced contracts, shared migrations, generated artifacts, and
   required integration fixtures.
5. Stabilize shared contracts before producer and consumer nodes diverge. Parallelize leaves with
   disjoint outputs. Serialize shared-interface mutations and repository hotspots.
6. Minimize convergence points. Prefer a small contract-setting unit followed by independent
   consumers over several branches inventing the same boundary.

Path overlap affects scheduling but is not a semantic conflict. Implementation uncertainty
triggers exploration in an isolated node. Use the decision interview only when the consequence
gate identifies a consequential unresolved choice.

## Runtime state

When execution is requested and authorized, write an ephemeral plan under
`<git-common-dir>/intent/plans/<plan>.yml`. It may contain node ids, branches, worktrees,
dependencies, scopes, interfaces, checks, and landing order. Never commit it or put task summaries
and general reasoning in tracked intent state.

Create a local branch and linked worktree per parallel node, using repository branch conventions.
Create matching claims automatically. Do not create worktrees for sequential nodes that are
cheaper to implement in one branch.

Respect `.intent/config.yml`:

- `advisory`: emit the graph and exact commands only.
- `assisted`: create local worktrees when the current task authorizes implementation; ask before
  merging to the integration branch.
- `autonomous`: create local worktrees and hand the completed graph to `intent-land` without a
  routine merge confirmation.

The config does not authorize pushes, deployments, publishing, destructive cleanup, or external
side effects.

## Output

Render the graph compactly with units, dependencies, contracts, parallel groups, and landing
order. If `--execute` was used, also report created branches, worktrees, claims, and the runtime
plan path. Then implement the nodes or dispatch them through the caller's available execution
mechanism.
