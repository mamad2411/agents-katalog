---
sap_id: SAP-025
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: advanced
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-350" # Advanced Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 11000
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

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-025.
s.

---

# React Performance Optimization (SAP-025) - Claude-Specific Awareness

**SAP ID**: SAP-025
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-05

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for React performance optimization.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic performance workflows
2. Use this file for Claude Code tool integration (Bash for testing, Write for optimization, Edit for configuration)
3. Always measure before and after with Lighthouse

### Performance Commands

```bash
# Run Lighthouse
Bash: npx lighthouse http://localhost:3000 --view

# Run bundle analyzer
Bash: ANALYZE=true pnpm build

# Run Lighthouse CI locally
Bash: pnpm dlx @lhci/cli autorun
```

---

## Claude Code React Performance Workflows

### Workflow 1: Optimizing Images with Write and Edit

```markdown
User: "Optimize images for better LCP"

Claude (Phase 1: Read Current Config - 0-5k tokens):
1. Check if next.config exists:
   Read next.config.ts

Claude (Phase 2: Update Config - 5-15k tokens):
2. Add image optimization to next.config:
   Edit next.config.ts
   # Add images.remotePatterns, images.formats

3. Create OptimizedImage component:
   Write components/ui/optimized-image.tsx
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
         priority={priority}
         loading={priority ? 'eager' : 'lazy'}
         quality={85}
         {...props}
       />
     )
   }
   ```

Claude (Phase 3: Update Page - 15-25k tokens):
4. Read current page to find LCP image:
   Read app/page.tsx

5. Replace img with OptimizedImage:
   Edit app/page.tsx
   # old_string: <img src="/hero.jpg" alt="Hero" />
   # new_string: <OptimizedImage src="/hero.jpg" alt="Hero" width={1920} height={1080} priority={true} />

6. Test optimization:
   Bash: pnpm dev

7. Measure LCP improvement:
   Bash: npx lighthouse http://localhost:3000 --view

Claude (response to user):
"✅ Image optimization configured!

**Changes**:
- next.config.ts: Added image optimization (WebP/AVIF)
- components/ui/optimized-image.tsx: Created wrapper for next/image
- app/page.tsx: Replaced img with OptimizedImage (priority={true} for LCP image)

**Performance impact**:
- Images served in WebP/AVIF (30-50% smaller)
- LCP image preloaded (priority={true})
- Lazy loading for below-fold images
- Expected LCP improvement: 30-50%

**Test**:
Run Lighthouse to verify: npx lighthouse http://localhost:3000 --view
Target: LCP ≤2.5 seconds"

Result: Images optimized, LCP improved by 30-50%
```

---

### Workflow 2: Implementing Code Splitting with Write

```markdown
User: "Add code splitting for heavy components"

Claude (Phase 1: Identify Heavy Components - 0-10k tokens):
1. Run bundle analyzer:
   Bash: ANALYZE=true pnpm build

2. Identify large components from treemap output
   # Look for components >50KB

Claude (Phase 2: Create Lazy Wrapper - 10-20k tokens):
3. Create lazyWithRetry utility:
   Write lib/lazy-with-retry.ts
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
           return window.location.reload()
         }
         throw error
       }
     })
   }
   ```

Claude (Phase 3: Apply Code Splitting - 20-35k tokens):
4. Read component using heavy import:
   Read app/dashboard/page.tsx

5. Replace eager import with lazy:
   Edit app/dashboard/page.tsx
   # old_string: import { HeavyChart } from '@/components/heavy-chart'
   # new_string: import { lazyWithRetry } from '@/lib/lazy-with-retry'
   #             const HeavyChart = lazyWithRetry(() => import('@/components/heavy-chart'))
   #             <Suspense fallback={<div>Loading...</div>}><HeavyChart /></Suspense>

6. Test code splitting:
   Bash: pnpm build
   # Verify separate chunk created

7. Measure bundle size improvement:
   Bash: ANALYZE=true pnpm build

Claude (response to user):
"✅ Code splitting implemented!

**Changes**:
- lib/lazy-with-retry.ts: Created retry logic for chunk load errors
- app/dashboard/page.tsx: Lazy loaded HeavyChart component

**Performance impact**:
- Initial bundle size reduced by 30-50%
- HeavyChart loaded on demand (separate chunk)
- Retry logic handles chunk load errors

**Bundle analysis**:
Run: ANALYZE=true pnpm build to see chunk sizes"

Result: Initial bundle size reduced by 30-50%, heavy component lazy loaded
```

