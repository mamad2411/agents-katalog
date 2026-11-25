# service-runstate

Run State records durable progress, artifacts and auditable references for any
agent-coordinated operation. It does not perform the work being tracked.

## Agent Workflows

1. Call `runstate_StartRun` when multi-step work needs durable progress.
2. Use generic `items` and a workflow `kind`; a Knowledge document is an item,
   not a special service concept.
3. Record item phases with `runstate_UpdateItemState` and attach artifact
   references or the `referenceId` returned by completed service calls. Store
   that audit lookup reference, not an internal tool-call or service-call ID.
4. Use `runstate_GetRun`, `runstate_ListRuns`, or
   `runstate_ListIncompleteItems` to resume interrupted work.
5. Close terminal state using `runstate_MarkComplete`,
   `runstate_MarkFailed`, or `runstate_CancelRun`.

## Service Functions

- `runstate_StartRun`, `runstate_GetRun`, `runstate_ListRuns`, `runstate_ResumeRun`
- `runstate_UpdateItemState`, `runstate_AppendArtifact`, `runstate_AppendReference`
- `runstate_MarkFailed`, `runstate_MarkComplete`, `runstate_CancelRun`
- `runstate_ListIncompleteItems`, `runstate_ListArtifacts`
- `runstate_AcquireLease`, `runstate_RenewLease`, `runstate_ReleaseLease`

## Boundary

- The agent/runtime coordinates work; Run State records it.
- Active coordination leases use NATS KV with ownership and revision checks.
- Durable run records remain service-owned files with retention metadata.
- Run State never parses content, calls models, indexes content, or calls
  another service.
