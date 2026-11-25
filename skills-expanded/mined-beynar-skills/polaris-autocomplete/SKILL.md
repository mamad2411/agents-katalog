---
name: polaris-autocomplete
description: Shopify Polaris Autocomplete component. Use this skill when building searchable input fields with dropdown suggestions, autocomplete search, filtering large option lists. Provides selectable suggestions as merchants type, wrapping Combobox and Listbox with minor UI differences.
---

# Autocomplete

## When to use

Help merchants complete text input quickly from a large collection of options. Use as a convenience wrapper around Combobox and Listbox when you need a searchable input with autocomplete suggestions.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | string | - | Unique identifier for the Autocomplete |
| `options` | OptionDescriptor[] \| SectionDescriptor[] | - | Collection of options to be listed |
| `selected` | string[] | - | Selected options |
| `textField` | React.ReactElement | - | Text field component attached to the list |
| `preferredPosition` | 'above' \| 'below' \| 'mostSpace' \| 'cover' | 'below' | Preferred direction to open popover |
| `listTitle` | string | - | Title of the list of options |
| `allowMultiple` | boolean | false | Allow more than one option selected |
| `actionBefore` | ActionListItemDescriptor & { wrapOverflow?: boolean } | - | Action to render above options |
| `loading` | boolean | false | Display loading state |
| `willLoadMoreResults` | boolean | false | Indicates if more results will load dynamically |
| `emptyState` | React.ReactNode | - | Rendered when no options available |
| `onSelect` | (selected: string[]) => void | - | Callback when selection changes |
| `onLoadMoreResults` | () => void | - | Callback when end of list reached |

## Examples

```jsx
import { Autocomplete, Icon } from '@shopify/polaris';
import { SearchIcon } from '@shopify/polaris-icons';
import { useState, useCallback, useMemo } from 'react';

function AutocompleteExample() {
  const deselectedOptions = useMemo(() => [
    { value: 'rustic', label: 'Rustic' },
    { value: 'antique', label: 'Antique' },
    { value: 'vinyl', label: 'Vinyl' },
  ], []);

  const [selectedOptions, setSelectedOptions] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [options, setOptions] = useState(deselectedOptions);

  const updateText = useCallback((value) => {
    setInputValue(value);
    if (value === '') {
      setOptions(deselectedOptions);
      return;
    }
    const filterRegex = new RegExp(value, 'i');
    const resultOptions = deselectedOptions.filter(
      (option) => option.label.match(filterRegex)
    );
    setOptions(resultOptions);
  }, [deselectedOptions]);

  const updateSelection = useCallback((selected) => {
    const selectedValue = selected.map((selectedItem) => {
      const matchedOption = options.find(
        (option) => option.value.match(selectedItem)
      );
      return matchedOption && matchedOption.label;
    });
    setSelectedOptions(selected);
    setInputValue(selectedValue[0] || '');
  }, [options]);

  const textField = (
    <Autocomplete.TextField
      onChange={updateText}
      label="Tags"
      value={inputValue}
      prefix={<Icon source={SearchIcon} tone="base" />}
      placeholder="Search"
      autoComplete="off"
    />
  );

  return (
    <div style={{ height: '225px' }}>
      <Autocomplete
        options={options}
        selected={selectedOptions}
        onSelect={updateSelection}
        textField={textField}
      />
    </div>
  );
}
```

## Best practices

- Be clearly labeled so merchants know what options will be available
- Limit the number of options displayed at once
- Not be used within a popover
- Indicate a loading state while option data is being populated

## Accessibility

Based on ARIA 1.2 combobox and listbox patterns.

- Use autocomplete as progressive enhancement
- Always allow search, entry, or other activities without relying on autocomplete
- Keyboard: Tab to focus, arrow keys to navigate options, Enter to select
- List displays below by default but can change with `preferredPosition` prop

## Related components

- Text field: for input without suggested options
- Option list: for selectable options not linked to input
- Combobox: for a text field that triggers a popover
