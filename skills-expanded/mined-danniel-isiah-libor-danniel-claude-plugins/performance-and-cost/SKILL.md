---
name: performance-and-cost
description: Keep the whole application performant and cost-effective. Use when designing, implementing, or reviewing for latency, throughput, resource use, and cloud cost. Covers N+1 queries, caching, async/queues, payload size, and right-sizing. Used by the architect, implementer, and code-reviewer.
---

# Performance & Cost

## Hotspots to check
- **Database access** — N+1 queries (eager-load), missing indexes (coordinate with `database-design`), over-fetching columns/rows, unbounded queries (paginate).
- **Caching** — cache expensive/repeated reads with correct invalidation; HTTP caching for static responses.
- **Async** — move slow/non-critical work (email, image processing) to queues/jobs.
- **Payloads** — paginate lists; select only needed fields; compress; avoid loading whole files into memory.
- **Hot loops** — no queries/allocations inside loops; precompute.

## Cost awareness
Prefer managed/right-sized resources; avoid always-on for bursty work (scale-to-zero/queues); watch egress and per-request external-API costs; cache to cut paid calls.

## Review output
Per finding: file:line, the cost (latency/$/memory), and a concrete optimization. Measure before micro-optimizing.
