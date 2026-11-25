---
name: compiler-runtime-analysis
description: Analyze compiler, runtime, and code generation systems including IR lowering, scheduling, memory layout, graph compilation, autotuning, and runtime overhead. Use when profiling a compiler stack, comparing generated code, debugging performance cliffs, or evaluating compiler research claims.
---
# Compiler Runtime Analysis

Use this skill when performance claims depend on what the compiler and runtime actually did.

## Core Workflow

1. State the source program, target hardware, runtime model, and optimization goal.
2. Trace the path from high-level program to lowered IR, generated code, and runtime launch behavior.
3. Use `references/measurement-checklist.md` before claiming a codegen win.
4. Separate compilation time, runtime overhead, and steady-state kernel performance.
5. Compare generated artifacts, not just wall-clock summaries.

## Execution Rules

1. Keep correctness and speed as separate gates.
2. Check shape specialization, caching, and autotuning warmup effects.
3. Distinguish compiler wins from library or kernel wins.
4. Always name the target backend and input regime.

## Output Contract

Return:

1. Pipeline map.
2. Measurement plan.
3. Likely bottlenecks.
4. Artifact comparison points.
5. Recommended interventions.
