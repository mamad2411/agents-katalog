---
name: rust-crate-decomposition
description: >
  Splits a large single-compilation-unit codebase (e.g. one giant crate,
  or a monolithic Zig/C project being ported) into many Rust crates to
  parallelize and speed up compilation — while avoiding cyclic
  dependencies and minimizing divergence from the original structure. Use
  when Rust build times are dominated by one huge crate, when planning how
  to organize a ported codebase into crates, when the user hits "cyclic
  dependency between crates" errors, or asks "how do I split my Rust
  project into crates" / "how many crates should this be". This skill is
  about DESIGNING crate boundaries and breaking dependency cycles; for
  burning down the mass of compiler errors that a split produces, use
  compiler-errors-as-work-queue. Part of the port-to-rust-playbook.
---

# Rust crate decomposition

Rust compiles a crate as a unit, so one enormous crate compiles slowly and serially. Splitting a ported codebase into many crates (Bun targeted ~100) lets the build parallelize — but crate boundaries are a directed acyclic graph, and a codebase that used to be one compilation unit almost certainly contains dependency cycles that only become errors once you draw the boundaries. This skill is about drawing those boundaries well.

## Goals, in priority order

1. **Acyclic crate graph.** Rust forbids circular crate dependencies. This is the hard constraint everything else bends around.
2. **Minimize divergence from the original structure.** A mechanical port's value is that the new code mirrors the old; gratuitous re-architecture during the split makes the port harder to review against the source. Move code only as much as breaking cycles requires.
3. **Parallelizable compilation.** Prefer many focused crates over a few broad ones, and keep widely-depended-on crates (core types, allocator, string, collections) small and leaf-like so they don't serialize the build.

These pull against each other: perfectly clean boundaries would move a lot of code (violating #2), and minimal movement leaves cycles (violating #1). The job is the least code movement that yields an acyclic graph.

## Sequence

Splitting is easiest to do as its own stage, not tangled into translation or error-fixing.

1. **Attempt the split before/early in the port if you can.** A pre-port PR that reorganizes the source into would-be crate boundaries gives the translation a target shape. Expect it to be **insufficient** — some cycles only appear once the code is actually in Rust with real crate boundaries. That's normal; don't treat the initial split as final.
2. **Classify where cyclic code should go — as a written plan first.** Run a dedicated analysis pass (a workflow loop, see `porting-workflow-loops`) that identifies each cyclic dependency and *records* where the offending code should live to break the cycle. Do the thinking and write it down before touching code — cycles are a graph problem, and solving them while also fixing unrelated compile errors mixes two hard tasks.
3. **Run the refactor pass** that executes the classification plan: move types, split modules, introduce a shared leaf crate for commonly-referenced definitions.
4. **Let the compiler-error queue clean up the rest** (see `compiler-errors-as-work-queue`). Fixing the cycles will surface a large number of downstream errors — Bun's split revealed ~16,000. That count is a queue, not a disaster.

## Techniques for breaking cycles

When crate A and crate B depend on each other:

- **Extract the shared surface into a leaf crate.** If A and B both need type `T`, move `T` into a small `*_core` / `*_types` crate that both depend on. This is the most common and least disruptive fix — it moves definitions, not logic.
- **Invert a dependency with a trait.** If A calls into B only through a narrow interface, define a trait in A (or the core crate) and have B implement it, so the concrete dependency points one way.
- **Split a crate that wears two hats.** A crate that is depended on for one purpose and depends back for another is really two crates; separate the halves.
- **Move the offending item, not the whole module.** Prefer relocating the specific type/function causing the cycle over reorganizing everything around it — keeps divergence from the source low.

Avoid resolving cycles by merging crates back together (defeats the compile-time goal) or by stubbing/gating code to make the error disappear (see the anti-stub rule in `compiler-errors-as-work-queue`).

## Guardrails

- **Keep core crates tiny and dependency-free.** `*_alloc`, `*_string`, `*_collections`, `*_ptr`, `*_core` should sit at the bottom of the graph with no upward edges. If a foundational crate starts depending on a feature crate, that's a cycle waiting to happen.
- **Name crates after the source's modules** where possible, so the crate graph reads like the original architecture.
- **Do the split as one deliberate phase**, then freeze boundaries while the error queue and tests run — reshuffling crates mid-error-burndown invalidates in-flight fixes.
