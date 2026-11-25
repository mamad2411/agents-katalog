---
name: polaris-inline-stack
description: Shopify Polaris InlineStack component. Use to display children horizontally with flexible spacing. CSS Flexbox-based layout for horizontal arrangements.
---

# InlineStack

## When to use
Use to arrange elements horizontally with consistent spacing. Complement to BlockStack for left-to-right or right-to-left layouts. Responsive and mobile-friendly.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | Child elements to arrange horizontally |
| as | 'div' \| 'span' \| 'ul' \| 'ol' \| 'li' | 'div' | HTML element type |
| gap | SpaceScale \| ResponsiveSpaceScale | - | Horizontal space between children |
| align | 'start' \| 'center' \| 'end' \| 'space-around' \| 'space-between' \| 'space-evenly' | - | Vertical alignment of items |
| blockAlign | 'start' \| 'center' \| 'end' \| 'baseline' \| 'stretch' | - | Horizontal alignment |
| id | string | - | HTML id attribute |
| reverseOrder | boolean | false | Reverse render order |
| role | any | - | ARIA role |
| wrap | boolean | true | Allow wrapping on mobile |

## Examples

```jsx
import { InlineStack, Button, Badge, Text } from '@shopify/polaris';

// Basic inline arrangement
<InlineStack gap="400">
  <Button>Cancel</Button>
  <Button variant="primary">Save</Button>
</InlineStack>

// Status with badge
<InlineStack gap="200" align="center">
  <Text>Order status</Text>
  <Badge tone="success">Fulfilled</Badge>
</InlineStack>

// Distributed spacing
<InlineStack gap="400" align="space-between">
  <Text variant="headingMd">Products</Text>
  <Button>Add product</Button>
</InlineStack>

// Centered items
<InlineStack gap="300" align="center" blockAlign="center">
  <Icon />
  <Text>Processing payment...</Text>
</InlineStack>

// Responsive gap
<InlineStack gap={{ xs: '200', md: '400', lg: '600' }}>
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</InlineStack>

// No wrap (horizontal scroll on mobile)
<InlineStack gap="300" wrap={false}>
  <Badge>Tag 1</Badge>
  <Badge>Tag 2</Badge>
  <Badge>Tag 3</Badge>
</InlineStack>

// List of items
<InlineStack as="ul" gap="200">
  <li>Home</li>
  <li>Products</li>
  <li>Settings</li>
</InlineStack>

// Icons and text
<InlineStack gap="200" blockAlign="center">
  <CheckIcon />
  <Text>Complete</Text>
</InlineStack>

// Reverse order
<InlineStack reverseOrder>
  <div>Second</div>
  <div>First</div>
</InlineStack>
```

## Alignment details

**align** (vertical positioning, CSS justify-content):
- `start`: align items to left/start edge
- `center`: center items vertically
- `end`: align items to right/end edge
- `space-between`: first at left, last at right
- `space-around`: equal space around each item
- `space-evenly`: equal space between all items

**blockAlign** (horizontal positioning, CSS align-items):
- `start`: top alignment
- `center`: middle alignment
- `end`: bottom alignment
- `baseline`: baseline alignment (text-based)
- `stretch`: full height

## Best practices

- Use for related horizontal actions (buttons, tags)
- Consider mobile wrapping behavior
- Use responsive gap for better mobile layouts
- Combine with BlockStack for 2D layouts
- Use semantic HTML (ul/ol for lists)
- Don't nest too deeply
- Keep items minimal on mobile

## When to use wrap

- `wrap={true}` (default): items wrap to next line on mobile
- `wrap={false}`: items stay in row with horizontal scroll

## Related components

- [BlockStack](../block-stack) - vertical layout
- [ButtonGroup](../button-group) - specific button arrangement
- [FormLayout](../form-layout) - form field arrangement
- [Box](../box) - primitive layout
