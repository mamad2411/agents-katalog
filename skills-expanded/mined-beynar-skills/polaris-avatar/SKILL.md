---
name: polaris-avatar
description: Shopify Polaris Avatar component. Use when displaying a thumbnail representation of a person, customer, or business. Shows initials or image fallback.
---

# Avatar

## When to use
Display a thumbnail representation of an individual or business in the interface. Use avatars to identify merchants, customers, or staff members with initials or images.

## Props
- `size?` 'xs' | 'sm' | 'md' | 'lg' | 'xl' - Avatar size. Defaults to 'md'.
  - Extra small (20x20): tightly condensed layouts
  - Small (24x24): when medium is too big
  - Medium (28x28): default size
  - Large (32x32): focal point on cards
  - Extra large (40x40): primary focal point
- `name?` string - Name of the person
- `initials?` string - Initials to display
- `customer?` boolean - Whether avatar is for a customer
- `source?` string - URL of avatar image (falls back to initials if load fails)
- `onError?` () => void - Callback when image fails to load
- `accessibilityLabel?` string - Accessible label for screen readers

## Examples
```jsx
import { Avatar } from '@shopify/polaris';

// With initials
<Avatar name="Farrah" />

// With customer indicator
<Avatar customer name="Farrah" />

// With image
<Avatar source="https://example.com/avatar.jpg" name="Farrah" />

// Extra small
<Avatar size="xs" name="Farrah" />
```

## Best practices
- Use appropriate size based on layout: xs for condensed, sm for secondary, md as default, lg/xl for focal points
- Include descriptive alt text via accessibilityLabel or name prop
- Always provide either a name or initials

## Accessibility
- Uses SVG with empty alt attribute, replaced with role="img" span for screen readers
- Name prop is used as default alternative text
- Use accessibilityLabel to override if needed
- For avatars next to text, use empty alt="" if name appears as adjacent text

## Related components
- Thumbnail (for objects rather than people)
