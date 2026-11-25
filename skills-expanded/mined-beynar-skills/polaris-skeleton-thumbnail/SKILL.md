---
name: polaris-skeleton-thumbnail
description: Shopify Polaris Skeleton thumbnail component. Use for low fidelity image representation. Shows placeholder for thumbnails during load.
---

# Skeleton Thumbnail

## When to use
Provide low fidelity representation of images before loading. Improve perceived load times. Use for thumbnails in and outside cards.

## Props
- `size?` 'extraSmall' | 'small' | 'medium' | 'large' - Thumbnail size. Defaults to 'medium'.

## Examples
```jsx
import { SkeletonThumbnail } from '@shopify/polaris';

// Medium (default)
<SkeletonThumbnail size="medium" />

// Extra small
<SkeletonThumbnail size="extraSmall" />

// Large
<SkeletonThumbnail size="large" />

// With display text
import { SkeletonDisplayText } from '@shopify/polaris';
<div>
  <SkeletonThumbnail />
  <SkeletonDisplayText size="small" />
</div>
```

## Best practices
- Match size to actual thumbnail for accuracy
- Pair with SkeletonDisplayText for card content
- Use for product images, file thumbnails

## Accessibility
- Provides visual indication of loading state

## Related components
- SkeletonDisplayText (text alongside images)
- Thumbnail (actual image component)
