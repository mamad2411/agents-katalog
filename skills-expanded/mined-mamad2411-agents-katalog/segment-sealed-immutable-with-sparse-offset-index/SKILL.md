---

name: segment-sealed-immutable-with-sparse-offset-index
description: Append-only segments become immutable when sealed, with a sparse offset index built at seal time for O(log n) lookup without scanning.
category: algorithms
triggers:
  - segment sealed immutable with sparse offset index
tags: [algorithms, segment, sealed, immutable, sparse, offset]
version: 1.0.0
---

# segment-sealed-immutable-with-sparse-offset-index

When building log-structured storage, the write path appends to an "active" segment while reads need fast random access across sealed segments. The pattern: keep exactly one mutable segment (append tail pointer only), and at a size/time threshold, flip it to sealed state which triggers (1) fsync of data, (2) generation of a sparse index sampling every Nth record's offset, (3) atomic rename to include the base offset in the filename (e.g. `000000000042.log` + `000000000042.index`). Lookups binary-search the index to find the nearest sampled offset, then linearly scan forward ≤N records.

The sparsity ratio is the tunable — too dense and the index bloats memory (defeats the purpose of not keeping a full map), too sparse and scan cost dominates. A reasonable default is one index entry per 4KB of data or every 128 records, whichever comes first. Critically, sealed segments are *content-addressed by base offset* — never mutate, never rename again — which lets the reader path be lock-free: grab the current segment list snapshot, binary-search by base offset, done.

```
activeSegment.append(record) -> tail++
if (activeSegment.size >= threshold) {
  activeSegment.fsync()
  activeSegment.sparseIndex = buildEveryNth(records, 128)
  seal(activeSegment)  // atomic: add to sealedList, new active created
}
read(offset) -> segment = binarySearch(sealedList, offset)
                entry = segment.index.floorEntry(offset)
                scanForward(segment, entry.fileOffset, offset)
```
