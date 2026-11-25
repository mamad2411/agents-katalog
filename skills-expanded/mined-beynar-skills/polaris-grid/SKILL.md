---
name: polaris-grid
description: Shopify Polaris Grid component. Use to create complex responsive layouts based on CSS Grid with multi-column support.
---

# Grid

## When to use
Use to create complex responsive layouts with multiple columns. Aligns to 12-column grid. Use Grid.Cell with columnSpan to control widths at different breakpoints.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | Grid cells |
| columns | { xs?, sm?, md?, lg?, xl? } | - | Number of columns per breakpoint |
| gap | { xs?, sm?, md?, lg?, xl? } | - | Space between cells per breakpoint |
| areas | { xs?, sm?, md?, lg?, xl? } | - | Template areas (deprecated) |

## Grid.Cell Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Cell content |
| columnSpan | { xs?, sm?, md?, lg?, xl? } | - | Column width at breakpoints |

## Examples

```jsx
import { Page, Grid, Card } from '@shopify/polaris';

// Two column layout (50/50)
<Page fullWidth>
  <Grid>
    <Grid.Cell columnSpan={{ xs: 6, sm: 3, md: 3, lg: 6, xl: 6 }}>
      <Card>
        <Text variant="headingMd">Sales</Text>
        <p>Summary of your sales</p>
      </Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 6, sm: 3, md: 3, lg: 6, xl: 6 }}>
      <Card>
        <Text variant="headingMd">Orders</Text>
        <p>Summary of your orders</p>
      </Card>
    </Grid.Cell>
  </Grid>
</Page>

// Two-thirds and one-third
<Page fullWidth>
  <Grid>
    <Grid.Cell columnSpan={{ xs: 12, sm: 8, md: 8, lg: 8, xl: 8 }}>
      <Card>
        <Text variant="headingMd">Main content (2/3)</Text>
      </Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 12, sm: 4, md: 4, lg: 4, xl: 4 }}>
      <Card>
        <Text variant="headingMd">Sidebar (1/3)</Text>
      </Card>
    </Grid.Cell>
  </Grid>
</Page>

// Three equal columns
<Page fullWidth>
  <Grid>
    <Grid.Cell columnSpan={{ xs: 6, sm: 4, md: 4, lg: 4, xl: 4 }}>
      <Card>Column 1</Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 6, sm: 4, md: 4, lg: 4, xl: 4 }}>
      <Card>Column 2</Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 6, sm: 4, md: 4, lg: 4, xl: 4 }}>
      <Card>Column 3</Card>
    </Grid.Cell>
  </Grid>
</Page>

// Custom responsive layout
<Page fullWidth>
  <Grid columns={{ xs: 6, md: 12 }} gap={{ xs: '200', md: '400' }}>
    <Grid.Cell columnSpan={{ xs: 6, md: 4 }}>
      <Card>Responsive card 1</Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 6, md: 4 }}>
      <Card>Responsive card 2</Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 6, md: 4 }}>
      <Card>Responsive card 3</Card>
    </Grid.Cell>
  </Grid>
</Page>

// Mixed column spans
<Grid>
  <Grid.Cell columnSpan={{ xs: 12, md: 6 }}>
    <Card>Half width on md+</Card>
  </Grid.Cell>
  <Grid.Cell columnSpan={{ xs: 6, md: 3 }}>
    <Card>1/4 width on md+</Card>
  </Grid.Cell>
  <Grid.Cell columnSpan={{ xs: 6, md: 3 }}>
    <Card>1/4 width on md+</Card>
  </Grid.Cell>
</Grid>
```

## Breakpoints

- `xs`: 0px and up (mobile)
- `sm`: 490px and up
- `md`: 992px and up (tablet)
- `lg`: 1400px and up (desktop)
- `xl`: 1680px and up (large desktop)

## Examples by responsive configuration

**columnSpan values out of 12**:
- Full width: `{ xs: 12, md: 12 }`
- Half: `{ xs: 6, md: 6 }`
- 2/3: `{ xs: 12, md: 8 }`
- 1/3: `{ xs: 12, md: 4 }`
- 1/4: `{ xs: 6, md: 3 }`
- 3/4: `{ xs: 12, md: 9 }`

## Best practices

- Wrap in Page with fullWidth prop
- Use columnSpan to be responsive
- Consider mobile-first (xs first, then larger breakpoints)
- Don't nest grids too deeply
- Leave room for content to breathe
- Use consistent gap spacing

## Related components

- [Page](../page) - page wrapper
- [Layout](../layout) - alternative for simpler layouts
- [Card](../card) - cell content
- [BlockStack](../block-stack) - for vertical arrangement within cells
