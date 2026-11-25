---
name: polaris-index-table
description: Shopify Polaris Index table component. Use to display collection of same-type objects (orders, products). Supports selection, sorting, filtering, pagination.
---

# Index Table

## When to use
Display collection of same-type objects like orders or products. Help merchants get at-a-glance view and navigate to full-page representation. Supports bulk actions, sorting, filtering.

## Props
- `headings` array - Column heading definitions with title, alignment
- `promotedBulkActions?` array - Priority bulk actions
- `bulkActions?` array - Additional bulk actions
- `children?` ReactNode - IndexTable.Row elements
- `emptyState?` ReactNode - Empty state content
- `sort?` ReactNode - Sort control
- `paginatedSelectAllActionText?` string - Select all text
- `paginatedSelectAllText?` string - Selection summary
- `lastColumnSticky?` boolean - Stick last column
- `selectable?` boolean - Enable row selection
- `sortable?` boolean[] - Enable sorting per column
- `defaultSortDirection?` 'ascending' | 'descending'
- `sortDirection?` 'ascending' | 'descending'
- `sortColumnIndex?` number - Current sort column
- `onSort?` callback - Sort change handler
- `hasZebraStriping?` boolean - Alternate row colors
- `pagination?` - Pagination props
- `itemCount` number - Total items
- `selectedItemsCount?` number | 'All' - Selected count
- `resourceName?` { singular, plural } - Item type name
- `loading?` boolean - Loading state
- `condensed?` boolean - Hide bulk actions on small screens
- `onSelectionChange?` callback - Selection change handler

## Subcomponents
- `IndexTable.Row` - Table row with id, position, selected state
- `IndexTable.Cell` - Table cell with as ('th'|'td'), alignment
- `IndexTable.Row.selectionRange` - For subheader rows spanning multiple rows

## Examples
```jsx
import { IndexTable, Card, useIndexResourceState, Badge } from '@shopify/polaris';

const orders = [
  { id: '1', order: '#1001', date: 'Jul 20', customer: 'John' },
];

const { selectedResources, handleSelectionChange } = useIndexResourceState(orders);

<Card>
  <IndexTable
    resourceName={{ singular: 'order', plural: 'orders' }}
    itemCount={orders.length}
    selectedItemsCount={selectedResources.length}
    onSelectionChange={handleSelectionChange}
    headings={[
      { title: 'Order' },
      { title: 'Date' },
      { title: 'Customer' },
    ]}
  >
    {orders.map((order, idx) => (
      <IndexTable.Row
        id={order.id}
        key={order.id}
        selected={selectedResources.includes(order.id)}
        position={idx}
      >
        <IndexTable.Cell>{order.order}</IndexTable.Cell>
        <IndexTable.Cell>{order.date}</IndexTable.Cell>
        <IndexTable.Cell>{order.customer}</IndexTable.Cell>
      </IndexTable.Row>
    ))}
  </IndexTable>
</Card>
```

## Best practices
- Items clickable (navigate to details or provide detail)
- Support sorting for long lists
- Support filtering for long lists
- Paginate when > 50 items
- Use SkeletonPage for initial load when loading=true
- Right-align numeric cells with Text component
- Hide bulk actions on small screens (condensed prop)

## Accessibility
- Organized as <table> with proper <thead>/<tbody>
- Row selection with checkboxes or shift+click ranges
- Subheaders supported with proper aria relationships
- Keyboard: Tab through, Space to select, Shift+click for ranges

## Related components
- Filters (for filtering)
- Pagination (for pagination)
- SkeletonPage (for loading state)
