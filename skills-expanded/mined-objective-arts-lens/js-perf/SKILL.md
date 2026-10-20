---
name: js-perf
description: "JS performance patterns"
---
# Addy Osmani JavaScript Philosophy

Applying Addy Osmani's JavaScript performance optimization philosophy, design patterns, and web vitals expertise to frontend development. Use when optimizing page load times, implementing lazy loading, improving Core Web Vitals scores, applying JavaScript design patterns, optimizing images, implementing code splitting, or when performance budgets are discussed. Not for backend optimization, database queries, or non-JavaScript performance work.

---

## Core Philosophy

**Performance is User Experience**: Every millisecond of delay costs engagement. Measure real user metrics, not synthetic benchmarks.

**Progressive Enhancement**: Start with the minimal viable experience, enhance with JavaScript. Never require JS for core content.

**Ship Less JavaScript**: The fastest code is the code you don't ship. Question every dependency, every abstraction, every byte.

---

## Performance Optimization Hierarchy

### 1. Loading Strategy (Critical Path)

**Prioritize Above-the-Fold Content**
```html
<!-- Critical CSS inline -->
<style>/* Above-fold styles only */</style>

<!-- Preload critical resources -->
<link rel="preload" href="critical.js" as="script">
<link rel="preload" href="hero.webp" as="image">

<!-- Defer non-critical -->
<script defer src="analytics.js"></script>
```

**Resource Hints**
```html
<!-- DNS prefetch for third-party domains -->
<link rel="dns-prefetch" href="//cdn.example.com">

<!-- Preconnect for critical third-parties -->
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>

<!-- Prefetch for likely next navigation -->
<link rel="prefetch" href="/likely-next-page.html">

<!-- Modulepreload for ES modules -->
<link rel="modulepreload" href="/critical-module.js">
```

### 2. Code Splitting Patterns

**Route-Based Splitting (React)**
```javascript
// Lazy load routes
const Dashboard = React.lazy(() => import('./Dashboard'));
const Settings = React.lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Skeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

**Magic Comments for Webpack**
```javascript
// Named chunks for debugging
import(/* webpackChunkName: "lodash" */ 'lodash');

// Prefetch - load during idle time
import(/* webpackPrefetch: true */ './HeavyComponent');

// Preload - load in parallel with parent
import(/* webpackPreload: true */ './CriticalComponent');
```

### 3. Image Optimization

**Modern Formats with Fallbacks**
```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero" loading="lazy" decoding="async">
</picture>
```

**Responsive Images**
```html
<img
  srcset="small.jpg 400w, medium.jpg 800w, large.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  src="medium.jpg"
  alt="Responsive image"
  loading="lazy"
  decoding="async"
>
```

**Native Lazy Loading**
```html
<!-- Lazy load below-fold images -->
<img src="photo.jpg" loading="lazy" alt="...">

<!-- Eager load above-fold (LCP candidates) -->
<img src="hero.jpg" loading="eager" fetchpriority="high" alt="...">
```

### 4. Core Web Vitals Optimization

**Largest Contentful Paint (LCP) < 2.5s**
- Preload LCP image
- Inline critical CSS
- Remove render-blocking resources
- Use CDN for static assets

**First Input Delay (FID) < 100ms / Interaction to Next Paint (INP) < 200ms**
```javascript
// Break up long tasks
function processLargeArray(items) {
  const CHUNK_SIZE = 100;
  let index = 0;

  function processChunk() {
    const chunk = items.slice(index, index + CHUNK_SIZE);
    chunk.forEach(processItem);
    index += CHUNK_SIZE;

    if (index < items.length) {
      requestIdleCallback(processChunk);
    }
  }

  processChunk();
}
```

**Cumulative Layout Shift (CLS) < 0.1**
```css
/* Reserve space for dynamic content */
.image-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* Avoid inserting content above existing */
.ad-slot {
  min-height: 250px;
}
```

### 5. JavaScript Design Patterns

**Module Pattern (Encapsulation)**
```javascript
const ShoppingCart = (() => {
  let items = [];
  const calculateTotal = () => items.reduce((sum, item) => sum + item.price, 0);

  return {
    add(item) { items.push(item); },
    remove(id) { items = items.filter(i => i.id !== id); },
    getTotal() { return calculateTotal(); },
    getItems() { return [...items]; }
  };
})();
```

**Observer Pattern (Pub/Sub)**
```javascript
class EventBus {
  #subscribers = new Map();

  subscribe(event, callback) {
    if (!this.#subscribers.has(event)) {
      this.#subscribers.set(event, new Set());
    }
    this.#subscribers.get(event).add(callback);
    return () => this.#subscribers.get(event).delete(callback);
  }

  publish(event, data) {
    this.#subscribers.get(event)?.forEach(cb => cb(data));
  }
}
```

### 6. Runtime Performance

**Debounce & Throttle**
```javascript
const debounce = (fn, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

const throttle = (fn, limit) => {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};
```

**Memoization**
```javascript
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}
```

### 7. Bundle Optimization

**Tree Shaking Best Practices**
```javascript
// BAD - imports entire library
import _ from 'lodash';
_.debounce(fn, 100);

// GOOD - imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 100);

// BEST - use native or minimal alternatives
function debounce(fn, delay) { /* ... */ }
```

**Performance Budgets**
```javascript
// webpack.config.js
module.exports = {
  performance: {
    maxAssetSize: 250000, // 250 KB
    maxEntrypointSize: 250000,
    hints: 'error' // Fail build if exceeded
  }
};
```

---

## Measurement & Monitoring

**Real User Monitoring**
```javascript
import { onCLS, onFID, onLCP, onINP, onTTFB } from 'web-vitals';

function sendToAnalytics({ name, value, id }) {
  navigator.sendBeacon('/analytics', JSON.stringify({ name, value, id }));
}

onCLS(sendToAnalytics);
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
```

---

## Anti-Patterns to Avoid

1. **Layout Thrashing**: Batch DOM reads before writes
2. **Forced Synchronous Layouts**: Avoid reading layout props after writes
3. **Memory Leaks**: Clean up event listeners, timers, subscriptions
4. **Blocking the Main Thread**: Use Web Workers for heavy computation
5. **Render Blocking Resources**: Defer non-critical JS/CSS
6. **Over-Engineering**: Simple solutions before patterns
7. **Premature Optimization**: Measure first, optimize second

---

## Performance Checklist

- [ ] LCP under 2.5s
- [ ] FID under 100ms / INP under 200ms
- [ ] CLS under 0.1
- [ ] JavaScript bundle under 200KB (gzipped)
- [ ] Critical CSS inlined
- [ ] Images in modern formats (WebP/AVIF)
- [ ] Lazy loading for below-fold content
- [ ] Code splitting by route
- [ ] Third-party scripts async/defer
- [ ] Performance budgets enforced in CI
