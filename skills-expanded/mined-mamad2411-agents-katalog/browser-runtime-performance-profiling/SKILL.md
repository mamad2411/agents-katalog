---
name: browser-runtime-performance-profiling
version: "1.0"
description: >
  Browser runtime profiling with Chrome DevTools and Core Web Vitals optimization.
  PROACTIVELY activate for: (1) Using Chrome Performance panel, (2) Analyzing flame charts,
  (3) Diagnosing long tasks, (4) Core Web Vitals optimization, (5) Memory profiling.
  Triggers: "devtools", "performance panel", "lighthouse", "flame graph", "jank", "long task", "fps", "layout thrashing", "core web vitals"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Browser Runtime Performance Profiling

This skill provides mastery of Chrome DevTools Performance panel to diagnose and resolve runtime performance issues, including rendering bottlenecks, long tasks that block the main thread, and memory leaks.

## Recording a Performance Profile

Proper setup ensures useful, actionable profiling data.

### Setup Steps

1. **Use Incognito Mode**: Extensions can skew results
2. **Open DevTools**: F12 or Cmd+Option+I (Mac)
3. **Navigate to Performance Panel**: Top navigation bar
4. **Configure Settings** (gear icon):
   - Enable "Screenshots": Visual timeline of page changes
   - Set "Network": "Slow 3G" to simulate slow connections
   - Set "CPU": "4x slowdown" to amplify bottlenecks
5. **Click Record** (circle icon)
6. **Perform Actions**: Interact with the page
7. **Stop Recording**: Click stop or press Cmd/Ctrl+E

### Best Practices

- **Profile production builds**: Development builds have extra overhead
- **Record 5-10 seconds**: Enough data without overwhelming detail
- **Focus on user interactions**: Scrolling, clicking, typing
- **Use throttling**: CPU and network throttling reveals issues on slower devices

### Quick Keyboard Shortcuts

- **Cmd/Ctrl+E**: Start/stop recording
- **Cmd/Ctrl+Shift+E**: Reload and record
- **WASD**: Navigate timeline (W/S = zoom, A/D = pan)

## Analyzing the Flame Chart

The flame chart is the primary tool for diagnosing runtime issues. It shows main thread activity over time.

### Reading the Flame Chart

**Vertical axis**: Call stack depth (top = innermost function)
**Horizontal axis**: Time
**Colors**:
- **Yellow**: JavaScript execution
- **Purple**: Rendering and layout
- **Green**: Painting
- **Gray**: Other (idle, system)

### Identifying Long Tasks

**Long Task**: Any task that blocks the main thread for > 50ms

**Visual indicator**: Yellow blocks with a **red triangle** in the upper right corner

```
Example:
┌────────────────────────────────┐
│ ▲ (Long Task)                  │ ← Red triangle
│ evaluateScript     248ms       │ ← Problem!
│  └─ processData                │
│      └─ heavyCalculation       │
└────────────────────────────────┘
```

**Impact**: Blocks user interactions (scrolling, clicking). Aim for tasks < 50ms.

**Solution**: Break up work with:
- `setTimeout` for splitting tasks
- `requestIdleCallback` for low-priority work
- Web Workers for heavy computation
- React `useTransition` for large UI updates

### Identifying Layout Thrashing

**Layout Thrashing**: Reading layout properties immediately after changing them, forcing synchronous layout recalculation.

**Visual indicator**: Multiple purple "Layout" blocks in rapid succession

```
Example flame chart:
JavaScript
  └─ updateElements
      ├─ element.style.height = '100px'   (Write)
      ├─ Layout (Forced)                   ← Purple block
      ├─ element.offsetHeight              (Read)
      ├─ element.style.width = '200px'     (Write)
      └─ Layout (Forced)                   ← Purple block
```

**Solution**: Batch reads and writes

```js
// BAD: Layout thrashing
elements.forEach(el => {
  el.style.height = el.offsetWidth + 'px' // Read, then write
})

// GOOD: Batch reads, then writes
const widths = elements.map(el => el.offsetWidth) // All reads
elements.forEach((el, i) => {
  el.style.height = widths[i] + 'px' // All writes
})
```

### Identifying Expensive Scripts

**Visual indicator**: Wide yellow blocks labeled "Evaluate Script" or "Function Call"

**Impact**: Delays page interactivity (FID/INP)

**Solution**:
- Code splitting (load less JavaScript upfront)
- Lazy load non-critical features
- Optimize algorithms (reduce time complexity)
- Offload to Web Workers

### Identifying Excessive Rendering

**Visual indicator**: Many purple "Recalculate Style" or "Layout" blocks

**Causes**:
- Large DOM trees
- Complex CSS selectors
- Unnecessary re-renders in React
- CSS animations triggering layout

