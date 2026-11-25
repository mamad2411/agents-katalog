---
name: domain-embedded-and-iot
description: Use for Rust `no_std`, firmware, device control, interrupts, constrained edge nodes, and Internet of Things (IoT) systems where memory, timing, and hardware contracts dominate.
globs: ["**/Cargo.toml", "**/*.rs", "**/.cargo/config.toml"]
---

# Rust Embedded and IoT

Use this when hardware or edge-device constraints change the normal Rust
trade-offs.

## Working stance

- Own hardware resources explicitly and keep access paths singular.
- Prefer fixed-size storage and predictable timing over convenience.
- Interrupt and task boundaries are data-ownership boundaries.
- Unsafe code is often justified here, but only with tight invariants.
- Pair this skill with `rust-memory-and-state` first, then
  `rust-unsafe-and-ffi` or `rust-performance-and-layout` if needed.

## Domain pressure

- Heap use may be unavailable or strategically forbidden.
- Shared state must be safe across interrupts, tasks, or device callbacks.
- IO reliability often matters more than throughput.
- Device update and reconnect paths need explicit failure classification.

## Red flags

- ownership of peripherals is ambiguous,
- timing-sensitive paths allocate or lock unpredictably,
- interrupts mutate shared state without a clear synchronization story,
- unsafe register or FFI access is written before the contract is stated.
