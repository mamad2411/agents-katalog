---
name: memory-safety-sanitizers
description: Verify C/C++/Rust native code against UAF, buffer overflows, data races, and leaks using ASan, MSan, TSan, and UBSan.
---
# Native Memory Safety & Sanitizer Verification

## Purpose & Rigor
Verify C/C++/Rust native code against UAF, buffer overflows, data races, and leaks using ASan, MSan, TSan, and UBSan.

## Operational Invariants
1. **Academic Rigor & First Principles:** Prioritize formal correctness, proof of termination, memory safety, and algorithmic complexity over convenience.
2. **Deterministic Evidence:** Never declare success without verifiable test, benchmark, or formal audit evidence.
3. **Fail-Closed Security:** In the presence of ambiguity or missing specifications, deny access and reject unsafe operations.
