---
name: visible-agent-work
description: Makes agent and subagent work visible, inspectable, and task-local. Use when hidden background workers, child agents, tool calls, run IDs, task rails, progress streams, or parent-thread summaries must prove what is happening without leaking unrelated work.
---

# Visible Agent Work

## Overview

Use this skill when agents delegate work or run background tasks and the user needs to see what is happening.

Invisible work creates distrust. If a child agent is working, the parent surface should show the task, run ID, status, and completion evidence.

## When to Use

- Parent agents dispatch builders, reviewers, or research workers.
- A UI shows a right rail, task list, activity card, or progress stream.
- Users ask whether an agent is actually working.
- Background processes are used as proof.
- A platform supports run IDs, task records, logs, or streamed events.

## Core Rules

1. **Visible ID or it did not happen.** Prefer task IDs, run IDs, PRs, commits, or transcript handles over hidden process IDs.
2. **Task-local only.** Show work connected to the selected parent task. Do not fall back to global agent activity.
3. **Stream truth, not theatre.** Do not fake token streaming with final ledger updates.
4. **Keep completed work visible briefly.** If active rows disappear immediately on completion, users think the work vanished.
5. **Parent chat should mirror child work.** A side rail alone is not enough for important child-agent progress.

## Required Fields

Each visible child work item should have:

- child run ID or task ID;
- agent name and role;
- status: queued, invoking, streaming, completed, failed, interrupted, stalled;
- compact task title;
- request preview;
- response or output preview when safe;
- link to full transcript, artefact, PR, or log;
- timestamps.

## Parent-Child Association

Associate child work with the parent task using explicit references:

- parent thread mentions child `run-...`;
- parent task record lists child IDs;
- dispatch ledger links parent ID to child ID;
- PR/check metadata links review/fix runs.

Never infer association from same agent name or recent global activity alone.

## Streaming Contract

If streaming is supported, use durable run IDs:

```json
{
  "event": "stream_delta",
  "run_id": "run-...",
  "agent": "reviewer",
  "role": "reviewer",
  "delta": "token text"
}
```

Provider-internal response IDs may be included as metadata, but UI state should key on the durable run/task ID.

## Verification

Prove:

- child run exists in the backend ledger;
- parent task explicitly references it;
- UI shows only referenced child runs;
- streaming events append to the right buffer;
- completed rows remain visible long enough to inspect;
- unrelated global runs do not appear.

## Stop Conditions

Hold if:

- only a hidden process ID exists;
- child work cannot be linked to the parent task;
- the UI shows full roster fallback instead of task-local work;
- streaming is simulated rather than forwarded from real deltas;
- completed output is inaccessible.
