---
name: polaris-tabs
description: Shopify Polaris Tabs component. Use to switch between related sections of content. Organize content into separate views.
---

# Tabs

## When to use
Organize content into separate sections or views. Switch between related content without page navigation. Keep related content together but separated.

## Props
- `tabs` array - Tab definitions
  - `id` string - Unique identifier
  - `content` string - Tab label
  - `url?` string - URL for tab (if links between pages)
  - `badge?` ReactNode - Badge content
  - `isNew?` boolean - Show "New" indicator
- `selected?` number - Index of selected tab (controlled)
- `onSelect?` (index: number) => void - Tab selection callback
- `fitted?` boolean - Stretch tabs to container
- `discardConfirmationModal?` boolean - Show confirmation on unsaved changes

## Examples
```jsx
import { Tabs, Card } from '@shopify/polaris';
import { useState } from 'react';

function TabsExample() {
  const [selected, setSelected] = useState(0);

  const tabs = [
    { id: 'all', content: 'All products' },
    { id: 'active', content: 'Active' },
    { id: 'draft', content: 'Draft' },
    { id: 'archived', content: 'Archived' },
  ];

  return (
    <Card>
      <Tabs
        tabs={tabs}
        selected={selected}
        onSelect={setSelected}
      >
        <div>
          {selected === 0 && <AllProducts />}
          {selected === 1 && <ActiveProducts />}
          {selected === 2 && <DraftProducts />}
          {selected === 3 && <ArchivedProducts />}
        </div>
      </Tabs>
    </Card>
  );
}

// With badges
const tabs = [
  { id: 'inbox', content: 'Inbox', badge: { content: '5' } },
];

// With URLs (page navigation)
const tabs = [
  { id: 'products', content: 'Products', url: '/products' },
  { id: 'orders', content: 'Orders', url: '/orders' },
];
```

## Best practices
- Keep tabs related to same context
- 3-6 tabs optimal (max 7)
- Use clear, scannable labels
- Place above content they control
- Maintain scroll position on tab switch

## Content guidelines
- Tab labels: noun or verb+noun
- Keep labels concise
- Avoid articles (the, a, an)
- Consistent capitalization

## Accessibility
- Tabs as ARIA tab pattern
- Tab key selects tab
- Arrow keys navigate tabs
- Current tab marked (aria-selected)
- Content behind tab (role="tabpanel")

## Related components
- SkeletonTabs (loading state)
