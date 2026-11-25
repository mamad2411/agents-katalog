---
name: repo-delivery
description: "Execute authorized Git commits, pushes, integration, history changes, or cleanup."
---

# Repository Delivery

## Entry Gate

Own authorized Git mutation only. Require exact target repository/branch, mutation
scope, reviewed basis, and any required destination authorization; preserve unrelated
Worktree changes and stop on ambiguous scope or failed preflight.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Commit, push, sync, integration, cleanup, or local checkpoint | [checklist](references/checklist.md) | Exact, authorized Git transition |
| A large authorized task is still in progress and needs durable milestones | [execution durability](references/execution-durability.md) | Bounded milestone/fixup/checkpoint state |
| Conflicts or divergent-history strategy is actually needed | [resolving merge conflicts](references/resolving-merge-conflicts.md) | Resolved/blocked integration path |
| Fixup/checkpoint normalization is authorized | [history normalization](references/history-normalization.md) | Tree-proven normalized history |
| Catalog release applies | [skills release](references/skills-release.md) | Fixed-basis catalog delivery |
| Need final report | [delivery report](references/delivery-report.md) | Evidence-bounded outcome |

## Invariants

- No commit/push/integration/cleanup follows from implementation or review wording alone.
- Stage only frozen exact paths; never use broad pathspecs or hide unrelated dirty content.
- Ordinary commit/push does not require a merge strategy; apply it only for actual divergent integration.
- For integration, honor effective project and host guidance first. Without a contrary rule, use a non-squash rebase onto the fixed target tip, preserving commit order; judge publication or consumption from the source-only commits actually replayed, and let an authorized ordinary rebase with no conflict or sensitive semantic overlap proceed directly; the strategy never authorizes the Git mutation.
- Report local and remote refs separately; never claim publication, merge, or runtime installation without evidence.

## Output Map

Report authorized mode, basis, exact staged scope, validation/review state, local SHA,
remote result if applicable, residual Worktree, and every unverified boundary.

## Reference Map

- Read [checklist](references/checklist.md) for every mutation. Read [execution durability](references/execution-durability.md) only for the in-progress large-task route; ordinary completed-change commit/push does not load it.
- Read [resolving merge conflicts](references/resolving-merge-conflicts.md), [history normalization](references/history-normalization.md), [skills release](references/skills-release.md), and [delivery report](references/delivery-report.md) only when their route applies.
- Read [usage](references/usage.md) for modes/boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