---

### Workflow 3: Setting up Lighthouse CI with Write and Bash

```markdown
User: "Setup Lighthouse CI for performance testing"

Claude (Phase 1: Install Dependencies - 0-5k tokens):
1. Install Lighthouse CI:
   Bash: pnpm add -D @lhci/cli

Claude (Phase 2: Create Config - 5-15k tokens):
2. Create Lighthouse CI configuration:
   Write lighthouserc.json
   ```json
   {
     "ci": {
       "collect": {
         "startServerCommand": "pnpm start",
         "url": ["http://localhost:3000/"],
         "numberOfRuns": 3
       },
       "assert": {
         "assertions": {
           "categories:performance": ["error", { "minScore": 0.9 }],
           "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
           "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
         }
       }
     }
   }
   ```

Claude (Phase 3: Create GitHub Actions Workflow - 15-30k tokens):
3. Create GitHub Actions workflow:
   Write .github/workflows/lighthouse-ci.yml
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
           run: pnpm dlx @lhci/cli@0.15.x autorun
   ```

4. Test Lighthouse CI locally:
   Bash: pnpm build
   Bash: pnpm dlx @lhci/cli autorun

5. Commit and push:
   Bash: git add lighthouserc.json .github/workflows/lighthouse-ci.yml && git commit -m "feat: Add Lighthouse CI" && git push

Claude (response to user):
"✅ Lighthouse CI configured!

**Configuration**:
- lighthouserc.json: Performance budgets (LCP ≤2.5s, CLS ≤0.1)
- .github/workflows/lighthouse-ci.yml: GitHub Actions workflow

**Performance budgets**:
- Performance score: ≥90
- LCP: ≤2.5 seconds
- CLS: ≤0.1

**Testing**:
- Local: pnpm dlx @lhci/cli autorun
- CI: Runs on every push/PR

**Result**: CI fails if performance regresses"

Result: Lighthouse CI automated, performance budgets enforced
```

---

## Claude-Specific Tips

### Tip 1: Always Measure Before and After with Bash

**Pattern**:
```markdown
# Before optimization:
Bash: npx lighthouse http://localhost:3000 --view
# Note LCP score (e.g., 3.2s)

# Apply optimization:
Write components/ui/optimized-image.tsx
Edit app/page.tsx

# After optimization:
Bash: npx lighthouse http://localhost:3000 --view
# Verify LCP improved (e.g., 2.1s)
```

**Why**: Data-driven optimization, verify impact

---

### Tip 2: Use Bash to Run Bundle Analyzer Before Code Splitting

**Pattern**:
```markdown
# Before code splitting:
Bash: ANALYZE=true pnpm build
# Identify large modules from treemap

# Then apply code splitting:
Edit app/dashboard/page.tsx
# Lazy load heavy components

# After code splitting:
Bash: ANALYZE=true pnpm build
# Verify bundle size reduced
```

**Why**: Identify optimization targets before splitting

---

### Tip 3: Read Existing Config Before Editing

**Pattern**:
```markdown
# Before editing next.config:
Read next.config.ts
# Check existing structure

# Then edit:
Edit next.config.ts
# Add image optimization
```

**Why**: Preserve existing configuration, avoid breaking changes

---

### Tip 4: Test Locally Before Committing Lighthouse CI

**Pattern**:
```markdown
# After creating lighthouserc.json:
Bash: pnpm build
Bash: pnpm dlx @lhci/cli autorun

