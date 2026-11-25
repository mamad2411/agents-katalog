---
name: polaris-badge
description: Shopify Polaris Badge component. Use to inform merchants of tone or status of an object. Display progress states or status indicators.
---

# Badge

## When to use
Inform merchants about the tone or status of an object. Display non-critical status updates. Use for fulfillment/payment status, progress states, or workflow indicators.

## Props
Complex union type supporting either progress or icon:
- `progress?` 'incomplete' | 'partiallyComplete' | 'complete' - Progress state (mutually exclusive with icon)
- `icon?` FunctionComponent | 'placeholder' | string - Icon to display (mutually exclusive with progress)
- Children: text content for badge

## Examples
```jsx
import { Badge, Card } from '@shopify/polaris';

// Default
<Badge>Fulfilled</Badge>

// With progress
<Badge progress="complete">Paid</Badge>
<Badge progress="partiallyComplete">Partially refunded</Badge>
<Badge progress="incomplete">Unfulfilled</Badge>

// Tones
<Badge>Success</Badge>
<Badge>Warning</Badge>
<Badge>Critical</Badge>
```

## Best practices
- Use established color patterns for quick identification
- Use clear, scannable labels (single word preferred)
- Limit to two words for complex states (e.g., "Partially refunded")
- Always describe in past tense ("refunded" not "refund")
- Position clearly to identify the object being labeled

## Financial tone badges
- Authorized, Pending, Paid, Unpaid, Voided, Partially paid, Partially refunded, Refunded

## Fulfillment tone badges
- Fulfilled, Complete, Partial, Unfulfilled, Restocked

## Accessibility
- Badges with icons/color include visually hidden text
- Uses VisuallyHidden component for screen reader access
- Color and icons convey meaning but must have text equivalent

## Related components
- Tag (for interactive categories)
