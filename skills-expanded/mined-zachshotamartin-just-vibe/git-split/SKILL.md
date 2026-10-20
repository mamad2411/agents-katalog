---
name: git-split
description: "Divide a mixed change into understandable commits. Use to separate a change into coherent commits; git-commit handles one selected unit."
---

# git-split

Divide a mixed change into understandable commits.

## Choose this workflow

Use to separate a change into coherent commits; git-commit handles one selected unit.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Git methods](../../references/packs/git.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; mixed changes or commits and desired grouping. Applying a split uses apply mode and creates new commits only on the current unpublished branch.

**Pack prerequisites:** Git, exact repository/worktree, and readable refs/index. Record branch, HEAD, staged/unstaged/untracked state before mutation. Preserve unrelated edits and never default to broad staging, hard reset, clean, force push, or history rewriting.

- **Infer from evidence:** Read repository root, HEAD, branch, refs and staged/unstaged/untracked distinctions; use the configured human identity.
- **Reasonable default:** Limit an ambiguous inspection to the current repository and report that scope; preserve all existing changes.
- **Ask only when needed:** Before mutation, resolve uncertain commit membership, destination ref or history-rewrite intent; do not ask again about already authorized exact actions.

Declared evidence requirements: `git.repo`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Separate coherent changes while preserving content; rewriting published history is a distinct action.

Inspect/plan: propose the grouping; save requested artifacts only. Apply: create the new commits only on the current, unpublished branch after preserving the original patch and index. Rewriting pushed or shared history, force-pushing and other remote actions require their exact action and target in session authorization.

## Execute

1. Snapshot the current state, preserving the original patch and index.
2. Map hunks to behaviors and dependencies and propose a commit ordering; validate each proposed intermediate tree in isolation when feasible.
3. In apply mode, create the grouped commits and verify the final content matches the original.
4. All changes are owned by the user. Add no agent/model self-attribution, AI-generated signature, badge, or agent Co-authored-by trailer to commits, PRs, comments, release notes or messages. Use the existing user Git identity; preserve legitimate human attribution and required third-party notices.

## Technical method

- **Inspect:** Inspect overlapping hunks, generated files, dependency order and pre-existing staged content.
- **Method:** Build an ordered series whose intermediate trees are coherent; regenerate derived artifacts from the matching source change.
- **Avoid misdiagnosis:** Splitting by filename alone can leave a commit importing an API that appears only in the next commit.
- **Check the result:** Check each candidate tree independently where required, then verify the union matches only the intended changes and preserves unrelated work.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Git worked example](../../references/examples/git.md).


## Decision branches

- **When inseparable hunks cross proposed commits:** Adjust boundaries or keep them together rather than producing a broken intermediate commit.

## Deliver and verify

- Ordered commit groups with dependency rationale, or the resulting commits, plus evidence the final content is preserved.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Formatting and functional edits separate cleanly; overlapping hunks retain both intended behaviors.
- Review newly prepared commit/PR/message text, including template or hook additions, for agent self-attribution before submission; verify the resulting artifact when available. Do not silently rewrite existing history or remove human credits.

## Stop and recover

- Do not rewrite shared history implicitly or lose pre-existing index state. Stop if grouping cannot preserve a buildable dependency order.

## Example requests

- **Normal (plan):** Plan separate formatting and checkout-fix commits without changing shared history.
- **Edge (apply):** Split a refactor and fix that overlap in one function.
- **Blocked (inspect):** Propose a split without permission to rewrite shared history.
