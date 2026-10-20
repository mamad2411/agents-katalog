---
name: frontend-performance-pro
description: Frontend performance optimization — code splitting, lazy loading, image optimization, bundle analysis
triggers: [performance, optimization, bundle size, lazy load, code split, lighthouse, web vitals]
---

# SKILL: Frontend Performance Pro

## Core Web Vitals (Google's Standards)

```
LCP (Largest Contentful Paint): < 2.5s
FID (First Input Delay): < 100ms  
CLS (Cumulative Layout Shift): < 0.1

How to measure:
- Lighthouse in Chrome DevTools
- web.dev/measure
- Real user monitoring (RUM)
```

## Pattern 1: Code Splitting
```tsx
// ❌ BAD: Import everything upfront
import Dashboard from './Dashboard'
import Settings from './Settings'
import Profile from './Profile'

// ✅ GOOD: Dynamic import (loads on demand)
const Dashboard = lazy(() => import('./Dashboard'))
const Settings = lazy(() => import('./Settings'))
const Profile = lazy(() => import('./Profile'))

// Usage
<Suspense fallback={<Spinner />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/settings" element={<Settings />} />
  </Routes>
</Suspense>
```

## Pattern 2: Image Optimization
```tsx
// Next.js Image component (automatic optimization)
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority  // LCP image: preload
  placeholder="blur"  // Show blur while loading
  blurDataURL="data:image/..."
/>

// For non-Next.js: Use modern formats
<picture>
  <source srcSet="/image.avif" type="image/avif" />
  <source srcSet="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="..." loading="lazy" />
</picture>
```

## Pattern 3: Bundle Analysis
```bash
# Analyze what's in your bundle
npm install --save-dev @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // ... config
})

# Run analysis
ANALYZE=true npm run build
```

## Pattern 4: Lazy Loading Heavy Components
```tsx
// Only load chart library when needed
const Chart = lazy(() => import('./Chart'))

function Dashboard() {
  const [showChart, setShowChart] = useState(false)
  
  return (
    <div>
      <button onClick={() => setShowChart(true)}>
        Show Chart
      </button>
      
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <Chart data={data} />
        </Suspense>
      )}
    </div>
  )
}
```

## Pattern 5: Prefetching (Load Before Needed)
```tsx
// Prefetch on hover (user likely to click)
<Link 
  href="/dashboard"
  onMouseEnter={() => {
    // Start loading Dashboard component
    import('./Dashboard')
  }}
>
  Dashboard
</Link>

// Or use Next.js built-in prefetch
<Link href="/dashboard" prefetch={true}>
  Dashboard
</Link>
```

## Pattern 6: Memoization (Prevent Unnecessary Rerenders)
```tsx
// ❌ BAD: Recomputes on every render
function ProductList({ products }) {
  const expensiveTotal = products.reduce((sum, p) => sum + p.price, 0)
  return <div>Total: ${expensiveTotal}</div>
}

// ✅ GOOD: Only recompute when products change
function ProductList({ products }) {
  const expensiveTotal = useMemo(
    () => products.reduce((sum, p) => sum + p.price, 0),
    [products]
  )
  return <div>Total: ${expensiveTotal}</div>
}
```

## Pattern 7: Virtual Scrolling (Large Lists)
```tsx
import { FixedSizeList } from 'react-window'

// Render only visible items (not all 10,000)
<FixedSizeList
  height={600}
  itemCount={10000}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      Item {index}
    </div>
  )}
</FixedSizeList>
```

## Quality Checks
- [ ] Lighthouse score > 90
- [ ] LCP < 2.5s, FID < 100ms, CLS < 0.1
- [ ] Images lazy-loaded (except above fold)
- [ ] Code split by route
- [ ] Heavy libraries lazy-loaded
- [ ] Bundle size analyzed
- [ ] Unused code removed (tree-shaking)
- [ ] Critical CSS inlined
