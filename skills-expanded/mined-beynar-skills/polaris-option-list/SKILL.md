---
name: polaris-option-list
description: Shopify Polaris Option list component. Use to create grouped selectable items. Single or multiple selection. Usually in popover/modal.
---

# Option List

## When to use
Create list of grouped items merchants can pick from. Single or multiple selection. Usually appears in popover, modal, or sidebar. Styled differently from ChoiceList.

## Props
- `id?` string - Unique identifier
- `title?` string - List title
- `options?` OptionDescriptor[] - Collection of options with value, label, disabled
- `role?` string - ARIA role attribute
- `sections?` SectionDescriptor[] - Sectioned options with header
- `selected` string[] - Selected option values
- `allowMultiple?` boolean - Allow multiple selection
- `verticalAlign?` 'top' | 'center' | 'bottom' - Vertical alignment
- `onChange` (selected: string[]) => void - Selection change callback
- `onPointerEnterOption?` (selected: string) => void - Pointer enter callback
- `onFocusOption?` (selected: string) => void - Focus callback

## Examples
```jsx
import { OptionList, Card } from '@shopify/polaris';
import { useState } from 'react';

function OptionListExample() {
  const [selected, setSelected] = useState([]);

  return (
    <Card>
      <OptionList
        title="Inventory Location"
        options={[
          { value: 'byward', label: 'Byward Market' },
          { value: 'centretown', label: 'Centretown' },
          { value: 'westboro', label: 'Westboro' },
        ]}
        selected={selected}
        onChange={setSelected}
      />
    </Card>
  );
}

// Multiple selection
<OptionList
  allowMultiple
  options={options}
  selected={selected}
  onChange={setSelected}
/>

// Sectioned
<OptionList
  sections={[
    {
      title: 'Cities',
      options: [{ value: '1', label: 'Ottawa' }],
    },
  ]}
  selected={selected}
  onChange={setSelected}
/>
```

## Best practices
- Place on its own in container (like popover)
- Don't place other components in same container
- Not when Select component will do
- Use for grouped selections

## Content guidelines
- Clear and descriptive options
- "Traffic referrer source" not "Source"

## Accessibility
- Items as <li> in <ul> (related group)
- Single selection: buttons
- Multiple selection: checkboxes
- Custom roles supported per W3C ARIA spec

## Related components
- ActionList (for action lists)
- ChoiceList (for form checkboxes/radio)
- Select (for simple single choice)
- Listbox (for custom interactive lists)
