---

name: barrier-alignment-buffer-spill
description: Buffer post-barrier records from fast channels while waiting for slow channels, spilling to disk when buffer exceeds threshold.
category: backend
triggers:
  - barrier alignment buffer spill
tags: [backend, barrier, alignment, buffer, spill]
version: 1.0.0
---

# barrier-alignment-buffer-spill

In checkpoint-barrier protocols (Chandy-Lamport style), an operator with N input channels must wait for barrier N on all channels before triggering its snapshot. Records arriving on channel A *after* barrier N but before channel B's barrier N must be buffered — they belong to the next epoch and cannot be processed yet, or the snapshot becomes inconsistent. The reusable pattern is a per-channel "aligned" flag plus a bounded in-memory buffer that spills to a memory-mapped file once it exceeds a watermark (e.g., 64MB).

```
onRecord(channel, record):
  if channel.aligned:
    buffer.append(record)      # belongs to epoch N+1
    if buffer.size > spillThreshold: buffer.spillToDisk()
  else:
    process(record)            # still in epoch N

onBarrier(channel, epoch):
  channel.aligned = true
  if all channels aligned:
    snapshot(); clearAlignment()
    replay(buffer)             # drain into epoch N+1
```

Two subtle bugs: (1) if you forget to replay the buffer *in channel arrival order*, you break FIFO per-channel ordering downstream; tag each buffered record with channel-id and drain per-channel queues. (2) Spill files must be deleted on successful snapshot AND on crash recovery — orphaned spill files from crashed epochs will be replayed incorrectly if the recovery logic picks them up. Name spill files with `{epoch}-{channel}-{uuid}` and garbage-collect anything older than the last committed epoch on startup.
