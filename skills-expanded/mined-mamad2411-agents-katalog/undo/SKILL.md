---
name: undo
description: "Reverse a recorded local task while preserving unrelated changes. Use for a recorded local working-tree task; git-commit undoes or reverts a commit, and remote rollback requires its own exact target and authorization."
---

# undo

Reverse a recorded local task while preserving unrelated changes.

## Choose this workflow

Use for a recorded local working-tree task; git-commit undoes or reverts a commit, and remote rollback requires its own exact target and authorization.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [General methods](../../references/packs/general.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply for an explicit undo request against a known local ownership record; preview/inspect requests never write.

**Pack prerequisites:** Resolve the user brief and inspect the relevant project or supplied evidence. External capabilities are optional unless the selected action actually needs them.

- **Infer from evidence:** Resolve the named files, existing scripts, current task and earlier corrections from the conversation and repository.
- **Reasonable default:** Use the narrowest interpretation that completes a reversible local task; state a consequential assumption once.
- **Ask only when needed:** Ask when competing targets or incompatible success conditions would change the result; continue independent inspection first.

Declared evidence requirements: `git.repo`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Selected task ownership record, current Git identity/index and affected file contents.

Only the conflict-free inverse of the recorded task; preserve index and other work. Remote effects and Git history are outside scope.

## Execute

1. Identify the named ownership record using workbench list and task show. Reconcile the requested task, project, original branch/HEAD, external effects and actual current files; never infer ownership from the whole dirty tree.
2. Read the selective task undo guide and run task preview. Inspect affected files and any overlap; unchanged task regions must preserve later user edits. A missing record or ambiguous authorship requires useful Git inspection and a narrow clarification, not a fabricated snapshot.
3. For an authorized, unambiguous undo with no conflicts, run task undo using the exact current revision. Preview-only requests stop with the dry-run result. Do not ask again merely because a reversible requested action writes files.
4. Refuse overlapping creation/deletion/binary edits, changed scoped staging, unknown concurrent file versions or a different branch/HEAD. Recover an interrupted known transaction using task recover after inspecting the journal; do not reset or clean broadly.
5. Run proportionate existing checks on the resulting tree and explain what was reversed, which later changes were preserved, and any external effects that remain. Never add agent attribution to the user-owned changes.

## Technical method

- **Inspect:** Read recorded before/after hashes, owned paths and the current worktree/index, including later edits.
- **Method:** Preview inverse changes and apply only paths whose expected post-task state still matches; preserve conflicts for review.
- **Avoid misdiagnosis:** Whole-repository reset destroys unrelated work; matching a filename alone does not prove the task still owns its contents.
- **Check the result:** Check restored paths, unchanged unrelated files and partial-operation recovery; later modifications must block automatic reversal of that path.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [General worked example](../../references/examples/general.md).
- Recording, previewing, applying or recovering a task inverse: [Selective task undo](../../references/task-undo.md).

## Decision branches

- **When later edits overlap the inverse patch:** Preserve every current file and report the conflict before any initial undo writes.
- **When no ownership record exists:** Inspect a narrowly attributable inverse or ask for missing ownership information; do not invent automatic coverage.

## Deliver and verify

- Task identity, dry-run conflict/affected-file assessment, applied inverse when authorized, preserved later edits, verification and external effects left in place.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A later nonoverlapping edit in the same file survives undo; an overlapping edit blocks all initial writes; the original index remains unchanged.
- An interrupted journal accepts only recorded before/after bytes and refuses a third version.

## Stop and recover

- Unknown ownership, changed branch/HEAD or scoped index, overlapping edits, unsupported files and external effects require explicit reconciliation without destructive Git shortcuts.

## Example requests

- **Normal (apply):** Undo checkout-retry and keep my later copy changes.
- **Edge (inspect):** Preview undo after I edited a different paragraph in the same file.
- **Blocked (inspect):** Undo a change with no ownership snapshot; inspect what is attributable first.
