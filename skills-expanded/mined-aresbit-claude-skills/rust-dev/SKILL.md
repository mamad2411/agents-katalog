---
name: rust-dev-skill
description: >-
  AI-assisted Rust development with code contracts, lightweight spec-driven
  development, and performance optimization. Use when writing, reviewing, or
  optimizing Rust code -- especially for distributed systems, consensus protocols,
  or any correctness-critical Rust project. Triggers on Rust development tasks,
  performance tuning requests, "write Rust code with contracts", "optimize Rust
  performance", "spec-driven Rust development", or AI-assisted Rust workflows
  modeled on 100K+ line production-grade Rust projects.
---

# Rust AI-Assisted Development

Production-grade Rust development methodology distilled from building a 130K-line multi-Paxos consensus engine with AI coding agents. Covers code contracts for correctness, lightweight spec-driven development, and aggressive performance optimization.

## Core Workflow

```
Specify → Clarify → Contract → Implement → Test → Optimize
```

Each phase below has a corresponding deep-dive reference. Load the reference when entering that phase.

## 1. Lightweight Spec-Driven Development

Use `/specify` (spec-kit) to generate a spec markdown with user stories and acceptance criteria. One user story is the "sweet spot" unit of work for today's AI agents.

**Workflow:**
1. `/specify` — Generate spec with user stories + acceptance criteria
2. `/clarify` — AI self-critiques and improves the spec; suggest additional user stories
3. Enter **plan mode** for a single user story
4. Implement that user story end-to-end
5. Repeat for next user story

**Key insight:** Rigid SDD (requirements → design → task list) is too brittle. A single spec markdown per feature, clarified and refined interactively, keeps documents consistent while avoiding overhead.

> See [references/sdd-workflow.md](references/sdd-workflow.md) for the full `/clarify` interaction pattern and user story templates.

## 2. Code Contracts — Three Levels

Code contracts specify **preconditions**, **postconditions**, and **invariants** for critical functions. They become runtime asserts in testing and are compiled out in production.

### Level 1: AI Writes Contracts

Ask AI to write contracts for critical functions. GPT-5 High writes the best contracts; Opus 4.1 is adequate. Focus human effort on reviewing and refining.

Example for a Paxos `process_2a` method (16 contracts total):
```rust
/// Precondition: ballot_number > 0
/// Precondition: slot_number >= first_slot
/// Postcondition: returns Ok(()) iff the proposal is accepted
/// Postcondition: accepted_proposals[slot_number] == Some(proposal)
/// Invariant: accepted_proposals.len() does not decrease
fn process_2a(&mut self, msg: Phase2aMessage) -> Result<()> { ... }
```

### Level 2: Generate Tests from Contracts

For each postcondition, ask AI to generate targeted test cases covering edge cases.

### Level 3: Property-Based Tests

Ask AI to translate contracts into property-based tests (e.g., with `proptest`). Randomized inputs explore a vast state space — any contract violation triggers a panic.

> See [references/code-contracts.md](references/code-contracts.md) for contract authoring guidelines and property-based test patterns.

## 3. Testing Pyramid

Layer tests by scope — AI excels at generating all three levels:

1. **Unit tests** — Per-function, contract-driven
2. **Minimal integration tests** — Two-component pairs (e.g., proposer + acceptor)
3. **Full integration tests** — Multi-replica with injected failures (network partition, crash-recovery, message reordering)

Aim for tests to comprise 60%+ of the codebase. 1,300+ tests for a 130K-line project is a healthy ratio.

## 4. Performance Optimization Loop

Rust's safety model enables aggressive optimization without fear. The proven loop:

```
1. Instrument → add latency metrics across all code paths
2. Measure    → run perf tests, output trace logs
3. Analyze    → AI writes Python scripts for quantile/bottleneck analysis
4. Optimize   → AI proposes optimizations, implement one at a time
5. Repeat     → re-measure after each change
```

**Rust-specific targets (in priority order):**
- Minimize allocations (use `&[u8]` over `Vec<u8>`, arena allocators)
- Apply zero-copy techniques (`Bytes`, `Cow`, borrowed slices)
- Eliminate lock contention (consider `parking_lot`, sharded locks, lock-free structures)
- Remove unnecessary async overhead (don't `tokio::spawn` for trivial work)
- Batch operations to amortize syscall/network costs

> See [references/perf-optimization.md](references/perf-optimization.md) for the full instrumentation and analysis workflow.

## 5. AI Coding Agent Patterns

### CLI-First Workflow
Code from the terminal (Claude Code / Codex CLI), use VS Code only for diff review and minor edits. This creates an asynchronous flow that maximizes throughput.

### Task Sizing
One user story = one coding session. AI agents handle this scope well without context compression becoming a problem.

### Rate Limit Strategy
For heavy usage, stagger across multiple subscriptions or accounts to handle rate limits.

## Quick Reference

| Phase | Command/Tool | Output |
|-------|-------------|--------|
| Specify | `/specify` from spec-kit | Spec markdown with user stories |
| Clarify | `/clarify` | Refined stories + edge cases |
| Contract | Ask AI: "write contracts for X" | Pre/post/invariant annotations |
| Test Gen | Ask AI: "generate tests from these contracts" | Unit + property-based tests |
| Perf | `perf` script (see references) | Latency breakdown → bottleneck |

## Resources

### scripts/
- `instrument_rust.py` — Add `tracing` instrumentation spans to Rust functions

### references/
- [code-contracts.md](references/code-contracts.md) — Contract authoring, property-based test patterns, Paxos case study
- [sdd-workflow.md](references/sdd-workflow.md) — `/specify` → `/clarify` → plan mode full workflow
- [perf-optimization.md](references/perf-optimization.md) — Instrumentation, bottleneck analysis, Rust-specific optimizations
