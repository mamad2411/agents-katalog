---
name: smart-memory-guard
description: Use when reading from or writing to memory and you need guardrails against stale records, bloated memory files, or low-value writes that will not remain useful after the current workstream
---

# Smart Memory Guard

## Overview

Memory is useful only while it stays accurate, compact, and worth loading. This skill operationalizes the guardrails implied by `src/memdir/memoryTypes.ts`, `src/services/SessionMemory/prompts.ts`, and `src/services/extractMemories/prompts.ts`.

## Three Defenses

### 1. Drift Guard

Treat memory as a snapshot, not as present truth.

Before acting on a memory:

- if it names a file, check the file still exists
- if it names a function or flag, grep for it
- if it describes current state, verify current state directly

If memory conflicts with the repo or source of truth, trust what you observe now and update or remove the stale memory.

### 2. Bloat Guard

Oversized memory degrades prompt quality.

When a memory file starts crowding the prompt:

- condense older detail
- keep the current state crisp
- preserve only the parts another agent would truly need
- prefer short index entries and info-dense bodies

Do not let memory become a second transcript.

### 3. Write Filter

Before saving anything, ask:

- is this non-obvious?
- is this not derivable elsewhere?
- will it still help after the current task is over?

If the answer is no, do not save it.

## Read-Side Rules

- Access memory when it is relevant or explicitly requested.
- If the user says to ignore memory, act as if it were empty.
- Verify recalled facts before recommending action from them.

## Write-Side Rules

- Update existing memory instead of creating duplicates.
- Prefer semantically organized files over chronological dumping.
- Remove or correct memories that have expired.
- Keep sensitive data out of shared memory.

## Typical Rejects

Reject writes like:

- "save this PR list"
- "save what we changed today"
- "save the fix steps for this bug"
- "save the repo structure"

Those are activity logs, not durable memory.

## Typical Accepts

Accept writes like:

- "this project never mocks the database in integration tests"
- "merge freeze starts on 2026-03-05"
- "the user is strong in Go but new to the React side"
- "production latency is watched in this external dashboard"

## Done Condition

You have applied this skill correctly when memory is verified before use, compressed before it becomes noise, and written only when the information is durable enough to earn a place in future context.
