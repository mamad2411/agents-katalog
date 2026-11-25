---
name: polaris-form
description: Shopify Polaris Form component. Use this skill when building form wrappers, handling form submission, managing form state. A wrapper component that handles submission of forms.
---

# Form

## When to use

Wrap form input elements to handle form submission. Use as a wrapper around all form input elements with custom onSubmit callback.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | React.ReactNode | - | Content to display inside form |
| `onSubmit` | (event: React.FormEvent<HTMLFormElement>) => unknown | - | Callback when form submitted (required) |
| `acceptCharset` | string | - | Space-separated character encodings |
| `action` | string | - | Where to send form-data on submit |
| `autoComplete` | boolean | true | Allow browser autocomplete |
| `encType` | 'application/x-www-form-urlencoded' \| 'multipart/form-data' \| 'text/plain' | - | Media type for submit |
| `implicitSubmit` | boolean | true | Submit on Enter in text fields |
| `method` | 'post' \| 'get' \| 'action' | 'post' | HTTP method for submit |
| `name` | string | - | Unique form name |
| `noValidate` | boolean | false | Skip validation on submit |
| `preventDefault` | boolean | false | Block default form action |
| `target` | string | - | Where to display response |

## Examples

```jsx
import { Form, FormLayout, Checkbox, TextField, Button } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function FormOnSubmitExample() {
  const [newsletter, setNewsletter] = useState(false);
  const [email, setEmail] = useState('');

  const handleSubmit = useCallback(() => {
    setEmail('');
    setNewsletter(false);
  }, []);

  const handleNewsLetterChange = useCallback(
    (value) => setNewsletter(value),
    []
  );

  const handleEmailChange = useCallback((value) => setEmail(value), []);

  return (
    <Form onSubmit={handleSubmit}>
      <FormLayout>
        <Checkbox
          label="Sign up for the Polaris newsletter"
          checked={newsletter}
          onChange={handleNewsLetterChange}
        />
        <TextField
          value={email}
          onChange={handleEmailChange}
          label="Email"
          type="email"
          autoComplete="email"
          helpText={
            <span>
              We'll use this email address to inform you on future changes to Polaris.
            </span>
          }
        />
        <Button submit>Submit</Button>
      </FormLayout>
    </Form>
  );
}
```

## Best practices

- Wrap all form input elements
- Use with FormLayout for standard spacing
- Use onSubmit callback instead of default action

## Accessibility

- Wraps content in native HTML `<form>` element
- Supports assistive technologies
- Forms can have only one submit button at end
- By default, buttons get type="button" to avoid conflicts
- Set submit prop on button to make it type="submit"
- By default, implicitSubmit=true allows Enter key to submit

## Keyboard support

- By default, implicitSubmit=true: merchants can submit with Enter key in text fields
- Set implicitSubmit=false if this behavior doesn't fit

## Related components

- FormLayout: for arranging fields with standard spacing
- Text field, Checkbox, etc.: form input components
