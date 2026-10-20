---
name: wp-divi-5-cache-performance-diagnostics
description: Diagnoses Divi 5 static CSS, plugin, server, object, CDN, browser, and performance-option behavior, and distinguishes stale assets from backward-compatibility overhead using one-layer-at-a-time tests.
---

# Divi 5 Cache and Performance Diagnostics

Use this skill for stale styles, update-related display regressions, slow Divi pages, or suspected compatibility-mode overhead.

## Procedure

1. Capture the symptom, timing, URLs, cache headers, version state, and baseline performance evidence.
2. Determine whether the issue is correctness, latency, or both.
3. Test private window and `?nocache=1` as clues.
4. Clear the Divi CSS cache and recheck.
5. Clear plugin, server, object, and CDN caches one layer at a time.
6. Record which action changed the symptom.
7. Review Divi performance options one at a time; restore non-causal settings.
8. Check affected pages for backward-compatibility mode and legacy modules.
9. Compare native Divi 5 pages and compatibility-mode pages under similar conditions.
10. Document the cause, confidence, and durable remediation.

## Guardrails

- Do not purge every cache layer at once before evidence capture.
- Do not disable multiple performance options together.
- Do not promise that cache clearing or compatibility cleanup will solve unrelated server, database, media, or network bottlenecks.
- Do not delete cache directories directly unless the environment owner approves the path and blast radius.
- Treat one legacy module as page-wide Divi 4 framework overhead.

## Workflow

Use [diagnose-divi-cache-performance-workflow.md](workflows/diagnose-divi-cache-performance-workflow.md).

## Resources

- [cache-layer-checklist.md](resources/cache-layer-checklist.md)
- [performance-investigation-record-example.md](examples/performance-investigation-record-example.md)

## Output

Return:

- Symptom and baseline.
- Cache/performance layers tested in order.
- Evidence for the causal layer.
- Compatibility-mode findings.
- Smallest durable remediation.
- Remaining non-Divi hypotheses.
