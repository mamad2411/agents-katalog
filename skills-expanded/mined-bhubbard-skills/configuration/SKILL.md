---
name: configuration
description: Configure Unlighthouse using unlighthouse.config.ts. Use this skill when the user needs to customize scan rules, budgets, URLs to ignore, or other advanced settings.
---

# Unlighthouse Configuration

Unlighthouse can be configured using an `unlighthouse.config.ts` (or `.js`) file in the root of your project.

## Basic Configuration Example

```typescript
// unlighthouse.config.ts
export default {
  // The base URL to scan
  site: 'https://example.com',
  
  // Customizing the scanner
  scanner: {
    // Ignore specific routes
    exclude: ['/admin/*', '/login'],
    
    // Simulate mobile or desktop
    device: 'mobile', // 'mobile' or 'desktop'
  },
  
  // Lighthouse specific options
  puppeteerOptions: {
    headless: true,
  },
  
  // Enforcing budgets (useful for CI)
  ci: {
    budget: {
      performance: 90,
      accessibility: 100,
      bestPractices: 90,
      seo: 100,
    }
  }
}
```

## Best Practices
- Always exclude dynamic or authenticated routes unless you are specifically configuring puppeteer to handle authentication.
- Set realistic budgets for your CI pipeline so that developers are not blocked by minor fluctuations in Lighthouse scores.
