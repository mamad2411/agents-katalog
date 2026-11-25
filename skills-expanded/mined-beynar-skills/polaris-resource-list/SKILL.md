---
name: polaris-resource-list
description: Shopify Polaris Resource list component. Use to display collection of same-type objects. Helps merchants find and navigate to full-page representation.
---

# Resource List

## When to use
Display collection of same-type objects like products or customers. Help merchants find objects and navigate to full-page representation. Supports selection, bulk actions, filtering.

## Props
- `resourceName` { singular, plural } - Resource type name
- `items` array - Collection of items to display
- `renderItem` (item) => ReactNode - Render function for items
- `selectable?` boolean - Enable item selection
- `onSelectionChange?` callback - Selection change handler
- `selectedItems?` array - Selected item IDs
- `emptyState?` ReactNode - Empty state content
- `filterControl?` ReactNode - Filter UI
- `sortOptions?` array - Sort choices
- `sortValue?` string - Current sort
- `onSortChange?` callback - Sort change handler
- `bulkActions?` array - Bulk action buttons
- `promotedBulkActions?` array - Priority bulk actions
- `paginatedSelectAllText?` string - Selection text
- `paginatedSelectAllActionText?` string - Action text
- `hasMoreItems?` boolean - More items available
- `loading?` boolean - Loading state
- `totalItemsCount?` number - Total items

## Examples
```jsx
import { ResourceList, ResourceItem, Card } from '@shopify/polaris';
import { useState } from 'react';

const items = [
  { id: '1', url: '#', name: 'Product 1' },
  { id: '2', url: '#', name: 'Product 2' },
];

<Card>
  <ResourceList
    resourceName={{ singular: 'product', plural: 'products' }}
    items={items}
    renderItem={(item) => (
      <ResourceItem
        id={item.id}
        url={item.url}
        name={item.name}
      >
        {item.name}
      </ResourceItem>
    )}
  />
</Card>

// With selection
const [selected, setSelected] = useState([]);
<ResourceList
  resourceName={{ singular: 'product', plural: 'products' }}
  items={items}
  selectedItems={selected}
  onSelectionChange={setSelected}
  selectable
  renderItem={...}
/>
```

## Best practices
- Items perform action when clicked
- Tailor content/layout to resource type
- Support sorting for long lists
- Support filtering for long lists
- Paginate > 50 items
- Use SkeletonPage on initial load
- Use ResourceItem for consistent styling

## Bulk actions
- Act on multiple items at once
- Example: add tag to many products
- Promoted: primary actions shown always
- Regular: in menu

## Content guidelines
- Identify resource type (with heading)
- Indicate when not all resources shown
- Follow verb+noun formula for actions
- Follow filter content guidelines

## Accessibility
- Items as links with unique names
- Supports selection and bulk operations
- Keyboard accessible

## Related components
- ResourceItem (individual resource display)
- IndexTable (for more complex tables)
- Filters (for filtering support)
