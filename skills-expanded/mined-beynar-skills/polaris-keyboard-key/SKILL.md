---
name: polaris-keyboard-key
description: Shopify Polaris Keyboard key component. Use to educate merchants about keyboard shortcuts and hotkey combinations.
---

# Keyboard Key

## When to use
Educate merchants about keyboard shortcuts. Display keyboard combinations to explain hotkeys and available shortcuts.

## Props
- `children?` string - The key text to display
- `size?` 'small' - Size of the key. Defaults to medium.

## Examples
```jsx
import { Card, KeyboardKey } from '@shopify/polaris';

// Single key
<Card>
  <KeyboardKey>Ctrl</KeyboardKey>
</Card>

// Key combination
Press the <KeyboardKey>Ctrl</KeyboardKey> key.

// With description
<p>Keyboard shortcuts:</p>
<div>
  <KeyboardKey>Ctrl</KeyboardKey> + <KeyboardKey>S</KeyboardKey> Save
</div>
```

## Best practices
- Include a heading to introduce shortcuts (e.g., "Keyboard shortcuts")
- Include action labels describing what happens when using the key combo
- Follow content guidelines for headings
- Use consistently phrased shortcut descriptions
- Always provide context for the keyboard shortcut

## Accessibility
- Text is read by screen readers, but visual formatting isn't conveyed
- Ensure understanding without relying on visual style
- Pair keyboard key with context text
- Don't use keyboard key component alone
- Screen readers read the text content of the key

## Related components
- Tooltip (for button shortcuts)
