---
name: polaris-icon
description: Shopify Polaris Icon component. Use for visually communicating core product parts and available actions. Import from @shopify/polaris-icons.
---

# Icon

## When to use
Visually communicate core product parts and available actions. Use icons as wayfinding tools to help merchants understand location and interaction patterns.

## Props
- `source` any - SVG contents (must fit 20x20 pixel viewBox)
- `tone?` 'base' | 'inherit' | 'subdued' | 'caution' | 'warning' | 'critical' | 'interactive' | 'info' | 'success' | 'primary' | 'emphasis' | 'magic' | 'textCaution' | 'textWarning' | 'textCritical' | 'textInfo' | 'textSuccess' | 'textPrimary' | 'textMagic' - Icon color. Defaults to 'base'.
- `accessibilityLabel?` string - Text read by screen readers

## Examples
```jsx
import { Icon } from '@shopify/polaris';
import { PlusCircleIcon } from '@shopify/polaris-icons';

// Basic icon
<Icon source={PlusCircleIcon} />

// With tone
<Icon source={PlusCircleIcon} tone="critical" />

// With accessibility label
<Icon source={PlusCircleIcon} accessibilityLabel="Add item" />

// Pair with text
<Icon source={OrderIcon} />
<p>No orders yet</p>
```

## Best practices
- Pair text and icons for clarity
- Give icons text equivalents if purpose isn't clear
- Use consistent 20x20 pixel SVGs
- Refer to @shopify/polaris-icons documentation for icon availability

## Accessibility
- SVGs conveyed inconsistently to assistive tech
- Use accessibilityLabel for icon-only usage
- Don't describe what icon looks like in label
- Don't include "icon" in accessibility label
- Don't duplicate adjacent text in alt text

## Related components
- See @shopify/polaris-icons documentation
- Icon design guidelines available in Polaris documentation
