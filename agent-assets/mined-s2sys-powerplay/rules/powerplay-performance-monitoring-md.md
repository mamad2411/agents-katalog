---
name: performance-monitoring
description: Web performance monitoring — Core Web Vitals, performance budgets, RUM, APM setup and standards
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js", "**/*.json"]
alwaysApply: false
---

# Performance Monitoring Standards

Web performance is a feature. Monitor Core Web Vitals, track real user metrics, and maintain performance budgets.

---

## Core Web Vitals

**ALWAYS**:
- Track LCP (Largest Contentful Paint) — target < 2.5s
- Track FID (First Input Delay) — target < 100ms (INP in 2024+)
- Track CLS (Cumulative Layout Shift) — target < 0.1
- Monitor in real user monitoring (RUM)
- Set up alerts for metric regressions
- Test on low-end devices (slow 4G, mid-range phone)

**NEVER**:
- Ignore performance metrics
- Only test on fast desktop
- Miss LCP opportunities (images, fonts, critical JS)

### ✅ GOOD Core Web Vitals Monitoring

```typescript
// lib/vitals.ts — Web Vitals tracking
import {
  getCLS,
  getFID,
  getFCP,
  getLCP,
  getTTFB,
  getINP,
} from 'web-vitals/attribution';

interface VitalMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
}

export function reportWebVitals() {
  // LCP — Largest Contentful Paint
  getLCP((metric) => {
    const vital: VitalMetric = {
      name: 'LCP',
      value: metric.value,
      rating: metric.rating || 'needs-improvement',
    };
    
    // Send to analytics
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'page_view', {
        lcp: metric.value,
        lcp_rating: metric.rating,
      });
    }

    // Log for debugging
    console.log(`[${vital.rating.toUpperCase()}] LCP: ${vital.value.toFixed(2)}ms`);
  });

  // FID → INP (Interaction to Next Paint)
  getINP((metric) => {
    const vital: VitalMetric = {
      name: 'INP',
      value: metric.value,
      rating: metric.rating || 'needs-improvement',
    };
    
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'page_view', {
        inp: metric.value,
        inp_rating: metric.rating,
      });
    }

    console.log(`[${vital.rating.toUpperCase()}] INP: ${vital.value.toFixed(2)}ms`);
  });

  // CLS — Cumulative Layout Shift
  getCLS((metric) => {
    const vital: VitalMetric = {
      name: 'CLS',
      value: metric.value,
      rating: metric.rating || 'needs-improvement',
    };
    
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'page_view', {
        cls: metric.value,
        cls_rating: metric.rating,
      });
    }

    console.log(`[${vital.rating.toUpperCase()}] CLS: ${vital.value.toFixed(3)}`);
  });

  // TTFB — Time to First Byte
  getTTFB((metric) => {
    console.log(`TTFB: ${metric.value.toFixed(2)}ms`);
  });

  // FCP — First Contentful Paint
  getFCP((metric) => {
    console.log(`FCP: ${metric.value.toFixed(2)}ms`);
  });
}

// pages/_app.tsx or App.tsx
if (typeof window !== 'undefined') {
  reportWebVitals();
}
```

### ❌ BAD Performance Monitoring

```typescript
// ❌ No metrics tracking
export function App() {
  return <Main />;
}

// ❌ Only tracking in development
if (process.env.NODE_ENV === 'development') {
  reportWebVitals(); // Missing production data!
}

// ❌ No goals or baselines
// Just collecting metrics without targets
```

---

## Performance Budgets

**ALWAYS**:
- Set bundle size budget: < 250KB (gzip)
- Set FCP budget: < 1.5s
- Set LCP budget: < 2.5s
- Set INP budget: < 200ms
- Set CLS budget: < 0.1
- Enforce in CI (fail build if exceeded)
- Monitor per-page bundles

**NEVER**:
- Ship without performance budgets
- Ignore budget alerts
- Set unrealistic targets

### ✅ GOOD Performance Budget Setup

```typescript
// performance-budget.json
{
  "bundles": [
    {
      "name": "main",
      "maxSize": "250kb"
    },
    {
      "name": "vendor",
      "maxSize": "150kb"
    },
    {
      "name": "polyfills",
      "maxSize": "20kb"
    }
  ],
  "metrics": [
    {
      "name": "LCP",
      "target": 2500,
      "description": "Largest Contentful Paint target"
    },
    {
      "name": "FID",
      "target": 100,
      "description": "First Input Delay target"
    },
    {
      "name": "CLS",
      "target": 0.1,
      "description": "Cumulative Layout Shift target"
    }
  ]
}

// package.json scripts
{
  "scripts": {
    "build": "next build",
    "analyze": "ANALYZE=true npm run build",
    "bundle-budget": "bundle-budget-cli check --config performance-budget.json",
    "lighthouse": "lighthouse https://example.com --view"
  }
}

// .github/workflows/performance.yml
name: Performance Budget Check

on: [pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Check bundle size
        run: npm run bundle-budget
      
      - name: Run Lighthouse
        run: |
          npm install -g @lhci/cli@latest
          lhci autorun
```

---

## Lighthouse & Monitoring Tools

**ALWAYS**:
- Run Lighthouse in CI on every PR
- Monitor with Lighthouse CI
- Set up Google Analytics Real User Monitoring (RUM)
- Use Sentry for error tracking + performance
- Monitor with New Relic or Datadog for backend

**NEVER**:
- Only test locally (CI provides consistent data)
- Forget to monitor after deploy
- Ignore performance regressions

### ✅ GOOD Monitoring Setup

```typescript
// lighthouserc.json
{
  "ci": {
    "collect": {
      "url": [
        "http://localhost:3000/",
        "http://localhost:3000/about",
        "http://localhost:3000/blog"
      ],
      "numberOfRuns": 3,
      "settings": {
        "configPath": "./lighthouse-config.js"
      }
    },
    "upload": {
      "target": "lhci",
      "serverBaseUrl": "https://lhci.example.com"
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.9 }],
        "categories:seo": ["error", { "minScore": 0.9 }]
      }
    }
  }
}

// sentry.client.config.ts — Error and Performance Monitoring
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  
  // Performance Monitoring
  tracesSampleRate: 1.0,
  
  // Capture Web Vitals
  integrations: [
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
  
  replaySessionSampleRate: 0.1,
  replayOnErrorSampleRate: 1.0,
  
  // Profiling
  profilesSampleRate: 0.1,
});

// Google Analytics with Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  window.gtag?.('event', metric.name, {
    value: Math.round(metric.value),
    event_category: 'Web Vitals',
    event_label: metric.id,
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

---

## Image Optimization

**ALWAYS**:
- Use WebP format with JPEG fallback
- Lazy load images below the fold
- Serve responsive images with `srcset`
- Use `next/image` or similar optimization
- Optimize for mobile-first (smaller on mobile)
- Set explicit width/height to prevent CLS

**NEVER**:
- Serve high-resolution images to mobile
- Forget alt text
- Skip lazy loading
- Use images without aspect ratio (causes shift)

### ✅ GOOD Image Optimization

```typescript
import Image from 'next/image';

export function OptimizedImage() {
  return (
    <Image
      src="/images/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      sizes="(max-width: 640px) 100vw,
             (max-width: 1024px) 50vw,
             33vw"
      priority={false} // Set true for LCP images only
      quality={75}
      placeholder="blur" // Show blur while loading
      onLoadingComplete={(result) => {
        // Track image load time
        console.log(`Image loaded: ${result.naturalWidth}x${result.naturalHeight}`);
      }}
    />
  );
}

// For LCP images (hero, above-fold)
export function LCPImage() {
  return (
    <Image
      src="/images/hero.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority={true} // Preload, high fetchpriority
      quality={85}
    />
  );
}
```

---

## JavaScript Performance

**ALWAYS**:
- Code split by route (avoid loading everything)
- Lazy load heavy components (chart libraries, editors)
- Minify and compress (gzip, brotli)
- Remove unused dependencies
- Tree-shake dead code
- Monitor main thread blocking

**NEVER**:
- Bundle entire frameworks on every page
- Ship source maps to production
- Block page load on non-critical JS

### ✅ GOOD Code Splitting

```typescript
// pages/dashboard.tsx — Dynamic imports
import dynamic from 'next/dynamic';

// Lazy load heavy chart library
const RevenueChart = dynamic(() => import('@/components/charts/Revenue'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Don't render on server
});

// Lazy load editor (only when user clicks)
const CodeEditor = dynamic(() => import('@monaco-editor/react'), {
  loading: () => <EditorSkeleton />,
  ssr: false,
});

export function Dashboard() {
  const [showEditor, setShowEditor] = useState(false);

  return (
    <div>
      <h1>Dashboard</h1>
      <RevenueChart /> {/* Loads in background */}
      
      {showEditor && (
        <CodeEditor
          defaultValue="// Your code here"
          language="typescript"
        />
      )}
      <button onClick={() => setShowEditor(true)}>
        Open Editor
      </button>
    </div>
  );
}
```

---

## Rendering Performance

**ALWAYS**:
- Avoid layout thrashing (read/write DOM alternately)
- Use `requestAnimationFrame` for animations
- Batch DOM updates
- Use React.memo, useMemo for expensive renders
- Profile with DevTools (Performance tab)

**NEVER**:
- Force sync layout calculations in loops
- Re-render on every state change
- Leave expensive computations in render path

### ✅ GOOD Rendering Pattern

```typescript
// Memoize expensive component
const ExpensiveChart = React.memo(({ data }: { data: DataPoint[] }) => {
  return (
    <div>
      {/* Complex rendering logic */}
    </div>
  );
});

