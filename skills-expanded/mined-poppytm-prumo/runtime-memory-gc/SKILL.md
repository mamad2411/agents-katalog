---
name: runtime-memory-gc
description: Implement custom allocators (arenas, pools, TLSF) and garbage collectors (generational, incremental, concurrent).
---
# Runtime Memory Management & Garbage Collection

## Purpose & Rigor
Implement custom allocators (arenas, pools, TLSF) and garbage collectors (generational, incremental, concurrent).

## Operational Invariants
1. **Academic Rigor & First Principles:** Prioritize formal correctness, proof of termination, memory safety, and algorithmic complexity over convenience.
2. **Deterministic Evidence:** Never declare success without verifiable test, benchmark, or formal audit evidence.
3. **Fail-Closed Security:** In the presence of ambiguity or missing specifications, deny access and reject unsafe operations.
