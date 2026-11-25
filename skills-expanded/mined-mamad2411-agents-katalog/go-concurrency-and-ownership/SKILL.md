---
name: go-concurrency-and-ownership
description: Use when Go work changes shared mutable state, goroutines, channels, bounded admission, asynchronous completion, or resources used by concurrent work. Skip private serial calculations and local fixes without these decisions.
---

# Go concurrency and ownership

Identify the shared invariant, admission policy, blocking boundaries and owner
of each goroutine, channel and resource. Preserve APIs, accepted effects,
dependencies and supported Go versions. Keep serial work serial when it meets
the contract; choose the smallest existing mechanism that does the job.

## Protect the observation and its aliases

Guard a compound invariant at one observation boundary. Independently atomic
fields do not make their combined snapshot coherent. For count and sum that
must describe the same updates, a single lock is enough:

```go
type totals struct {
	mu         sync.Mutex
	count, sum int64
}

func (t *totals) add(delta int64) {
	t.mu.Lock()
	t.count++
	t.sum += delta
	t.mu.Unlock()
}

func (t *totals) snapshot() (count, sum int64) {
	t.mu.Lock()
	defer t.mu.Unlock()
	return t.count, t.sum
}
```

This uses `sync`, has a usable zero value and returns scalar observations.
Referenced results need their own alias policy. Sending a slice, map or pointer
through a channel does not remove the sender's aliases: transfer mutation
ownership, synchronize access or copy what the contract requires. Publish
initialized state. Do not copy locks, WaitGroups or atomic values after use.
Keep unrelated callbacks/I/O outside locks; if an invariant requires holding
a lock across them, account for reentry and blocked progress. Choose RWMutex,
atomics or sharding for semantics and measured need, not presumed speed.

## Make admission and supervision progress together

Define what the bound counts: running callbacks, admitted work, queued values
or acquired resources. Reserve capacity before the counted acquisition/work;
a lease bound remains held through completed release, including a lease whose
Run never starts. A buffer bounds its queued values, not all external work.

When ready work must progress with spare capacity, start it without waiting
for a full batch or input closure. Observe failures while awaiting input,
capacity, acquisition or release. Publish failure and request stop **before**
potentially slow cleanup; waiting to report until Close finishes can strand
another acquisition that needs that stop. A bounded worker loop can often do
this without a scheduler framework. A blocking group-admission call must not
block the only failure supervisor.

Check the stop boundary before admitting another unit and before starting
work on a late acquisition. Work already admitted before a concurrent failure
may be starting; do not promise instantaneous interruption. Batching is valid
when it preserves the required progress and capacity semantics.

## Stop, join and release what you own

On observed cancellation or failure, stop affected admission, request
cooperative stopping, observe every owned completion, then release each
resource after its users finish. Close an acquired resource even if its Run
never started. For independent leases, one completed Run can release its lease
while others run; join the entire cohort first only when the contract shares
that lifecycle. One failed join or Close does not complete another lifetime
or excuse another owned release.

Cancellation and timeouts request stopping; they do not kill goroutines or
authorize closing resources still in use. Account for held callback cleanup
and acquisitions that finish after stopping. With WaitGroup, register before
launch, signal every exit and wait before returning owned resources. Check
the effective Go version for loop capture and newer helpers; `WaitGroup.Go`
requires Go 1.25+. Add no automatic panic recovery without an outcome policy.

## Preserve channel and result policies

Give blocking sends/receives a termination path when required. Normal early
consumer completion may stop a producer and still succeed; producer failure
may need to stop a blocked consumer. Join both callbacks before returning.
Only an owner that can establish all sends have finished may close a channel.
Do not close borrowed input or let a receiver close because it stops reading;
not every channel needs closing.

Retain independent failures and accepted effects. An error matching
`context.Canceled` or `DeadlineExceeded` can still be an independent failure.
Suppress only a stop acknowledgement defined by the callback contract, with
its origin established before your own stop request. Broad `errors.Is`
classification cannot establish that origin. Preserve the promised caller
cancellation separately; arbitrary custom causes need not be comparable.
If an API cannot distinguish failure from stopping, preserve the ambiguity or
settle its contract instead of silently erasing an outcome.

Verify progress, bounds and actual stop/join/release with held work,
acquisition and cleanup events, including sparse input and early completion.
Keep test completion independent of the value being asserted. Race checks
support these observations; they do not prove coherent snapshots or every
schedule. API/lifecycle shape stays with composition, time-budget/result
policy with context and the operation contract, and test mechanics with their
existing owners. Report actual checks and unverified boundaries.