// Batch updates
export function BatchedUpdates() {
  const [items, setItems] = useState<Item[]>([]);

  const handleAddMany = () => {
    // Add multiple items in one batch
    setItems((prev) => [
      ...prev,
      ...newItems.map((item) => ({ ...item, id: generateId() })),
    ]);
  };

  return <button onClick={handleAddMany}>Add Items</button>;
}

// Avoid layout thrashing
export function EfficientDOM() {
  const handleUpdate = () => {
    // ❌ Bad: alternates read/write
    // element.style.width = element.offsetWidth + 10 + 'px';

    // ✅ Good: batch reads, then writes
    const width = element.offsetWidth;
    element.style.width = (width + 10) + 'px';
  };
}
```

---

## Performance Monitoring Checklist

- [ ] Core Web Vitals tracked (LCP, INP, CLS)
- [ ] Performance budgets set and enforced
- [ ] Lighthouse CI configured
- [ ] Google Analytics RUM enabled
- [ ] Sentry performance monitoring enabled
- [ ] Bundle size analyzed and optimized
- [ ] Images optimized (WebP, responsive, lazy)
- [ ] Code splitting by route
- [ ] Heavy libraries lazy-loaded
- [ ] No blocking JavaScript
- [ ] Main thread unblocked (< 50ms tasks)
- [ ] Rendering performance profiled
- [ ] Alerts set for metric regressions
- [ ] Low-end device tested (slow 4G)

---

## Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| LCP | < 2.5s | Good |
| INP | < 200ms | Good |
| CLS | < 0.1 | Good |
| FCP | < 1.5s | Good |
| TTFB | < 600ms | Good |
| Bundle (gzip) | < 250KB | Good |
| Lighthouse | > 90 | Good |

---

## Summary

Good performance monitoring:
1. **Measured** — Core Web Vitals tracked in production
2. **Budgeted** — Clear targets enforced in CI
3. **Optimized** — Images, bundles, code split
4. **Tested** — Low-end devices, multiple runs
5. **Alerted** — Regressions caught immediately
6. **Analyzed** — Lighthouse, DevTools profiling

Performance is a feature, not an afterthought.
