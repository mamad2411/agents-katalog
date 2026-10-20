---
name: jquery-performance
description: Use when diagnosing or improving jQuery performance covering selector efficiency, DOM operation batching, event delegation, memory management, and render-blocking reduction.
---

# jQuery Performance

## Specialization

Diagnose and improve jQuery performance with evidence-first analysis covering selector caching, DOM batching, event delegation efficiency, loop optimization, effects throttling, and memory-leak prevention — grounded in official jQuery performance guidance and browser rendering models.

## Trigger Conditions

- Identifying slow jQuery selectors or excessive DOM re-queries.
- Diagnosing sluggish page interactions caused by unoptimized event handlers.
- Reducing layout thrash from interleaved reads and writes in jQuery manipulation chains.
- Detecting memory leaks from unbound handlers or uncleaned `.data()` caches.
- Profiling jQuery effects and animations that cause frame drops.
- Reviewing jQuery-heavy code before production release.
- Establishing performance baseline for a project transitioning from jQuery to native APIs.

## Scope Boundaries

In scope:

- Selector efficiency and caching strategy.
- DOM read/write batching and layout thrash avoidance.
- Event delegation topology and handler accumulation prevention.
- Loop optimization: `.each()` vs. native loops, minimizing jQuery wrapping overhead.
- Effects and animation: `requestAnimationFrame`-aware patterns, `jQuery.fx.off` for test environments.
- Memory management: handler unbinding, `.data()` cleanup, detach patterns.
- Deferred and AJAX performance: request coalescing, debouncing, throttling.

Out of scope:

- Server-side rendering or SSR performance.
- Network-layer optimization beyond request coalescing.
- Framework migration decisions (documented as outcomes but not implemented here — see `jquery-migration`).

## Inputs

- Performance symptoms: slow interaction, layout jank, high memory, excessive DOM queries.
- jQuery version and browser target.
- Profiler data if available (Chrome DevTools Performance or Memory tabs).
- Code section under review.

## Required Outputs

- Selector audit with cached-vs-uncached recommendation per query.
- DOM batch plan: reads grouped before writes, detach-mutate-reattach applied where applicable.
- Event delegation topology review: delegation roots, handler count estimate.
- Memory audit: unbound handler candidates, `.data()` cleanup gaps.
- Effects audit: animation queue depth, `fx.interval` settings, `stop()` usage.
- Prioritized remediation list with estimated impact (High / Medium / Low).

## Core Performance Patterns

### Selector Caching

```javascript
// Bad: re-queries DOM on every loop iteration
$('.items').each(function() {
  $(this).addClass('active'); // wraps 'this' each iteration
});

// Good: cache wrapper, use native 'this' where possible
const $items = $('.items');
$items.addClass('active'); // operates on collection — one traversal
```

- Cache every jQuery object used more than once: `const $el = $('#target');`
- In loops, avoid `$(this)` overhead for operations where the native element suffices (`this.className`, `this.value`).
- Prefer `.find()` on a cached context over a new top-level query.

### DOM Read/Write Batching

- Never interleave DOM reads and writes — each interleave forces a synchronous layout (layout thrash).
- Batch all reads first, then apply all writes:
  ```javascript
  // Read phase
  const heights = $items.map(function() { return $(this).height(); }).get();
  // Write phase
  $items.each(function(i) { $(this).css('top', heights[i] + 'px'); });
  ```
- Use `detach()` before performing multiple structural mutations on a subtree; reattach once.
- Build HTML strings or document fragments off-DOM; insert in a single `.append()` call.

### Event Handler Efficiency

- Delegate to the closest stable ancestor — not `document` — to minimize bubbling cost.
- One delegated handler per event type per container outperforms N direct handlers on N children.
- Audit handler count: an element accumulating handlers across renders indicates missing `.off()` in teardown.
- Use `.one()` instead of `.on()` + manual `.off()` for fire-once patterns.

### Loop Optimization

- Prefer native `for` or `Array.prototype.forEach` over `.each()` for pure computation loops (no jQuery API needed).
- When `.each()` is needed, use the callback's `index` and `element` (native) parameters; wrap in `$()` only when a jQuery method is called.
- Avoid calling jQuery methods inside tight loops; extract invariant operations outside.

### Effects and Animation

- Use `$(el).stop(true, true)` before starting a new animation on the same element to clear the queue and avoid animation queue buildup.
- Set `jQuery.fx.off = true` in test environments to eliminate animation delays.
- Prefer CSS transitions over jQuery `.animate()` for performant GPU-composited animations.
- Use `requestAnimationFrame`-based scheduling (e.g., via plugin or native) for high-frequency visual updates instead of `$.animate()`.

### Memory Management

- Call `.off('.namespace')` before `.remove()` or DOM replacement to prevent closure-captured scope leaks.
- Call `.removeData()` when associated state is no longer needed.
- Use `.detach()` instead of `.remove()` for temporarily displaced elements to preserve handler and data cache.
- In SPAs: always tear down handlers and data in component unmount/destroy lifecycle.

### Debounce and Throttle

- Wrap scroll, resize, and input handlers in a debounce/throttle function — never bind expensive logic directly.
- Use a 150–250 ms debounce for search-on-type; use 100 ms throttle for scroll-driven layout.
- Cancel pending debounced calls on component teardown.

### Request Coalescing

- Batch multiple data requests in `$.when()` rather than issuing them sequentially.
- Debounce AJAX calls triggered by rapid user input (e.g., live search).

## Workflow

1. Identify performance symptom and measurement target.
2. Audit selectors: find uncached queries and repeated `$(this)` inside loops.
3. Audit DOM operations: locate interleaved reads/writes and unbatched structural mutations.
4. Audit event topology: count handlers, identify non-delegated listeners on dynamic elements.
5. Audit memory: verify handler unbinding and `.data()` cleanup on element removal.
6. Audit effects: check for animation queue buildup and non-stopped transitions.
7. Prioritize remediations by impact; emit a ranked remediation list.

## Done Criteria

- All repeated selectors are cached.
- DOM reads precede writes — no interleaved layout thrash.
- Structural mutations use detach-mutate-reattach.
- Event handlers are delegated from the closest stable ancestor.
- All handlers have paired `.off()` calls in teardown paths.
- Scroll/resize/input handlers are debounced or throttled.
- Animation queue buildup is prevented with `.stop()`.

## References

- [jQuery Learn: Performance](https://learn.jquery.com/performance/)
- [jQuery Learn: Avoid Unnecessary DOM Queries](https://learn.jquery.com/performance/avoid-unnecessary-dom-queries/)
- [jQuery Learn: Cache Your jQuery Objects](https://learn.jquery.com/performance/cache-your-jquery-objects/)
- [jQuery Learn: Detach Elements to Work with Them](https://learn.jquery.com/performance/detach-elements-before-work-with-them/)
- [jQuery API: .stop()](https://api.jquery.com/stop/)
- [MDN: Avoid Forced Layout/Reflows](https://developer.mozilla.org/en-US/docs/Tools/Performance/Scenarios/Unnecessary_layout)
