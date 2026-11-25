---
name: polaris-select
description: Shopify Polaris Select component. Use this skill when building dropdown menus, single option selection, long option lists. A classic dropdown select field for choosing one option from a menu.
---

# Select

## When to use

Let merchants choose one option from an options menu. Use select when you have 4 or more options to avoid cluttering the interface.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | React.ReactNode | - | Label for select (required) |
| `options` | (string \| StrictOption \| SelectGroup)[] | - | List of options or groups |
| `value` | string | - | Value for form input |
| `disabled` | boolean | false | Disable input |
| `id` | string | - | ID for form input |
| `name` | string | - | Name for form input |
| `placeholder` | string | - | Example text placeholder |
| `helpText` | React.ReactNode | - | Additional text to aid use |
| `error` | any | - | Display error state |
| `labelAction` | Action | - | Action added to label |
| `labelHidden` | boolean | false | Visually hide label |
| `labelInline` | boolean | false | Show label to left of value |
| `requiredIndicator` | boolean | false | Visual required indicator (asterisk) |
| `tone` | 'magic' | - | Tone of select |
| `onChange` | (selected: string, id: string) => void | - | Callback on change |
| `onFocus` | (event?: React.FocusEvent) => void | - | Callback on focus |
| `onBlur` | (event?: React.FocusEvent) => void | - | Callback on blur |

## Examples

```jsx
import { Select } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function SelectExample() {
  const [selected, setSelected] = useState('today');

  const handleSelectChange = useCallback((value) => setSelected(value), []);

  const options = [
    { label: 'Today', value: 'today' },
    { label: 'Yesterday', value: 'yesterday' },
    { label: 'Last 7 days', value: 'lastWeek' },
  ];

  return (
    <Select
      label="Date range"
      options={options}
      onChange={handleSelectChange}
      value={selected}
    />
  );
}

// With option groups
function SelectWithGroups() {
  const options = [
    {
      title: 'Colors',
      options: [
        { label: 'Red', value: 'red' },
        { label: 'Blue', value: 'blue' },
      ],
    },
  ];

  return <Select label="Choose color" options={options} />;
}
```

## Best practices

- Use for selecting between 4 or more pre-defined options
- Have default option selected whenever possible
- Use "Select" as placeholder only if no logical default
- Present options in logical order (alphabetical, numerical, etc.)

## Content guidelines

- Labels: short (1-3 words), sentence case, no punctuation/articles
- Independent sentences, not first part of sentence completed by options
- Descriptive, not instructional
- Don't say "What is your email?" say "Email address"
- Options: start with "Select" if no default, alphabetical/logical order, sentence case, no commas/semicolons
- Options clearly labeled based on what they do

## Accessibility

- Native HTML `<select>` element
- Screen readers convey available options
- Keyboard: Tab to focus, Arrow keys to navigate, Enter to select

## Related components

- Choice list: for single selection from fewer than 4 options
- Option list in popover: for multiple selections or advanced option formatting
