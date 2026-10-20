---
description: Run Frontend Performance, Bundle, and Web Vitals Checks
globs: ['src/components/**/*.tsx', 'src/app/**/*.tsx', 'src/pages/**/*.tsx', 'package.json']
---

# Performance: Frontend & Core Web Vitals

<audit_rules>

- You MUST verify that heavy third-party libraries are tree-shaken or lazy-loaded (`next/dynamic` or `React.lazy`) to stay within bundle budgets (<200KB gzipped for landing pages).
- You MUST enforce the use of framework-optimized image components (e.g., Next.js `<Image>`) instead of standard `<img>` tags.
- You MUST ensure images have explicit `width` and `height` properties or use `fill` with `sizes` to prevent Cumulative Layout Shift (CLS).
- You MUST verify that critical above-the-fold images use the `priority={true}` prop to improve Largest Contentful Paint (LCP).
- You MUST check for render-blocking scripts in the `<head>`. Third-party scripts MUST be loaded asynchronously or deferred (e.g., using `next/script` with `strategy="lazyOnload"`).
- You MUST enforce font optimization using framework utilities (e.g., `next/font`) or `font-display: swap` to prevent Flash of Unstyled Text (FOUT).
  </audit_rules>

<example_good>

```tsx
import Image from 'next/image'
import dynamic from 'next/dynamic'

// Lazy loading a heavy charting component
const HeavyChart = dynamic(() => import('./HeavyChart'), { ssr: false })

export default function Hero() {
  return (
    <section>
      <Image src='/hero-banner.jpg' alt='Hero Banner' width={1200} height={600} priority={true} />
      <HeavyChart />
    </section>
  )
}
```

</example_good>

<example_bad>

```tsx
import { HeavyChart } from 'heavy-charting-library' // BAD: Synchronous import bloats initial bundle

export default function Hero() {
  return (
    <section>
      {/* BAD: Missing dimensions causes Layout Shift, missing priority hurts LCP */}
      <img src='/hero-banner.jpg' alt='Hero Banner' />
      <HeavyChart />
    </section>
  )
}
```

</example_bad>
