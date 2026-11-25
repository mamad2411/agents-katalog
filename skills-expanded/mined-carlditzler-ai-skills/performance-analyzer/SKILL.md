---
name: performance-analyzer
description: Use for startup slowness, jank, memory growth, oversized work, bridge overhead, expensive recomposition or rendering, and other runtime performance problems across Swift, Android, Flutter, Tauri, Rust, and frontend code.
---

# Performance Analyzer

## Use when
- the user reports slowness, jank, excessive memory use, or costly repeated work
- the task is performance improvement rather than feature delivery
- a review needs to focus on runtime or rendering efficiency

## Do not use when
- the performance concern is speculative and there is no meaningful symptom
- the task is mostly architecture or feature work with no performance requirement

## Working rules
- Prioritize user-perceived responsiveness before micro-optimization.
- Remove repeated or unnecessary work before tuning constants.
- Prefer evidence from measurements, tooling, traces, or strong repo-local reasoning.
- Avoid caches, memoization, or complexity that outlives the actual bottleneck.
- Re-check correctness and UX after optimization work.

## Workflow
1. Define the symptom precisely: startup, navigation, interaction latency, render jank, memory growth, bridge overhead, or bundle size.
2. Identify where time, allocations, or invalidation are likely being spent.
3. Measure when tooling is available; otherwise state the strongest evidence and uncertainty.
4. Choose the highest-impact, lowest-risk changes first.
5. Apply the smallest fixes that reduce real work.
6. Re-validate behavior, correctness, and release risk.

## Quality bar
- Focus on work that users can feel or that meaningfully affects release quality.
- Call out likely issues separately from confirmed issues.
- Do not trade maintainability for tiny wins unless the impact is real.

## Reference routing
- Read `references/performance-checklist.md` for optimization and triage prompts.
- Read `references/release-quality-gates.md` when performance threatens release quality.
- Read `references/official-docs.md` only for platform-specific performance semantics.

## Output contract
Provide:
- confirmed issues
- likely issues still needing measurement
- fixes ordered by impact versus effort
- validation run
- release-risk assessment
