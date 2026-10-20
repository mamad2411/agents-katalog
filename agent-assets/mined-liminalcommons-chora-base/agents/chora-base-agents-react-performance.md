---
sap_id: SAP-025
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: advanced
estimated_reading_time: 13
progressive_loading:
  phase_1: "lines 1-220"   # Quick Start + Core Workflows
  phase_2: "lines 221-450" # Advanced Workflows
  phase_3: "full"          # Complete including best practices and pitfalls
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 13500
---

## 📖 Quick Reference

**New to SAP-025?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Install performance dependencies
- 📚 **Time Savings** - 91% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-005, SAP-020, SAP-021, SAP-023, SAP-024, SAP-026

This AGENTS.md provides: Agent-specific patterns for implementing SAP-025.
s.

---

# React Performance Optimization (SAP-025) - Agent Awareness

**SAP ID**: SAP-025
**Agent Compatibility**: All AI agents with command execution and file operations
**Last Updated**: 2025-11-05

---

## Quick Start for Agents

This SAP provides workflows for **React performance optimization** to meet Core Web Vitals targets.

### First-Time Session

1. **Identify performance issue**: Slow LCP, high INP, or layout shifts (CLS)
2. **Choose optimization**: Code splitting, image optimization, or font loading
3. **Implement pattern**: Use production-ready templates
4. **Measure impact**: Lighthouse CI, Web Vitals monitoring

### Core Web Vitals Targets

- **LCP** (Largest Contentful Paint): ≤2.5 seconds
- **INP** (Interaction to Next Paint): ≤200 milliseconds
- **CLS** (Cumulative Layout Shift): ≤0.1

---

## User Signal Pattern Tables

### Table 1: Performance Optimization Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Optimize images** | "Optimize images", "Lazy load images", "Image performance" | Execute Workflow 1: Setup Image Optimization | Next.js Image or Vite image components configured |
| **Code splitting** | "Split bundle", "Lazy load routes", "Reduce bundle size" | Execute Workflow 2: Setup Code Splitting | Route-based and component-based code splitting |
| **Optimize fonts** | "Font loading", "Optimize web fonts", "Preload fonts" | Execute Workflow 3: Setup Font Optimization | next/font or @font-face optimized |
| **Lighthouse CI** | "Setup Lighthouse", "CI performance tests", "Core Web Vitals CI" | Execute Workflow 4: Setup Lighthouse CI | Lighthouse CI configured in GitHub Actions |
| **Bundle analysis** | "Analyze bundle", "Bundle size", "Tree shaking" | Execute Workflow 5: Setup Bundle Analysis | Bundle analyzer showing module sizes |

### Table 2: Performance Measurement Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Measure Core Web Vitals** | "Check Core Web Vitals", "LCP score", "Performance metrics" | Run Lighthouse | LCP, INP, CLS measurements |
| **Analyze bundle size** | "Bundle size analysis", "What's in my bundle?" | Run bundle analyzer | Visual treemap of bundle contents |
| **Profile React components** | "React DevTools Profiler", "Component render times" | Use React DevTools Profiler | Component render performance data |
| **Test on slow network** | "Throttle network", "Simulate 3G" | Use Lighthouse throttling | Performance on slow connections |
| **Monitor in production** | "Track Web Vitals", "Real user monitoring" | Setup Web Vitals monitoring | Real-user performance data |

---

## Workflow 1: Setup Image Optimization for Next.js 15 (10-15 minutes)

**When to use**: Optimizing images to improve LCP (Largest Contentful Paint)

**Prerequisites**:
- Next.js 15 project
- Images in project (e.g., public/images/ or remote URLs)

**Steps**:

1. **Configure next.config.ts for external images** (`next.config.ts`):
   ```typescript
   import type { NextConfig } from 'next'

   const nextConfig: NextConfig = {
     images: {
       remotePatterns: [
         {
           protocol: 'https',
           hostname: 'images.unsplash.com',
           port: '',
           pathname: '/**',
         },
         {
           protocol: 'https',
           hostname: 'cdn.example.com',
           port: '',
           pathname: '/images/**',
         },
       ],
       formats: ['image/webp', 'image/avif'],
       deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
       imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
     },
   }

   export default nextConfig
   ```

