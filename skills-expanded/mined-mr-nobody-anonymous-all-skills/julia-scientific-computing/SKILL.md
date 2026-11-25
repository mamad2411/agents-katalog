---
name: julia-scientific-computing
description: "Write performant Julia: type-stable functions, multiple dispatch, broadcasting, project environments, and benchmarking with BenchmarkTools."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - julia type stability
  - julia performance optimization
  - julia multiple dispatch design
  - julia project environment
  - julia benchmark
keywords:
  - julia
  - multiple-dispatch
  - type-stability
  - benchmarktools
  - scientific-computing
source: custom
enabled: true
---

# Julia Scientific Computing

## Purpose

Write performant Julia: type-stable functions, multiple dispatch, broadcasting, project environments, and benchmarking with BenchmarkTools.

## When to Use

- You are writing numerical or scientific Julia code that must be fast.
- An allocation or dispatch problem is making a loop slow.
- You need a reproducible project environment with pinned packages.

## When NOT to Use

- The task is a one-off data munge better served by a scripting language already installed.
- The bottleneck is I/O or an external solver rather than Julia code.
- You need GPU kernels; that requires a separate, hardware-specific skill.

## Capabilities

- Write type-stable functions verified with `@code_warntype`.
- Use dispatch and parametric types instead of runtime branching.
- Measure allocations and time with BenchmarkTools rather than `@time` guesses.
- Pin dependencies per project with Project.toml and Manifest.toml.

## Inputs

- The Julia version and whether a project environment exists.
- The hot loop or function and its measured baseline.
- Array shapes, dtypes and expected sizes.

## Workflow

1. Activate the project environment so results are reproducible.
2. Profile or benchmark the current implementation and record the number.
3. Make the function type-stable; add type parameters rather than `Any` containers.
4. Reduce allocations in the inner loop; hoist work out and preallocate outputs.
5. Re-benchmark with the same inputs and keep the before/after evidence.

## Tools

- julia --project
- BenchmarkTools
- Profile / @code_warntype

## Examples

- `julia --project=. -e 'using Pkg; Pkg.instantiate()'`
- `@benchmark sum_loop(data)`
- `@code_warntype simulate(1.0, params)`

## Safety

- Global variables with non-constant types silently destroy performance.
- Do not commit Manifest.toml changes you did not intend to pin.
- Numerical results must be validated against a known reference, not just timed.

## Source

All-Skills canonical library (`skills/programming/julia-scientific-computing`). First-party skill, maintained in this repository.

## Notes

- Type stability beats micro-optimization: fix `@code_warntype` first.
- Broadcasting with `.` avoids temporary copies only when the expression is fused.
- Pairs with: `programming/numerical-methods`, `scientific/computational-physics`.
