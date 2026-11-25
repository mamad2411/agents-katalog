---
name: polaris-divider
description: Shopify Polaris Divider component. Use to separate or group content visually with a line separator.
---

# Divider

## When to use
Use to separate sections or group related content. Simple horizontal line separator between content blocks.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| borderColor | ColorBorderAlias \| 'transparent' | 'border-secondary' | Border color token |
| borderWidth | BorderWidthScale | '025' | Border width |

## Examples

```jsx
import { Card, Divider, Text, BlockStack } from '@shopify/polaris';

// Default divider
<Card>
  <BlockStack gap="500">
    <Text as="h1" variant="headingSm">Section 1</Text>
    <Divider />
    <Text as="h1" variant="headingSm">Section 2</Text>
  </BlockStack>
</Card>

// With custom border color
<BlockStack gap="400">
  <Text>Default</Text>
  <Divider />

  <Text>Border color</Text>
  <Divider borderColor="border" />

  <Text>Inverse</Text>
  <Divider borderColor="border-inverse" />

  <Text>Transparent</Text>
  <Divider borderColor="transparent" />
</BlockStack>

// With border width
<Card>
  <Text>Content above</Text>
  <Divider borderWidth="100" />
  <Text>Content below</Text>
</Card>

// Separating card sections
<Card>
  <BlockStack>
    <Box padding="400">
      <Text variant="headingMd">Header</Text>
    </Box>
    <Divider />
    <Box padding="400">
      Main content
    </Box>
    <Divider />
    <Box padding="400">
      Footer with action
    </Box>
  </BlockStack>
</Card>
```

## Best practices

- Use to separate visually related sections
- Use within BlockStack for consistent spacing
- Choose appropriate border color for contrast
- Avoid overusing - too many dividers clutter layout
- Works well in cards and page sections

## Border colors

Common color tokens:
- `border-secondary` (default) - standard separation
- `border` - stronger contrast
- `border-inverse` - on dark backgrounds
- `transparent` - spacing without visual line

## Related components

- [Card](../card) - container for sections
- [BlockStack](../block-stack) - vertical layout with dividers
- [Box](../box) - for custom separators
