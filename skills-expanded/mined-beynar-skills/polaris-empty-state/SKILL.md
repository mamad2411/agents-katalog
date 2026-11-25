---
name: polaris-empty-state
description: Shopify Polaris EmptyState component. Use when lists, tables, or pages have no data. Explains feature and guides merchants to next steps.
---

# EmptyState

## When to use
Use when a page, list, table, or chart is empty. Provides explanation and guidance to help merchants progress. For full-page emptiness, not individual empty areas.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| heading | string | - | Empty state title |
| image | string | Required | Path to image (add ~40px white space above) |
| largeImage | string | - | Image for large screens |
| imageContained | boolean | false | Limit image size to container |
| fullWidth | boolean | false | Content spans full container width |
| children | ReactNode | - | Body content/description |
| action | ComplexAction | - | Primary action button |
| secondaryAction | ComplexAction | - | Secondary action (Learn more) |
| footerContent | ReactNode | - | Content below actions |

## Examples

```jsx
import { EmptyState, Card } from '@shopify/polaris';

// Basic empty state
<Card>
  <EmptyState
    heading="Manage transfers"
    image="https://cdn.shopify.com/s/files/.../emptystate-files.png"
    action={{ content: 'Add transfer' }}
  >
    <p>Track and receive incoming inventory from suppliers.</p>
  </EmptyState>
</Card>

// With secondary action
<EmptyState
  heading="Create your first order"
  image="https://cdn.shopify.com/s/files/.../orders.png"
  action={{
    content: 'Create order',
    onAction: () => {},
  }}
  secondaryAction={{
    content: 'Learn more',
    url: 'https://help.shopify.com',
  }}
>
  <p>Get started by creating your first order.</p>
</EmptyState>

// Full width
<EmptyState
  heading="No products yet"
  image="https://cdn.shopify.com/s/files/.../products.png"
  action={{ content: 'Add product' }}
  fullWidth
>
  <p>Add products to your store to get started selling.</p>
</EmptyState>

// With footer context
<EmptyState
  heading="No data available"
  image="https://cdn.shopify.com/s/files/.../analytics.png"
  action={{ content: 'View help' }}
  footerContent={<Text tone="subdued">Check back later</Text>}
>
  <p>Data will appear here once activity starts.</p>
</EmptyState>
```

## Best practices

- Orient merchants with clear benefit explanation
- Use simple, clear, empowering language
- Explain steps to activate feature
- Use illustration thoughtfully
- Only one primary call-to-action button
- Never make merchants feel unsuccessful
- Focus on key features and benefits
- Include proper white space above image (40px)

## Content guidelines

**Title**:
- Action-oriented ("Create orders", not "Orders")
- Follow heading content guidelines
- Clear expectations

**Subtitle/Body**:
- Describe or explain title
- Conversational (include articles: the, a, an)
- Clear and scannable

**Primary action**:
- Clear and predictable
- Strong verb + noun (Create order, Buy label)
- No unnecessary words or articles

**Secondary action**:
- For "Learn more" or support actions
- Follow button guidelines
- Lower priority than primary

## Accessibility

- Illustrations are decorative (empty alt attributes)
- Screen readers skip images
- Use actionable language for clarity
- Headings provide structure

## Related components

- [Layout](../layout) - page-level layout
- [CalloutCard](../callout-card) - feature promotion
- [Card](../card) - content grouping
