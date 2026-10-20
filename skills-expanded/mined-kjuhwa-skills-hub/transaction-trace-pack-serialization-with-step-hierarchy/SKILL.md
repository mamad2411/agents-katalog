---
name: transaction-trace-pack-serialization-with-step-hierarchy
description: Encode per-request distributed traces as a hierarchical list of typed steps (method, DB, external call, error) in a compressed binary pack, indexed by request end-time
category: apm
version: 1.0.0
source_type: extracted-from-git
source_url: https://github.com/kjuhwa/scouter
source_ref: master
source_commit: 126bb19f07d1fe4fe915eb408c381e2c140cc94c
source_project: scouter
version_origin: extracted
tags: [tracing, apm, xlog, serialization, perf]
confidence: high
---

# Transaction Trace Pack Serialization with Step Hierarchy

Apply when building an APM or observability system where you want per-transaction drill-down without the overhead of span-level distributed tracing (Jaeger/Zipkin) for every hop.

## Pattern

1. Treat each inbound request (HTTP, gRPC, async task) as one XLog entry.
2. Inside the entry, record a typed step list: `MethodStep`, `SqlStep`, `ApiCallStep`, `MessageStep`, `ErrorStep`. Each step carries `start`, `elapsed`, and type-specific fields.
3. Steps form a flat-list-with-depth-marker hierarchy, not a nested tree — cheap to serialize and traverse.
4. Index by **end time** (not start time) so slow / in-flight transactions don't vanish from recent views.
5. Compress the step buffer per-entry (LZ4). Metadata (elapsed, status, user, URI) stays plain for server-side filter/search without decompression.

## Evidence

- `scouter.common/src/main/java/scouter/lang/pack/Pack.java`
- `scouter.agent.java/src/main/java/scouter/agent/trace/TraceMain.java`
- `scouter.document/client/Reading-XLog.md`

## Trade-offs

- Plots well as (end-time, elapsed) scatter — instant feedback on hot spots.
- Not a distributed trace protocol — cross-service spans need correlation IDs layered on top (scouter uses `PCODE` / `GXID`).
- End-time indexing means you can't answer "what's currently running" without a separate active-transactions table.

## Related knowledge

- `xlog-extended-transaction-trace-with-compression` (api)
- `trace-context-async-execution-propagation` (pitfall)
