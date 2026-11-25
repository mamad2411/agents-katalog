---
name: polaris-popover
description: Shopify Polaris Popover component. Use to display content in floating container next to activator. Often wraps ActionList for menus.
---

# Popover

## When to use
Display content in floating container anchored to activator element. Use for dropdown menus, filters, additional options. Content appears on demand.

## Props
- `active` boolean - Whether popover is visible
- `activator` ReactNode - Element triggering popover (Button, Link, etc.)
- `children?` ReactNode - Popover content
- `onClose` () => void - Close callback
- `onOpen?` () => void - Open callback
- `preferredPosition?` 'above' | 'below' | 'mostSpace' - Position preference
- `preferredAlignment?` 'left' | 'center' | 'right' - Alignment preference
- `fullWidth?` boolean - Match activator width
- `fullHeight?` boolean - Match activator height
- `fluidContent?` boolean - Content is flexible width
- `sectioned?` boolean - Add padding/spacing
- `autofocusTarget?` 'first-node' | 'none' - Focus behavior

## Examples
```jsx
import { Button, Popover, ActionList } from '@shopify/polaris';
import { useState } from 'react';

function PopoverExample() {
  const [active, setActive] = useState(false);

  return (
    <Popover
      active={active}
      activator={
        <Button onClick={() => setActive(!active)} disclosure>
          More actions
        </Button>
      }
      onClose={() => setActive(false)}
    >
      <ActionList
        items={[
          { content: 'Edit', onAction: () => {} },
          { content: 'Delete', onAction: () => {} },
        ]}
      />
    </Popover>
  );
}

// With custom content
<Popover active={active} activator={activator} onClose={...}>
  <div style={{ padding: '16px' }}>
    <FilterUI />
  </div>
</Popover>
```

## Best practices
- Use for secondary actions/content
- Keep content focused and concise
- ActionList common pairing for menus
- Close on outside click or action selection
- Position to avoid viewport edges

## Content guidelines
- Concise labels for action items
- Clear action descriptions
- Avoid unnecessary complexity

## Accessibility
- Opens/closes on Enter or Space when focused
- Click outside closes popover
- Tab/focus management
- Escape key closes
- ARIA attributes for relationships

## Related components
- ActionList (common content)
- Button (common activator)
- Tooltip (for inline help)
- Modal (for larger dialogs)
