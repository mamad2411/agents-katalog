---
name: polaris-color-picker
description: Shopify Polaris Color picker component. Use this skill when merchants need to visually select colors, customize email template colors, brand color selection. Makes color selection a visual task rather than a technical one.
---

# Color picker

## When to use

Let merchants select a color visually. Use when merchants need to customize colors like email template accent colors or brand colors for their shop.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | Color | - | Currently selected color (required) |
| `onChange` | (color: HSBAColor) => void | - | Callback when color selected (required) |
| `id` | string | - | ID for the element |
| `allowAlpha` | boolean | false | Allow user to select alpha (transparency) value |
| `fullWidth` | boolean | false | Allow hue picker to take full width |

## Color object structure

```typescript
interface HSBAColor {
  hue: number;       // 0-360
  saturation: number; // 0-1
  brightness: number; // 0-1
  alpha?: number;    // 0-1 (optional)
}
```

## Examples

```jsx
import { ColorPicker } from '@shopify/polaris';
import { useState } from 'react';

function ColorPickerExample() {
  const [color, setColor] = useState({
    hue: 120,
    brightness: 1,
    saturation: 1,
  });

  return (
    <ColorPicker onChange={setColor} color={color} />
  );
}

// With alpha (transparency)
function ColorPickerWithAlpha() {
  const [color, setColor] = useState({
    hue: 120,
    brightness: 1,
    saturation: 1,
    alpha: 1,
  });

  return (
    <ColorPicker
      onChange={setColor}
      color={color}
      allowAlpha
    />
  );
}
```

## Best practices

- Use alpha slider if allowing merchants to select transparent colors
- Use visual selection to reduce friction in color choice

## Accessibility

- Visual selection aids merchants with difficulty using technical color inputs

## Related components

- Form layout: for arranging color picker in forms
- Text field: for manual color value entry (hex codes)
