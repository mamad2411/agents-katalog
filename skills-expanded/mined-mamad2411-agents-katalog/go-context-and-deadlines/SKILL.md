---
name: go-context-and-deadlines
description: Use when Go work changes cancellation propagation, operation or stage deadlines, cancellation causes, or required work after caller cancellation. Skip pure calculations and synchronization changes without a context or budget decision.
---

# Go context and deadlines

Give each operation a clear stopping boundary, time budget and cancel owner.
Read its callers and result contract before adding context checks. Preserve
supported signatures and Go versions; pure helpers need no context parameter.

## Preserve the result policy

Decide separately what cancellation means at entry, between units of work,
after an independent failure, and after completion. Follow the operation's
policy at each boundary:

| Condition | Decision |
| --- | --- |
| Empty work is promised success | Return that success before checking cancellation; invoke no work. |
| More work must not start after observed cancellation | Check before admitting the next unit; retain accepted progress. |
| Work completed successfully | Return the completed result; a late cancellation check must not invent failure. |
| An operation failed during cancellation | Keep its error and usable result; add only the cancellation information promised to callers. |

Preserve an independent callback, read, write or finalization error even when
it wraps or joins `context.Canceled` or `DeadlineExceeded`. Classification
does not establish origin: `errors.Is` matching cancellation is not a reason
to replace an operation error with `ctx.Err()` or `context.Cause(ctx)`.

When cancellation must be exposed, sample `ctx.Err()` once at the failed or
stopped-work decision. If nonnil, retain that standard classification and
the promised custom cause alongside independent failures. A custom cause may
be noncomparable; avoid equality between arbitrary error interfaces. Do not
sample after canceling your own scope and mistake resource cleanup for the
failure that stopped work. General error exposure and compatibility still
follow the public contract.

## Keep the scope alive for its work

Pass the caller context through cooperating blocking boundaries. Derive one
child for a **total** operation budget; derive stage budgets from that child.
A stage can narrow the remaining allowance, not restart it. Preserve an
earlier parent deadline. Use request metadata in context values, and ordinary
parameters/fields for dependencies and configuration.

The scope owner calls cancel on every exit. Check the client's ownership
contract on each outcome: an `http.Client.Do` error can accompany an
already-closed redirect body; do not close it again. A successful `Do`
transfers body closure to you, including on status/read failure.

Keep an HTTP request's scope live
through response reading and owned-body closure, not merely until headers
arrive. For repeated stages, release each stage before the next; a helper
makes the lifetime visible:

```go
func runStage(parent context.Context, limit time.Duration, work func(context.Context) error) error {
	ctx, cancel := context.WithTimeout(parent, limit)
	defer cancel()
	return work(ctx) // Include body consumption and closure inside work.
}
```

If returning live work or a body, explicitly transfer cancel ownership instead
of deferring cancel in its creator. Cancellation requests stopping; it does
not interrupt arbitrary I/O or establish completion. `AfterFunc`'s stop
function also does not join an already-started callback.

## Finalize accepted work deliberately

If the contract requires finalization after the caller stops, use a separate
owned, bounded scope. On Go 1.21+, combine `WithoutCancel(ctx)` with a local
timeout to retain metadata without the caller's cancellation or deadline.
Wait for cooperative finalization, then release its scope. Preserve processing
and finalization outcomes separately before combining promised failures.
Detach only the required work, not the whole operation. A timeout cannot
authorize releasing a resource still in use.

Verify applicable empty/entry/completed policies, retained progress,
independent failures, absolute total/stage deadlines, and scope lifetime at
the real callback/client boundary. Keep synchronization mechanics with
concurrency, API/lifecycle shape with composition, and test mechanics with
their existing owners. Report actual checks and unverified boundaries.
