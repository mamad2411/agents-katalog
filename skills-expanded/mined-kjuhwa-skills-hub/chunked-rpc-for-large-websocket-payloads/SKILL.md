---
name: chunked-rpc-for-large-websocket-payloads
description: Send large (>5MB) RPC arguments over WebSocket as a sequence of base64 chunks via transfer:start/chunk/commit channels with per-chunk retry, a sha256 checksum, and a placeholder in the original call's arg array.
category: build
version: 1.0.0
version_origin: extracted
tags: [websocket, rpc, chunking, large-payloads, retry]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: apps/electron/src/main/chunked-rpc.ts
imported_at: 2026-04-18T00:00:00Z
---

# Chunked RPC for large WebSocket payloads

## When to use
- WebSocket RPC server where a small subset of calls (e.g. `sessions:import`, `workspace:bulkUpload`) carry 10MB–500MB payloads.
- A proxy / tunnel / browser imposes a per-message size limit (~32MB common).
- Can't switch to plain HTTP for these calls because they need to run through the same authenticated RPC lane.

## How it works
1. Caller detects size: if the target arg's serialized size is over `CHUNKED_TRANSFER_THRESHOLD` (5MB), fall into the chunked path.
2. Build `PreparedChunkedPayload`: `{ bytes: Buffer, checksum: sha256, chunkCount: ceil(bytes.length / CHUNK_SIZE) }`. `CHUNK_SIZE = 2MB raw` (~2.7MB base64).
3. Build `deferredArgs` = original args with the large arg replaced by `null` placeholder.
4. **Three transfer channels**: `transfer.START`, `transfer.CHUNK`, `transfer.COMMIT` (plus `transfer.ABORT`):
   - `START`: send `{ totalBytes, chunkCount, channel, args: deferredArgs, largeArgIndex, checksum }`. Server returns a `transferId`.
   - `CHUNK`: send `{ transferId, index, data: base64(chunk) }` for each chunk, sequentially.
   - `COMMIT`: send `{ transferId }`. Server verifies checksum, reassembles, injects the reconstructed value at `largeArgIndex`, dispatches the original RPC normally.
5. **Per-chunk retry** (max 3 attempts, 1s between): transient WebSocket hiccups through proxies are common, retry individual chunks instead of the whole transfer.
6. On any failure: `transfer.ABORT` best-effort so the server can GC its partial buffer.
7. Progress callback `onProgress(sent, total)` lets UI show an upload bar.

## Example
```ts
const CHUNK_SIZE = 2 * 1024 * 1024;
const THRESHOLD = 5 * 1024 * 1024;

export async function invokeChunked(client, channel, args, largeArgIndex, onProgress) {
  const json = JSON.stringify(args[largeArgIndex]);
  const bytes = Buffer.from(json, 'utf8');
  const checksum = createHash('sha256').update(bytes).digest('hex');
  const chunkCount = Math.ceil(bytes.length / CHUNK_SIZE);

  const deferredArgs = [...args]; deferredArgs[largeArgIndex] = null;
  const { transferId } = await client.invoke('transfer:start', {
    totalBytes: bytes.length, chunkCount, channel, args: deferredArgs, largeArgIndex, checksum,
  });
  try {
    for (let i = 0; i < chunkCount; i++) {
      const slice = bytes.subarray(i * CHUNK_SIZE, Math.min((i + 1) * CHUNK_SIZE, bytes.length));
      await withRetry(3, 1000, () =>
        client.invoke('transfer:chunk', { transferId, index: i, data: slice.toString('base64') })
      );
      onProgress?.(i + 1, chunkCount);
    }
    return await client.invoke('transfer:commit', { transferId });
  } catch (e) {
    try { await client.invoke('transfer:abort', { transferId }); } catch {}
    throw e;
  }
}
```

## Gotchas
- Base64 expands ~33%, so a 2MB raw chunk is ~2.7MB on the wire - stay under common proxy per-message caps.
- Do NOT interleave chunks from different transfers on the same socket - server reassembly keeps a single buffer per transferId.
- Checksum verification catches corruption that would otherwise pass type-check but break the handler.
- Include `channel` in the START message so the server can validate authorization BEFORE accepting the upload.
- Placeholder `null` in args is fine if the handler expects a non-null value - the reassembly step replaces it.
