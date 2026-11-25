---
name: polaris-skeleton-body-text
description: Shopify Polaris Skeleton body text component. Use for low fidelity loading representation. Improves perceived load time for content blocks.
---

# Skeleton Body Text

## When to use
Provide low fidelity representation before content appears. Improve perceived load times. Use for content loading inside or outside cards. Represent blocks of text being loaded.

## Props
- `lines?` number - Number of lines to display. Defaults to 3.

## Examples
```jsx
import { SkeletonBodyText } from '@shopify/polaris';

// Default (3 lines)
<SkeletonBodyText />

// Single line
<SkeletonBodyText lines={1} />

// Multiple lines
<SkeletonBodyText lines={5} />

// Inside card
import { Card } from '@shopify/polaris';
<Card>
  <Card.Section>
    <SkeletonBodyText lines={2} />
  </Card.Section>
</Card>
```

## Best practices
- Use with SkeletonPage when all content loads at once
- Use standalone inside containers (Card) for partial loads
- Match line count to actual content for accuracy
- Show static content, skeleton for dynamic content

## Content guidelines
- Use skeleton for dynamic content that changes
- Show actual static content (never placeholders)
- Don't use placeholder text

## Accessibility
- Provides visual indication of loading state

## Related components
- SkeletonPage (full page loads)
- SkeletonDisplayText (headings/titles)
- ProgressBar / Spinner (in-context operations)
