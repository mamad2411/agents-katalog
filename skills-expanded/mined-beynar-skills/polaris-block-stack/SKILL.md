---
name: polaris-block-stack
description: Shopify Polaris BlockStack component. Use to display children vertically with full width by default. Based on CSS Flexbox for flexible layouts.
---

# BlockStack

## When to use
Use to stack elements vertically with consistent spacing. Common for form fields, content sections, and vertical arrangements. Based on CSS Flexbox.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | Child elements to stack |
| as | 'div' \| 'span' \| 'ul' \| 'ol' \| 'li' \| 'fieldset' | 'div' | HTML element type |
| gap | SpaceScale \| ResponsiveSpaceScale | - | Vertical space between children |
| align | 'start' \| 'center' \| 'end' \| 'space-around' \| 'space-between' \| 'space-evenly' | - | Vertical alignment |
| inlineAlign | 'start' \| 'center' \| 'end' \| 'baseline' \| 'stretch' | - | Horizontal alignment |
| id | string | - | HTML id attribute |
| reverseOrder | boolean | false | Reverse render order |
| role | any | - | ARIA role |

## Examples

```jsx
import { BlockStack } from '@shopify/polaris';

// Basic vertical stack
<BlockStack gap="400">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</BlockStack>

// Form fields with spacing
<BlockStack gap="500">
  <TextField label="Name" />
  <TextField label="Email" />
  <TextField label="Phone" />
</BlockStack>

// Center aligned
<BlockStack align="center" gap="300">
  <div>Centered item 1</div>
  <div>Centered item 2</div>
</BlockStack>

// Space between
<BlockStack align="space-between" gap="500">
  <div>Top</div>
  <div>Bottom</div>
</BlockStack>

// Responsive gap
<BlockStack gap={{ xs: '200', md: '400', lg: '600' }}>
  <div>Item 1</div>
  <div>Item 2</div>
</BlockStack>

// Full width stretch with centered content
<BlockStack inlineAlign="center">
  <div>Horizontally centered</div>
</BlockStack>

// List semantic
<BlockStack as="ul" gap="300">
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</BlockStack>

// Reverse order
<BlockStack reverseOrder>
  <div>Appears second</div>
  <div>Appears first</div>
</BlockStack>
```

## Best practices

- Not for complex or unique component arrangements
- Not for large-scale page layout (use Layout component instead)
- Use for consistent vertical spacing in simple arrangements
- Combine with responsive gap for mobile-friendly layouts
- Use semantic HTML element (ul/ol for lists, fieldset for form groups)
- Consider InlineStack for horizontal arrangements

## Props guidance

**align**: vertical alignment (CSS flex justify-content)
- `start`: top alignment
- `center`: center alignment
- `end`: bottom alignment
- `space-between`: first at top, last at bottom
- `space-around`: equal space around items
- `space-evenly`: equal space between all items

**inlineAlign**: horizontal alignment (CSS flex align-items)
- `start`: left alignment
- `center`: center alignment
- `end`: right alignment
- `baseline`: baseline alignment
- `stretch`: full width

## Related components

- [InlineStack](../inline-stack) - horizontal layout
- [Layout](../layout) - page-level layout
- [FormLayout](../form-layout) - form field arrangement
