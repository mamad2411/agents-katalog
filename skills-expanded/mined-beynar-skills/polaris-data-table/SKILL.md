---
name: polaris-data-table
description: Shopify Polaris Data table component. Use to present structured data for comparison and analysis. For insights and analytics review.
---

# Data Table

## When to use
Present structured data for comparison and analysis. Use when helping merchants gain insights or review analytics. Different from IndexTable which is for object collections.

## Props
Comprehensive table props (see Polaris docs for detailed prop list):
- `columnContentTypes?` array - Content type hints for columns
- `firstColumnMinWidth?` number - Minimum width for first column
- `hoverable?` boolean - Show hover state
- `footerContent?` ReactNode - Footer content
- `truncate?` boolean - Truncate overflow text
- `verticalAlign?` - Vertical alignment
- `rows` array - Table row data
- `headings` array - Column heading definitions
- `totals?` array - Total row values
- `expandedRows?` array - Row expansion IDs
- `onSort?` callback - Sort handler
- `defaultSortDirection?` 'ascending' | 'descending'
- `sortColumnIndex?` number - Current sort column
- `sortDirection?` 'ascending' | 'descending'
- `columnVisibilityData?` - Column visibility config

## Examples
```jsx
import { DataTable } from '@shopify/polaris';

<DataTable
  columnContentTypes={['text', 'numeric', 'numeric']}
  headings={['Product', 'Quantity', 'Revenue']}
  rows={[
    ['Laptop', '10', '$5,000'],
    ['Mouse', '50', '$500'],
    ['Keyboard', '30', '$900'],
  ]}
  totals={['Total', '90', '$6,400']}
  truncate
/>
```

## Best practices
- Use for comparison and analysis
- Use when helping merchants review data/analytics
- Suitable for metrics, financial data, performance reports
- Pair with visualizations (charts, graphs)

## Related components
- IndexTable (for object collections with actions)
- ProgressBar / Spinner (for loading)
- Skeleton components (for loading state)
