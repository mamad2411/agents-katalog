---
name: cursor-cancel-ralph
description: Cancel an active Ralph Loop. Use when the user wants to stop, cancel, or abort a running ralph loop.
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Cancel a native Codex Ralph Loop

Cancel only the exact active loop identified by its retained native child identity.

## Workflow

1. Read the bounded loop state and verify the project/task scope, child identity, current iteration, and active status.
2. Call the native interrupt operation for that exact child. Do not terminate by process name or broad repository scope.
3. Record the returned previous status and mark the loop cancelled. If the child was already complete or inactive, report that state without widening the action.
4. Preserve unrelated state. Remove a local loop state file only when it belongs to the matching task and the removal is within the authorized cleanup scope.
5. To recover after an accidental interruption, use a native follow-up on the same verified child identity and record the resumed state.

The observed proof interrupted `/root/cancel_native_probe` while running and then resumed that same identity through two bounded follow-ups. No recursive deletion, process-name kill, or automatic hook was used.
