---
name: bundle-analyze
description: Analyzes frontend bundle size and suggests optimizations
user-invocable: true
allowed-tools: Bash Read Edit Glob
effort: medium
---

## Bundle Analysis

1. Check build tool:
```bash
cat package.json | grep -E '"build"|vite|webpack|rollup|esbuild|next'
```

2. Generate bundle stats:
```bash
# Next.js
npx next build --analyze 2>/dev/null

# Vite
npx vite-bundle-visualizer 2>/dev/null

# Generic build size
bun run build 2>&1 | grep -E "\.js|\.css|kB|MB"
```

3. Identify heavy dependencies:
```bash
cat package.json | grep -E '"dependencies"' -A 50
# Check bundle phobia for top suspects
```

4. Find optimization opportunities:
   - Libraries with lighter alternatives (moment.js → date-fns, lodash → native)
   - Packages imported entirely but only a few functions used
   - Client-side code that could be server-side
   - Missing dynamic imports for routes/heavy components

5. Report:
```
Total bundle: X KB (gzipped: Y KB)

Top 5 contributors:
  react-dom         45 KB
  chart-library    120 KB  ← consider lighter alternative
  ...

Potential savings: ~Z KB with recommended changes
```
