---
name: overdrive-auditor
trigger: /overdrive
description: Run performance optimization audits and rendering budget verification on Pi Orchestra code paths. Use when optimizing UI rendering, resolving performance bottlenecks, or reviewing architectural memory constraints.
---

# /overdrive

Track, benchmark, and resolve performance regressions in Pi Orchestra using systematic measurement and structural refactoring. Focus primarily on eliminating $O(N^2)$ (O(N²)) iterations, preventing main-thread UI render stalls, and minimizing DOM/string overhead in high-throughput components (like the TUI and orchestrator dashboards).

## Key Principles

- **Measure First:** Never apply "optimizations" blindly. Use `vitest` benchmarks to prove a bottleneck exists, then measure again to prove your fix improves it.
- **Budget-Aware:** The TUI dashboard must render empty in under 0.5ms and handle 1000 running agents in under 40ms. Any code change that exceeds these budgets must be reverted.
- **Memory Overhead:** Prefer single-pass iterative loops and map lookups over chained `.map().filter()` calls that allocate massive intermediate arrays.
- **Async Awareness:** Do not block the Pi main thread. Calculate deterministic values (like text widths) *outside* of rendering loops.

## Operations

```
/overdrive run bench       # Run the full benchmark suite via `npm run bench:all`
/overdrive measure <file>  # Create a targeted benchmark for a specific file
/overdrive optimize <path> # Analyze the given path for common algorithmic violations
```

## Journaling
Always record major algorithmic findings in `.jules/overdrive.md`. Use the format:
- **Systemic Bottleneck:** ...
- **Refactor Strategy:** ...
- **Key Metric Shift:** ...
- **Actionable Principle:** ...