# Verify assertions pass
# Then commit
```

**Why**: Catch configuration errors before CI

---

### Tip 5: Use Write for New Optimization Components

**Pattern**:
```markdown
# New OptimizedImage component → Use Write:
Write components/ui/optimized-image.tsx
# Full component implementation

# Update existing page → Use Edit:
Edit app/page.tsx
# Replace img with OptimizedImage
```

**Why**: Write for new files, Edit for targeted changes

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Adding priority={true} to LCP Image

**Problem**: Optimize images but miss priority prop

**Fix**: Add priority={true}
```markdown
# ❌ BAD: Missing priority
Edit app/page.tsx
# <OptimizedImage src="/hero.jpg" alt="Hero" width={1920} height={1080} />

# ✅ GOOD: Add priority
Edit app/page.tsx
# <OptimizedImage src="/hero.jpg" alt="Hero" width={1920} height={1080} priority={true} />
```

**Why**: LCP image must be preloaded

---

### Pitfall 2: Forgetting Suspense Boundary with React.lazy

**Problem**: Add lazy import without Suspense

**Fix**: Wrap with Suspense
```markdown
# ❌ BAD: No Suspense
Edit app/dashboard/page.tsx
# const HeavyChart = lazy(() => import('@/components/heavy-chart'))
# <HeavyChart />

# ✅ GOOD: Wrap with Suspense
Edit app/dashboard/page.tsx
# <Suspense fallback={<div>Loading...</div>}><HeavyChart /></Suspense>
```

**Why**: React.lazy requires Suspense boundary

---

### Pitfall 3: Not Running Lighthouse After Optimization

**Problem**: Apply optimization but don't verify impact

**Fix**: Measure before and after
```markdown
# After optimization:
Bash: npx lighthouse http://localhost:3000 --view

# Verify:
# - LCP improved
# - Bundle size reduced
# - Performance score increased
```

**Why**: Verify optimization actually improved metrics

---

### Pitfall 4: Not Testing Lighthouse CI Locally

**Problem**: Commit lighthouserc.json without testing

**Fix**: Test locally first
```markdown
# Before commit:
Bash: pnpm build
Bash: pnpm dlx @lhci/cli autorun

# Verify assertions pass
# Then commit
```

**Why**: Catch configuration errors before CI fails

---

### Pitfall 5: Using Edit Instead of Bash for Bundle Analyzer

**Problem**: Try to manually analyze bundle

**Fix**: Use Bash to run analyzer
```markdown
# ❌ BAD: Manually inspect build output
Read .next/build-manifest.json

# ✅ GOOD: Use bundle analyzer
Bash: ANALYZE=true pnpm build
# Opens visual treemap
```

**Why**: Analyzer provides visual treemap, easier to understand

---

## Support & Resources

**SAP-025 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic React performance workflows
- [Capability Charter](capability-charter.md) - React performance problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [Web Vitals](https://web.dev/vitals/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)
- [Next.js Image Optimization](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [React.lazy](https://react.dev/reference/react/lazy)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-024 (react-styling)](../react-styling/) - Styling strategies

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-025
  - 3 workflows: Optimizing Images with Write/Edit, Implementing Code Splitting with Write, Setting up Lighthouse CI with Write/Bash
  - Tool patterns: Bash for testing and measurement, Write for optimization components, Edit for configuration updates, Read for existing code
  - 5 Claude-specific tips: Measure before and after with Bash, use Bash for bundle analyzer, read existing config before editing, test locally before committing Lighthouse CI, use Write for new components
  - 5 common pitfalls: Not adding priority to LCP image, forgetting Suspense boundary, not running Lighthouse after optimization, not testing Lighthouse CI locally, using Edit for bundle analyzer
  - Focus on Core Web Vitals (LCP, INP, CLS) and measurement-driven optimization

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic React performance workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Measure: `npx lighthouse http://localhost:3000 --view`
