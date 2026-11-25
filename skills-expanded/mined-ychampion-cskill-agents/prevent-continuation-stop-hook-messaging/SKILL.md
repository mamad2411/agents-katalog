---
name: prevent-continuation-stop-hook-messaging
description: "Collect stop-hook progress/errors, emit a structured prevented-continuation attachment, and summarize the block for users and logs."
metadata:
  author: ychampion
---

# SKILL: Prevent Continuation Stop Hook Messaging
**Domain:** tool-orchestration  
**Trigger:** Use when stop hooks prevent continuation so you can surface a consistent attachment plus a summary notification that downstream UI/logging consumes.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Capture every hook progress update while the stop-hook generator runs, track how many hooks fired, preserve per-hook command and prompt details, then attach later timing/error data to the matching hook entries. When a hook asks to prevent continuation, emit a machine-readable `hook_stopped_continuation` attachment with the hook name, tool use ID, and stop reason, then synthesize the concise `StopHookSummary` message that surfaces counts, errors, and whether the turn was blocked. This keeps UI banners, transcript log notifications, and verbose hooks in sync, with a single reusable pattern that works whenever any hook stops the turn.

## Key Rules
- Gather `hookInfos` from `progress` attachments (command, prompt, duration) and `hookErrors` from non-blocking or blocking attachments so you can summarize each hook’s outcome.
- Emit the `hook_stopped_continuation` attachment exactly when `preventContinuation` becomes true, supplying `toolUseID`, hook name, and the stop reason so log processors and tool-tracking pipelines get a structured signal.
- After the generator completes, call `createStopHookSummaryMessage` with counts, accumulated info, the prevented flag, and whether actual output already streamed; this keeps UI, transcript, and notification consumers aligned on the stop reason.
- Send the notification that references `stop-hook-error` only when there are errors so verbose transcript/ctrl+o viewers know the details exist.
- Keep the machine-readable attachment and summary message in lockstep so telemetry and UI never disagree about whether continuation was blocked and why.

## Example Application
When the `Stop` hook intercepts a red team command that would delete infrastructure, emit the `hook_stopped_continuation` attachment with `hookEvent: 'Stop'`, then send the summary message so the REPL banner shows “Stop hook prevented continuation: <reason>” while telemetry records how many hooks fired and what errors occurred.

## Anti-Patterns (What NOT to do)
- Do not rely on inconsistent manual logs; the single attachment + summary pair is the structured contract.
- Do not record hook errors without feeding them into the summary message or notification; UI and logs must share the same explanation.
