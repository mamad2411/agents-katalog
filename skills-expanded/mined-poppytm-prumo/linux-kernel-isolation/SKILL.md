---
name: linux-kernel-isolation
description: Enforce process sandboxing and isolation via seccomp-BPF, Landlock LSM, cgroups v2, and Linux namespaces.
---
# Linux Kernel Isolation & Sandboxing

## Purpose & Rigor
Enforce process sandboxing and isolation via seccomp-BPF, Landlock LSM, cgroups v2, and Linux namespaces.

## Operational Invariants
1. **Academic Rigor & First Principles:** Prioritize formal correctness, proof of termination, memory safety, and algorithmic complexity over convenience.
2. **Deterministic Evidence:** Never declare success without verifiable test, benchmark, or formal audit evidence.
3. **Fail-Closed Security:** In the presence of ambiguity or missing specifications, deny access and reject unsafe operations.
