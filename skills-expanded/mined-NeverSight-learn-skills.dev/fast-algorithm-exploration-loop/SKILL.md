---
name: fast-algorithm-exploration-loop
description: Benchmark-driven workflow for converging on algorithms through small implementation spikes, fuzzing, visual diagnostics, and spec refinement. Use for algorithms, numerical methods, geometry, graphs, optimization, or data structures with multiple plausible approaches and measurable constraints such as correctness, error, runtime, memory, or robustness.
---

# Fast Algorithm Exploration Loop

## Purpose

Use this skill to find the right algorithm quickly when the correct approach is not obvious.

The core pattern is:

1. define a measurable target
2. build a tiny benchmark harness
3. try a few genuinely different algorithm families
4. learn from failures and measurements
5. narrow toward the most promising candidate

Prefer many cheap iterations over one elaborate design pass.

## When to use

Use this skill when:

- the task is algorithmic rather than product- or UI-driven
- multiple approaches are plausible
- success can be measured by correctness, numerical error, runtime, memory, or robustness
- the true specification will likely become clearer through experimentation

Do not use this skill for:

- standard CRUD or application glue
- tasks with a single obvious implementation path
- repo-wide planning or multi-milestone execution management

## Default operating surface

By default, keep the exploration state in a small local working set:

- `cases.json` for thresholds, seeds, and canonical cases
- `bench.py` for the executable comparison harness
- `spikes/` for competing implementations
- `notes.md` for hypotheses, results, failure patterns, and decisions

Do not assume any other planning skill or document structure exists.

## Optional composition with `long-horizon-codex`

If `long-horizon-codex` is also active, adapt this workflow to its control-plane documents instead of duplicating them.

- keep this skill focused on the algorithm exploration loop
- mirror durable conclusions into the long-horizon docs
- avoid creating a competing project-planning system

The long-horizon skill only changes where durable planning and status information live.

## Operating model

Treat the specification as a versioned hypothesis.

- spec v0: initial guess
- spec v1: learned constraint
- spec v2: refined behavior
- spec freeze: stable enough to implement cleanly

Early iterations are for discovery. Later iterations are for convergence.

## Minimal harness

Keep the exploration harness small enough that one full loop is cheap to run.

Example shape:

```text
bench.py            # golden + fuzz + perf summary
cases.json          # seeds, thresholds, golden cases, spec version
spikes/
  ref.py            # slow but trusted oracle or baseline
  a.py
  b.py
  c.py
notes.md            # hypotheses, results, and durable takeaways
```

Prefer one command such as `python bench.py`.

The full loop should usually stay under about five minutes. If it is slower, shrink the default workload and keep heavier runs optional.

## Exploration loop

### 1. Define "good enough"

Before trying optimizations, define the measurable target:

- correctness requirements
- error tolerance
- runtime target such as p50 or p95
- memory ceiling if relevant
- fuzz policy such as zero failures or a specific tolerance

These thresholds may change early, but every change must be explicit.

### 2. Build a minimal benchmark

Use three inputs:

- golden cases: 10-30 deterministic edge cases
- fuzz cases: random generation with a fixed seed
- perf cases: representative fixed workloads run repeatedly

Golden cases should include:

- boundary inputs
- degenerate structures
- previously failing examples
- domain-specific tricky cases

Any failing fuzz seed that matters should be promoted into a regression case.

Avoid heavyweight benchmarking infrastructure unless the task truly needs it.

### 3. Generate diverse spikes

Before coding, sketch 3-5 materially different algorithm families.

Try to cover distinct categories such as:

- reference or oracle
- exact but slower
- accelerated
- approximate
- hybrid

Do not waste iterations on cosmetic variants of the same idea until evidence says a family is worth refining.

### 4. Implement minimal spikes

Rules:

- keep the same interface across spikes
- avoid heavy dependencies unless they are intrinsic to the approach
- optimize for learning value first
- keep one trusted baseline, even if it is slow

The reference implementation is the correctness anchor.

### 5. Run, compare, narrow

Each benchmark pass should answer:

- which spikes are correct
- which failures are new
- which candidate dominates on the target metric
- what assumption just broke

A simple table is enough:

```text
impl | golden | fuzz | max_err | p95_ms | notes
ref  | pass   | pass | 0       | 950    | slow baseline
a    | pass   | fail | 1e-4    | 12     | numeric instability
b    | pass   | pass | 1e-8    | 15     | candidate
```

Use the result to either:

- kill a weak approach
- refine a promising family
- or revise the spec

## Failure handling

Every real failure should produce one of these outcomes:

- a new regression case
- a recorded failing seed
- a sharper statement of the spec
- rejection of the current algorithm family

Useful failure categories:

- boundary condition
- degenerate input
- numerical precision
- invalid hidden assumption
- performance blow-up

The loop is only working if failures become permanent knowledge.

## Visual diagnostics

If the problem has a natural visual representation, generate at least one lightweight visual artifact during benchmark runs.

This is especially useful for:

- geometry and spatial algorithms
- graphs and topology
- raster or grid processing
- clustering or segmentation
- simulation states
- pathfinding

Good artifacts include:

- GeoJSON or SVG overlays
- scatterplots
- heatmaps
- convergence curves
- focused failure snapshots

Prefer visuals that show input, output, and the failing or intermediate structure in one view.

## Notes and artifacts

Keep experiment records short and operational.

For each meaningful iteration, capture:

- hypothesis
- spike path or implementation name
- result summary
- interpretation
- next experiment

A single local `notes.md` is usually enough.

If another planning skill is active, mirror durable conclusions into that system, but keep the local exploration notes lean and practical.

## Commit behavior

Do not assume every iteration should become its own git commit.

- if the repo already has a commit cadence or the active plan specifies one, follow that
- if the user explicitly wants experimental checkpoints, commit at useful learning boundaries
- otherwise optimize for a clean, reviewable final change rather than noisy experiment history

## Exit criteria

Leave exploration mode when all of these are true:

- one candidate clearly satisfies the target thresholds, or the remaining tradeoff is explicit
- known important failures are either fixed or intentionally accepted
- the specification is stable enough to implement or integrate cleanly
- the next step is ordinary engineering rather than more search

At that point, stop generating new spikes and fold the winning approach into the main implementation or plan.
