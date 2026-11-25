---
name: git-diff
description: "Summarize changes by behavior and identify unrelated edits. Use to understand changes against specified refs; review evaluates their correctness."
---

# git-diff

Summarize changes by behavior and identify unrelated edits.

## Choose this workflow

Use to understand changes against specified refs; review evaluates their correctness.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Git methods](../../references/packs/git.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; working/index state or exact base/head refs and desired review focus.

**Pack prerequisites:** Git, exact repository/worktree, and readable refs/index. Record branch, HEAD, staged/unstaged/untracked state before mutation. Preserve unrelated edits and never default to broad staging, hard reset, clean, force push, or history rewriting.

- **Infer from evidence:** Read repository root, HEAD, branch, refs and staged/unstaged/untracked distinctions; use the configured human identity.
- **Reasonable default:** Limit an ambiguous inspection to the current repository and report that scope; preserve all existing changes.
- **Ask only when needed:** Before mutation, resolve uncertain commit membership, destination ref or history-rewrite intent; do not ask again about already authorized exact actions.

Declared evidence requirements: `git.repo`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Selected changes and their behavioral meaning; no staging or editing.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Resolve the requested comparison and its refs, separating index versus HEAD, worktree versus index and branch versus merge-base.
2. Inspect rename, binary and submodule metadata and read surrounding context, then group hunks by purpose and identify unrelated edits.

## Technical method

- **Inspect:** Resolve comparison refs and merge-base, then inspect rename, mode, binary and submodule changes as well as text.
- **Method:** Summarize user-visible behavior and dependencies between hunks; identify which tree each diff represents.
- **Avoid misdiagnosis:** Branch-tip comparison and merge-base comparison answer different questions; text-only review misses executable-bit changes.
- **Check the result:** Cite a representative hunk for each behavior claim and account for changed files outside ordinary source extensions.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Git worked example](../../references/examples/git.md).


## Decision branches

- **When rename, binary or submodule entries appear:** Report their metadata and scope instead of inventing text diffs or flattening submodule changes.

## Deliver and verify

- Comparison refs, files and hunks grouped by purpose, impacted contracts, notable risks, unrelated changes and files requiring deeper review.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Staged and unstaged changes are not conflated; a binary change is acknowledged without invented contents.

## Stop and recover

- Missing comparison refs require resolution. Do not assume every change belongs to the current task.

## Example requests

- **Normal (inspect):** Summarize the diff against main and identify unrelated edits.
- **Edge (inspect):** Explain a file with different staged and unstaged edits.
- **Blocked (inspect):** Compare against a missing base ref without guessing main or fetching.
