---

name: rolling-hash-chunk-boundary-detector
description: Use content-defined chunking via rolling hash to produce stable segment boundaries across divergent replicas before diffing.
category: algorithms
triggers:
  - rolling hash chunk boundary detector
tags: [algorithms, rolling, hash, chunk, boundary, detector]
version: 1.0.0
---

# rolling-hash-chunk-boundary-detector

When reconciling two byte streams or record logs that have drifted (insertions, deletions, partial overwrites), fixed-size chunking produces cascading false differences: a single byte insertion shifts every downstream block. A rolling hash (Rabin-Karp, gear hash, buzhash) over a sliding window solves this by declaring a chunk boundary wherever `hash(window) & mask == 0`. Boundaries land on the same content bytes on both sides regardless of offset, so only the truly-changed chunks show up as deltas.

Pick the mask to target an average chunk size (e.g. `mask = (1<<13)-1` ≈ 8KB avg) and clamp with hard min/max bounds so pathological inputs don't produce one-byte or megabyte chunks. The reconciliation loop becomes: chunk both sides → hash each chunk with a strong digest (SHA-256/BLAKE3) → set-diff the digest lists → transfer only missing chunks. This is the core mechanic behind rsync, borg, and restic.

```python
def cdc_boundaries(buf, mask=0x1FFF, min_sz=2048, max_sz=65536):
    h, start = 0, 0
    for i, b in enumerate(buf):
        h = ((h << 1) | (h >> 63)) ^ GEAR[b]  # gear hash
        sz = i - start
        if sz >= max_sz or (sz >= min_sz and (h & mask) == 0):
            yield start, i; start = i
    if start < len(buf): yield start, len(buf)
```

Common mistake: hashing the window with a non-rolling hash, which makes chunking O(n·w) instead of O(n). Verify your hash updates in O(1) per byte.
