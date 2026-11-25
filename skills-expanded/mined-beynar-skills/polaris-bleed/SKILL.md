---
name: polaris-bleed
description: Shopify Polaris Bleed component. Use to apply negative margin allowing content to extend beyond surrounding container layout.
---

# Bleed

## When to use
Use to allow content to bleed out into surrounding layout with negative margins. Common for edge-to-edge images in cards or sections.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Content that bleeds out |
| marginInline | SpaceScale \| ResponsiveSpaceScale | - | Negative horizontal space |
| marginBlock | SpaceScale \| ResponsiveSpaceScale | - | Negative vertical space |
| marginBlockStart | SpaceScale \| ResponsiveSpaceScale | - | Negative top space |
| marginBlockEnd | SpaceScale \| ResponsiveSpaceScale | - | Negative bottom space |
| marginInlineStart | SpaceScale \| ResponsiveSpaceScale | - | Negative left space |
| marginInlineEnd | SpaceScale \| ResponsiveSpaceScale | - | Negative right space |

## Examples

```jsx
import { Bleed, Card, Text } from '@shopify/polaris';

// Horizontal bleed
<Card>
  <Text>Content inside card</Text>
  <Bleed marginInline="400">
    <img src="..." alt="" width="100%" />
  </Bleed>
</Card>

// Vertical bleed
<Card>
  <Bleed marginBlock="300">
    <div>Full width content</div>
  </Bleed>
</Card>

// Directional bleed
<Card>
  <Text>Intro text</Text>
  <Bleed marginInlineStart="400" marginInlineEnd="400">
    <img src="..." alt="" width="100%" />
  </Bleed>
</Card>

// Responsive bleed
<Card>
  <Bleed marginInline={{ xs: '200', md: '400' }}>
    <img src="..." alt="" />
  </Bleed>
</Card>
```

## Best practices

- Content should never exceed parent container edges
- Choose bleed values that work within containing layout
- Use for edge-to-edge images or full-width sections
- Pair with cards for visual break in spacing
- Consider responsive bleed values for mobile

## Spacing tokens

Common space scale values: '100', '200', '300', '400', '500', '600', '700', '800', '900'

Responsive syntax:
```jsx
marginInline={{ xs: '200', sm: '300', md: '400', lg: '500', xl: '600' }}
```

## Related components

- [Card](../card) - container for content with padding
- [Box](../box) - primitive layout component
- [BlockStack](../block-stack) - vertical layout
