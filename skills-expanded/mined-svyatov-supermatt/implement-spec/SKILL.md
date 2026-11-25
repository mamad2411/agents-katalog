---
name: implement-spec
description: "Implement a whole spec through parallel ticket worktrees on one integration branch."
argument-hint: "[spec path or issue reference]"
disable-model-invocation: true
license: MIT
---

Implement the supplied spec and its tickets on one **integration branch**, ready for a single pull request. Use the host's native subagents and git worktrees; Herdr is not required. Keep communication sparse: pass pointers to the spec, tickets, commits, and evidence instead of repeating their contents.

## 1. Pin the spec and task graph

Read `docs/agents/issue-tracker.md`, then use its operations to read the spec, every child ticket, and their blocking relationships. If the tracker instructions are missing, tell the user to run `/setup-supermatt-skills` in Claude linked installs or Cursor, `/supermatt:setup-supermatt-skills` from the Claude plugin, `$setup-supermatt-skills` in Codex, or `/skill:setup-supermatt-skills` in OMP, then stop.

Use the child implementation tickets as the nodes of the graph. Include every state: if the tracker's child query filters to open issues, repeat the lookup across all states, including native and body-linked children. An incomplete lookup blocks graph construction. When the tracker confirms there are no implementation tickets:

- If the issue carries a configured triage state that rules out agent work, such as `ready-for-human` or `wontfix`, report the conflict and stop for a maintainer decision.
- If the spec is a tracker issue that fits one session and has either acceptance criteria or the configured `ready-for-agent` role, use that issue as the sole ticket. Keep its tracker reference and blocking relationships.
- For any other spec without tickets, tell the user to run `/to-tickets` in Claude linked installs or Cursor, `/supermatt:to-tickets` from the Claude plugin, `$to-tickets` in Codex, or `/skill:to-tickets` in OMP, then stop.

Build a **task graph** with ticket states `pending`, `running`, `integrated`, and `blocked`. Keep it with the worker assignments, branch names, commit SHAs, and evidence paths in an OS temporary directory outside the repository. A closed ticket counts as integrated only after verifying its implementation is in the integration branch. Surface contradictory criteria before implementation. For Linear, read explicit blockers outside the spec, including cross-project links, without changing them. A verified `completed` workflow type satisfies an external dependency, including work delivered outside this repository. A canceled in-spec ticket blocks the run. For other trackers an open blocker outside this spec stays blocked until its work is merged into the default branch. A dependency cycle needs a user decision.

The **frontier** contains pending tickets whose prerequisites are all present on the integration branch. For a Linear blocker outside this spec, verified `completed` status satisfies that prerequisite even when the work lives outside this branch. Within this run, a ticket becomes integrated after step 3 verifies its merge. That makes its in-spec dependents eligible for this integration branch even though its tracker issue stays open. This is branch-local evidence only. It never satisfies an external Linear dependency or changes a Linear ticket's state. An empty frontier with unfinished tickets and no running worker is blocked, not complete: report the blocking edges and stop.

## 2. Prepare the integration branch

Discover the default branch and record its current commit as `BASE`, the fixed point for final QA and review. Create a branch from it using the repository's naming convention in a dedicated worktree. Preserve the caller's existing work and branches. If the user supplied an existing integration branch, inspect it, record its merge-base with the default branch as `BASE`, and reconcile the graph against its actual commits before assigning work.

Create each worker's worktree on its own new branch from the current integration tip. Verify that starting commit before dispatch; if the base is wrong, preserve the worktree and correct the assignment instead of resetting existing work. Start a new implementer for each ticket with only its brief and the referenced evidence. Select a fresh context when the host defaults to forking the coordinator's conversation. Keep that worker for fixes and integration of its own ticket. Respect the host's available subagent slots. Without fresh workers, use fresh sessions sequentially where possible. Otherwise work one ticket at a time, keep the worktree and verification steps, and report the context limitation.

## 3. Build and integrate the frontier

Before dispatching parallel workers, read [Parallel resources](../../references/parallel-resources.md) and record their resource ownership with the task graph. Dispatch frontier tickets only where their edits and mutable resources can proceed independently. Give each implementer its ticket, relevant spec sections, worktree, starting SHA, resource assignment, and this contract:

- Work only in the assigned worktree. Load and follow the `tdd` skill through the host's skill mechanism at the agreed test seams. For a refactor without tests, first pin current behavior with characterization tests in a separate commit.
- Before changing data contracts, state transitions, shared mutable state, or retryable effects, load `codebase-design` through the host's skill mechanism. Follow its state-contract guidance for the affected behavior.
- Use focused checks during TDD cycles. Before committing a completed behavior, complete the repository's full required gate. Reuse passing checks only when their relevant files, dependencies, configuration, and environment are unchanged.
- Commit the completed work with the ticket reference. Report the commit SHA, acceptance-criterion coverage, check results, evidence paths, and any unresolved question. Leave tracker issues open and let the coordinator integrate the branch.

