---
name: polaris-exception-list
description: Shopify Polaris Exception list component. Use to highlight important standout information adding context to tasks. Items with icons or bullets.
---

# Exception List

## When to use
Help merchants notice important, standout information that adds context. Highlight exceptional states helping decision-making. Use sparingly for high-impact messaging.

## Props
- `items` Item[] - Collection of items for list
  - `icon?` - Icon component to display
  - `description` string - Description text

## Examples
```jsx
import { ExceptionList } from '@shopify/polaris';
import { NoteIcon } from '@shopify/polaris-icons';

// Basic
<ExceptionList
  items={[
    {
      icon: NoteIcon,
      description: 'This customer is awesome. Treat them right!'
    }
  ]}
/>

// Multiple items
<ExceptionList
  items={[
    {
      icon: WarningIcon,
      description: 'High risk order - verify customer'
    },
    {
      icon: AlertIcon,
      description: 'Item out of stock'
    }
  ]}
/>
```

## Best practices
- Attach to another component (not standalone)
- Inform about extra context helping better decisions
- Surface only noteworthy, actionable content
- Use sparingly for greater impact
- Only use icons if they add clarity
- For errors: tell how to solve or attach to fixable item

## Content guidelines
- Highlight exceptional state aiding decisions
- Use appropriate color for message tone
- Include description (title optional)
- Be concise
- Error states: provide solution or link to fix

## Resource list usage
- Make entire list item clickable
- Exception lists themselves aren't clickable

## Accessibility
- Items organized as <li> in <ul>
- Conveyed as group of related elements
- Icons skip screen readers (aria-hidden="true")
- Icons visually reinforce adjacent info only

## Related components
- Banner (errors at page top)
- Resource list (often contains exception lists)
