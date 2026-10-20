# Go Concurrency Patterns

## Summary

**One-sentence:** Implement safe, leak-free Go concurrency via bounded worker pools, fan-out/fan-in pipelines, and context-cancellation throughout.

**One-paragraph:** Every concurrent Go path uses bounded worker pools (no unbounded goroutine spawns), passes context.Context for cancellation, closes channels on the sender side, and pairs each goroutine with a deterministic exit signal. Fan-out/fan-in is the canonical pipeline shape; errgroup.WithContext coordinates worker shutdown on first error. Output is concurrent code + lifecycle invariants documented at the package level.

**Ефективно для:**

- Backend services with parallelisable I/O or CPU work.
- Replacing ad-hoc `go func()` calls with bounded pools.
- Refactoring leaking pipelines that build up goroutines under load.
- Adding cancellation to existing long-running operations.

## Applies If (ALL must hold)

- Go 1.21+ project with measurable concurrent work.
- Service handles concurrent requests or processes bounded queues.
- Code touches I/O (HTTP, DB, message queue) where parallelism reduces latency.
- Goroutine leaks have been observed or are a real risk (pprof shows growth).

## Skip If (ANY kills it)

- Service is sequential with no I/O parallelism opportunity.
- Concurrency is delegated to a framework (gqlgen DataLoader, etc.) that owns the pool.
- Project uses an alternative runtime model (work stealing, async runtime).
- Single-shot CLI where complexity exceeds payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload description: producer rate, consumer cost, latency budget | doc | tech-lead |
| pprof goroutine profile of current state (if refactoring) | profile | ops |
| Cancellation source: HTTP context, signal handler, parent context | code | tech-lead |
| errgroup or sync/x packages available (golang.org/x/sync) | dep | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[go-error-handling-patterns]] | Worker errors propagate through errgroup. |
| [[logging-patterns]] | Pool lifecycle events log structured fields. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (bounded pool, context everywhere, channel closed by sender, no goroutine without exit signal, fan-out-fan-in pipeline, errgroup for first-error) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for concurrent code module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: workload sketch → pool sizing → pipeline shape → cancellation → leak audit | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pool_design` | opus | Pool sizing + backpressure decisions need deep synthesis. |
| `pipeline_assembly` | sonnet | Mechanical fan-out/fan-in wiring. |
| `cancellation_plumbing` | sonnet | Thread context through call sites. |
| `leak_audit` | sonnet | Run pprof and identify goroutine accumulators. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pool.go` | Bounded worker pool with context cancellation + errgroup coordination |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-concurrency-patterns.py` | Validate concurrent code module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-error-handling-patterns]]
- [[logging-patterns]]
- [[performance-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps workload type, framework ownership, and observed leaks to a rule from `01-core-rules.xml`, telling the agent whether to apply Go concurrency patterns or skip when the runtime already owns the model. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pool.go`

```go
// pkg/worker/pool.go
// Leak-safe bounded worker pool with context cancellation and error collection.
// Usage:
//   p := NewPool(ctx, 8, 100)
//   p.Submit(func(ctx context.Context) error { return doWork(ctx) })
//   p.Stop()
//   for err := range p.Errors() { log.Print(err) }
package worker

import (
	"context"
	"sync"
)

// Job is a unit of work. Must respect ctx cancellation.
type Job func(ctx context.Context) error

// Pool is a bounded goroutine pool with error collection.
type Pool struct {
	jobs   chan Job          // owned and closed by Stop()
	errs   chan error        // closed by Stop() after all workers finish
	wg     sync.WaitGroup
	cancel context.CancelFunc
}

// NewPool starts `workers` goroutines reading from a channel of capacity `buffer`.
func NewPool(ctx context.Context, workers, buffer int) *Pool {
	ctx, cancel := context.WithCancel(ctx)
	p := &Pool{
		jobs:   make(chan Job, buffer),
		errs:   make(chan error, buffer),
		cancel: cancel,
	}
	for i := 0; i < workers; i++ {
		p.wg.Add(1)
		go func() {
			defer p.wg.Done()
			defer func() { _ = recover() }() // prevent single-job panic from crashing pool
			for {
				select {
				case <-ctx.Done():
					return
				case job, ok := <-p.jobs:
					if !ok {
						return
					}
					if err := job(ctx); err != nil {
						select {
						case p.errs <- err:
						default: // drop if error buffer full; log if needed
						}
					}
				}
			}
		}()
	}
	return p
}

// Submit enqueues a job. Blocks if the buffer is full.
func (p *Pool) Submit(j Job) { p.jobs <- j }

// Errors returns the read-only error channel. Drain after Stop().
func (p *Pool) Errors() <-chan error { return p.errs }

// Stop closes the job channel, waits for all workers to finish, then closes the error channel.
func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
	close(p.errs)
	p.cancel()
}
```
