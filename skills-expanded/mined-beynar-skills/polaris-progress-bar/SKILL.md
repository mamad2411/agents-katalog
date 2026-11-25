---
name: polaris-progress-bar
description: Shopify Polaris Progress bar component. Use to visually represent task/operation completion. Shows progress and remaining work.
---

# Progress Bar

## When to use
Visually represent task or operation completion. Show how much is complete and how much remains. Use for operations with measurable progress.

## Props
- `progress?` number - Progression percentage. Defaults to 0.
- `size?` 'small' | 'medium' | 'large' - Bar size. Defaults to 'medium'.
- `animated?` boolean - Whether fill animation triggers. Defaults to true.
- `ariaLabelledBy?` string - ID(s) of elements describing progress bar
- `tone?` 'highlight' | 'primary' | 'success' | 'critical' - Bar color. Defaults to 'highlight'.

## Examples
```jsx
import { ProgressBar } from '@shopify/polaris';

// Basic (75% complete)
<div style={{ width: 225 }}>
  <ProgressBar progress={75} />
</div>

// Small with custom tone
<ProgressBar progress={50} size="small" tone="success" />

// Non-animated
<ProgressBar progress={33} animated={false} />

// Large with critical tone
<ProgressBar progress={90} size="large" tone="critical" />
```

## Best practices
- Give indication of task completion and remaining
- Not for entire page loads (use SkeletonPage)
- Suitable for file uploads, data processing, imports

## Accessibility
- Use ariaLabelledBy to describe what's being measured
- Pair with supporting text explaining progress

## Related components
- Spinner (for short load times)
- SkeletonPage (for full page loads)
