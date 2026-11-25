---
name: canon-bundle-size
description: Use when auditing or reducing JavaScript and CSS bundle sizes, setting performance budgets, choosing lighter alternatives to heavy libraries, configuring tree shaking, code splitting, and lazy loading. Trigger when the user mentions bundle size, JavaScript size, tree shaking, code splitting, lazy loading, or performance budget.
---

# CANON · Bundle Size

Every kilobyte of JavaScript costs twice: once to download, once to parse and execute. CSS blocks render. Both have budgets.

## Budgets

| Asset | Budget (gzipped) |
|---|---|
| Initial JS (critical path) | ≤ 200KB |
| Total JS (all routes) | ≤ 500KB |
| CSS (total) | ≤ 60KB |
| Total page weight (first load) | ≤ 1.5MB |

These are starting points. Rich apps (maps, editors) may exceed them with justification. Simple marketing pages should come in far under.

## Strategies (ordered by impact)

1. **Don't ship what you don't use.** Audit imports. Remove dead code. Tree shake.
2. **Replace heavy libraries with lighter alternatives.** moment → date-fns. lodash → per-function imports or native. chart.js → uPlot.
3. **Code-split by route.** `React.lazy()` + `Suspense`, or dynamic `import()`. Every route loads only its code.
4. **Lazy-load below-the-fold components.** Image galleries, comments, maps — load when the user scrolls near.
5. **Externalize large deps.** CDN-hosted React/Vue/Angular with proper cache headers.
6. **Compress.** Brotli > gzip. 15–20% smaller.

## Measuring

```bash
# Webpack
npx webpack --profile --json > stats.json
npx webpack-bundle-analyzer stats.json

# Vite
npx vite build --report

# Per-package
npx bundlephobia <package-name>
```

Track sizes in CI. Alert on regressions.

## Common heavy dependencies

| Package | Size (minified) | Alternative |
|---|---|---|
| moment | 300KB | date-fns (tree-shakeable), dayjs (2KB) |
| lodash (full) | 70KB | lodash-es (per-function), native |
| chart.js | 200KB | uPlot (35KB), lightweight D3 |
| Ant Design (full) | 1MB+ | Cherry-pick components |
| Three.js | 600KB | Only if you need 3D |

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Importing full lodash for one function | 70KB for `_.debounce` |
| No code splitting (single bundle) | Every route pays for every other route |
| Polyfilling for IE11 in 2026 | Dead weight for 99.9% of users |
| Source maps in production bundle | Inflates download (serve separately) |
| No tree shaking (CommonJS imports) | Dead code shipped |

## Audit checklist

- [ ] Initial JS ≤ 200KB gzipped
- [ ] CSS ≤ 60KB gzipped
- [ ] Bundle analyzer run, largest deps identified
- [ ] Code split by route
- [ ] Below-fold components lazy loaded
- [ ] No full-library imports where per-function works
- [ ] Brotli compression enabled
- [ ] Bundle size tracked in CI

## Sources

- web.dev · "Reduce JavaScript payloads with code splitting"
- Bundlephobia · package size checker
- `canon-performance` for Core Web Vitals targets
