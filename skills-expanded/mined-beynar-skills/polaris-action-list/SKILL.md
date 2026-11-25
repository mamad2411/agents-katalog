---
name: polaris-action-list
description: Shopify Polaris Action list component. Use to render list of actions or selectable options. Usually placed in popover for dropdown menus.
---

# Action List

## When to use
Render list of actions or selectable options. Usually placed in popover to create dropdown menus. Use for secondary or less important actions.

## Props
- `items?` ActionListItemDescriptor[] - Collection of action items
  - `content` - Item text
  - `onAction` - Click handler
  - `icon?` - Icon component
  - `badge?` - Badge component
  - `destructive?` - Red/destructive style
  - `disabled?` - Disabled state
- `sections?` ActionListSection[] - Sectioned items with headers
- `actionRole?` string - ARIA role (e.g., 'menuitem')
- `allowFiltering?` boolean - Show search filter (>8 items)
- `filterLabel?` string - Filter placeholder text
- `onActionAnyItem?` () => void - Fired when any item clicked

## Examples
```jsx
import { Button, Popover, ActionList } from '@shopify/polaris';
import { useState } from 'react';

function ActionListExample() {
  const [active, setActive] = useState(true);

  return (
    <Popover
      active={active}
      activator={<Button onClick={() => setActive(!active)}>More</Button>}
      onClose={() => setActive(false)}
    >
      <ActionList
        items={[
          { content: 'Import', onAction: () => {} },
          { content: 'Export', onAction: () => {} },
        ]}
      />
    </Popover>
  );
}

// With sections
<ActionList
  sections={[
    {
      title: 'Copy',
      items: [
        { content: 'Copy link' },
        { content: 'Copy ID' },
      ],
    },
    {
      title: 'Delete',
      items: [
        { content: 'Delete', destructive: true },
      ],
    },
  ]}
/>
```

## Best practices
- Use for secondary or less important actions
- Contain actions that are related
- Each item clear and predictable
- Lead with strong verb
- Use {verb}+{noun} format
- Keep scannable (avoid articles)

## Accessibility
- Items as <li> in <ul> (group of related)
- Each item is a button
- When actionRole="menuitem": arrow keys navigate list
- Space or Enter to activate
- Tab for focus

## Content guidelines
- "Buy shipping label" not "Buy"
- "Rename" not "File name changes"
- "Add menu item" not "Add a menu item"

## Related components
- OptionList (for selection-based lists)
- ButtonGroup (for multiple buttons)
- List (for text-only lists)
