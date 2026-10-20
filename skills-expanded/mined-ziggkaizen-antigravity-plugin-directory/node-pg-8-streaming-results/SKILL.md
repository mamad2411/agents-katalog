---
name: node-pg-8-streaming-results
description: Implements and reviews memory-safe large result processing in Node pg 8.x using pg-cursor, pg-query-stream, cursors, and Node stream backpressure.
license: MIT
compatibility: Node applications using Node pg 8.x plus optional pg-cursor or pg-query-stream.
---

# Node pg 8 Streaming Results

This skill guides streaming and cursor-based reads for large PostgreSQL result sets in Node `pg` 8.x.

## When to Use

Use this skill when the task involves:

- large exports
- CSV/report generation
- ETL jobs
- reading many rows without loading all rows into memory
- `pg-cursor`
- `pg-query-stream`
- Node stream pipelines
- HTTP response streaming
- cancelling or aborting long reads

## Decision Guide

- Use normal `pool.query` for small bounded result sets.
- Use `pg-cursor` when you need explicit batch size control, early exit, or custom loop processing.
- Use `pg-query-stream` when you need Node stream backpressure or want to pipe through transforms.
- Avoid manual `LIMIT/OFFSET` loops for huge tables unless keyset pagination is explicit and correct.

## Safety Rules

- Use a checked-out client for the full stream/cursor lifetime.
- Close or destroy the cursor/stream on errors, cancellation, client disconnect, and early return.
- Release the client only after the stream/cursor is closed.
- Use read-only queries unless the workflow has explicit approval.
- Use explicit columns and stable ordering when export consistency matters.
- Avoid streaming secrets or identity-sensitive data to logs or untrusted clients.

## Workflows

Use `workflows/implement-streaming-query-workflow.md` when implementing or reviewing streaming/cursor-based reads.

## Resources

Use `resources/streaming-decision-checklist.md` before implementing.

## Examples

Use `examples/cursor-stream-example.md` for manual batches with `pg-cursor`.

Use `examples/query-stream-example.md` for Node stream pipelines with `pg-query-stream`.
