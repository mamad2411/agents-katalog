---
name: z-refactor
description: Zero-regression refactoring and modularization workflow enforcing the Net Engineering Value (NEV) gate. Use when refactoring, splitting large classes, localizing DTOs, or cleaning tech debt.
---

# Z-Refactor Protocol

Refactoring improves code structure without altering external behavior. Never introduce new features or behavior changes during a refactor.

## Net Engineering Value (NEV) Gate

Every refactoring proposal must demonstrate a positive score across 4 axes:

| Axis | Requirement | Immediate Failure Condition |
| :--- | :--- | :--- |
| **1. Runtime Performance** | Latency $\le$ baseline, allocations $\le$ baseline | Memory spikes or query count increases |
| **2. Abstraction Tax** | Zero wrapper hell, deleted dead code | Single-implementation interfaces, LOC bloat > 30% |
| **3. Cognitive Complexity** | Direct call paths, nesting $\le 3$ | Indirection layers with zero domain value |
| **4. Test Contract** | 100% existing test pass rate | Broken or deleted assertions |

## Refactoring Steps

1. **Baseline Pinning**: Run all tests before touching code; ensure clean baseline.
2. **Atomic Steps**:
   - Extract method / Rename symbol / Localize DTO / Inline shallow wrapper.
   - Run tests after each micro-step.
3. **Deletion Test**: For every abstraction touched, ask: *"If this interface or wrapper is removed, does anything break?"* If no, delete it.
4. **Post-Refactor Benchmark**: Verify memory allocations and execution times did not regress.
