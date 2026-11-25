---
name: polaris-list
description: Shopify Polaris List component. Use for text-only related items. Display bulleted or numbered lists with consistent phrasing.
---

# List

## When to use
Display set of related text-only content. Each item begins with bullet or number. Use for scannable information without icons or other indicators.

## Props
- `gap?` 'extraTight' | 'loose' - Space between items. Defaults to 'loose'.
- `type?` 'bullet' | 'number' - List style. Defaults to 'bullet'.
- `children?` ReactNode - List.Item elements

## Subcomponents
- `List.Item` - Individual list item

## Examples
```jsx
import { List } from '@shopify/polaris';

// Bulleted
<List type="bullet">
  <List.Item>Yellow shirt</List.Item>
  <List.Item>Red shirt</List.Item>
  <List.Item>Green shirt</List.Item>
</List>

// Numbered
<List type="number">
  <List.Item>First step</List.Item>
  <List.Item>Second step</List.Item>
  <List.Item>Third step</List.Item>
</List>

// Extra tight spacing
<List gap="extraTight" type="bullet">
  <List.Item>Item 1</List.Item>
  <List.Item>Item 2</List.Item>
</List>
```

## Best practices
- Break up related content chunks for scanning
- Use consistent phrasing (start with noun or verb)
- Not for action-oriented lists
- Use when order doesn't matter (bullet) or matters (number)

## Content guidelines
- Start each item with capital letter
- No commas/semicolons at end of lines
- Write in sentence case
- Each item consistent in structure
- Avoid "Item One", use "Item one"

## Accessibility
- Produces <ul> (bullet) or <ol> (number)
- Items as <li> conveyed as related group
- For layout-only grouping, use VerticalStack

## Related components
- ChoiceList (for checkboxes/radio buttons)
- ResourceList (for objects/collections)
- DescriptionList (for terms with descriptions)
