---
description: Run Edge Computing and CDN Standards Check
globs: ['**/edge/**/*.ts', '**/cdn/**/*.ts', 'vercel.json', 'next.config.js', 'cloudflare.yml']
---

# Performance: Edge Computing & CDN Standards

<audit_rules>

- You MUST implement edge functions for compute-intensive operations close to users for reduced latency.
- You MUST configure proper CDN caching strategies with appropriate cache headers and invalidation rules.
- You MUST implement edge-side rendering for dynamic content that benefits from geographic distribution.
- You MUST ensure proper edge runtime compatibility and avoid Node.js-specific APIs in edge functions.
- You MUST implement proper error handling and fallback mechanisms for edge function failures.
- You MUST configure proper edge caching for static assets with version-based cache busting.
- You MUST implement proper edge-side request routing and A/B testing capabilities.
- You MUST ensure proper monitoring and logging for edge functions and CDN performance.
- You MUST implement proper security headers and rate limiting at the edge level.
- You MUST configure proper edge-side personalization and localization based on geographic data.
  </audit_rules>

<example_good>

```typescript
// Edge function for dynamic pricing based on location
import { NextRequest, NextResponse } from 'next/server'
import { getGeolocation } from '@vercel/edge-config'

export const config = {
  runtime: 'edge',
}

export async function middleware(req: NextRequest) {
  const url = req.nextUrl

  // Edge-side geolocation
  const geo = getGeolocation(req)
  const country = geo?.country || 'US'

  // Dynamic pricing based on location
  if (url.pathname.startsWith('/api/pricing')) {
    const response = await fetch(`${url.origin}/api/base-pricing`)
    const basePricing = await response.json()

    const adjustedPricing = adjustPricingForRegion(basePricing, country)

    return NextResponse.json(adjustedPricing, {
      headers: {
        'Cache-Control': 's-maxage=3600, stale-while-revalidate=86400',
        'Edge-Cache-Tag': `pricing-${country}`,
      },
    })
  }

  // Edge-side A/B testing
  const abTestVariant = getABTestVariant(req, geo)
  if (abTestVariant) {
    url.searchParams.set('variant', abTestVariant)
  }

  return NextResponse.rewrite(url)
}

function adjustPricingForRegion(pricing: any, country: string) {
  const multipliers: Record<string, number> = {
    US: 1.0,
    EU: 1.2,
    GB: 1.3,
    JP: 1.1,
  }

  const multiplier = multipliers[country] || 1.0

  return Object.entries(pricing).reduce(
    (acc, [key, value]) => {
      acc[key] = typeof value === 'number' ? value * multiplier : value
      return acc
    },
    {} as typeof pricing
  )
}
```

</example_good>

<example_bad>

```typescript
// BAD: Using Node.js APIs in edge function
export async function middleware(req: Request) {
  // BAD: fs is not available in edge runtime
  const fs = require('fs')
  const config = fs.readFileSync('./config.json')

  // BAD: No caching headers
  return new Response(JSON.stringify(config), {
    headers: { 'Content-Type': 'application/json' },
  })
}

// BAD: No edge optimization, everything runs at origin
export async function getPricing() {
  // This should be edge-optimized for better performance
  const pricing = await fetchFromDatabase()
  return pricing
}
```

</example_bad>
