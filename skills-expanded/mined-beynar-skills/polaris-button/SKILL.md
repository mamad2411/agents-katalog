---
name: polaris-button
description: Shopify Polaris Button component. Use for primary actions like Add, Save, Delete. Plain variants for secondary actions. Supports icons, loading, disabled states.
---

# Button

## When to use
Use for actions like "Add", "Close", "Cancel", "Save". Use plain variants for less important actions like "view settings". Use links for navigation within sentences.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | string \| string[] | - | Content to display inside button |
| size | 'medium' \| 'large' \| 'micro' \| 'slim' | 'medium' | Button size with padding |
| variant | 'primary' \| 'secondary' \| 'tertiary' \| 'plain' \| 'monochromePlain' | - | Visual appearance |
| tone | 'success' \| 'critical' | - | Color treatment (critical for dangerous actions) |
| disabled | boolean | false | Disable button interaction |
| loading | boolean | false | Show spinner while action is processing |
| pressed | boolean | - | Pressed state for toggle buttons |
| url | string | - | Destination link (renders as anchor) |
| external | boolean | false | Open link in new tab |
| download | string \| boolean | - | Download file instead of navigating |
| submit | boolean | false | Submit form |
| icon | any | - | Icon to display left of text |
| disclosure | boolean \| 'up' \| 'down' \| 'select' | false | Show disclosure icon |
| fullWidth | boolean | false | Grow to container width |
| textAlign | 'start' \| 'center' \| 'end' | - | Inner text alignment |
| accessibilityLabel | string | - | Screen reader label |
| onClick | () => unknown | - | Click callback |
| onFocus | () => void | - | Focus callback |
| onBlur | () => void | - | Blur callback |

## Examples

```jsx
import { Button } from '@shopify/polaris';

// Basic button
<Button>Add product</Button>

// Primary action
<Button variant="primary">Save</Button>

// Dangerous action
<Button tone="critical">Delete</Button>

// Loading state
<Button loading>Saving...</Button>

// Disabled
<Button disabled>Unavailable</Button>

// Link button
<Button url="https://example.com">Learn more</Button>

// External link with icon
<Button
  url="https://example.com"
  external
  accessibilityLabel="Terms (opens new window)"
>
  Terms
</Button>

// Icon button
<Button icon={EditIcon}>Edit</Button>

// Icon only
<Button icon={DeleteIcon} accessibilityLabel="Delete" />

// Full width
<Button fullWidth>Continue</Button>

// Disclosure
<Button disclosure>More</Button>
```

## Best practices

- Use clear, actionable verbs (Add, Save, Delete, not "Click here")
- Prioritize important actions - primary variant for most important
- Use red/critical only for difficult-to-undo actions
- Place buttons in consistent locations
- Position primary action first
- Use sentence case (capitalize first word only)
- No articles (a, an, the)
- No punctuation
- Use established button colors appropriately
- Limit calls to action to avoid confusion

## Accessibility

- Use `accessibilityLabel` when button text doesn't convey purpose or for icon-only buttons
- Use `ariaControls` to point to managed content ID
- Use `ariaExpanded` for expand/collapse buttons
- Use `disabled` prop for inactive buttons
- Use `pressed` prop for toggle buttons (adds aria-pressed)
- Keyboard: Tab/Shift+Tab to focus, Enter/Space to activate
- For external links: include "(opens new window)" in label
- Don't use custom key events unless necessary - document if you do

## Related components

- [ButtonGroup](../button-group) - for multiple related buttons
- [Link](https://polaris.shopify.com/components/link) - for navigation within text
