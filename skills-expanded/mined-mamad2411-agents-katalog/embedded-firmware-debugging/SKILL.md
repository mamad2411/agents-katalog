---
name: embedded-firmware-debugging
description: Debug embedded C, C++, or Rust firmware, RTOS tasks, drivers, DMA, interrupts, peripherals, and board bring-up. Use when tracking timing bugs, register misconfiguration, boot failures, memory corruption, peripheral deadlocks, or hardware-software integration issues on MCUs, SoCs, and edge devices.
---
# Embedded Firmware Debugging

Use this skill when the boundary between firmware and hardware is the actual bug.

## Core Workflow

1. Reproduce with the exact board, clock tree, power path, firmware revision, and toolchain.
2. Build the boot path or event timeline.
3. Check registers, pin mux, clocks, interrupts, DMA, caches, and memory ownership with `references/bringup-checklist.md`.
4. Reduce to the smallest failing case.
5. If `platformio`, `cmake`, `cargo`, or vendor tools exist, use them; otherwise focus on static review and logs.
6. End with one best next probe, not a long list of guesses.

## Execution Rules

1. Keep ISR work minimal.
2. Verify volatile and atomic usage where concurrency exists.
3. Treat undefined behavior, stack issues, and memory ownership as first-class suspects.
4. Separate electrical uncertainty from firmware uncertainty.
5. Prefer timestamped traces and register snapshots over intuition.

## Output Contract

Return:

1. Reproduction facts.
2. Fault tree.
3. Suspect list.
4. Best next probe.
5. Code, config, or instrumentation changes.
