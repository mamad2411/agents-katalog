---
name: close-feature
description: Finalize a completed Beads feature by reconciling documentation, validating delivery, recording implementation, reviewing drift, and executing `pr`, `merge`, or `ready`. Use when asked to close a feature, prepare it for delivery, or reconcile implementation and documentation after its implementation coordinator closes.
metadata:
  version: "0.5.9"
allowed-tools: Read Glob Grep Edit Write Bash Task AskUserQuestion
---

# Purpose

Use this skill after the lifecycle implementation coordinator closes. Accept the same human feature selectors as
`/start-feature`. It converts delivered code into reconciled, validated, auditable product state. Resolve `<core-dir>`
as the installed `../dstack-core` skill directory.

## Shared trust contract

Before executing this workflow, read and follow
[`../dstack-core/references/TRUST-AND-AUTHORITY.md`](../dstack-core/references/TRUST-AND-AUTHORITY.md). That contract is
normative for this workflow. If it conflicts with this skill, follow the more restrictive rule and report the conflict.

Delivery authority:

- Invocation authorizes local reconciliation, validation, workflow commits, and Beads updates for the selected feature.
- Only explicit `pr` mode authorizes pull-request creation. Only explicit `merge` mode authorizes merge and post-merge
  worktree removal. `ready` and no-action mode authorize neither.
- Merge mode authorizes a fast-forward-only merge by default. A merge commit is authorized only when the target
  repository's `AGENTS.md` explicitly states that merge commits are accepted.
- The workflow never force-pushes, deletes a remote branch, bypasses hooks, or removes a worktree before a confirmed
  merge.
- Holistic-review subagents are read-only.

## Supported Actions

- `pr`: create a pull request after successful close-out.
- `merge`: merge after successful close-out and finalize the feature.
- `ready`: leave the feature ready without PR or merge.
- no action: complete close-out, then ask the user to choose `pr`, `merge`, or `ready`.

## Execution

## 1. Activate and Inspect

Run `bd prime`, then resolve the supplied feature selector. When the selector is omitted, infer it only from an active
`feat/<slug>` branch. If the current branch is not a feature branch, stop and require a selector rather than closing
unrelated ready work:

```bash
branch=$(git branch --show-current)
feature_selector=${branch#feat/}  # only when branch matches feat/*
uv run <core-dir>/scripts/resolve-feature.py "<feature-selector>" --json
bd show <resolved-root-id> --json
```

Use the returned root ID for Beads operations and its canonical `<slug>` reference for worktrees, reports, and delivery
commands. Resolve `docs_reconcile_id`, `validation_id`, `review_delivery_id`, `review_drift_id`, and `delivery_id` from
root metadata. Query the full molecule or child list only to repair missing metadata. Activate and verify `feat/<slug>`.
Inspect commits, implementation, tests, and changed files before deciding whether documentation is accurate.

Continue only after all lifecycle IDs resolve, the active worktree is `feat/<slug>`, the implementation coordinator is
closed, and no open `migration:reconciliation` task blocks close-out.

## 2. Reconcile Documentation

Claim the documentation-reconciliation step. Compare delivered behavior with:

- feature `design.md`;
- every exact page named in Documentation Impact;
- every reader-facing page changed by implementation;
- relevant architecture and reference pages;
- `docs/src/planned-features.md`;
- `docs/src/features/index.md`;
- `docs/src/SUMMARY.md`.

Create or update:

```text
docs/src/features/<slug>/index.md
```

Use `docs/src/features/_template/index.md`. The record must stand alone; it may link to `design.md` but must not embed
`design.md` or a legacy `tasks.md`. Ensure the design is registered between the feature-design markers in `SUMMARY.md`,
then add the implemented record between the implemented-feature markers in both `SUMMARY.md` and `features/index.md`.

Record delivered behavior, intentional changes, corrected drift, deferred work, documentation paths, commits, and
evidence in the reconciliation bead.

## 3. Validate

