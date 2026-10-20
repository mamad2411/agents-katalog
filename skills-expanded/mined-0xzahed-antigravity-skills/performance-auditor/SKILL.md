---
name: performance-auditor
description: Run an end-to-end performance audit. Use when diagnosing overall
  system slowness or setting perf targets.
metadata:
  tags: performance, auditor
---

# Performance Auditing

## Use this skill when
- Investigating slow user-visible performance
- Finding the dominant bottleneck across stack
- Recommending and verifying fixes

## Do not use this skill when
- Frontend-only (use frontend-performance)
- DB-only (use database-performance-auditor)

## Instructions
1. Define the observed symptom and SLO (latency/throughput).
2. Measure across layers: network, CDN, app, data.
3. Identify where time actually goes (traces, profiles).
4. Check topology: payloads, caching, latency chains.
5. Prioritize by user impact and effort.
6. Verify each fix with before/after numbers.
7. Produce a prioritized, evidence-based report.

## Checklist
- Measurement driven
- Dominant bottleneck identified
- Fixes verified

## Output Format
- Area | evidence | bottleneck | fix | verified impact

## Common Mistakes
- Optimizing without baseline
- Splitting time across layers haphazardly
- No re-measurement

## References
- `references/audit-method.md` – Measurement method, layering cheat-sheet, golden signals, before/after discipline
