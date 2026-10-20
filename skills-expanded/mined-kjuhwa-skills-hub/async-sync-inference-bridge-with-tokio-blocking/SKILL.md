---
name: async-sync-inference-bridge-with-tokio-blocking
description: Provide both async and sync APIs for inference by writing the core as async and using tokio::task::block_in_place for the sync wrappers.
category: async
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, async]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Async Sync Inference Bridge With Tokio Blocking

**Trigger:** Building an inference library that must serve both async (HTTP servers, tokio apps) and sync (CLIs, scripts) clients without two parallel codepaths.

## Steps

- Implement core inference as async fn identify_file(), async fn identify_content().
- Provide thin sync wrappers (identify_file_sync, identify_content_sync) that call exec(async_method()).
- Define an exec() helper that uses tokio::task::block_in_place inside a tokio runtime, or spawns a blocking thread when there is no runtime.
- Document the contract: which methods are safe in which context.
- Test both paths against the same input corpus; assert identical results.
- Don't mix sync and async in the same call chain — design the API so callers commit to one world.

## Counter / Caveats

- block_in_place panics outside a tokio multi-thread runtime; provide a thread-pool fallback.
- Sync wrappers carry runtime startup overhead; long sync loops are slower than one async batch.
- File handle lifetimes differ: async drops at .await, sync holds until drop — beware file lock interactions.
- Mixed sync/async can deadlock; document and lint against it.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/lib/src/session.rs:40-47`
- `rust/lib/src/future.rs`
- `rust/lib/src/input.rs:15-102`
