---
name: zephyr-kernel-synchronization
description: Expert guidance on Zephyr kernel synchronization primitives (Semaphores, Mutexes, Events, Condition Variables). Use when the user asks about thread synchronization, locking, signaling, mutual exclusion, priority inversion, thread-safe resource access, ISR-to-thread signaling, or choosing the right synchronization primitive in Zephyr RTOS.
---

# Zephyr Kernel Synchronization

## Overview

This skill provides expert knowledge on the four main synchronization primitives in the Zephyr kernel: Semaphores, Mutexes, Events, and Condition Variables. It helps in selecting the right primitive for the task and provides implementation details, common patterns, and pitfall avoidance.

When synchronization choices affect whether threads block cleanly enough for the system to reach low-power states, also read [../zephyr-power-management/SKILL.md](../zephyr-power-management/SKILL.md).

## Workflow

### 1. Selection Strategy

To choose the correct synchronization primitive, first determine the requirements:

-   **ISR Involvement?** Can an ISR give/take/signal, or only threads?
-   **Ownership?** Must the same thread that locks also unlock?
-   **Priority Inversion?** Is priority inheritance needed?
-   **Signaling Pattern?** One-to-one, one-to-many, many-to-many?
-   **Condition Complexity?** Simple event bits or complex state predicates?

**Step 1:** Read [references/comparison.md](references/comparison.md) for the feature matrix and decision flowchart.

### 2. Implementation

Once the primitive is selected, use the implementation guide to write the code.

**Step 2:** Read the appropriate reference:

-   **Semaphores**: [references/semaphores.md](references/semaphores.md) — Counting/binary semaphores, ISR signaling, resource limiting.
-   **Mutexes**: [references/mutexes.md](references/mutexes.md) — Mutual exclusion, priority inheritance, reentrant locking.
-   **Events**: [references/events.md](references/events.md) — Bitmask events, many-to-many signaling, wait options.
-   **Condition Variables**: [references/condvar.md](references/condvar.md) — Waiting for complex state changes with a mutex.

### 3. API & Configuration

For complete API signatures, Kconfig options, and resource locations.

**Step 3:** Read [references/api.md](references/api.md) for:

-   Complete API function signatures for all primitives.
-   Relevant Kconfig options.
-   Header file locations.

### 4. Troubleshooting

Common issues with synchronization:

-   **Deadlocks**: Multiple mutexes locked in inconsistent order.
-   **Priority Inversion**: Use mutexes (not semaphores) when threads of different priorities share resources.
-   **Spurious Wakeups**: Always use `while()` loops with condition variables.
-   **ISR Blocking**: Never wait/block in ISRs — use `K_NO_WAIT` or check return values.

Refer to the **Common Pitfalls** sections in each reference file for detailed guidance.

## Source Locations

| Description | Path |
| :--- | :--- |
| **Synchronization Docs** | `<zephyr-ws>/deps/zephyr/doc/kernel/services/synchronization` |
| **Kernel Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/kernel.h` |
| **Semaphore Sample** | `<zephyr-ws>/deps/zephyr/samples/synchronization` |
| **Condition Var Sample** | `<zephyr-ws>/deps/zephyr/samples/kernel/condition_variables` |
| **Philosophers Sample** | `<zephyr-ws>/deps/zephyr/samples/philosophers` |

*Note: `<zephyr-ws>` represents the root of the Zephyr workspace.*
