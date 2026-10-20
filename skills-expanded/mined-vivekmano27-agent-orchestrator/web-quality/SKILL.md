---
name: web-quality
description: Audit web application quality — Core Web Vitals (LCP, FID, CLS), Lighthouse scores, performance optimization, accessibility compliance, SEO, and best practices. Use when the user mentions "performance audit", "Lighthouse", "Core Web Vitals", "LCP", "page speed", "web quality", or needs to improve web app metrics.
allowed-tools: Read, Bash, Grep, Glob
---

# Web Quality Skill

## Step 1 — Identify Performance-Critical Pages

Scan for routes and prioritize by traffic impact:

```bash
# Find all page/route entry points
find . -path "*/app/**/page.tsx" -o -path "*/pages/**/*.tsx" | grep -v node_modules | head -30

# Find dynamic routes (often slower due to data fetching)
grep -rn "getServerSideProps\|getStaticProps\|generateStaticParams\|loader\|useLoaderData" --include="*.ts" --include="*.tsx" | grep -v node_modules

# Find client-side heavy pages
grep -rn "'use client'\|\"use client\"" --include="*.tsx" | grep -v node_modules
```

Pages with `getServerSideProps` (not cached) and `'use client'` at the page level are highest priority for optimization.

## Step 2 — Configure Lighthouse CI

Create `lighthouserc.js` in the project root:

```javascript
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/dashboard',
        'http://localhost:3000/login',
        // Add all critical routes
      ],
      startServerCommand: 'npm run start',  // use production build, NOT dev
      startServerReadyPattern: 'ready on',
      numberOfRuns: 3,  // median of 3 runs reduces variance
      settings: {
        preset: 'desktop',  // also run with preset: 'mobile' separately
        throttling: {
          // Simulate real-world conditions — do NOT test unthrottled
          cpuSlowdownMultiplier: 4,
          rttMs: 40,
          throughputKbps: 10240,
        },
      },
    },
    assert: {
      assertions: {
        // Core Web Vitals — hard gates
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'interactive': ['error', { maxNumericValue: 3800 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],

        // Category scores — hard gates
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],

        // Individual audits — warn on regression
        'uses-responsive-images': 'warn',
        'offscreen-images': 'warn',
        'render-blocking-resources': 'warn',
        'unused-css-rules': 'warn',
        'unused-javascript': 'warn',
      },
    },
    upload: {
      target: 'temporary-public-storage',  // free Lighthouse CI storage
      // Or use: target: 'lhci', serverBaseUrl: 'https://your-lhci-server.com'
    },
  },
};
```

**Install and run:**
```bash
npm install -D @lhci/cli
npx lhci autorun
```

## Step 3 — Performance Budget Configuration

Create `budget.json` for build-time enforcement:

```json
[
  {
    "path": "/*",
    "timings": [
      { "metric": "largest-contentful-paint", "budget": 2500 },
      { "metric": "cumulative-layout-shift", "budget": 0.1 },
      { "metric": "total-blocking-time", "budget": 200 }
    ],
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "stylesheet", "budget": 50 },
      { "resourceType": "image", "budget": 500 },
      { "resourceType": "total", "budget": 1000 }
    ],
    "resourceCounts": [
      { "resourceType": "script", "budget": 15 },
      { "resourceType": "third-party", "budget": 5 }
    ]
  }
]
```

For webpack/Next.js, also configure bundle size alerts:

```javascript
// next.config.js
module.exports = {
  experimental: {
    // Fail build if page JS exceeds budget
    largePageDataWarnings: true,
  },
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.performance = {
        hints: 'error',             // fail the build, don't just warn
        maxAssetSize: 250_000,      // 250 KB per asset
        maxEntrypointSize: 300_000, // 300 KB per entry point
      };
    }
    return config;
  },
};
```

**Constraint:** Performance budgets must use `'error'` not `'warning'`. Warnings are ignored. A budget that doesn't break the build is not a budget.

## Step 4 — Find Optimization Opportunities

Run these searches to find common performance problems:

```bash
# Unoptimized images (not using next/image or responsive formats)
grep -rn '<img ' --include="*.tsx" --include="*.jsx" | grep -v 'next/image\|Image ' | grep -v node_modules

# Large client-side bundles (barrel imports)
grep -rn "from '[^']*'" --include="*.ts" --include="*.tsx" | grep "import {" | grep -v node_modules | head -30
# Check for barrel file re-exports that pull entire packages
grep -rn "export \*" --include="index.ts" --include="index.js" | grep -v node_modules

# Synchronous data fetching blocking render
grep -rn "await.*fetch\|await.*axios\|await.*prisma\|await.*db\." --include="*.tsx" | grep -v node_modules
# Multiple sequential awaits in a page component = waterfall

# Missing lazy loading
grep -rn "import.*from" --include="*.tsx" --include="*.jsx" | grep -v "lazy\|dynamic\|Suspense\|node_modules" | head -30

# Web font loading without display swap
grep -rn "@font-face\|font-display" --include="*.css" --include="*.scss" | grep -v node_modules
grep -rn "fonts.googleapis.com" --include="*.html" --include="*.tsx" | grep -v "display=swap"

# Missing rel=preload/preconnect for critical resources
grep -rn "rel=\"preload\"\|rel=\"preconnect\"" --include="*.html" --include="*.tsx" | grep -v node_modules
```

