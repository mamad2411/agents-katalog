---
name: polaris-inline-error
description: Shopify Polaris Inline error component. Use this skill when displaying form validation errors, field-specific error messages, in-context error feedback. Shows brief messages that explain what went wrong with a form input.
---

# Inline error

## When to use

Display brief, in-context messages that tell merchants something went wrong with a single or group of inputs in a form. Use to help merchants understand why a form input may not be valid and how to fix it.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `message` | any | - | Content briefly explaining how to resolve invalid input (required) |
| `fieldID` | string | - | Unique identifier of the invalid form field |

## Examples

```jsx
import { InlineError } from '@shopify/polaris';

function InlineErrorExample() {
  return (
    <InlineError
      message="Store name is required"
      fieldID="myFieldID"
    />
  );
}

// With form field
import { TextField, InlineError } from '@shopify/polaris';
import { useState } from 'react';

function FormWithError() {
  const [value, setValue] = useState('');
  const [error, setError] = useState(false);

  const handleBlur = () => {
    if (!value) {
      setError(true);
    }
  };

  return (
    <div>
      <TextField
        id="storeName"
        label="Store name"
        value={value}
        onChange={setValue}
        onBlur={handleBlur}
      />
      {error && (
        <InlineError
          message="Store name is required"
          fieldID="storeName"
        />
      )}
    </div>
  );
}
```

## Best practices

- Be brief and written in sentence case
- Be visible immediately upon invalid input
- Be removed as soon as input becomes valid
- Describe specific solutions for successful completion
- Not be placed out of context from the input
- Be placed directly below the source of problem

## Content guidelines

- Clearly explain what went wrong
- Optionally clarify what to do next
- Keep to single sentence, short and concise
- Use passive voice so merchants don't feel blamed
- Don't say "You didn't enter" - say "Store name is required"

## Accessibility

- Use required `fieldID` prop to tie error to form field with aria-describedby
- Use required `message` prop for error description text
- Error icon helps visually identify error for merchants with color blindness

## Related components

- Exception list: for list of exceptions describing a resource
- Banner: for more prominent error messaging
- Form: for form container
