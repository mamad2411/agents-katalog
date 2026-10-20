---
name: performance-patterns
description: "When to activate: Core Web Vitals, LCP, INP, CLS, performance optimization, lazy loading, code splitting, resource hints"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: frontend
  language: web
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Web Performance Patterns

## Core Web Vitals Targets
- **LCP** (Largest Contentful Paint): < 2.5s
- **INP** (Interaction to Next Paint): < 200ms
- **CLS** (Cumulative Layout Shift): < 0.1

## LCP Optimization

```html
<!-- Preload hero image -->
<link rel="preload" as="image" href="/hero.avif" fetchpriority="high">

<!-- Hero img: eager + high priority -->
<img src="/hero.avif" alt="Hero" width="1200" height="600"
     loading="eager" fetchpriority="high" decoding="sync">

<!-- Below-fold images: lazy -->
<img src="/card.avif" alt="Card" width="400" height="300"
     loading="lazy" decoding="async">
```

```js
// Measure LCP in JS
new PerformanceObserver(list => {
  const entries = list.getEntries();
  const last = entries[entries.length - 1];
  console.log('LCP:', last.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

## CLS Prevention

```css
/* Always set explicit dimensions on images/video */
img, video { width: 100%; height: auto; aspect-ratio: 16 / 9; }

/* Reserve space for dynamic content */
.ad-slot { min-height: 250px; }

/* Font loading — prevent FOUT/FOIT layout shift */
@font-face {
  font-family: 'Inter';
  src: url('/inter.woff2') format('woff2');
  font-display: optional; /* no fallback flash */
  size-adjust: 100%;
}
```

## INP / Interaction Optimization

```js
// Defer non-critical work with scheduler.postTask
async function handleClick() {
  // Critical: update UI immediately
  button.textContent = 'Processing...';

  // Non-critical: background work
  await scheduler.postTask(() => heavyComputation(), { priority: 'background' });
}

// Break up long tasks with yield
async function processItems(items) {
  for (let i = 0; i < items.length; i++) {
    process(items[i]);
    if (i % 50 === 0) await new Promise(r => setTimeout(r, 0)); // yield
  }
}

// Debounce input handlers
function debounce(fn, ms) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}
const onSearch = debounce(search, 300);
```

## Code Splitting

```js
// Route-level splitting (React)
const Dashboard = lazy(() => import('./Dashboard'));
const Settings  = lazy(() => import('./Settings'));

// Prefetch on hover
function NavLink({ to, children }) {
  return (
    <Link to={to}
      onMouseEnter={() => import(`./pages/${to}`)}
      onFocus={() => import(`./pages/${to}`)}>
      {children}
    </Link>
  );
}

// Vite dynamic import with chunk name
const { Chart } = await import(/* @vite-chunk-name: "charts" */ './Chart');
```

## Resource Hints

```html
<!-- Preconnect to critical third parties -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- DNS prefetch for non-critical origins -->
<link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Prefetch likely next page -->
<link rel="prefetch" href="/dashboard" as="document">

<!-- Modulepreload for ES modules -->
<link rel="modulepreload" href="/src/main.js">
```

## Image Optimization

```html
<!-- Modern format with fallback -->
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img src="/hero.jpg" alt="Hero" width="1200" height="600" loading="eager">
</picture>

<!-- Responsive images -->
<img
  srcset="/img-400.webp 400w, /img-800.webp 800w, /img-1200.webp 1200w"
  sizes="(max-width: 600px) 100vw, (max-width: 1000px) 50vw, 400px"
  src="/img-800.webp" alt="Product" width="800" height="600" loading="lazy">
```

## Bundle Analysis (Vite)

```js
// vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';

export default {
  plugins: [visualizer({ open: true, gzipSize: true })],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['recharts'],
        }
      }
    }
  }
};
```