**Solution**:
- Simplify CSS selectors
- Use `transform` and `opacity` for animations (these don't trigger layout)
- Minimize DOM depth
- Memoize React components

## Interpreting Core Web Vitals

Core Web Vitals are user-centric performance metrics.

### Largest Contentful Paint (LCP)

**Definition**: Time until the largest content element is rendered

**Target**: < 2.5 seconds

**Where to Find**: "Timings" section, blue "LCP" marker

**Common Causes**:
- Slow server response (TTFB)
- Large, unoptimized images
- Render-blocking CSS/JS
- Client-side rendering

**Solutions**:
- Optimize server response time
- Use next/image with priority attribute
- Inline critical CSS
- Server-side rendering (Next.js RSC)
- Preload LCP resource: `<link rel="preload" as="image" href="/hero.jpg">`

### Interaction to Next Paint (INP)

**Definition**: Time from user interaction to visual response

**Target**: < 200ms (good), < 500ms (acceptable)

**Where to Find**: "Experience" section when interacting

**Common Causes**:
- Long JavaScript tasks
- Excessive event handlers
- Slow React re-renders
- Main thread blocked

**Solutions**:
- Break up long tasks
- Debounce/throttle event handlers
- Use React `useTransition` for non-urgent updates
- Code splitting
- Web Workers for heavy computation

### Cumulative Layout Shift (CLS)

**Definition**: Sum of all unexpected layout shifts

**Target**: < 0.1

**Where to Find**: "Experience" section, red "Layout Shift" markers

**Common Causes**:
- Images without dimensions
- Ads/embeds without reserved space
- Web fonts causing FOIT/FOUT
- Dynamic content injection

**Solutions**:
- Always specify image width/height
- Reserve space for ads/embeds with CSS
- Use `font-display: optional` or preload fonts
- Avoid inserting content above existing content

## Using the Performance Monitor

Real-time graph of key metrics during interaction.

### Enable Performance Monitor

1. Open DevTools
2. Cmd/Ctrl+Shift+P (Command Palette)
3. Type "Show Performance Monitor"
4. Select from dropdown

### Key Metrics

- **CPU usage**: Spikes indicate heavy computation
- **JS heap size**: Increasing = potential memory leak
- **DOM Nodes**: High count = slow rendering
- **JS event listeners**: Too many = overhead
- **Layouts/sec**: High = layout thrashing
- **Style recalcs/sec**: High = CSS performance issues

### Using the Data

- **CPU consistently high**: Profile to find bottleneck
- **Heap size growing**: Take heap snapshot, find leaks
- **DOM nodes growing**: Check for detached nodes
- **High layouts/repaints**: Look for layout thrashing

## Memory Profiling

Identify memory leaks and excessive memory usage.

### Taking a Heap Snapshot

1. **Open DevTools** → **Memory** panel
2. Select **Heap snapshot**
3. Click **Take snapshot**
4. Interact with the page
5. Take another snapshot
6. Compare snapshots

### Finding Memory Leaks

**Detached DOM Nodes**: Nodes removed from DOM but still in memory

**How to Find**:
1. Take heap snapshot
2. Search for "Detached"
3. Expand "Detached HTMLDivElement" (or other elements)
4. Check "Retainers" to see what's holding the reference

**Common Causes**:
- Event listeners not removed
- Closures capturing DOM nodes
- Global variables referencing DOM
- Third-party libraries not cleaning up

**Solution**:
```js
// BAD: Event listener not removed
useEffect(() => {
  window.addEventListener('resize', handleResize)
  // Missing cleanup!
}, [])

// GOOD: Cleanup function
useEffect(() => {
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
}, [])
```

### Allocation Timeline

Shows memory allocations over time.

1. **Memory** panel → **Allocation timeline**
2. Click **Record**
3. Interact with the page
4. Stop recording
5. Blue bars show allocations

**Look for**: Steadily increasing allocations (potential leak)

## Lighthouse Integration

Automated performance audits providing actionable recommendations.

### Running Lighthouse

1. Open DevTools → **Lighthouse** panel
2. Select **Performance** category
3. Click **Analyze page load**

### Key Sections

**Metrics**: LCP, FID, CLS, TTFB, Speed Index
**Opportunities**: Specific optimizations with estimated savings
**Diagnostics**: Issues to investigate
**Passed Audits**: What's working well

### Common Recommendations

- **Reduce unused JavaScript**: Code splitting needed
- **Properly size images**: Use next/image with proper dimensions
- **Eliminate render-blocking resources**: Defer non-critical CSS/JS
- **Avoid enormous network payloads**: Reduce total page weight
- **Serve static assets with efficient cache policy**: Set cache headers

## Anti-Patterns

### Profiling Development Builds

Development builds have extra debugging code and are not representative of production performance.

**Always profile production builds**: `npm run build && npm start`

### Profiling with Extensions Enabled

Extensions add overhead and can skew results.

**Always use incognito mode** for profiling.

### Not Using Throttling

Your development machine is faster than most user devices.

**Always enable CPU and network throttling** to simulate real-world conditions.

### Ignoring the Cause of Long Tasks

Seeing a long task isn't enough—you must drill down into the flame chart to find the specific function causing the issue.

### Premature Optimization

Profile first, then optimize. Don't guess at what's slow.

## Performance Profiling Checklist

- [ ] Profile production builds, not development
- [ ] Use incognito mode (no extensions)
- [ ] Enable CPU and network throttling
- [ ] Record realistic user interactions
- [ ] Check for long tasks (> 50ms)
- [ ] Look for layout thrashing (forced layouts)
- [ ] Verify Core Web Vitals meet targets
- [ ] Use Performance Monitor for real-time metrics
- [ ] Take heap snapshots to find memory leaks
- [ ] Run Lighthouse for automated recommendations
- [ ] Fix issues in priority order (based on user impact)

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| INP | ≤ 200ms | 200ms - 500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

## Quick Reference: Performance Issues

| Symptom | Likely Cause | Where to Look |
|---------|--------------|---------------|
| Slow page load | Large bundles, slow server | Network tab, Lighthouse |
| Jank during scroll | Layout thrashing, expensive paints | Flame chart (purple blocks) |
| Slow click response | Long tasks blocking main thread | Flame chart (yellow blocks) |
| Content shifting | Missing image dimensions | Experience section (CLS) |
| Memory increasing | Leaking DOM nodes/listeners | Memory panel (heap snapshots) |
| Slow initial render | Large LCP element, render-blocking | Timings section (LCP) |
