---
name: compiler-ir-optimization
description: Transform AST into SSA form, compute dominance frontiers, and perform dead code elimination, GVN, and vectorization.
---
# Compiler IR & SSA Optimization

## Purpose & Rigor
Transform AST into SSA form, compute dominance frontiers, and perform dead code elimination, GVN, and vectorization.

## Operational Invariants
1. **Academic Rigor & First Principles:** Prioritize formal correctness, proof of termination, memory safety, and algorithmic complexity over convenience.
2. **Deterministic Evidence:** Never declare success without verifiable test, benchmark, or formal audit evidence.
3. **Fail-Closed Security:** In the presence of ambiguity or missing specifications, deny access and reject unsafe operations.
