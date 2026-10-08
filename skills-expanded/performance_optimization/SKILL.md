---
name: performance-optimization
description: Performance profiling, optimization, and benchmarking across the stack.
---

# Performance Optimization

Systematic performance improvement across all layers.

## Profiling
- **CPU**: perf, Instruments, py-spy, flamegraphs, Chrome DevTools
- **Memory**: heap snapshots, allocation tracking, leak detection
- **I/O**: iostat, strace/dtrace, query analysis
- **Network**: Wireshark, tcpdump, waterfall analysis

## Frontend Performance
1. **Bundle Size**: Tree shaking, code splitting, dynamic imports
2. **Rendering**: Virtual DOM reconciliation, memoization, windowing
3. **Loading**: Preconnect, preload, prefetch, lazy loading
4. **Images**: WebP/AVIF, responsive srcset, lazy loading, CDN
5. **Core Web Vitals**: LCP, FID/INP, CLS optimization

## Backend Performance
1. **Database**: Query plans, N+1 elimination, index optimization, read replicas
2. **Caching**: In-memory (Redis), application-level, HTTP caching
3. **Async**: Event loops, worker pools, backpressure handling
4. **Compression**: Gzip/Brotli, response compression, payload reduction
5. **Connection Pooling**: Database, HTTP, WebSocket connection reuse

## Algorithmic Optimization
1. Time/space complexity analysis (Big-O)
2. Data structure selection (hash map vs tree vs array)
3. Algorithmic improvements (O(n²) → O(n log n))
4. Memoization and dynamic programming
5. Parallelization and vectorization

## Benchmarking
```bash
# Before optimizing, always measure
1. Establish a baseline metric
2. Profile to find the bottleneck
3. Optimize the hottest path first
4. Re-measure to verify improvement
5. Repeat until target is met
```

## Common Bottlenecks
- Database queries (missing index, N+1, full table scan)
- Memory allocation (GC pressure, object churn)
- Network latency (chatty protocols, no batching)
- Lock contention (coarse locks, busy-wait)
- I/O blocking (synchronous file/DB/network calls)
