---
name: polaris-spinner
description: Shopify Polaris Spinner component. Use to notify merchants that actions are being processed. Shows loading indicator for in-progress operations.
---

# Spinner

## When to use
Notify merchants that requested action is being processed. Use for content that can't be represented with skeleton loading (e.g., data charts). Not for entire page loads.

## Props
- `size?` 'small' | 'large' - Spinner size. Defaults to 'large'.
- `accessibilityLabel?` string - Accessible label for spinner
- `hasFocusableParent?` boolean - Apply correct accessibility roles when parent is focusable

## Examples
```jsx
import { Spinner } from '@shopify/polaris';

// Large (default)
<Spinner accessibilityLabel="Spinner example" size="large" />

// Small
<Spinner accessibilityLabel="Loading" size="small" />

// In button
<Button disabled>
  <Spinner size="small" accessibilityLabel="Submitting" />
  Submit
</Button>

// With focusable parent
<Spinner
  accessibilityLabel="Processing"
  hasFocusableParent
  size="large"
/>
```

## Best practices
- Notify that request received and action completing soon
- Not for entire page loads (use SkeletonPage)
- Small spinner: white only on actionable components (buttons)
- Web: use with skeleton loading for non-typographic content (graphs)

## Accessibility
- SVGs conveyed inconsistently to assistive tech
- Use accessibilityLabel to explain state ("Loading", "Submitting", "Processing")
- Set hasFocusableParent=true when parent component is focusable
- Use few words for accessibility label
- Paired with supporting text explaining operation

## Related components
- ProgressBar (for measurable progress)
- SkeletonPage / SkeletonBodyText / SkeletonDisplayText (for content loading)
