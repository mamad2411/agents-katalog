---
name: capability-aware-offload-skipping
description: "Skip generic offload wrappers for tools that already bound output locally or would become circular if wrapped again."
metadata:
  author: ychampion
---

# SKILL: Capability-Aware Offload Skipping
**Domain:** tool-result-storage
**Trigger:** Use when a generic result-offload layer wraps many tools, but some tools already enforce their own output bounds or would recurse if wrapped again.
**Source Pattern:** Distilled from reviewed output-budget enforcement and selective offload-policy implementations.

## Core Method
Before applying a generic persistence or preview wrapper, inspect each tool's declared behavior and opt out the tools whose own contract already bounds output or would create a circular readback loop. Treat the skip as a stable policy decision rather than a one-off exception so identical tools keep the same behavior across turns. This preserves the generic offload path where it adds value while avoiding redundant or self-referential wrapping.

## Key Rules
- Check declared limits and self-bounded reader behavior before applying a generic offload layer.
- Keep the skip decision stable across turns so identical tool results do not oscillate between wrapped and unwrapped behavior.
- Mark skipped results consistently when broader budgeting logic depends on deterministic treatment across turns.
- Prefer tool-specific contracts over wrapper-level force when the wrapper would just reintroduce the same content through another tool.

## Example Application
If a read-style tool already caps output aggressively, exclude it from a generic file-offload wrapper; otherwise the wrapper would persist bounded content and ask the model to read it back through the same tool, adding complexity with no real gain.

## Anti-Patterns (What NOT to do)
- Do not wrap every tool uniformly just because a generic offload helper exists; some tools already solve the problem locally.
- Do not let skip decisions fluctuate between turns, or identical tool results will produce inconsistent prompt prefixes and cache behavior.
