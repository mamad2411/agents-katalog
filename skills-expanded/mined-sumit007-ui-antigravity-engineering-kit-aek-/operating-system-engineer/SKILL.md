---
name: operating-system-engineer
description: Architect OS kernels, bootloaders, interrupt handlers, virtual memory paging, and device drivers using Rust no_std, C, and assembly. Enforces hardware isolation and deterministic scheduling.
---

# Operating System Engineer Skill

## Purpose
Directs OS kernel architecture, bare-metal hardware bring-up, memory management units (MMU), and kernel debugging.

## When to Use
- Implementing bare-metal kernels or embedded microkernels in Rust (`no_std`) or C.
- Configuring page tables (x86_64 4-level/5-level paging, ARM64 TTBR).
- Writing interrupt descriptor tables (IDT), APIC timer drivers, and virtio drivers.

## Engineering Workflow
1. **Hardware Invariants**: Verify memory mappings, volatile register reads, and atomic barriers.
2. **Kernel Testing**:
   - Run integration tests inside headless QEMU (`qemu-system-x86_64`).
   - Debug state with GDB remote target (`target remote :1234`).

