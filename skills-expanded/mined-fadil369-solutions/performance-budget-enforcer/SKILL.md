---
name: "Performance Budget Enforcer"
version: "1.0.0"
description: "Enforces performance budgets for bundle size, load time, memory usage, and API response times. Integrates with CI/CD."
author: "workspace"
activated: false
---

# Performance Budget Enforcer

Enforces performance budgets for bundle size, load time, memory usage, and API response times. Integrates with CI/CD.

## Decision Framework

### When to Apply
Use when: Performance is critical, CI/CD integration needed, bundle size growing, slow page loads

### When NOT to Apply
Don't use when: Performance is not a concern (rare), simple scripts

## Anti-Patterns

### 1. Loading Everything Upfront
```javascript
// BAD: Import everything
import { every, feature, known } from './massive-library';

// GOOD: Lazy load
const Feature = lazy(() => import('./Feature'));
```

### 2. No Performance Monitoring
You can't improve what you don't measure.


## Trigger Phrases

- "Performance budget"
- "Bundle size"
- "Load time optimization"
- "Lighthouse score"
- "Core Web Vitals"

## Patterns

### Bundle Budget
```javascript
// webpack.config.js
module.exports = {
  performance: {
    maxAssetSize: 250000,      // 250KB per asset
    maxEntrypointSize: 400000, // 400KB total entry
    hints: 'error'
  }
};
```

### Performance Monitor
```javascript
class PerformanceBudget {
  constructor(budgets) { this.budgets = budgets; }

  check(metrics) {
    const violations = [];
    for (const [metric, budget] of Object.entries(this.budgets)) {
      if (metrics[metric] > budget.max) {
        violations.push({ metric, actual: metrics[metric], budget: budget.max, over: metrics[metric] - budget.max });
      }
    }
    return { passed: violations.length === 0, violations };
  }
}

const budgets = {
  fcp: { max: 1800, name: 'First Contentful Paint' },
  lcp: { max: 2500, name: 'Largest Contentful Paint' },
  tti: { max: 3800, name: 'Time to Interactive' },
  cls: { max: 0.1, name: 'Cumulative Layout Shift' },
  bundleSize: { max: 250000, name: 'Bundle Size' }
};
```

## Integration
- Works with: deployment-pipeline-architect, dashboard-composition-engine

