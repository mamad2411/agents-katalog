---
name: tpl-situacao-debug-performance
description: Template do pack (situacao/03-debug-performance.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/03-debug-performance.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Performance Debugging & Optimization

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/03-debug-performance.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when investigating slow application performance, high memory usage, CPU spikes, slow database queries, long page load times, or high server costs. This is NOT premature optimization — you have a measured problem and must find its cause. The rule is: measure first, optimize second, measure again.

## OBJECTIVES
- Identify the actual bottleneck with data (not guesses)
- Establish a measurable baseline before any changes
- Optimize the highest-impact area first (Pareto principle)
- Verify improvement with the same measurement tools used for baseline
- Avoid introducing regressions elsewhere while optimizing

## APPROACH RULES

1. **Never optimize without measuring first.** State the current metric (latency, query time, memory MB, bundle size KB) before writing any code. Optimization without a baseline is guessing.

2. **One change at a time.** Change one thing, measure, record result. Multiple simultaneous optimizations make it impossible to know what helped.

3. **Profile, don't eyeball.** Use proper profiling tools. Your intuition about where the bottleneck is will be wrong 70% of the time.

4. **Fix the algorithm before fixing the implementation.** An O(n²) algorithm with micro-optimizations will always lose to an O(n log n) algorithm written simply.

5. **Database queries are almost always the bottleneck.** Check queries before optimizing application code.

6. **Pareto principle.** Fix the top 20% of problems causing 80% of slowness. Don't optimize uniform slowness — find the spike.

7. **Record every experiment.** Keep a performance log: what you tried, what the result was. This prevents repeating failed experiments.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Slow API endpoint | Check: DB query count (N+1?), query execution time, external HTTP calls, missing indexes. Use `EXPLAIN ANALYZE` on all queries |
| N+1 query problem | Use eager loading (`include`/`joins`), DataLoader pattern, or batch queries. Never fix N+1 with caching — fix the query |
| Memory leak (Node.js) | Use `--inspect` flag + Chrome DevTools heap snapshot. Look for: event listener accumulation, closures retaining references, circular references |
| High CPU usage | Profile with `clinic.js` (Node) / `py-spy` (Python) / `async-profiler` (Java). Find hot functions. |
| Slow frontend page load | Run Lighthouse. Check: LCP, FID, CLS, bundle size, render-blocking resources, unused JavaScript |
| Large JS bundle | Run `webpack-bundle-analyzer` or `vite-bundle-visualizer`. Look for: duplicate packages, unused imports, missing code splitting |
| Slow database queries | Run `EXPLAIN ANALYZE`. Look for: Sequential Scans on large tables, missing indexes, sort operations without indexes, high actual vs estimated rows |
| Too many HTTP requests | Implement HTTP/2 multiplexing, batch API calls, or GraphQL. Check for unnecessary polling. |
| Slow image loading | Check: format (WebP > JPEG > PNG), compression, serving from CDN, proper dimensions (not oversized) |
| Memory growing indefinitely | It's a leak. Take heap snapshots at T0, T+5min, T+10min. Compare retained objects. |

## DO NOT

- **DO NOT** add caching as the first solution — it hides the problem and adds complexity
- **DO NOT** optimize code paths that are not in the hot path — use profiler data to confirm
- **DO NOT** mix optimization commits with feature commits — impossible to bisect regressions
- **DO NOT** use `SELECT *` — always select only needed columns
- **DO NOT** add indexes blindly — each index slows down writes. Measure read gain vs write cost
- **DO NOT** prematurely optimize O(n) operations that run once — focus on hot loops
- **DO NOT** claim an optimization is complete without a before/after benchmark comparison
- **DO NOT** use synchronous operations in async code paths (Node.js fs.readFileSync, etc.)

## OUTPUT FORMAT

For each performance investigation, produce a **Performance Report**:

```
## Performance Investigation Report

### Problem Statement
[What is slow, by how much, measured how]

### Baseline Metrics
- Endpoint: GET /api/products
- P50 latency: 1,240ms
- P95 latency: 3,800ms
- DB queries per request: 47
- Memory: 512MB steady state

### Root Cause Analysis
1. N+1 query on Product.findWithRelations() — 45 of 47 queries
2. Missing index on products.category_id

### Changes Made
1. Added eager loading for categories and tags
2. Added index: CREATE INDEX idx_products_category_id ON products(category_id)

### Post-Optimization Metrics
- P50 latency: 180ms (85% improvement)
- P95 latency: 420ms (89% improvement)
- DB queries per request: 2

### Remaining Opportunities
- Bundle size still large — investigate lodash import
```

## QUALITY GATES

- [ ] Baseline metrics documented before any change
- [ ] Profiler output attached (screenshot or exported data)
- [ ] `EXPLAIN ANALYZE` output included for any changed queries
- [ ] Before/after metrics comparison present for every optimization
- [ ] No regressions in other endpoints/routes (run full suite)
- [ ] Memory baseline stable over 30-minute load test (no creeping growth)
- [ ] Optimization verified in staging with production-like data volume
- [ ] P95 (not just average) latency measured — averages hide tail latency problems
- [ ] No new `SELECT *` queries introduced
- [ ] Caching, if added, has an explicit invalidation strategy documented
