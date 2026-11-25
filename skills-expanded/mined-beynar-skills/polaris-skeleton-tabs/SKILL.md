---
name: polaris-skeleton-tabs
description: Shopify Polaris Skeleton tabs component. Use for low fidelity tab representation. Shows placeholder for tab navigation during load.
---

# Skeleton Tabs

## When to use
Provide low fidelity representation of tabbed content during load. Improve perceived load times. Use with SkeletonPage and other skeleton components.

## Props
- `count?` number - Number of tab skeletons to display
- `fitted?` boolean - Fit tabs to container

## Examples
```jsx
import { Card, SkeletonTabs } from '@shopify/polaris';

// Basic
<Card>
  <SkeletonTabs />
</Card>

// Custom count
<Card>
  <SkeletonTabs count={5} />
</Card>

// Fitted to container
<Card>
  <SkeletonTabs fitted />
</Card>
```

## Best practices
- Give indication of page content once loaded
- Use with SkeletonPage for full layout
- Combine with other skeleton components

## Accessibility
- Provides visual indication of loading state

## Related components
- SkeletonPage (full page layouts)
- SkeletonBodyText (content blocks)
- SkeletonDisplayText (headings)
