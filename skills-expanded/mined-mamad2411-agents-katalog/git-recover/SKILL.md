---
name: git-recover
description: "Investigate reflog and history to recover lost work. Use to find and preserve lost Git content; git-conflicts resolves an active operation."
---

# git-recover

Investigate reflog and history to recover lost work.

## Choose this workflow

Use to find and preserve lost Git content; git-conflicts resolves an active operation.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Git methods](../../references/packs/git.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; lost commit/file symptom, approximate event, and repository. Restoring uses apply mode and writes only a new preservation ref.

**Pack prerequisites:** Git, exact repository/worktree, and readable refs/index. Record branch, HEAD, staged/unstaged/untracked state before mutation. Preserve unrelated edits and never default to broad staging, hard reset, clean, force push, or history rewriting.

- **Infer from evidence:** Read repository root, HEAD, branch, refs and staged/unstaged/untracked distinctions; use the configured human identity.
- **Reasonable default:** Limit an ambiguous inspection to the current repository and report that scope; preserve all existing changes.
- **Ask only when needed:** Before mutation, resolve uncertain commit membership, destination ref or history-rewrite intent; do not ask again about already authorized exact actions.

Declared evidence requirements: `git.repo`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Find recoverable history and prepare non-destructive restoration; no reset by default.

Inspect/plan: locate candidates and describe restoration steps without writing. Apply: create only a new preservation ref (branch or tag) for the chosen content, or a copy of a recovered file outside tracked paths; never move the active branch, reset, rewrite history or run garbage collection.

## Execute

1. Inspect reflog, refs, stashes and reachable candidates, then unreachable objects with read-only git fsck --unreachable --no-reflogs (stash commits are merge commits titled WIP on or On); avoid commands that may trigger automatic garbage collection until the candidate is preserved.
2. Compare candidate file contents and explain confidence.
3. In apply mode, when restoration is requested, preserve the chosen commit with a new ref or copy before any active-branch movement.

## Technical method

- **Inspect:** Inspect reflogs, stashes, reachable refs, unreachable objects from git fsck and candidate object contents before changing active refs.
- **Method:** Preserve a verified candidate with a new branch or copy, then explain how it differs from current work.
- **Avoid misdiagnosis:** Reflogs expire and may not exist for another clone; garbage collection can remove the very objects being recovered.
- **Check the result:** Verify the recovered tree contains the requested content and leaves the original branch, index and worktree recoverable.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Git worked example](../../references/examples/git.md).


## Decision branches

- **When the candidate is absent after the reflog, ref, stash and unreachable-object search:** State the recovery limit only then, and avoid cleanup that could reduce recoverability.

## Deliver and verify

- Candidate identities with confidence, exact preservation/restoration steps or the recovered location, and the preserved current state.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A lost commit can be preserved without moving the active branch; absent recovery evidence is not claimed as recoverable.

## Stop and recover

- Do not run garbage collection or destructive cleanup during recovery. Preserve current work before any authorized restore.

## Example requests

- **Normal (inspect):** Find a lost commit in reflog without resetting the current branch.
- **Edge (apply):** Recover a dropped commit without moving the current branch.
- **Blocked (inspect):** Inspect recovery options after missing reflog history; do not promise restoration.
- **Edge (inspect):** Find stash entries lost after git stash clear without running garbage collection.
