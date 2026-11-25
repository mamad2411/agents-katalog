---
name: zephyr-memory
description: Expert guidance on Zephyr RTOS memory management (Heaps, Memory Slabs, Memory Blocks, Memory Domains, Virtual Memory). Use when the user asks about dynamic memory allocation, memory pools, k_malloc, k_heap, memory slabs, fixed-size allocators, memory protection, memory partitions, userspace memory isolation, virtual memory, demand paging, or choosing the right memory allocator in Zephyr.
---

# Zephyr Memory Management

## Overview

Zephyr provides multiple memory management mechanisms tailored for different embedded use cases. This skill helps select the right allocator, implement memory patterns correctly, and avoid common pitfalls.

## Workflow

### 1. Allocator Selection

Determine requirements before choosing:

-   **Block size variability?** Fixed vs variable-size allocations
-   **Determinism needed?** Constant-time allocation requirements
-   **Fragmentation tolerance?** Long-running systems need fragmentation resistance
-   **Memory protection?** Userspace isolation requirements
-   **ISR context?** Some allocators cannot be used from ISRs

**Step 1:** Read [references/comparison.md](references/comparison.md) for the allocator decision matrix.

### 2. Implementation

Once the allocator is selected, implement using the appropriate guide.

**Step 2:** Read the appropriate reference:

-   **Heaps**: [references/heaps.md](references/heaps.md) — Variable-size dynamic allocation (`k_heap`, `k_malloc`, `sys_heap`).
-   **Memory Slabs**: [references/slabs.md](references/slabs.md) — Fixed-size block allocation with zero fragmentation.
-   **Memory Blocks**: [references/mem_blocks.md](references/mem_blocks.md) — Multi-block allocator with external bookkeeping.
-   **Memory Domains**: [references/domains.md](references/domains.md) — Memory partitions for userspace thread isolation.
-   **Virtual Memory**: [references/virtual.md](references/virtual.md) — MMU-based memory mapping and demand paging.

### 3. API & Configuration

For complete API signatures and Kconfig options.

**Step 3:** Read [references/api.md](references/api.md) for:

-   Complete API function signatures for all allocators.
-   Relevant Kconfig options.
-   Header file locations.

### 4. Troubleshooting

Common memory management issues:

-   **Fragmentation**: Use slabs or mem_blocks for fixed-size allocations; prefer multiple purpose-specific heaps over one large heap.
-   **Stack overflow**: Enable `CONFIG_HW_STACK_PROTECTION`; size stacks appropriately with `CONFIG_*_STACK_SIZE`.
-   **ISR allocation failures**: Never block in ISRs; use `K_NO_WAIT` and handle allocation failures.
-   **Memory leaks**: Track allocations; use heap listeners (`CONFIG_HEAP_LISTENER`) for debugging.
-   **Userspace access violations**: Verify memory partitions are correctly configured and threads are assigned to the right domains.

## Source Locations

| Description | Path |
| :--- | :--- |
| **Memory Management Docs** | `<zephyr-ws>/deps/zephyr/doc/kernel/memory_management` |
| **Memory Domain Docs** | `<zephyr-ws>/deps/zephyr/doc/kernel/usermode/memory_domain.rst` |
| **Memory Services Docs** | `<zephyr-ws>/deps/zephyr/doc/services/mem_mgmt` |
| **Kernel Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/kernel.h` |
| **Sys Heap Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/sys/sys_heap.h` |
| **Mem Blocks Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/sys/mem_blocks.h` |
| **Mem Domain Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/app_memory/mem_domain.h` |
| **Heap Sample** | `<zephyr-ws>/deps/zephyr/samples/kernel/heap` |
| **Slab Sample** | `<zephyr-ws>/deps/zephyr/samples/kernel/mem_slab` |

*Note: `<zephyr-ws>` represents the root of the Zephyr workspace.*
