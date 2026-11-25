---
name: polaris-button-group
description: Shopify Polaris ButtonGroup component. Use to space and arrange multiple related action buttons evenly with consistent spacing.
---

# ButtonGroup

## When to use
Use to group related buttons together with proper spacing and alignment. Combine up to 6 icon-only buttons or more text buttons. Consider mobile layout when using multiple buttons.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Button components to group |
| gap | 'extraTight' \| 'tight' \| 'loose' | - | Space between buttons |
| variant | 'segmented' | - | Segmented styling for button group |
| fullWidth | boolean | false | Buttons stretch to fill container |
| connectedTop | boolean | false | Remove top border radius |
| noWrap | boolean | false | Prevent wrapping to next line |

## Examples

```jsx
import { ButtonGroup, Button } from '@shopify/polaris';

// Basic group
<ButtonGroup>
  <Button>Cancel</Button>
  <Button variant="primary">Save</Button>
</ButtonGroup>

// Segmented buttons
<ButtonGroup variant="segmented">
  <Button>Day</Button>
  <Button>Week</Button>
  <Button>Month</Button>
</ButtonGroup>

// Full width
<ButtonGroup fullWidth>
  <Button>Decline</Button>
  <Button variant="primary">Accept</Button>
</ButtonGroup>

// With gap control
<ButtonGroup gap="loose">
  <Button>Cancel</Button>
  <Button variant="primary">Save</Button>
</ButtonGroup>

// Multiple action groups
<ButtonGroup>
  <Button>Edit</Button>
  <Button>Duplicate</Button>
  <Button variant="primary" tone="critical">Delete</Button>
</ButtonGroup>
```

## Best practices

- Use only buttons that follow button component best practices
- Group buttons that have a relationship (Cancel/Save, Yes/No)
- Limit groups to avoid overwhelming merchants with options
- Consider mobile appearance - buttons may wrap
- Max 6 icon-only buttons in a group
- Too many buttons cause confusion - prioritize
- Place primary action last in left-to-right layouts
- Ensure adequate spacing between groups

## Content guidelines

Follow button component content guidelines: clear verbs, sentence case, no articles, no punctuation.

## Related components

- [Button](../button) - individual button component
- [Link](https://polaris.shopify.com/components/link) - for navigation