Claim the validation step. Classify every required check as `passed`, `failed`, `unavailable`, `waived`, or
`not-applicable`. Run `uv run scripts/check-docs.py`, repository-wide checks, and every feature-specific command named
by the design or implementation beads. Record commands, outcomes, skipped checks, and limitations. Treat these results
as valid only for the exact files and commit tested; any later holistic-review fix invalidates the affected results. Do
not close validation until required evidence is complete and current. `unavailable` remains blocking unless the user
explicitly waives that exact check. A waiver must record the command, reason, affected commit, accepting user decision,
and residual risk.

## 4. Build Context Once, Then Run Two Holistic Reviews

Launch exactly one fresh, read-only context builder. Store its packet in the subagent run's ephemeral artifact
directory, never in the repository. The factual packet covers feature authority, reviewed requirements, implementation
diff, architecture and reference contracts, reader documentation, implemented record, roadmap/navigation, Beads history,
and validation evidence with exact source locations. It contains no findings, recommendations, or verdict.

Then launch exactly two reviewers with `context: fresh`, giving both the same packet and their distinct roles below.
Each reviewer reasons independently, verifies evidence critical to its role, and reads additional source only when
needed. Do not add confidence reviewers without a distinct uncovered risk or an explicit user request.

### Delivery Reviewer

Review correctness, failure behavior, security-sensitive changes, maintainability, test quality, and delivered-scope
compliance.

### Drift Reviewer

Compare implementation, design, reader-facing docs, architecture decisions, reference contracts, implemented-feature
record, roadmap, and Beads history. Distinguish intentional evolution from accidental drift.

Claim the matching review task and record each finding and resolution. Resolve actionable findings. Resume only the
reviewer whose domain changed: delivery for code/tests/failure/security changes, drift for design/docs/roadmap/Beads
changes, or both for cross-domain fixes. Refresh the shared packet only after broad design, architecture, task-graph, or
documentation-structure changes. Launch a fresh replacement only when the original cannot be resumed or the fix
materially changes that role's scope; provide the original packet, findings, resolutions, and post-review diff.

After the final review fix, rerun every affected formatter, linter, build, test, feature-specific command, and
`uv run scripts/check-docs.py`. Update the validation bead with the post-fix commands and outcomes; do not reuse pre-fix
results. Close each review and the validation step only when no actionable finding remains and validation reflects the
final worktree state.

## 5. Commit Reconciliation

Run `git status --short`; identify pre-existing or out-of-scope changes and exclude them from the commit. Commit final
code, tests, documentation, and audit-record changes. Include the feature root ID in the commit message. Record the
commit SHA and review outcomes in Beads. Close-out is ready when the delivery step is the next ready item.

## 6. Choose Delivery Action

When no action was supplied, ask exactly one question:

```text
create PR
merge
leave ready with no delivery action
```

### `ready`

Add `delivery:ready`, record the reconciliation commit, and leave delivery/root open.

### `pr`

Create the pull request with `gh pr create`, record its URL, add `delivery:pr-open`, and leave the root open until merge
is confirmed.

### `merge`

Read the target repository's `AGENTS.md` merge policy. Resolve the worktree that has `<base-branch>` checked out from
`git worktree list --porcelain`; do not assume the current directory is the base worktree. Verify its branch and require
a clean worktree without stashing, deleting, or including unrelated changes:

```bash
git -C <base-worktree> branch --show-current  # must equal <base-branch>
test -z "$(git -C <base-worktree> status --porcelain)"
git -C <base-worktree> merge --ff-only feat/<slug>
git -C <base-worktree> merge-base --is-ancestor feat/<slug> <base-branch>
```

If the base worktree is missing, dirty, or on another branch, stop before merging. If `--ff-only` fails, report that the
feature must be updated or rebased; never fall back to a merge commit. Only an explicit repository policy in `AGENTS.md`
may replace this default with a merge-commit flow. User selection of `merge` alone does not authorize a merge commit.

After success, record the fast-forward target (or explicitly authorized merge commit), close delivery, close the feature
root, verify navigation and the implemented record, and remove the worktree. If `dstack.activeFeature` still equals this
feature, clear that repository-local setting after confirmed delivery. Never push or delete a remote branch unless
separately authorized.

Return one readiness state: `ready for delivery`, `ready after reconciliation fixes`,
`blocked by implementation/docs mismatch`, or `blocked by incomplete validation`, together with the canonical feature
reference and human name, root ID, docs, evidence, reviews, commit, action, and Beads changes.
