---
name: semwright-cross-app-artifacts
description: Use when an agent must move a real artifact between Semwright-controlled applications while preserving semantic type, digest evidence, scoped filesystem authority, and destination verification.
---

# Cross-application artifacts

Use this procedure for a producer → handoff → consumer workflow.

1. Discover the producer's export capability and inspect its `artifact-out:<type>` tags.
2. Discover the consumer's import/rescan capability and inspect compatible `artifact-in:<type>` tags.
3. Describe both operations. Confirm the actual schemas and current routes.
4. Export through the producer and record the returned artifact identity, media/semantic type, and digest when available.
5. If the route uses a filesystem handoff, call `artifact.handoff` with explicit owner-granted source/destination roots. Supply an expected SHA-256 when the producer provided one.
6. Invoke the consumer's documented import/rescan operation. Do not assume copying a file makes an application ingest it.
7. Verify the destination semantically.

`artifact.handoff` is a bounded binary copy primitive, not a universal materializer or streaming bus. Artifact tokens returned by drivers are not automatically filesystem paths.

See [ports](references/ports.md), [handoff](references/handoff.md), and [recovery](references/recovery.md).
