---
name: ops-process-optimization
version: 1.0.0
description: Find the constraint in a slow or error-prone process and propose the smallest changes that move a measured metric.
author: matrixx0070
tags: [operations, process, optimization, lean, bottleneck, theory-of-constraints]
capabilities: []
---

# Process Optimization

## When to use
Use this when a process is too slow, error-prone, costly, or inconsistent, and you need to find the constraint and propose changes that move a metric — not just redraw the diagram.

**Not for:** documenting a process for the first time (use ops-process-doc — you cannot optimize what you cannot measure), or processes with no baseline data. If there are no numbers, stop and collect them first.

## Method
1. **Quantify current state.** Measure the baseline: cycle time, throughput, error rate, cost per unit, and lead vs. process time. *Decision:* no numbers? Stop and instrument before proposing anything.
2. **Map the value stream.** Break the process into steps; tag each as value-add, necessary non-value-add, or waste.
3. **Find the bottleneck.** Identify the constraint (longest queue or slowest step) and the waste types present (waiting, rework, handoffs, over-processing).
4. **Root-cause it.** Apply 5 Whys or cause categorization to the constraint; separate symptoms from causes.
5. **Design improvements.** Propose changes (eliminate, automate, parallelize, reorder, standardize) and estimate each one's metric impact.
6. **Prioritize.** Rank by impact vs. effort; fix the constraint first. *Decision:* improving a non-bottleneck step adds zero throughput — resist it.
7. **Define measurement.** State how you confirm the improvement and guard against regression.

## Example
Invoice approval: lead time 6 days, but process time only 40 min — 99% is waiting. Value-stream map shows invoices queue 4 days at manager approval (the constraint). 5 Whys: manager approves in weekly batch. **Change:** auto-approve invoices under $500 (60% of volume), route rest daily. **Projected:** lead time 6 days -> 1.5 days; effort low. **Verify:** track weekly lead-time median for 4 weeks; alert if >2 days.

## Pitfalls
- **Optimizing a non-bottleneck.** Speeding up a step upstream of the constraint just grows the queue in front of it.
- **No baseline.** Without before-numbers you can't prove improvement or catch regression — it becomes opinion.
- **Solving symptoms.** "Add a checker" treats rework, not the cause producing defects.
- **Big-bang redesign.** The smallest change that relieves the constraint beats a total re-architecture nobody adopts.

## Output format
```
Baseline:       metric | current value
Value stream:   step | time | classification (VA / NNVA / waste)
Constraint:     bottleneck + root cause
Backlog:        change | expected impact | effort | priority
After-state:    metric | target value
Verification:   how measured | regression guard
```
