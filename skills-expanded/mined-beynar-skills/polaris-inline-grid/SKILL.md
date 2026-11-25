---
name: polaris-inline-grid
description: Shopify Polaris InlineGrid component. Use to create flexible inline grid layouts with CSS Grid for product cards, thumbnails, and compact multi-column arrangements.
---

# InlineGrid

## When to use
Use to create compact multi-column grid layouts that wrap responsively. Ideal for product thumbnails, image galleries, tag displays, and compact card arrangements.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Grid items |
| columns | number \| ResponsiveValue | - | Number of columns |
| gap | SpaceScale \| ResponsiveSpaceScale | - | Space between items |
| alignItems | 'start' \| 'center' \| 'end' \| 'stretch' | - | Vertical alignment |
| justifyItems | 'start' \| 'center' \| 'end' \| 'stretch' | - | Horizontal alignment |

## Examples

```jsx
import { InlineGrid, Card, Text, Thumbnail } from '@shopify/polaris';

// Two column product grid
<InlineGrid columns={2} gap="400">
  <Card>
    <img alt="Product 1" src="..." />
    <Box padding="400">
      <Text>Product A</Text>
    </Box>
  </Card>
  <Card>
    <img alt="Product 2" src="..." />
    <Box padding="400">
      <Text>Product B</Text>
    </Box>
  </Card>
</InlineGrid>

// Responsive columns
<InlineGrid
  columns={{ xs: 2, md: 3, lg: 4 }}
  gap={{ xs: '200', md: '400' }}
>
  {/* Product items */}
</InlineGrid>

// Thumbnail gallery
<InlineGrid columns={6} gap="200">
  <img alt="Thumb 1" src="..." width="60" height="60" />
  <img alt="Thumb 2" src="..." width="60" height="60" />
  <img alt="Thumb 3" src="..." width="60" height="60" />
  {/* More thumbnails */}
</InlineGrid>

// Centered items
<InlineGrid
  columns={3}
  gap="300"
  alignItems="center"
  justifyItems="center"
>
  <Badge>Tag 1</Badge>
  <Badge>Tag 2</Badge>
  <Badge>Tag 3</Badge>
</InlineGrid>

// Product card grid with varied sizes
<InlineGrid columns={{ xs: 2, md: 3 }} gap="400">
  <Card>
    <Box background="bg-surface-secondary" minHeight="200px">
      {/* Image */}
    </Box>
    <Box padding="300">
      <Text variant="headingSm">Product</Text>
      <Text tone="subdued" variant="bodySm">$99.99</Text>
    </Box>
  </Card>
  {/* More product cards */}
</InlineGrid>

// List of variant options
<InlineGrid columns={4} gap="200">
  <Box
    padding="300"
    borderColor="border"
    borderWidth="025"
    borderRadius="200"
    textAlign="center"
  >
    <Text>Red</Text>
  </Box>
  <Box padding="300" borderColor="border" borderWidth="025" borderRadius="200">
    <Text>Blue</Text>
  </Box>
  {/* More options */}
</InlineGrid>

// Image mosaic
<InlineGrid columns={{ xs: 2, md: 4 }} gap="200">
  <img alt="1" src="..." style={{ width: '100%' }} />
  <img alt="2" src="..." style={{ width: '100%' }} />
  <img alt="3" src="..." style={{ width: '100%' }} />
  <img alt="4" src="..." style={{ width: '100%' }} />
</InlineGrid>
```

## Responsive columns

```jsx
// Mobile: 2, Tablet: 3, Desktop: 4
columns={{ xs: 2, md: 3, lg: 4 }}

// Mobile: 1, Desktop: 2
columns={{ xs: 1, md: 2 }}

// Fixed 3 columns
columns={3}
```

## Spacing options

Common gap values:
- `100` - extra tight
- `200` - tight
- `300` - moderate
- `400` - loose
- `500` - extra loose

Use responsive gaps:
```jsx
gap={{ xs: '200', md: '300', lg: '400' }}
```

## Best practices

- Use for compact arrangements
- Define responsive column counts
- Keep gaps consistent
- Pair with cards for content cards
- Use for image galleries
- Consider mobile (fewer columns on small screens)
- Align items for consistency
- Use for product thumbnails and variations

## When to use InlineGrid vs Grid

**InlineGrid**:
- Compact inline arrangements
- Product cards, thumbnails
- Tag/badge displays
- Simple multi-column layouts

**Grid**:
- Page-level layouts
- Complex responsive patterns
- Combine one/two/three column layouts
- Detailed column span control

## Related components

- [Grid](../grid) - complex page layouts
- [Card](../card) - item containers
- [BlockStack](../block-stack) - vertical stacking
- [InlineStack](../inline-stack) - horizontal stacking
