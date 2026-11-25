---
name: polaris-combobox
description: Shopify Polaris Combobox component. Use this skill when building accessible autocomplete inputs, filterable option lists, tag selection inputs. Enables merchants to filter a list and select one or more values.
---

# Combobox

## When to use

An accessible autocomplete input where merchants can filter a list of options and select one or more values. Use when merchants can select from a predefined or editable list.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `activator` | React.ReactElement | - | Text field component that activates popover (required) |
| `children` | any | - | Content to display inside popover |
| `allowMultiple` | boolean | false | Allow more than one selection |
| `preferredPosition` | 'above' \| 'below' \| 'mostSpace' \| 'cover' | 'below' | Preferred direction to open |
| `willLoadMoreOptions` | boolean | false | Whether more options available to lazy load |
| `height` | string | - | Height of popover pane |
| `maxHeight` | string | - | Max height of popover pane |
| `minHeight` | string | - | Min height of popover pane |
| `onScrolledToBottom` | () => void | - | Callback when bottom reached (lazy load) |
| `onClose` | () => void | - | Callback when popover closes |

## Anatomy

- **TextField**: Text input that activates popover with filtered list
- **Popover**: Overlay containing option list
- **Listbox**: List of options to filter and select
- **Listbox.Option**: Individual options with various content support

## Examples

```jsx
import { Listbox, Combobox, Icon } from '@shopify/polaris';
import { SearchIcon } from '@shopify/polaris-icons';
import { useState, useCallback, useMemo } from 'react';

function ComboboxExample() {
  const deselectedOptions = useMemo(() => [
    { value: 'rustic', label: 'Rustic' },
    { value: 'antique', label: 'Antique' },
    { value: 'vinyl', label: 'Vinyl' },
  ], []);

  const [selectedOption, setSelectedOption] = useState();
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
    const matchedOption = options.find(
      (option) => option.value.match(selected)
    );
    setSelectedOption(selected);
    setInputValue((matchedOption && matchedOption.label) || '');
  }, [options]);

  const optionsMarkup = options.map(({ label, value }) => (
    <Listbox.Option
      key={value}
      value={value}
      selected={selectedOption === value}
      accessibilityLabel={label}
    >
      {label}
    </Listbox.Option>
  ));

  return (
    <div style={{ height: '225px' }}>
      <Combobox
        activator={
          <Combobox.TextField
            prefix={<Icon source={SearchIcon} />}
            onChange={updateText}
            label="Search tags"
            labelHidden
            value={inputValue}
            placeholder="Search tags"
            autoComplete="off"
          />
        }
      >
        {options.length > 0 ? (
          <Listbox onSelect={updateSelection}>
            {optionsMarkup}
          </Listbox>
        ) : null}
      </Combobox>
    </div>
  );
}
```

## Best practices

- Be clearly labeled so merchant knows what options available
- Not be used within a popover
- Indicate loading state while option data populates
- Order items intentionally for easy discovery
- Apply custom filtering if default behavior doesn't fit

## Content guidelines

Follow text field content guidelines for input field.

## Accessibility

Based on ARIA 1.2 combobox pattern with Listbox component.

- Use as progressive enhancement, not requirement
- Popover displays below by default
- Keyboard: Tab to focus, arrow keys to navigate, Enter to select
- Merchants should have alternative ways to search/enter without relying on combobox

## Related components

- Text field: for input without suggestions
- Listbox: for option list not linked to input
- Popover: for overlay trigger
