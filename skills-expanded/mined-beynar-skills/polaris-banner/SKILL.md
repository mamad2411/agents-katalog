---
name: polaris-banner
description: Shopify Polaris Banner component. Use to inform merchants about important changes or persistent conditions prominently. Display at top of page/section.
---

# Banner

## When to use
Communicate important changes or persistent conditions prominently. Place at top of page/section for merchant-relevant information. Use sparingly for only most important info.

## Props
- `title?` string - Title content for banner
- `icon?` any - Status icon (use only major icons)
- `hideIcon?` boolean - Render without status icon
- `tone?` 'success' | 'info' | 'warning' | 'critical' - Banner status. Defaults to 'info'.
- `children?` ReactNode - Banner content
- `action?` DisableableAction & LoadableAction - Primary action
- `secondaryAction?` Action - Secondary action
- `onDismiss?` () => void - Callback when dismissed
- `stopAnnouncements?` boolean - Disable screen reader announcements on content change

## Examples
```jsx
import { Banner } from '@shopify/polaris';

// Basic
<Banner
  title="Order archived"
  onDismiss={() => {}}
>
  <p>This order was archived on March 7, 2017 at 3:12pm EDT.</p>
</Banner>

// With tone
<Banner title="Success" tone="success" onDismiss={() => {}}>
  Your changes have been saved.
</Banner>

// With action
<Banner
  title="Action needed"
  tone="critical"
  action={{ content: 'Review' }}
  onDismiss={() => {}}
>
  There was an error processing your request.
</Banner>
```

## Best practices
- Be dismissible unless critical info/important step required
- Use default icon for tone (only override with major icons)
- Remove icon only when space critical (small breakpoints)
- Place at top of page below header
- Be concise: focus on single theme
- Not for marketing/upsell (use callout cards)

## Placement
- Page-wide: top of page, below header, full content width
- Section-specific: inside section, below heading, less spacing
- Element-specific: immediately above/below element

## Content guidelines
- Keep to 1-2 sentences
- Clarify benefit/next action
- For warning/critical: explain how to resolve
- Use action labels with strong verbs

## Accessibility
- Critical/warning have role="alert" (announced immediately)
- Others have role="status" (read after alerts)
- aria-live and aria-describedby included
- tabindex="0" with focus indicator for discovery
- Form errors: banner summarizes, inline errors for details

## Related components
- Callout card (for feature/opportunity)
- Card (group similar concepts)