2. **Create optimized Image component** (`components/ui/optimized-image.tsx`):
   ```typescript
   import Image from 'next/image'
   import type { ImageProps } from 'next/image'

   interface OptimizedImageProps extends Omit<ImageProps, 'src'> {
     src: string
     alt: string
     priority?: boolean
   }

   export function OptimizedImage({ src, alt, priority = false, ...props }: OptimizedImageProps) {
     return (
       <Image
         src={src}
         alt={alt}
         priority={priority}  // For LCP image (above fold)
         loading={priority ? 'eager' : 'lazy'}
         placeholder="blur"  // Requires blurDataURL
         quality={85}  // 85 is optimal (90+ diminishing returns)
         {...props}
       />
     )
   }
   ```

3. **Use Image component for LCP image** (above fold):
   ```typescript
   import { OptimizedImage } from '@/components/ui/optimized-image'

   export default function Home() {
     return (
       <div>
         {/* LCP image: priority={true} */}
         <OptimizedImage
           src="/hero.jpg"
           alt="Hero image"
           width={1920}
           height={1080}
           priority={true}  // Preload (above fold)
         />

         {/* Below fold images: lazy loading */}
         <OptimizedImage
           src="/gallery-1.jpg"
           alt="Gallery image 1"
           width={800}
           height={600}
         />
       </div>
     )
   }
   ```

4. **Test image optimization**:
   ```bash
   pnpm dev
   ```

   Open browser DevTools → Network tab:
   - Verify images converted to WebP/AVIF
   - Check image sizes (responsive srcset generated)
   - LCP image preloaded (priority={true})

5. **Measure LCP improvement**:
   ```bash
   npx lighthouse http://localhost:3000 --view
   ```

   Target: LCP ≤2.5 seconds

**Expected outcome**:
- Images served in WebP/AVIF (smaller file sizes)
- Responsive srcset for different screen sizes
- LCP image preloaded with priority={true}
- Lazy loading for below-fold images
- 30-50% improvement in LCP

**Time saved**: 1-2 hours (manual image optimization) → 10-15 minutes (Next.js Image)

---

## Workflow 2: Setup Code Splitting with React.lazy (10-20 minutes)

**When to use**: Reducing initial bundle size, lazy loading routes and components

**Prerequisites**:
- React 19 project (Next.js 15 or Vite 7)
- Large components or routes to split

**Steps**:

1. **Identify large components**:
   ```bash
   # Run bundle analyzer
   pnpm add -D @next/bundle-analyzer  # Next.js
   # Or
   pnpm add -D rollup-plugin-visualizer  # Vite
   ```

   **Next.js** (`next.config.ts`):
   ```typescript
   import bundleAnalyzer from '@next/bundle-analyzer'

   const withBundleAnalyzer = bundleAnalyzer({
     enabled: process.env.ANALYZE === 'true',
   })

   export default withBundleAnalyzer({
     // ... config
   })
   ```

   Run analyzer:
   ```bash
   ANALYZE=true pnpm build
   ```

2. **Create code-split component with React.lazy** (`app/dashboard/page.tsx`):
   ```typescript
   import { lazy, Suspense } from 'react'

   // ❌ BAD: Eager import (always in bundle)
   // import { HeavyChart } from '@/components/heavy-chart'

   // ✅ GOOD: Lazy import (separate chunk)
   const HeavyChart = lazy(() => import('@/components/heavy-chart'))

   export default function Dashboard() {
     return (
       <div>
         <h1>Dashboard</h1>
         <Suspense fallback={<div>Loading chart...</div>}>
           <HeavyChart />
         </Suspense>
       </div>
     )
   }
   ```

3. **Create retry logic for dynamic imports** (`lib/lazy-with-retry.ts`):
   ```typescript
   import { ComponentType, lazy } from 'react'

   export function lazyWithRetry<T extends ComponentType<any>>(
     componentImport: () => Promise<{ default: T }>,
   ): React.LazyExoticComponent<T> {
     return lazy(async () => {
       const pageHasAlreadyBeenForceRefreshed = JSON.parse(
         window.sessionStorage.getItem('page-has-been-force-refreshed') || 'false',
       )

       try {
         const component = await componentImport()
         window.sessionStorage.setItem('page-has-been-force-refreshed', 'false')
         return component
       } catch (error) {
         if (!pageHasAlreadyBeenForceRefreshed) {
           window.sessionStorage.setItem('page-has-been-force-refreshed', 'true')
           return window.location.reload()  // Retry on chunk load error
         }
         throw error
       }
     })
   }
   ```

