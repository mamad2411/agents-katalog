---
name: polaris-listbox
description: Shopify Polaris Listbox component. Use for vertical interactive options list. Room for icons, descriptions, and custom elements.
---

# Listbox

## When to use
Display vertical list of interactive options. Allow merchants to select from options. Use with Combobox or as standalone. Room for icons and descriptions.

## Props
- `children` ReactNode - List.Option elements
- `autoSelection?` AutoSelection - Default active option. Defaults to FirstSelected.
- `enableKeyboardControl?` boolean - Explicitly enable keyboard control
- `accessibilityLabel?` string - Screen reader text
- `customListId?` string - Custom ID for list element
- `onSelect?` (value: string) => void - Selection callback
- `onActiveOptionChange?` (value: string, domId: string) => void - Active option change callback

## Subcomponents
- `Listbox.Option` - Individual option with value prop
- `Listbox.Divider` - Separator between items
- `Listbox.Header` - Section header

## Examples
```jsx
import { Listbox } from '@shopify/polaris';

<Listbox accessibilityLabel="Choose option">
  <Listbox.Option value="1">Item 1</Listbox.Option>
  <Listbox.Option value="2">Item 2</Listbox.Option>
  <Listbox.Option value="3">Item 3</Listbox.Option>
</Listbox>

// With sections
<Listbox>
  <Listbox.Header>Group 1</Listbox.Header>
  <Listbox.Option value="1">Option 1</Listbox.Option>
  <Listbox.Divider />
  <Listbox.Header>Group 2</Listbox.Header>
  <Listbox.Option value="2">Option 2</Listbox.Option>
</Listbox>

// With selection handler
<Listbox onSelect={(value) => setSelected(value)}>
  ...
</Listbox>
```

## Best practices
- Be clearly labeled
- Limit options displayed at once
- Indicate loading state while populating
- Don't place interactive elements inside options
- Use labels, not interactive elements

## Anatomy
- Options: selectable items
- Dividers: visual separators
- Section headers: group content

## Accessibility
- Based on ARIA 1.2 Listbox pattern
- Arrow keys navigate
- Enter/Return to select
- Don't use interactive elements inside
- Clear labels required

## Related components
- Combobox (text field + listbox)
- Autocomplete (convenience wrapper)
- OptionList (for simpler selections)
