---
name: polaris-thumbnail
description: Shopify Polaris Thumbnail component. Use as visual anchor and identifier for objects like products. Pair with text for context.
---

# Thumbnail

## When to use
Use thumbnails as visual anchors and identifiers for objects. Always pair with text to provide context. Show a small visual preview of products, files, or other objects.

## Props
- `size?` 'extraSmall' | 'small' | 'medium' | 'large' - Thumbnail size. Defaults to 'medium'.
  - Extra small (24x24): tightly condensed layouts
  - Small (40x40): when medium is too large
  - Medium (60x60): default size
  - Large (80x80): major focal point (avoid in lists)
- `source` any - URL for the image
- `alt` string - Alt text for the thumbnail image
- `transparent?` boolean - Transparent background. Defaults to false.

## Examples
```jsx
import { Thumbnail } from '@shopify/polaris';

// Basic
<Thumbnail
  source="https://burst.shopifycdn.com/photos/black-leather-choker.jpg"
  alt="Black choker necklace"
/>

// Extra small
<Thumbnail
  size="extraSmall"
  source="https://example.com/image.jpg"
  alt="Product thumbnail"
/>

// Large (focal point)
<Thumbnail
  size="large"
  source="https://example.com/image.jpg"
  alt="Featured product"
/>
```

## Best practices
- Use appropriate size: xs for condensed, sm for secondary, md as default, lg for focal points only
- Always include descriptive alt text: "Photo of {product}"
- Use empty alt="" only for decorative thumbnails
- Avoid large size in lists of similar items
- Match aspect ratio needs: typically square or 16:9

## Accessibility
- Use descriptive alt text describing the content
- Format: "Photo of {product}" (e.g., "Photo of black t-shirt")
- Empty alt="" ignores image in screen readers (decorative only)
- Include object description, not "image" or "thumbnail"

## Related components
- Avatar (for people/business representations)
