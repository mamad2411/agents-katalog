---
name: polaris-media-card
description: Shopify Polaris MediaCard component. Use to surface educational content with visual media, title, description, and call-to-action buttons.
---

# MediaCard

## When to use
Use to educate merchants about features with visual media (image, video). Combines visual and text content with clear calls to action. Dismissible cards.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Visual media (img, video element) |
| title | ReactNode | Required | Card title (becomes h2) |
| description | string | Required | Body content text |
| primaryAction | ComplexAction | - | Main call to action button |
| secondaryAction | ComplexAction | - | Secondary call to action |
| popoverActions | ActionListItemDescriptor[] | - | Ellipsis menu actions |
| portrait | boolean | false | Vertical layout instead of horizontal |
| size | 'small' \| 'medium' | 'medium' | Visual media size |
| onDismiss | () => void | - | Callback when dismissed |

## Examples

```jsx
import { MediaCard } from '@shopify/polaris';

// Basic media card
<MediaCard
  title="Getting started"
  description="Discover how Shopify powers your business."
  primaryAction={{
    content: 'Learn about getting started',
    onAction: () => {},
  }}
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <img
    alt=""
    width="100%"
    height="100%"
    src="https://burst.shopifycdn.com/photos/business-woman.jpg"
    style={{ objectFit: 'cover' }}
  />
</MediaCard>

// With secondary action
<MediaCard
  title="Sales channel optimization"
  description="Add your products to multiple sales channels."
  primaryAction={{
    content: 'Set up sales channel',
    onAction: () => {},
  }}
  secondaryAction={{
    content: 'Learn more',
    onAction: () => {},
  }}
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <img alt="" src="..." />
</MediaCard>

// Small size
<MediaCard
  title="Quick tip"
  description="You can bulk edit products."
  size="small"
  primaryAction={{
    content: 'Edit products',
    onAction: () => {},
  }}
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <img alt="" src="..." />
</MediaCard>

// Portrait layout (vertical)
<MediaCard
  title="Mobile optimization"
  description="Your store looks great on mobile devices."
  portrait
  primaryAction={{
    content: 'View mobile preview',
    onAction: () => {},
  }}
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <img alt="" src="..." />
</MediaCard>

// Video card
<MediaCard
  title="Store setup walkthrough"
  description="Complete the initial setup in 5 minutes."
  primaryAction={{
    content: 'Watch video',
    onAction: () => {},
  }}
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <video width="100%" height="100%">
    <source src="setup.mp4" type="video/mp4" />
  </video>
</MediaCard>

// Portrait video
<MediaCard
  title="Mobile sales"
  description="Reach customers on the go."
  portrait
  primaryAction={{
    content: 'Set up mobile sales',
    onAction: () => {},
  }}
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <video width="100%" height="100%">
    <source src="mobile.mp4" type="video/mp4" />
  </video>
</MediaCard>

// No actions (just dismissible)
<MediaCard
  title="Feature announcement"
  description="New features released today."
  popoverActions={[
    { content: 'Dismiss', onAction: () => {} }
  ]}
>
  <img alt="" src="..." />
</MediaCard>
```

## Best practices

- Pair text with visual content (image/video)
- Visual enhances written content, not required
- Educational focus, not advertisement
- Clear call to action
- Show targeted content to relevant merchants
- Always make dismissible
- Media size proportionate to content
- Content should stand alone without media

## Content guidelines

**Title**: Follow heading guidelines, clear and specific

**Description**:
- Actionable (start with imperative verbs, not "you can")
- Most critical info first
- Use "need" for required actions
- Clear and scannable

**Primary action**:
- Clear and predictable
- Verb + noun format (except Save, Close, Cancel, OK)
- No unnecessary words
- Example: "View shipping settings" not "View your settings"

**Secondary action**:
- Lower priority than primary
- Follow button guidelines
- For "Learn more" or support actions

## Accessibility

- Title becomes h2 heading for structure
- Use actionable language for clarity
- Media is supplementary to text
- Ensure text communicates without media

## Related components

- [Card](../card) - general content container
- [Layout](../layout) - page-level layout
- [EmptyState](../empty-state) - for unused features
- [CalloutCard](../callout-card) - feature promotion