The coordinator owns a **single merge slot**. When a worker finishes, hold that slot while it brings the latest integration tip into its branch. Resolve conflicts by loading and following the `resolving-merge-conflicts` skill through the host's skill mechanism in that worktree, then rerun checks invalidated by the merge, including the full required gate on the combined code. A failed check or unresolved question keeps the ticket out of the integration branch.

Wait for the worker and its subagents to finish writing. In the integration worktree, merge the verified worker commit with `git merge --ff-only`. If the integration tip advanced, sync and verify the worker again before retrying; never force the branch forward. Verify that the reported commit is now an ancestor of the integration tip, record its evidence, mark the ticket integrated, and release the merge slot. Recompute the frontier and dispatch newly eligible tickets. A merge into this branch does not close a tracker issue.

After the first successful merge, open a draft PR only if the tracker closes work through PRs or the user requested one. Target the default branch, reference the spec and all tickets it will finish, and load and follow the `pr` skill through the host's skill mechanism for the body. Keep one PR for the integration branch. Without a PR, retain the branch for the later shipping step.

## 4. Verify the whole spec

Once every ticket is integrated, run the repository's full required gate on the final integration commit, reusing unchanged valid results. Then run these checks in order:

For independently evolving providers and consumers, first identify the spec's authoritative contract and owner. Check actual serialized responses and consumer fixtures against that same artifact, including relevant errors, null values, mocks, and feature-flag paths. A matching mock or separately declared type alone does not verify the boundary. Missing ownership or contradictory contracts leave the affected acceptance criteria unresolved. Components changed and built atomically can use their existing shared type; add no contract tool without a demonstrated gap.

1. In a fresh subagent, load and follow the `qa` skill through the host's skill mechanism against `BASE` and the whole spec, including cross-ticket behavior. Pass working preview details and tell it to report without editing the repository or tracker. Without subagents, run QA yourself and state the independence limit. Fix each fail through `tdd`, commit, and repeat QA with the prior report, tested SHA, and fix diff. Keep evidence in the OS temporary directory.
2. Load and follow the `code-review` skill through the host's skill mechanism against `BASE`, with the whole spec and ticket references. Wait for its aggregate verdict; an individual reader's output is not the final review.
3. Resolve every verified finding at every severity. Fix behavior changes through "tdd" and keep behavior-preserving refactors separate. A fix that contradicts the spec or needs an external change goes to the user; a finding is settled only by a fix or an explicit user decision. Complete the required gate for fixes, run follow-up QA for affected behavior, then follow-up "code-review" from the last reviewed commit with the prior reports. Retain valid evidence for unaffected behavior; a test-only fix does not require fresh browser QA.

Ready means the entire spec is integrated, required checks pass, QA has no fails or blocked scenarios, every review axis completed, and every verified finding is fixed or explicitly settled by the user. If a check cannot run or work remains blocked, retain the draft state and report the exact gap. Update the PR evidence with the final commit and verdicts before marking it ready.

## 5. Hand off and clean up

Leave the integration branch, its worktree, and any PR available for shipping. Keep the spec and ticket issues open. Hand shipping the explicit references the PR resolves, including the spec only if every acceptance criterion is met. For Linear, shipping verifies completion after post-merge checks. When ready, tell the user to run `/ship-pr` in Claude linked installs or Cursor, `/supermatt:ship-pr` from the Claude plugin, `$ship-pr` in Codex, or `/skill:ship-pr` in OMP. This skill does not invoke that user-only skill or merge the PR.

Before removing a worker worktree, retain its reports and session references, confirm the worker and its subagents have exited, verify a clean tree, and verify all its commits are reachable from the integration branch. Remove only worktrees created by this run that meet those conditions. Retain dirty, unmerged, or failed worktrees and name them in the handoff; never force removal. Apply the same lifecycle rule when a run stops early.

Report the integration branch and commit, PR URL if any, integrated and blocked tickets, QA and review verdicts, retained evidence, and worktrees that remain. Before the user clears the session, recommend `/retro` in Claude linked installs or Cursor, `/supermatt:retro` from the Claude plugin, `$retro` in Codex, or `/skill:retro` in OMP, or pass the session logs for a later retrospective.

Adapted from Matt Pocock's [implement-spec at v1.3.1](https://github.com/mattpocock/skills/blob/v1.3.1/skills/engineering/implement-spec/SKILL.md).
