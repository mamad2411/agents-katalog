---
name: delegation-triggers
description: Use when deciding whether to spawn subagents — explicit rules for when delegation pays off and when direct work is faster. Opus 4.8 under-delegates by default; these rules correct that.
---

# Delegation Triggers

Opus 4.8 is documented to under-reach for subagents. Apply these rules instead of
intuition.

## Delegate (spawn subagents, in parallel where independent) when:
- Work fans out across **independent items**: reading/searching many files, auditing
  several modules, running several independent investigations.
- You need a **broad search** where only the conclusion matters (use a read-only
  explore subagent; you keep the answer, not the file dumps).
- You need **fresh-context verification** of your own work (see verification-loop).
- Two or more workstreams have **no shared state** and no ordering dependency — launch
  them in one message so they run concurrently.

## Work directly when:
- A single file read or a known-location lookup would answer the question.
- Edits are sequential and each depends on the previous result.
- The task is small enough that subagent setup costs more than it saves.

## How
- Give each subagent a self-contained brief: goal, exact scope, what to return.
- Don't duplicate a delegated search yourself — wait for the result.
- Prefer asynchronous delegation: keep working on the main thread while subagents run;
  intervene only if one goes off track.
