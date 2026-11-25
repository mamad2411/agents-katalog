---
name: polaris-radio-button
description: Shopify Polaris Radio button component. Use this skill when building single-choice selection lists, mutually exclusive options, toggling between radio button options. Presents items where merchants must make a single selection.
---

# Radio button

## When to use

Present each item in a list of options where merchants must make a single selection. Use radio buttons for mutually exclusive options.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | React.ReactNode | - | Label for the radio button (required) |
| `checked` | boolean | false | Radio button is selected |
| `disabled` | boolean | false | Disable input |
| `id` | string | - | ID for form input |
| `name` | string | - | Name for form input |
| `value` | string | - | Value for form input |
| `labelHidden` | boolean | false | Visually hide label |
| `onChange` | (newValue: boolean, id: string) => void | - | Callback when toggled |
| `onFocus` | () => void | - | Callback when focused |
| `onBlur` | () => void | - | Callback when focus removed |
| `helpText` | React.ReactNode | - | Additional helper text |
| `tone` | 'magic' | - | Tone of radio button |
| `ariaDescribedBy` | string | - | ID of describing element |
| `fill` | boolean \| Breakpoint | - | Grow to fill space |

## Examples

```jsx
import { LegacyStack, RadioButton } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function RadioButtonExample() {
  const [value, setValue] = useState('disabled');

  const handleChange = useCallback(
    (_, newValue) => setValue(newValue),
    []
  );

  return (
    <LegacyStack vertical>
      <RadioButton
        label="Accounts are disabled"
        helpText="Customers will only be able to check out as guests."
        checked={value === 'disabled'}
        id="disabled"
        name="accounts"
        onChange={handleChange}
      />
      <RadioButton
        label="Accounts are optional"
        helpText="Customers will be able to check out with a customer account or as a guest."
        id="optional"
        name="accounts"
        checked={value === 'optional'}
        onChange={handleChange}
      />
    </LegacyStack>
  );
}
```

## Best practices

- Always use with associated label component
- Be part of list with at least two or more choices
- Be used to have merchants select only one option
- Include mutually exclusive options
- List in rational order (logical, alphabetical, numerical)
- Have default option selected whenever possible

## Content guidelines

- Labels should be introduced with colon or heading
- Start with capital letter
- Not end in punctuation if single sentence/word/fragment

## Accessibility

- Screen readers convey state automatically
- Use `disabled` prop to prevent interaction
- Use unique `id` values for each radio button
- Use `labelHidden` to hide label visually but keep for assistive tech
- `ariaDescribedBy` for help text conveyed via aria-describedby
- Keyboard: Tab to focus group, Up/Down arrow keys to change selection

## Related components

- Choice list: for easier grouped radio buttons
- Select: for long lists of options
- Checkbox: for multiple selections
- Content list: for non-interactive lists
