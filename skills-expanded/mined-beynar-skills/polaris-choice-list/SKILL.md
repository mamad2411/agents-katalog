---
name: polaris-choice-list
description: Shopify Polaris Choice list component. Use this skill when building grouped radio buttons or checkboxes, single or multiple selection lists. Groups related interactive choices together.
---

# Choice list

## When to use

Create a list of grouped radio buttons or checkboxes. Use when you need to group together a related list of interactive choices where merchants select one or more options.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | React.ReactNode | - | Label for list of choices (required) |
| `choices` | Choice[] | - | Collection of choices |
| `selected` | string[] | - | Collection of selected choices |
| `name` | string | - | Name for form input |
| `allowMultiple` | boolean | false | Allow multiple selections at once |
| `titleHidden` | boolean | false | Toggle display of title |
| `error` | any | - | Display error message |
| `disabled` | boolean | false | Disable all choices |
| `onChange` | (selected: string[], name: string) => void | - | Callback when selections change |
| `tone` | 'magic' | - | Tone of choice list |

## Examples

```jsx
import { ChoiceList } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function SingleChoiceListExample() {
  const [selected, setSelected] = useState(['hidden']);

  const handleChange = useCallback(
    (value) => setSelected(value),
    []
  );

  return (
    <ChoiceList
      title="Company name"
      choices={[
        { label: 'Hidden', value: 'hidden' },
        { label: 'Optional', value: 'optional' },
        { label: 'Required', value: 'required' },
      ]}
      selected={selected}
      onChange={handleChange}
    />
  );
}
```

## Best practices

- Include a title explaining available options
- Label options clearly based on what they do
- Avoid mutually exclusive options when allowing multiple selection

## Content guidelines

- Help merchants understand how items are grouped
- Keep titles to single sentence
- End title with colon if it introduces the list
- Write in sentence case (first word capitalized)
- Don't use commas or semicolons at end of each line

## Accessibility

Uses accessibility features of checkbox and radio button components.

- Based on ARIA patterns
- Keyboard: Tab to focus, Space/Arrow keys to interact
- Label must convey purpose

## Related components

- Select: for long lists or constrained space
- Radio button: for custom layout radio buttons
- Checkbox: for custom layout checkboxes
- List component: for simple non-interactive lists
