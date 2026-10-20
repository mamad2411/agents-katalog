---
name: event-sourced-orchestration-with-decider-projector
description: Use event sourcing for domain state with pure decider (commands->events) and projector (events->read model) functions
category: architecture
version: 1.0.0
version_origin: extracted
confidence: high
tags: [event-sourcing, ddd, architecture]
source_type: extracted-from-git
source_url: https://github.com/pingdotgg/t3code.git
source_ref: main
source_commit: 9df3c640210fecccb58f7fbc735f81ca0ee011bd
source_project: t3code
imported_at: 2026-04-18
evidence:
  - apps/server/src/orchestration/Layers/OrchestrationEngine.ts
  - apps/server/src/orchestration/Layers/ProjectionPipeline.ts
  - .docs/encyclopedia.md
---

## When to Apply
- You need an audit trail of all state changes (threads, turns, checkpoints, approvals)
- You want to replay history without re-running external agents
- You need to support concurrent requests and rollback failed operations
- You want domain logic (commands + events) separate from read model updates

## Steps
1. Define command schemas: `Thread.Create`, `Thread.Turn.Start`, `Thread.Checkpoint.Revert` (in contracts)
2. Define event schemas: `ThreadCreated`, `MessageSent`, `TurnDiffCompleted` (in contracts)
3. Implement decider function:
   - Input: command + current aggregate state
   - Output: list of events or error
   - Pure function; no side effects
4. Implement projector function:
   - Input: event + current read model
   - Output: updated read model
   - Also pure
5. Orchestration engine:
   - Receives command from client
   - Validates via `commandInvariants`
   - Calls decider to produce events
   - Appends events to event log (durable storage)
   - Calls projector to update in-memory read model
   - Returns new projected state to client
6. On startup, replay event log through projector to rebuild read model

## Example
```typescript
const decider = (command, state) => {
  if (command.type === 'thread.create') {
    if (state.threads.has(command.threadId)) return Err('thread exists')
    return Ok([{ type: 'thread.created', threadId: command.threadId, title: command.title }])
  }
  return Err('unknown command')
}

const projector = (event, readModel) => {
  if (event.type === 'thread.created') {
    readModel.threads.set(event.threadId, { id: event.threadId, title: event.title })
  }
  return readModel
}

const engine = new OrchestrationEngine()
const [events, newState] = yield* engine.dispatch(command)
```

## Counter / Caveats
- Event log grows unbounded; implement snapshot/compaction strategy
- Projector must be deterministic; any randomness breaks replay
- Decider can be slow for large aggregates; consider per-thread vs global state
- Concurrent commands to same aggregate need optimistic locking or version checks