4. **Use lazyWithRetry for production reliability**:
   ```typescript
   import { lazyWithRetry } from '@/lib/lazy-with-retry'

   const HeavyChart = lazyWithRetry(() => import('@/components/heavy-chart'))
   ```

5. **Test code splitting**:
   ```bash
   pnpm build
   ```

   Check output:
   - Multiple chunks generated (e.g., `chunk-HASH.js`)
   - Initial bundle size reduced
   - Network tab shows lazy-loaded chunks

**Expected outcome**:
- Initial bundle size reduced by 30-50%
- Heavy components loaded on demand
- Retry logic for chunk load errors
- Faster initial page load (better LCP)

**Time saved**: 1-2 hours (manual code splitting) → 10-20 minutes (React.lazy pattern)

---

## Workflow 3: Setup Font Optimization with next/font (10-15 minutes)

**When to use**: Optimizing web font loading to reduce CLS (Cumulative Layout Shift)

**Prerequisites**:
- Next.js 15 project
- Custom fonts (Google Fonts or self-hosted)

**Steps**:

1. **Install Google Font with next/font** (`app/layout.tsx`):
   ```typescript
   import { Inter, Roboto_Mono } from 'next/font/google'

   const inter = Inter({
     subsets: ['latin'],
     variable: '--font-inter',
     display: 'swap',  // Font display strategy
     preload: true,
     fallback: ['system-ui', 'arial'],
   })

   const robotoMono = Roboto_Mono({
     subsets: ['latin'],
     variable: '--font-roboto-mono',
     display: 'swap',
     preload: true,
     fallback: ['courier', 'monospace'],
   })

   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
         <body className="font-sans">{children}</body>
       </html>
     )
   }
   ```

2. **Configure Tailwind to use font variables** (`tailwind.config.ts`):
   ```typescript
   const config: Config = {
     theme: {
       extend: {
         fontFamily: {
           sans: ['var(--font-inter)', 'system-ui', 'arial'],
           mono: ['var(--font-roboto-mono)', 'courier', 'monospace'],
         },
       },
     },
   }
   ```

3. **Use self-hosted fonts** (alternative to Google Fonts):
   ```typescript
   import localFont from 'next/font/local'

   const myFont = localFont({
     src: [
       {
         path: './fonts/my-font-regular.woff2',
         weight: '400',
         style: 'normal',
       },
       {
         path: './fonts/my-font-bold.woff2',
         weight: '700',
         style: 'normal',
       },
     ],
     variable: '--font-my-font',
     display: 'swap',
     preload: true,
   })
   ```

4. **Test font optimization**:
   ```bash
   pnpm dev
   ```

   Open DevTools → Network tab:
   - Fonts preloaded (in <head>)
   - WOFF2 format served (best compression)
   - No layout shift (font-display: swap + fallback)

5. **Measure CLS improvement**:
   ```bash
   npx lighthouse http://localhost:3000 --view
   ```

   Target: CLS ≤0.1

**Expected outcome**:
- Fonts preloaded (no CLS from font loading)
- WOFF2 format for smaller file sizes
- System font fallback (no invisible text)
- 50-70% reduction in CLS

**Time saved**: 30 minutes-1 hour (manual font optimization) → 10-15 minutes (next/font)

---

## Workflow 4: Setup Lighthouse CI for GitHub Actions (15-25 minutes)

**When to use**: Automating performance testing in CI/CD pipeline

**Prerequisites**:
- GitHub repository
- Next.js 15 or Vite 7 project
- Performance budgets defined

**Steps**:

1. **Install Lighthouse CI**:
   ```bash
   pnpm add -D @lhci/cli
   ```

2. **Create Lighthouse CI configuration** (`lighthouserc.json`):
   ```json
   {
     "ci": {
       "collect": {
         "startServerCommand": "pnpm start",
         "url": ["http://localhost:3000/"],
         "numberOfRuns": 3
       },
       "assert": {
         "preset": "lighthouse:recommended",
         "assertions": {
           "categories:performance": ["error", { "minScore": 0.9 }],
           "categories:accessibility": ["error", { "minScore": 0.9 }],
           "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
           "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
           "interactive": ["error", { "maxNumericValue": 3500 }],
           "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
         }
       },
       "upload": {
         "target": "temporary-public-storage"
       }
     }
   }
   ```

