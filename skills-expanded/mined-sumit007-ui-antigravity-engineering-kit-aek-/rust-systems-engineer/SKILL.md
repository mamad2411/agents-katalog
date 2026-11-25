---
name: rust-systems-engineer
description: Guides development, optimization, and auditing of mission-critical systems software in Rust. Enforces zero-cost abstractions, memory safety, async Tokio patterns, and fearless concurrency.
---

# Rust Systems Engineer Skill

## Purpose
Provides deep expertise in Rust systems programming, memory safety, async runtimes, and low-level performance engineering.

## When to Use
- Implementing Rust services, CLI tools, network daemons, or system libraries.
- Resolving complex borrow checker issues, lifetime bounds, or invariant generic parameters.
- Auditing `unsafe` blocks and designing sound safe abstractions.
- Optimizing CPU utilization, cache locality, and allocations.

## Engineering Workflow
1. **Architecture & Types**: Define strong newtypes, domain invariants, and typed error enums via `thiserror`.
2. **Concurrency**: Use Tokio or crossbeam channels with bounded capacity. Enforce cancellation safety.
3. **Verification**:
   - `cargo fmt --all -- --check`
   - `cargo clippy --workspace --all-targets -- -D warnings`
   - `cargo test --workspace`
4. **Safety Review**: Proactively audit pointer provenance, slice indexing bounds, and potential deadlocks.

