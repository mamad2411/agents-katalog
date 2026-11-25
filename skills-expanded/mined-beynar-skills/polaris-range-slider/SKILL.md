---
name: polaris-range-slider
description: Shopify Polaris Range slider component. Use this skill when merchants need to select numeric values within a range, single or dual-thumb sliders, opacity/percentage inputs. An input field for selecting numeric values between min and max.
---

# Range slider

## When to use

Let merchants select a numeric value within a given range (minimum and maximum values). Use for single values between 0-100 or dual-thumb ranges.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | ReactNode | - | Label for range input (required) |
| `value` | number \| [number, number] | - | Initial value(s) for range input |
| `id` | string | - | ID for range input |
| `min` | number | - | Minimum possible value |
| `max` | number | - | Maximum possible value |
| `step` | number | - | Increment value for changes |
| `output` | boolean | false | Provide tooltip showing current value |
| `helpText` | ReactNode | - | Additional text to aid use |
| `error` | any | - | Display error message |
| `disabled` | boolean | false | Disable input |
| `prefix` | ReactNode | - | Element before input |
| `suffix` | ReactNode | - | Element after input |
| `labelAction` | Action | - | Action added to label |
| `labelHidden` | boolean | false | Visually hide label |
| `onChange` | (value: number \| [number, number], id: string) => void | - | Callback on change |
| `onFocus` | () => void | - | Callback on focus |
| `onBlur` | () => void | - | Callback on blur |

## Examples

```jsx
import { LegacyCard, RangeSlider } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function RangeSliderExample() {
  const [rangeValue, setRangeValue] = useState(32);

  const handleRangeSliderChange = useCallback(
    (value) => setRangeValue(value),
    []
  );

  return (
    <LegacyCard sectioned title="Background color">
      <RangeSlider
        label="Opacity percentage"
        value={rangeValue}
        onChange={handleRangeSliderChange}
        output
      />
    </LegacyCard>
  );
}

// Dual thumb (range)
function DualThumbRangeSlider() {
  const [range, setRange] = useState([20, 80]);

  return (
    <RangeSlider
      label="Price range"
      value={range}
      onChange={setRange}
      min={0}
      max={100}
      step={5}
      output
      prefix="$"
    />
  );
}
```

## Best practices

- Always use with label, even if hidden
- When label visible, clearly communicate purpose and values
- Label as "Optional" when not required
- Validate as soon as merchants finish interacting
- For dual thumbs, use two text field alternatives for accessibility

## Content guidelines

- Labels: short (1-3 words), sentence case, placed above field
- Optional fields: add "(optional)" at end of label
- Help text: succinct, easy to read, clarify purpose
- Error messages: explain issue and fix, passive voice, single sentence

## Accessibility

- Provides large click and tap target for slider thumb
- Merchants can tap track to move closest thumb
- Single-thumb: uses ARIA 1.1 slider pattern on HTML `<input type="range">`
- Dual-thumb: ARIA 1.1 multi-thumb pattern, but not consistently supported on mobile
  - Best practice: pair with text fields for accessibility or provide alternative input method

## Keyboard support

- Tab to move focus to slider thumb
- Up/Down or Left/Right arrow keys to move thumb when focused

## Related components

- Text field: for manual numeric entry
