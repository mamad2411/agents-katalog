---
name: polaris-pagination
description: Shopify Polaris Pagination component. Use to divide large content into pages. Enable merchants to navigate through paginated content.
---

# Pagination

## When to use
Divide large content into pages. Enable navigation through paginated content. Use with lists, tables, and search results.

## Props
- `hasPreviousPage?` boolean - Show previous button
- `hasNextPage?` boolean - Show next button
- `onPrevious?` () => void - Previous page callback
- `onNext?` () => void - Next page callback
- `label?` string - Aria label
- `accessibilityLabel?` string - Label for pagination control

## Examples
```jsx
import { Pagination } from '@shopify/polaris';
import { useState } from 'react';

function PaginatedContent() {
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;
  const totalItems = 47;

  const hasPrevious = page > 1;
  const hasNext = page * itemsPerPage < totalItems;

  return (
    <>
      <YourContent items={getPageItems(page)} />
      <Pagination
        hasPreviousPage={hasPrevious}
        hasNextPage={hasNext}
        onPrevious={() => setPage(page - 1)}
        onNext={() => setPage(page + 1)}
      />
    </>
  );
}
```

## Best practices
- Use with IndexTable for large item collections
- Show current page context
- Disable buttons when not applicable
- Use with appropriate page size

## Content guidelines
- Clear navigation labels
- Show current position in results
- Display total count when possible

## Accessibility
- Previous/Next buttons
- Keyboard accessible
- Use accessibilityLabel for context
- Tells assistive tech what pagination controls

## Related components
- IndexTable (includes pagination)
- ResourceList (includes pagination)
