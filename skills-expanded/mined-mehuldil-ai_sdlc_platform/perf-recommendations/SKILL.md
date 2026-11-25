---
name: perf-recommendations
description: Generate optimization recommendations and validate performance improvements against budgets and targets
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

# Performance Recommendations Skill

Identifies performance bottlenecks, recommends optimizations, and validates improvements.

## Optimization Recommendations

### CPU Optimization
- Profile >50ms tasks, break into chunks
- Use requestIdleCallback for non-critical work
- Tree-shake unused code, code-split large modules
- Lazy load routes, remove unused polyfills
- Optimize loop performance

### Memory Optimization
- Remove event listeners on cleanup
- Clear timers/intervals, nullify references
- Profile with Heap Snapshots regularly
- Lazy load images/videos
- Implement cache eviction policies
- Use object pooling

### Render Optimization
- Optimize React renders (useMemo, useCallback)
- Reduce re-renders, use React Profiler
- Implement virtualization for long lists
- Debounce scroll/resize handlers
- Use transform/opacity instead of position changes

### Network Optimization
- Implement caching strategies (HTTP headers)
- Request batching (combine multiple requests)
- Response compression (gzip, brotli)
- Service workers for offline support
- Image optimization (WebP, responsive)

### Startup Optimization
- Lazy load non-critical features
- Prefetch critical resources
- Minimize initial bundle
- Async load analytics/ads
- Preload fonts and critical images

### Battery Optimization
- Reduce polling frequency
- Implement exponential backoff
- Cancel requests when backgrounded
- Use efficient networking (HTTP/2)
- Avoid continuous CPU usage

## Validation Against Budgets

Checks:
- Cold Startup: < 2000ms
- Memory Active: < 400MB
- FPS: >= 60
- Bundle Size: <= 50MB

Reports improvement percentages and pass/fail for each metric.

## Recommendation Report

Documents:
- Critical Issues (MUST FIX)
- High Priority (FIX SOON)
- Medium Priority (PLAN REMEDIATION)
- Low Priority (DOCUMENT FOR FUTURE)
- Total Effort & ROI

## Optimization Validation

1. Baseline Profile (before changes)
2. Apply Optimization
3. New Profile (after changes)
4. Compare Results
5. Validate Budgets
6. Report Impact

## Guardrails

- Fail: FPS < 60 mobile, < 30 browser
- Fail: Memory > 400MB, any leaks
- Fail: Bundle > 50MB
- Fail: Startup cold > 3s
- Warn: Startup approaching limits
- Warn: Cache approaching budgets
- Warn: API p95 > 500ms

## Triggers

Use when:
- Performance profiling complete
- Bottlenecks identified
- Optimization strategy needed
- Changes validated for performance
- Release performance validation needed

---
