---
name: polaris-filters
description: Shopify Polaris Filters component. Use this skill when building list/table filtering UI, search with multiple filter options, saved filter views. A composite component that filters items in a list or table.
---

# Filters

## When to use

Create a filtering system for list or table items. Use with query field and multiple filter options to help merchants narrow data.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `queryValue` | string | - | Currently entered text in query field |
| `queryPlaceholder` | string | - | Placeholder for query field |
| `focused` | boolean | false | Whether query field focused |
| `filters` | FilterInterface[] | - | Available filters for bar |
| `appliedFilters` | AppliedFilterInterface[] | - | Filters rendered as pills |
| `onQueryChange` | (queryValue: string) => void | - | Callback on query change (required) |
| `onQueryClear` | () => void | - | Callback on clear button (required) |
| `onClearAll` | () => void | - | Callback on reset all (required) |
| `onQueryBlur` | () => void | - | Callback on query blur |
| `onQueryFocus` | () => void | - | Callback on query focus |
| `children` | ReactNode | - | Content inline with controls |
| `disabled` | boolean | false | Disable all filters |
| `hideFilters` | boolean | false | Hide bar for applied filters |
| `hideQueryField` | boolean | false | Hide query field |
| `disableQueryField` | boolean | false | Disable query field |
| `disableFilters` | boolean | false | Disable filters |
| `borderlessQueryField` | boolean | false | Borderless text field |
| `loading` | boolean | false | Async task running |
| `onAddFilterClick` | () => void | - | Callback on add filter button |
| `closeOnChildOverlayClick` | boolean | false | Close on popover click |

## Examples

```jsx
import {
  ChoiceList,
  TextField,
  RangeSlider,
  LegacyCard,
  ResourceList,
  Filters,
} from '@shopify/polaris';
import { useState, useCallback } from 'react';

function FiltersExample() {
  const [accountStatus, setAccountStatus] = useState();
  const [taggedWith, setTaggedWith] = useState();
  const [queryValue, setQueryValue] = useState();

  const filters = [
    {
      key: 'accountStatus',
      label: 'Account status',
      filter: (
        <ChoiceList
          title="Account status"
          titleHidden
          choices={[
            { label: 'Enabled', value: 'enabled' },
            { label: 'Invited', value: 'invited' },
          ]}
          selected={accountStatus || []}
          onChange={setAccountStatus}
          allowMultiple
        />
      ),
      shortcut: true,
    },
  ];

  const appliedFilters = [];
  if (accountStatus?.length) {
    appliedFilters.push({
      key: 'accountStatus',
      label: accountStatus.join(', '),
      onRemove: () => setAccountStatus(),
    });
  }

  return (
    <Filters
      queryValue={queryValue}
      filters={filters}
      appliedFilters={appliedFilters}
      onQueryChange={setQueryValue}
      onQueryClear={() => setQueryValue('')}
      onClearAll={() => {
        setAccountStatus();
        setTaggedWith();
        setQueryValue();
      }}
    />
  );
}
```

## Best practices

- Promote 2-3 most commonly used filters
- Consider small screen sizes
- Use children only for filter-related content
- Help reduce merchant effort

## Content guidelines

- Filter text field: clearly labeled (e.g., "Filter orders")
- Filter badges: use clear names (e.g., "Fulfilled", "High risk")
- Group tags from same category together

## Accessibility

Relies on accessibility of: Text field, Button, Popover

- All controls must be identifiable and understood
- State changes must be announced
- All actions completable with keyboard

## Related components

- Text field: for search input
- Button: for actions
- Popover: for filter options
- ResourceList/DataTable: for filtered content
