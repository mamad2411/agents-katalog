---
name: realtime-audio-dsp
description: Build ultra-low latency, lock-free audio processing graphs with strict zero-allocation in the realtime audio thread.
---
# Realtime Audio DSP & Zero-Allocation Pipelines

## Purpose & Rigor
Build ultra-low latency, lock-free audio processing graphs with strict zero-allocation in the realtime audio thread.

## Operational Invariants
1. **Academic Rigor & First Principles:** Prioritize formal correctness, proof of termination, memory safety, and algorithmic complexity over convenience.
2. **Deterministic Evidence:** Never declare success without verifiable test, benchmark, or formal audit evidence.
3. **Fail-Closed Security:** In the presence of ambiguity or missing specifications, deny access and reject unsafe operations.
