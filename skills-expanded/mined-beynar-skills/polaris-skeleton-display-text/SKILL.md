---
name: polaris-skeleton-display-text
description: Shopify Polaris Skeleton display text component. Use for loading display/heading text. Shows placeholder for page titles and large metrics.
---

# Skeleton Display Text

## When to use
Provide low fidelity representation for display text before appearing. Improve perceived load times. Use for page titles, large metrics, and section headings.

## Props
- `size?` 'small' | 'medium' | 'large' | 'extraLarge' - Text size. Defaults to 'medium'.
- `maxWidth?` `${number}ch` | `${number}%` - Maximum width of text. Defaults to '120px'.

## Examples
```jsx
import { SkeletonDisplayText } from '@shopify/polaris';

// Medium (default)
<SkeletonDisplayText size="medium" />

// Large (page titles)
<SkeletonDisplayText size="large" />

// Extra large
<SkeletonDisplayText size="extraLarge" />

// Small
<SkeletonDisplayText size="small" />

// Custom width
<SkeletonDisplayText size="medium" maxWidth="200px" />
```

## Best practices
- Give indication of page layout once loaded
- Use real content for display text that never changes
- Use skeleton for dynamic display text only

## Content guidelines
- Show static display text (e.g., "Products" on product list)
- Use skeleton for dynamic titles (product detail page)
- Don't use placeholder content for dynamic text

## Accessibility
- Provides visual indication of loading state

## Related components
- SkeletonPage (full page layouts)
- SkeletonBodyText (body content)
- ProgressBar / Spinner (in-context operations)
