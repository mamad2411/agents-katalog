---
name: polaris-card
description: Shopify Polaris Card component. Use to group similar concepts and tasks together. Container for visual grouping with flexible composition.
---

# Card

## When to use
Use to visually group related content and actions. Acts as a container for organizing information hierarchically. Build with Box and other primitives for flexible layouts.

## When NOT to use
Don't use LegacyCard - use new Card component with layout primitives instead.

## Props

Card is a flexible container built from primitives. Typical usage:

```jsx
<Card>
  <Box padding="400">
    <Text variant="headingMd">Title</Text>
    <p>Content</p>
  </Box>
</Card>
```

For structured layouts with sections, combine with Box and other components.

## Examples

```jsx
import { Card, Box, Text, BlockStack, Button } from '@shopify/polaris';

// Simple card
<Card>
  <Box padding="400">
    <Text variant="headingMd">Online store</Text>
    <p>View a summary of your store's performance.</p>
  </Box>
</Card>

// Card with sections
<Card>
  <BlockStack>
    <Box padding="400" borderBlockEnd="solid">
      <Text variant="headingMd">Order details</Text>
    </Box>
    <Box padding="400">
      <BlockStack gap="300">
        <div>Item 1</div>
        <div>Item 2</div>
      </BlockStack>
    </Box>
    <Box padding="400" borderBlockStart="solid">
      <Button variant="primary">Complete order</Button>
    </Box>
  </BlockStack>
</Card>

// Card with header and footer
<Card>
  <Box padding="400" background="bg-surface-secondary">
    <Text variant="headingMd">Header section</Text>
  </Box>
  <Box padding="400">
    <p>Main content</p>
  </Box>
  <Box padding="400" background="bg-surface-secondary">
    <Button>Action</Button>
  </Box>
</Card>

// Multiple cards in layout
<BlockStack gap="400">
  <Card>
    <Box padding="400">
      <Text variant="headingMd">Card 1</Text>
    </Box>
  </Card>
  <Card>
    <Box padding="400">
      <Text variant="headingMd">Card 2</Text>
    </Box>
  </Card>
</BlockStack>
```

## Best practices

- Use clear, informative headings
- Prioritize information (important first)
- Group related concepts together
- Limit to one primary action per card
- Use card sections for different content types
- Avoid too many calls to action
- Keep cards focused and scannable
- Use consistent padding and spacing

## Composition approach

Modern Card component expects you to compose sections:

1. Use Box with padding for content areas
2. Use BlockStack/InlineStack for content arrangement
3. Use borderBlock props on Box for dividers
4. Apply background colors via Box for visual sections
5. Include actions at bottom or in header

## Related components

- [Box](../box) - primitive layout
- [BlockStack](../block-stack) - vertical arrangement
- [InlineStack](../inline-stack) - horizontal arrangement
- [Layout](../layout) - page-level layout
- [CalloutCard](../callout-card) - feature promotion
- [MediaCard](../media-card) - with visual media