3. **Create GitHub Actions workflow** (`.github/workflows/lighthouse-ci.yml`):
   ```yaml
   name: Lighthouse CI

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     lighthouse:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - uses: pnpm/action-setup@v4
           with:
             version: 10

         - uses: actions/setup-node@v4
           with:
             node-version: 22
             cache: 'pnpm'

         - run: pnpm install
         - run: pnpm build

         - name: Run Lighthouse CI
           run: |
             pnpm dlx @lhci/cli@0.15.x autorun
           env:
             LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
   ```

4. **Test Lighthouse CI locally**:
   ```bash
   pnpm build
   pnpm dlx @lhci/cli autorun
   ```

   Check assertions:
   - Performance score ≥90
   - LCP ≤2.5s
   - CLS ≤0.1

5. **Commit and push**:
   ```bash
   git add lighthouserc.json .github/workflows/lighthouse-ci.yml
   git commit -m "feat: Add Lighthouse CI"
   git push
   ```

   View results in GitHub Actions → Lighthouse CI

**Expected outcome**:
- Automated performance testing on every PR
- Performance budget enforced (fails CI if metrics regress)
- Lighthouse reports uploaded to temporary storage
- +30% earlier detection of performance regressions

**Time saved**: 1-2 hours (manual Lighthouse setup) → 15-25 minutes (template-based)

---

## Workflow 5: Setup Bundle Analysis (5-10 minutes)

**When to use**: Identifying large modules in bundle, finding optimization opportunities

**Prerequisites**:
- Next.js 15 or Vite 7 project

**Steps**:

1. **Install bundle analyzer**:

   **Next.js**:
   ```bash
   pnpm add -D @next/bundle-analyzer
   ```

   **Vite**:
   ```bash
   pnpm add -D rollup-plugin-visualizer
   ```

2. **Configure bundle analyzer**:

   **Next.js** (`next.config.ts`):
   ```typescript
   import bundleAnalyzer from '@next/bundle-analyzer'

   const withBundleAnalyzer = bundleAnalyzer({
     enabled: process.env.ANALYZE === 'true',
   })

   const nextConfig = {
     // ... your config
   }

   export default withBundleAnalyzer(nextConfig)
   ```

   **Vite** (`vite.config.ts`):
   ```typescript
   import { visualizer } from 'rollup-plugin-visualizer'

   export default defineConfig({
     plugins: [
       react(),
       visualizer({
         open: true,
         gzipSize: true,
         brotliSize: true,
       }),
     ],
   })
   ```

3. **Add bundle analysis script** (`package.json`):
   ```json
   {
     "scripts": {
       "analyze": "ANALYZE=true pnpm build"
     }
   }
   ```

4. **Run bundle analyzer**:
   ```bash
   pnpm analyze
   ```

   Opens browser with treemap visualization:
   - Largest modules highlighted
   - Gzip/Brotli sizes shown
   - Identify optimization targets

5. **Analyze results and optimize**:
   - Large libraries (>50KB): Consider alternatives or tree shaking
   - Duplicate dependencies: Check for version mismatches
   - Unused code: Remove dead code
   - Heavy components: Code split with React.lazy

**Expected outcome**:
- Visual treemap of bundle contents
- Module sizes (parsed, gzipped, brotli)
- Optimization targets identified
- Data-driven bundle optimization

**Time saved**: 30 minutes-1 hour (manual bundle analysis) → 5-10 minutes (analyzer setup)

---

## Best Practices

### 1. Preload LCP Image with priority={true}

**Pattern**:
```typescript
// ✅ GOOD: LCP image preloaded
<Image src="/hero.jpg" alt="Hero" width={1920} height={1080} priority={true} />

// ❌ BAD: LCP image lazy loaded
<Image src="/hero.jpg" alt="Hero" width={1920} height={1080} />
```

**Why**: LCP image should be preloaded (loaded before JavaScript executes)

---

### 2. Use React.lazy for Heavy Components

**Pattern**:
```typescript
// ✅ GOOD: Lazy load heavy component
const HeavyChart = lazy(() => import('@/components/heavy-chart'))

// ❌ BAD: Eager import (always in bundle)
import { HeavyChart } from '@/components/heavy-chart'
```

**Why**: Reduces initial bundle size by 30-50%

---

### 3. Use next/font for Zero CLS Font Loading

**Pattern**:
```typescript
// ✅ GOOD: next/font (preloaded, no CLS)
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], display: 'swap' })

// ❌ BAD: Link in <head> (CLS from font loading)
<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet" />
```

**Why**: next/font preloads fonts, eliminates CLS

---

