---
name: perf-profiling
description: Comprehensive profiling across CPU, memory, render, network, battery, and startup performance dimensions
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

# Performance Profiling Skill

Profiles and measures frontend performance across 6 key dimensions with data collection and analysis.

## 6 Performance Areas

1. **CPU**: Long tasks (>50ms), JS execution, parse/compile time
2. **Memory**: Peak/idle heap, leaks, GC pauses (Idle <200MB, Active <400MB)
3. **Render**: FPS (>=60 mobile, >=30 browser), jank, animation smoothness
4. **Network**: API p95 <500ms, data transfer, caching strategies
5. **Battery**: Background work, wakelock, CPU power draw
6. **Startup**: Cold <2s, warm <500ms, TTI <3s

## Performance Budgets & NFR Targets

- FPS >= 60 on mobile, >= 30 on browser
- Memory Idle < 200MB, Active < 400MB
- Bundle: Base <=10MB, Vendor <=20MB, Assets <=20MB, Total <=50MB
- Startup: Cold <2s, Warm <500ms
- API Response p95 < 500ms
- Cache budgets: Image 150MB, Video 150MB, Temp 50MB, Total 350MB

## Profiling Process

1. Setup Profilers
2. Run Baseline Profile (cold/warm, interaction, stress, leak check)
3. Collect Metrics (CPU, memory, render, network, battery, startup)
4. Analyze Data (identify bottlenecks, expensive ops, performance cliffs)
5. Generate Report (document findings with metrics)

## Analysis Tools

- Chrome DevTools (Lighthouse, Performance)
- Xcode Instruments (iOS)
- Android Profiler
- React Profiler
- webpack-bundle-analyzer
- WebPageTest
- Network waterfall tools

## Profiling Report Contents

- CPU Analysis: Parse time, execution, long tasks, main thread blocking
- Memory Analysis: Idle/peak heap, GC pauses, memory leaks
- Render Analysis: Average FPS, dropped frames, jank events, paint/composite time
- Network Analysis: Request count, total size, p50/p95 response time, cache hit rate
- Startup Analysis: Cold/warm startup, TTI, FCP/FP times
- Battery Impact: Idle/active power, background activity

## Measurement Techniques

### Desktop: Chrome DevTools, Lighthouse, WebPageTest
### Mobile: Android Profiler (device), Xcode Instruments (iOS)
### Synthetic vs Real: Lab (repeatable) vs RUM (realistic)

## Triggers

Use when:
- Baseline performance measurement needed
- Regression detection required
- Optimization validation after changes
- Performance benchmarking before release
- Comparative analysis between versions

---
