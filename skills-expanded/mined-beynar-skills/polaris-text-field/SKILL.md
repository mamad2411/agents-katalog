---
name: polaris-text-field
description: Shopify Polaris Text field component. Use this skill when building text input fields, number inputs, email fields, searchable inputs, multiline text areas. A general-purpose input field supporting various text formats.
---

# Text field

## When to use

Allow merchants to provide text input when expected input is short. For longer input, use auto-grow or multiline options. Supports text, numbers, email, dates, passwords, and more.

## Props

Standard text field props with full type support:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | React.ReactNode | - | Label for text field (required) |
| `value` | string | - | Current value (required) |
| `onChange` | (value: string) => void | - | Callback on change (required) |
| `type` | string | 'text' | Input type (text, number, email, password, tel, url, date, etc.) |
| `id` | string | - | ID for form input |
| `name` | string | - | Name for form input |
| `disabled` | boolean | false | Disable input |
| `readOnly` | boolean | false | Read-only input |
| `placeholder` | string | - | Placeholder text |
| `helpText` | React.ReactNode | - | Helper text |
| `error` | any | - | Error message |
| `labelHidden` | boolean | false | Visually hide label |
| `labelAction` | Action | - | Action added to label |
| `prefix` | React.ReactNode | - | Element before input |
| `suffix` | React.ReactNode | - | Element after input |
| `multiline` | boolean \| number | false | Multiline or number of rows |
| `autoComplete` | string | - | Autocomplete attribute value |
| `autoFocus` | boolean | false | Auto focus on mount |
| `characterCount` | boolean \| number | false | Show character count |
| `clearButton` | boolean | false | Show clear button |
| `inputMode` | string | - | Virtual keyboard type |
| `maxLength` | number | - | Maximum character length |
| `minLength` | number | - | Minimum character length |
| `max` | number \| string | - | Maximum value (for number type) |
| `min` | number \| string | - | Minimum value (for number type) |
| `step` | number \| string | - | Step value (for number type) |
| `requiredIndicator` | boolean | false | Visual required indicator |
| `tone` | 'magic' | - | Tone of text field |
| `onFocus` | () => void | - | Callback on focus |
| `onBlur` | () => void | - | Callback on blur |

## Examples

```jsx
import { TextField } from '@shopify/polaris';
import { useState, useCallback } from 'react';

// Basic text field
function TextFieldExample() {
  const [value, setValue] = useState('Jaded Pixel');

  const handleChange = useCallback((newValue) => setValue(newValue), []);

  return (
    <TextField
      label="Store name"
      value={value}
      onChange={handleChange}
      autoComplete="off"
    />
  );
}

// Email field
function EmailFieldExample() {
  const [email, setEmail] = useState('');

  return (
    <TextField
      label="Email address"
      type="email"
      value={email}
      onChange={setEmail}
      autoComplete="email"
      placeholder="example@shopify.com"
    />
  );
}

// Number field
function NumberFieldExample() {
  const [count, setCount] = useState('');

  return (
    <TextField
      label="Product quantity"
      type="number"
      value={count}
      onChange={setCount}
      min={0}
      step={1}
      inputMode="numeric"
    />
  );
}

// Multiline
function MultilineFieldExample() {
  const [description, setDescription] = useState('');

  return (
    <TextField
      label="Product description"
      value={description}
      onChange={setDescription}
      multiline={4}
    />
  );
}

// With character count
function CharacterCountExample() {
  const [text, setText] = useState('');

  return (
    <TextField
      label="Meta description"
      value={text}
      onChange={setText}
      characterCount={160}
      maxLength={160}
      helpText="SEO descriptions work best at 160 characters"
    />
  );
}
```

## Best practices

- Be clearly labeled so merchants know what to enter
- Label as "Optional" when not required
- Only ask for information that's really needed
- Validate as soon as merchants finish interacting (but not before)
- Always add autocomplete attribute if type is: text, email, password, number, url, tel, date, etc.

## Autocomplete guidance

- Enable browser autofill for better UX (users complete forms 30% faster)
- Use appropriate autocomplete values from WHATWG spec
- Use `autocomplete="off"` or `autocomplete="nope"` to disable autofill if needed
- Chrome supports "nope" value better than "off"
- Include `name` attribute when using `autocomplete="nope"`

## Virtual keyboard

- Use `inputMode` to select appropriate virtual keyboard for mobile
- Options: text, email, numeric, decimal, tel, search, url

## Accessibility

- Screen readers convey information automatically
- Use `disabled` prop to disable and convey inactive state
- Use `readOnly` prop for read-only fields
- Use `type` prop to adapt software keyboards for accessibility
- Use unique `id` values (auto-generated if not provided)
- Required `label` prop conveys purpose to all merchants
- Use `labelHidden` to visually hide label but keep for assistive tech
- Help text and error messages conveyed via aria-describedby
- Use placeholder for additional instructions, not critical info
- Don't rely on placeholder alone

## Keyboard support

- Tab to move focus between fields (or Shift+Tab backwards)
- Number type: Up/Down arrow keys to adjust value
- Disabled fields: can't receive focus or be edited
- ReadOnly fields: can receive focus but not be edited
- autoFocus: generally avoid (can skip other important controls)

## Content guidelines

See text fields experience page for full content guidelines.

## Related components

- Form layout: for responsive form field arrangement
- Inline error: for separate validation errors
- Select: often connected to left/right of text field