## Step 5 — CI Integration

Add to `.github/workflows/lighthouse.yml`:

```yaml
name: Lighthouse CI
on:
  pull_request:
    paths:
      - 'src/**'
      - 'app/**'
      - 'public/**'
      - 'package.json'

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - run: npx @lhci/cli autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: lighthouse-results
          path: .lighthouseci/
          retention-days: 14
```

## Output Format

Write to `.claude/specs/{feature}/web-quality-report.md`:

```markdown
# Web Quality Report — {Feature/Project Name}

**Date:** {YYYY-MM-DD}
**Pages audited:** {count}
**Lighthouse version:** {version}
**Throttling:** {4x CPU slowdown, 40ms RTT, 10Mbps}

## Scores Summary

| Page | Performance | Accessibility | Best Practices | SEO | LCP (ms) | CLS | TBT (ms) |
|------|-------------|---------------|----------------|-----|----------|-----|-----------|
| / | 94 | 98 | 100 | 100 | 1850 | 0.02 | 120 |
| /dashboard | 72 | 91 | 92 | 95 | 3200 | 0.15 | 450 |

## Core Web Vitals

| Metric | Target | Best Page | Worst Page | Status |
|--------|--------|-----------|------------|--------|
| LCP | < 2500ms | / (1850ms) | /dashboard (3200ms) | FAIL |
| CLS | < 0.1 | / (0.02) | /dashboard (0.15) | FAIL |
| TBT | < 200ms | / (120ms) | /dashboard (450ms) | FAIL |

## Bundle Analysis

| Entry Point | Size (gzip) | Budget | Status |
|-------------|-------------|--------|--------|
| pages/index | 142 KB | 300 KB | PASS |
| pages/dashboard | 380 KB | 300 KB | FAIL |

## Optimization Opportunities

### Critical (Blocking CWV Targets)

1. **{Page}: LCP — {cause}**
   - **Current:** {value}ms, **Target:** <2500ms
   - **Root cause:** {e.g., hero image is 2.4MB uncompressed PNG}
   - **Fix:** {exact change — e.g., convert to WebP, add `next/image` with priority, add `<link rel="preload">`}
   - **File:** `{path}:{line}`
   - **Estimated impact:** -{X}ms

### Recommended

1. **{Optimization}** — {estimated impact}
   - **File:** `{path}:{line}`
   - **Change:** {specific code/config change}

## Third-Party Script Impact

| Script | Size | Blocking? | Load Time Impact | Recommendation |
|--------|------|-----------|------------------|----------------|
| Google Analytics | 45 KB | No (async) | +120ms | Keep |
| Intercom widget | 210 KB | Yes | +800ms | Lazy-load after interaction |
```

## Constraints

- Always run Lighthouse on a production build (`npm run build && npm start`). Dev mode includes hot reload overhead, source maps, and unminified code. Dev-mode Lighthouse scores are meaningless.
- Never report Lighthouse scores without specifying throttling settings. Unthrottled scores are 20-40 points higher than real user experience.
- When a CWV metric fails, trace it to a specific resource or code path. "LCP is 3.2s" is a symptom. "LCP is 3.2s because the hero image at `public/hero.png` is 2.4MB and loaded without `priority`" is actionable.
- Do not recommend `loading="lazy"` on above-the-fold images. This worsens LCP. Only hero/LCP images should be eagerly loaded.
- `resourceSizes` budgets are in KB (kilobytes), not bytes. Getting this wrong creates budgets that are 1000x too permissive.

## Anti-Patterns

- **Dev-mode Lighthouse** — running Lighthouse against `npm run dev`; scores are meaningless without production build
- **Unthrottled scores** — reporting scores without specifying throttling; unthrottled is 20-40 points above real experience
- **Lazy-loading hero images** — `loading="lazy"` on above-the-fold LCP images worsens LCP; eagerly load hero content
- **Symptom-only reports** — "LCP is 3.2s" without tracing to a specific resource or code path; always identify the cause
- **Ignoring CLS** — focusing only on LCP/FID while layout shift goes unaddressed; CLS is user-visible jank
- **No budgets** — no performance budgets means no guardrails; set bundle and resource size budgets

## Checklist

- [ ] Lighthouse run on production build with throttling enabled
- [ ] LCP < 2.5s, FID < 100ms, CLS < 0.1 (Good thresholds)
- [ ] Performance budgets set for bundle and resource sizes
- [ ] Hero/LCP image eagerly loaded (no lazy loading)
- [ ] Images use next/image or explicit width/height for CLS prevention
- [ ] JavaScript bundle analyzed for large dependencies
- [ ] Core Web Vitals traced to specific causes (not just scores reported)
- [ ] Accessibility score included in quality report