### 4. Enforce Performance Budgets with Lighthouse CI

**Pattern**:
```json
// ✅ GOOD: Strict performance budgets
{
  "assertions": {
    "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
    "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
  }
}

// ❌ BAD: No performance budgets (regressions undetected)
```

**Why**: Prevents performance regressions in CI

---

### 5. Use Bundle Analyzer to Identify Optimization Targets

**Pattern**:
```bash
# ✅ GOOD: Regular bundle analysis
pnpm analyze

# Identify:
# - Large modules (>50KB)
# - Duplicate dependencies
# - Unused code

# ❌ BAD: No bundle analysis (blind to bundle bloat)
```

**Why**: Data-driven optimization (30-50% bundle size reduction)

---

## Common Pitfalls

### Pitfall 1: Not Using priority={true} for LCP Image

**Problem**: LCP image lazy loaded, slow LCP

**Fix**: Add priority={true}
```typescript
// ❌ BAD: LCP image lazy loaded
<Image src="/hero.jpg" alt="Hero" width={1920} height={1080} />

// ✅ GOOD: LCP image preloaded
<Image src="/hero.jpg" alt="Hero" width={1920} height={1080} priority={true} />
```

**Why**: LCP image must be preloaded for fast LCP (≤2.5s)

---

### Pitfall 2: Not Wrapping React.lazy with Suspense

**Problem**: React.lazy without Suspense causes error

**Fix**: Wrap with Suspense
```typescript
// ❌ BAD: React.lazy without Suspense
const HeavyChart = lazy(() => import('@/components/heavy-chart'))
<HeavyChart />  // Error: Suspense boundary required

// ✅ GOOD: Wrapped with Suspense
<Suspense fallback={<div>Loading...</div>}>
  <HeavyChart />
</Suspense>
```

**Why**: React.lazy requires Suspense boundary

---

### Pitfall 3: Using font-display: block (FOIT)

**Problem**: Flash of Invisible Text (FOIT), poor UX

**Fix**: Use font-display: swap
```typescript
// ❌ BAD: font-display: block (FOIT)
const inter = Inter({ display: 'block' })

// ✅ GOOD: font-display: swap (fallback font shown)
const inter = Inter({ display: 'swap' })
```

**Why**: font-display: swap shows fallback font immediately

---

### Pitfall 4: Not Setting Performance Budgets in Lighthouse CI

**Problem**: Performance regressions undetected

**Fix**: Add assertions
```json
// ❌ BAD: No assertions (regressions slip through)
{ "ci": { "collect": { "url": ["http://localhost:3000/"] } } }

// ✅ GOOD: Strict assertions
{
  "assert": {
    "assertions": {
      "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }]
    }
  }
}
```

**Why**: CI fails if performance regresses

---

### Pitfall 5: Not Analyzing Bundle After Adding Dependencies

**Problem**: Bundle bloat from large dependencies

**Fix**: Run bundle analyzer after adding dependencies
```bash
# After: pnpm add some-library
pnpm analyze

# Check:
# - Library size (gzipped)
# - Tree shaking working?
# - Alternatives available?
```

**Why**: Catch bundle bloat early (before production)

---

## Support & Resources

**SAP-025 Documentation**:
- [Capability Charter](capability-charter.md) - React performance problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and benchmarks
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [Web Vitals](https://web.dev/vitals/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)
- [Next.js Image Optimization](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [React.lazy](https://react.dev/reference/react/lazy)
- [next/font](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-024 (react-styling)](../react-styling/) - Styling strategies

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-025
  - 5 workflows: Setup Image Optimization, Setup Code Splitting, Setup Font Optimization, Setup Lighthouse CI, Setup Bundle Analysis
  - 2 user signal pattern tables: Performance Optimization Signals, Performance Measurement Signals
  - 5 best practices: Preload LCP image, React.lazy for heavy components, next/font for zero CLS, Lighthouse CI budgets, bundle analyzer
  - 5 common pitfalls: Not using priority for LCP image, not wrapping React.lazy with Suspense, using font-display block, no performance budgets, not analyzing bundle
  - Focus on Core Web Vitals (LCP, INP, CLS) and automated performance testing

---

**Next Steps**:
1. Review [protocol-spec.md](protocol-spec.md) for technical contracts
2. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
3. Install: `pnpm add -D @lhci/cli @next/bundle-analyzer`
4. Run: `npx lighthouse http://localhost:3000 --view`
