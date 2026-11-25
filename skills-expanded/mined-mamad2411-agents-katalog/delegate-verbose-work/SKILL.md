---
name: delegate-verbose-work
description: >-
  Use before running a broad grep/search sweep (roughly 10+ calls to answer one question) or
  re-Reading a file already read this session, on the main thread. Route that investigation to a
  subagent instead and keep only its conclusion. Triggers: "find every place that...", "search the
  whole repo for...", needing the same file's content again mid-session. Do NOT use for a single
  targeted grep or a file being read for the first time.
---

# Delegate verbose work

A broad search sweep or a repeated file re-read belongs on a subagent's thread, not the main
one. The main thread keeps orchestration, decisions, and concise summaries; a subagent absorbs
the many tool calls and reports back only the conclusion.

## When to delegate

- A question needs many grep/search calls to answer (roughly 10 or more) — "every caller of X",
  "where is Y configured across the repo", broad terminology or convention sweeps.
- A file has already been Read this session — check what you already have before issuing another
  Read; if the prior content is stale or incomplete, delegate the re-check rather than re-Reading
  from the main thread.

## When not to

- One or two targeted greps to confirm a specific claim.
- A file being read for the first time this session.
- The result must inform the very next tool call you make (delegating adds a round trip you can't
  afford there).

## How

Give the subagent the exact question and enough context to answer it standalone, and ask for a
conclusion, not a transcript — "report file paths and line numbers, not the full grep output."
Discard the sweep once you have the conclusion; do not pull it back into the main thread's
context.

If this trigger fires while running under a more specific skill that sets its own delegation
default (for example `ticket-to-pr`'s "keep implementation and review with the active agent; do
not hand either stage to another AI"), that skill's contract wins.

## Resuming after worktree loss

A worktree-isolated investigative subagent (an `Agent` tool call with `isolation: "worktree"`)
loses its worktree whenever the harness cleans it up between dispatch and resumption — this is
guaranteed, not occasional, for a read-only investigative subagent: it makes no changes by
construction, and the harness cleans up an unchanged worktree by default. A relaunch or resume
that follows a long idle period carries the same risk. Do not let the resumed subagent start
blind and redo the sweep from scratch:

- If an earlier notification from that subagent already reported a conclusion, pass that
  conclusion forward in the resume prompt instead of a bare re-dispatch, and instruct the
  subagent to use it unless it finds the conclusion stale or contradicted.
- If no conclusion was received yet, ask the resumed subagent to report what it already found —
  including any note it can recover from its own prior output — before it redoes the sweep, and
  have it redo only the portion that report cannot answer.

Losing worktree state is the harness's; redoing the investigation without checking for what
survived is the orchestrator's. The orchestrator, not the resumed subagent, is the one holding
the last notification, so the orchestrator is the one obligated to hand it forward.
