---
name: myopenpanels-task-queue
description: Use when inspecting or managing work in the MyOpenPanels project Task queue, or executing a Studio-provided Task Handoff.
---

Use the generic Task commands returned by command catalog discovery. The `tasks`
table and generic Task service are authoritative; do not call queue-specific
HTTP endpoints or mutate panel state to change a Task lifecycle.

Intent routing:

- For read-only Task state and its embedded execution summaries, read
  `references/inspect.md`.
- To retry a failed Task, read `references/retry.md`.
- To cancel a Task, read `references/cancel.md`.
- To archive a terminal Task, read `references/archive.md`.
- For an exact Studio Task scope handoff, read `references/execute-scope.md`.

1. Run the exact `task handoff start` selector supplied by Studio. It registers
   and claims on execution, not when the instruction is copied.
2. Follow the returned ExecutionBundle and Delivery Contract without separately
   loading Catalogs, Panel Skills, or portable Skills.
3. Write only the declared workspace artifacts and `execution-result.json`.
   Use `task handoff exec` only for commands explicitly allowed by the Bundle;
   it injects the private Broker and fencing context.
4. Heartbeat long work through `task handoff heartbeat`. Stop immediately when
   heartbeat or a work command returns `execution_fenced`.
5. Finish through `task handoff complete` or `task handoff fail`. The Runtime
   validates the result, stages declared outputs, and completes the
   Task, and immediately returns the next Bundle when the scope can continue.
6. Exit only at `complete` or `blocked`; use `task handoff stop` to abandon and
   release active work. Do not run low-level claim, complete, fail, or release
   commands for a handoff.

Use `task next` only for read-only discovery. A runnable Task has `ready: true`;
a Task can be blocked by a live lease, a future retry time, exhausted executions,
or the lack of an available Agent CLI. Persistent queue execution is owned by
the Studio Worker. Manual Agents process only the supplied execution scope.
`exact-task` selects only the named Task. `project-drain`
continues independent runnable Tasks before reporting blockers.
`wiki-mutation-drain` processes one prerequisite or mutation Task at a time in
mutation order until the mutation queue is empty.

Never treat process exit zero as proof of success. `task handoff complete`
performs the Handler's domain validation. A rejected completion is a failed
execution; stop task-bound writes as soon as the execution is fenced. Use
`task read` when diagnosing
prerequisite propagation or retries.
