---
name: polaris-callout-card
description: Shopify Polaris CalloutCard component. Use to encourage merchants to take action on new features or opportunities with illustration and clear CTA.
---

# CalloutCard

## When to use
Use to highlight a feature or opportunity with a clear single action. Common in sales channels and feature promotion. Include illustration, title, body, and primary action.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| title | ReactNode | Required | Card title (becomes h2) |
| illustration | string | Required | URL to card illustration |
| children | ReactNode | - | Body content (description) |
| primaryAction | IconableAction | Required | Primary call to action |
| secondaryAction | IconableAction & ButtonProps | - | Secondary action |
| onDismiss | () => void | - | Callback when dismissed |

## Examples

```jsx
import { CalloutCard } from '@shopify/polaris';

// Basic callout
<CalloutCard
  title="Customize your checkout"
  illustration="https://cdn.shopify.com/s/assets/.../image.svg"
  primaryAction={{
    content: 'Customize checkout',
    url: '#',
  }}
>
  <p>Upload your logo, change colors and fonts, and more.</p>
</CalloutCard>

// With secondary action
<CalloutCard
  title="Launch on TikTok"
  illustration="https://cdn.shopify.com/s/assets/.../tiktok.svg"
  primaryAction={{
    content: 'Get started',
    onAction: () => {},
  }}
  secondaryAction={{
    content: 'Learn more',
    onAction: () => {},
  }}
>
  <p>Reach millions of customers on TikTok.</p>
</CalloutCard>

// Dismissible
<CalloutCard
  title="Increase conversion"
  illustration="https://example.com/conversion.svg"
  primaryAction={{
    content: 'Set up',
    url: '/admin/settings',
  }}
  onDismiss={() => console.log('Dismissed')}
>
  <p>Enable payment methods that increase conversion rates.</p>
</CalloutCard>
```

## Best practices

- Clearly articulate feature benefit
- Include helpful illustration
- Provide clear call to action
- Target relevant merchants
- Make dismissible
- Use actionable body text
- Place at top of relevant sections

## Content guidelines

**Title**: Follow heading guidelines, clear and specific

**Body content**:
- Start with imperative verbs (not "you can")
- Most critical info first
- Use "need" for required actions
- Keep sentences clear and scannable

**Primary action**:
- Clear and predictable
- Strong verb + noun format (except Save, Close, Cancel, OK)
- Avoid unnecessary words and articles

## Accessibility

- Title becomes h2 heading for structure
- Illustrations are decorative (empty alt attributes)
- Use actionable language for clarity
- Screen readers skip illustration

## Related components

- [Card](../card) - for grouping similar concepts
- [Layout](../layout) - for page-level layout
- [EmptyState](../empty-state) - for explaining unused features
