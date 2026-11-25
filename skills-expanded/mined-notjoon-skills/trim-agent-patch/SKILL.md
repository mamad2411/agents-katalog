---
name: trim-agent-patch
description: Minimize a successful agent-generated Git patch through trajectory-guided removal and test validation. Use when asked to apply TRIM, reduce CodeSlop, or remove unnecessary agent edits without changing tested behavior; do not use for general refactoring or a patch that does not yet pass its validation.
---

# Trim Agent Patch

Reduce a successful patch to a smaller subset of its recorded edits. Remove edits only; do not rewrite or synthesize an alternative solution.

## Preconditions

Before minimizing, establish:

- the target Git repository and base revision;
- the exact patch to minimize, excluding unrelated user changes;
- at least one repeatable, non-destructive validation command that the full patch passes; and
- an ordered edit trajectory, checkpoint patches, or checkpoint commits.

If the full patch does not pass, stop: TRIM is post-processing for successful patches. If no reliable validation command exists, ask for one. If no trajectory exists, state that true trajectory-guided minimization is unavailable and use final-diff hunk minimization only when the user accepts that approximation.

Treat existing uncommitted and untracked files as user data. Never discard, overwrite, stash, commit, or include them unless they are explicitly part of the target patch.

## Fix the validation oracle

Build one validation oracle before trying removals:

- include the user-supplied command and relevant task tests observed in the trajectory;
- preserve the same test inputs for every candidate;
- keep patch-introduced regression tests outside the removable candidate set, or restore an immutable copy before each run; and
- reject destructive, externally mutating, credentialed, or production-facing commands unless the user explicitly authorizes them.

Run the oracle against the complete patch once. Stop if it fails or produces inconsistent results. A candidate must not pass merely because it removed or disabled its own test.

## Reconstruct the reduced trajectory

Prefer explicit checkpoint patches or commits. Otherwise, recover edits from the supplied agent log; for local Codex runs, relevant JSONL files are normally under `~/.codex/sessions/YYYY/MM/DD/`.

Keep only:

- code edits that survive into the final patch; and
- validation requests that separate edit sequences.

Group edits made between consecutive validation requests into an ordered edit sequence. Normalize each atomic edit as its target file plus before-text and after-text. Ignore reads, searches, navigation, commands that do not modify the patch, and edits later reverted or overwritten.

## Minimize in isolation

Operate in a newly created temporary Git worktree based on the resolved base revision. Record its exact path before using it. Reconstruct each candidate from the base and the surviving edit set instead of mutating the user's working tree or repeatedly reverse-applying the final diff.

Default to one reverse chronological pass over edit sequences (sequence-level TRIM-NG):

1. Temporarily omit one surviving sequence.
2. Rebuild the candidate patch.
3. Run the fixed validation oracle.
4. Accept the omission only when every validation passes and the patch has strictly fewer added-plus-deleted lines.
5. Otherwise retain the sequence.

Stop after that pass unless the user requests deeper minimization or the sequence result leaves a clear reason to continue. Then reuse the same procedure, first grouping surviving edits by file and finally considering individual atomic edits. Repeat a level to a fixpoint only when the user requests one-minimality and accepts the additional validation cost.

Skip binary changes and edits that cannot be replayed unambiguously; report them as retained. If a validation is flaky or interrupted, retain the candidate unit rather than treating the run as a pass.

## Deliver the result

Run the full fixed oracle once more on the final candidate. Produce:

- a binary-safe minimized patch;
- the resolved base revision;
- retained and removed edit groups;
- original and minimized added-plus-deleted line counts;
- validation commands, execution count, and final status; and
- any unreplayed, ambiguous, binary, or flaky cases.

Leave the original working tree unchanged by default. Apply the minimized patch there only when the user explicitly asks, after confirming it still matches the recorded base and target patch. Remove only the exact temporary worktree created for this run, after preserving the result artifacts.

State the guarantee narrowly: the result is minimal only relative to the tested behavior and the recorded removal units. Passing tests do not prove semantic equivalence.
