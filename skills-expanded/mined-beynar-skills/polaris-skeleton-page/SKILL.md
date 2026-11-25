---
name: polaris-skeleton-page
description: Shopify Polaris Skeleton page component. Use for low fidelity page representation. Combines skeleton components to show layout during load.
---

# Skeleton Page

## When to use
Provide low fidelity representation of entire page layout. Use with other skeleton components. Improves perceived load times. Use when all page content loads simultaneously.

## Props
- `title?` string - Page title in large type
- `fullWidth?` boolean - Remove normal max-width
- `narrowWidth?` boolean - Decrease max-width (single-column layouts)
- `primaryAction?` boolean - Show skeleton over primary action
- `backAction?` boolean - Show skeleton over back action
- `children?` ReactNode - Child elements (use Layout, SkeletonBodyText, etc.)

## Examples
```jsx
import {
  SkeletonPage,
  Layout,
  Card,
  SkeletonBodyText,
  SkeletonDisplayText,
} from '@shopify/polaris';

<SkeletonPage primaryAction>
  <Layout>
    <Layout.Section>
      <Card>
        <Card.Section>
          <SkeletonBodyText />
        </Card.Section>
      </Card>
    </Layout.Section>
    <Layout.Section variant="oneThird">
      <Card>
        <Card.Section>
          <SkeletonDisplayText size="small" />
          <SkeletonBodyText lines={2} />
        </Card.Section>
      </Card>
    </Layout.Section>
  </Layout>
</SkeletonPage>
```

## Best practices
- Use for pages where all content loads at once
- Give indication of final page layout
- Mirror actual layout structure with skeleton components
- Show actual static titles/content only

## Content guidelines
- Show page titles that never change
- Use skeleton for dynamic titles
- Don't use placeholder content
- Secondary actions always represented with skeleton
- Can customize number of skeleton actions

## Accessibility
- Provides visual layout indication during load

## Related components
- SkeletonBodyText (content blocks)
- SkeletonDisplayText (headings/titles)
- ProgressBar / Spinner (in-context operations)
