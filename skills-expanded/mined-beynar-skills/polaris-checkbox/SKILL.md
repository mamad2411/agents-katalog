---
name: polaris-checkbox
description: Shopify Polaris Checkbox component. Use this skill when building multiple selection inputs, toggle lists, agreement confirmations. Allows merchants to make zero, one, or multiple selections from a list.
---

# Checkbox

## When to use

Give merchants a way to make a range of selections (zero, one, or multiple). Also used to indicate agreement to specific terms and services.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | React.ReactNode | - | Label for the checkbox (required) |
| `checked` | boolean \| 'indeterminate' | false | Checkbox selected state or mixed |
| `disabled` | boolean | false | Disable input |
| `id` | string | - | ID for form input |
| `name` | string | - | Name for form input |
| `value` | string | - | Value for form input |
| `labelHidden` | boolean | false | Visually hide label |
| `onChange` | (newChecked: boolean, id: string) => void | - | Callback when toggled |
| `onFocus` | () => void | - | Callback when focused |
| `onBlur` | () => void | - | Callback when focus removed |
| `helpText` | React.ReactNode | - | Additional helper text |
| `error` | any | - | Display error message |
| `ariaControls` | string | - | ID of controlled element |
| `ariaDescribedBy` | string | - | ID of describing element |
| `tone` | 'magic' | - | Tone of checkbox |

## Examples

```jsx
import { Checkbox } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function CheckboxExample() {
  const [checked, setChecked] = useState(false);

  const handleChange = useCallback(
    (newChecked) => setChecked(newChecked),
    []
  );

  return (
    <Checkbox
      label="Basic checkbox"
      checked={checked}
      onChange={handleChange}
    />
  );
}
```

## Best practices

- Work independently from each other (except bulk selection cases)
- Be framed positively (e.g., "Publish store" not "Hide store")
- Always have a label when used to activate/deactivate a setting
- Be listed in logical order (alphabetical, numerical, time-based)
- Link to more information or include subtitles as needed

## Content guidelines

- Start with capital letter
- Use no commas or semicolons at end of lines
- For agreement, use first person ("I agree to...")

## Accessibility

- Screen readers convey state automatically
- Use `disabled` prop to prevent interaction
- Use unique `id` values for each checkbox
- `checked="indeterminate"` conveys mixed state via aria-checked
- `ariaControls` conveys which element is controlled
- Keyboard: Tab to move focus, Space to toggle

## Related components

- Radio button: for single choice selection
- Choice list: for grouped checkboxes/radio buttons
- Content list: for ungrouped lists
