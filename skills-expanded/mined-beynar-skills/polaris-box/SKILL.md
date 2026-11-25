---
name: polaris-box
description: Shopify Polaris Box component. Primitive layout component for accessing Polaris design tokens. Use for custom spacing, colors, borders, shadows, positioning.
---

# Box

## When to use
Use as the most primitive layout component to access Polaris design tokens. Build custom layouts with spacing, colors, borders, shadows, and positioning. Alternative to Card for simpler needs.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | Content |
| as | 'div' \| 'span' \| 'section' \| 'legend' \| 'ul' \| 'li' | 'div' | HTML element |
| background | ColorBackgroundAlias | - | Background color token |
| color | ColorTextAlias | - | Text color token |
| borderColor | ColorBorderAlias \| 'transparent' | - | Border color token |
| borderStyle | 'solid' \| 'dashed' | - | Border style |
| borderWidth | BorderWidthScale | - | Border width |
| borderRadius | BorderRadiusAliasOrScale | - | Corner radius |
| padding | SpaceScale \| ResponsiveSpaceScale | - | All-around padding |
| paddingBlock | SpaceScale \| ResponsiveSpaceScale | - | Top and bottom padding |
| paddingBlockStart | SpaceScale \| ResponsiveSpaceScale | - | Top padding |
| paddingBlockEnd | SpaceScale \| ResponsiveSpaceScale | - | Bottom padding |
| paddingInline | SpaceScale \| ResponsiveSpaceScale | - | Left and right padding |
| paddingInlineStart | SpaceScale \| ResponsiveSpaceScale | - | Left padding |
| paddingInlineEnd | SpaceScale \| ResponsiveSpaceScale | - | Right padding |
| shadow | ShadowAliasOrScale | - | Box shadow |
| width | string | - | Width |
| minWidth | string | - | Minimum width |
| maxWidth | string | - | Maximum width |
| minHeight | string | - | Minimum height |
| overflowX | 'hidden' \| 'scroll' \| 'clip' | - | Horizontal overflow |
| overflowY | 'hidden' \| 'scroll' \| 'clip' | - | Vertical overflow |
| position | 'relative' \| 'absolute' \| 'fixed' \| 'sticky' | - | Position type |
| insetBlockStart | SpaceScale \| ResponsiveSpaceScale | - | Top position |
| insetBlockEnd | SpaceScale \| ResponsiveSpaceScale | - | Bottom position |
| insetInlineStart | SpaceScale \| ResponsiveSpaceScale | - | Left position |
| insetInlineEnd | SpaceScale \| ResponsiveSpaceScale | - | Right position |
| zIndex | string | - | Z-index stacking |
| opacity | string | - | Opacity value |
| visuallyHidden | boolean | - | Hide visually (screen readers see) |
| printHidden | boolean | - | Hide on print |
| id | string | - | HTML id |
| tabIndex | any | - | Tab order |

## Examples

```jsx
import { Box, Text } from '@shopify/polaris';

// Background color
<Box background="bg-fill-info">
  <Text>Highlighted content</Text>
</Box>

// With padding and border
<Box
  padding="400"
  borderColor="border"
  borderWidth="025"
  borderRadius="200"
>
  <Text>Bordered box</Text>
</Box>

// With shadow
<Box padding="400" shadow="md">
  <Text>Elevated content</Text>
</Box>

// Responsive padding
<Box padding={{ xs: '200', md: '400', lg: '600' }}>
  <Text>Responsive padding</Text>
</Box>

// Directional padding
<Box paddingInline="400" paddingBlock="300">
  <Text>Custom padding</Text>
</Box>

// Positioned absolutely
<Box position="absolute" insetBlockStart="300" insetInlineStart="300">
  <Text>Positioned</Text>
</Box>

// Overflow control
<Box maxWidth="400px" overflowX="scroll">
  Long scrollable content...
</Box>

// Custom width/height with background
<Box
  width="100%"
  minHeight="200px"
  background="bg-fill-success"
>
  Content area
</Box>

// Semantically section
<Box as="section" background="bg-surface-secondary" padding="500">
  <Text as="h2">Section title</Text>
</Box>

// Visually hidden but accessible
<Box visuallyHidden>
  Extra context for screen readers
</Box>
```

## Best practices

- Use for simple layout needs - consider Card for more structured layouts
- Use design tokens from Polaris system (not custom values)
- Combine props for complex layouts
- Use responsive props for mobile-first design
- Use semantic HTML element (section, ul, li) via `as` prop
- Use visuallyHidden for accessibility needs, not display: none

## Design tokens

**Colors**: bg-fill-info, bg-fill-success, bg-fill-critical, bg-fill-warning, bg-surface, bg-surface-secondary, etc.

**Spacing**: 100, 200, 300, 400, 500, 600, 700, 800, 900

**Shadow**: sm, md, lg

**Border radius**: 100, 200, 300, 400, full

## Related components

- [Card](../card) - structured container with header, sections, footer
- [BlockStack](../block-stack) - vertical flex layout
- [InlineStack](../inline-stack) - horizontal flex layout
