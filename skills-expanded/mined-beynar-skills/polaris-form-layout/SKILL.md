---
name: polaris-form-layout
description: Shopify Polaris FormLayout component. Use to arrange form fields vertically with standard spacing for easier scanning and completion.
---

# FormLayout

## When to use
Use to stack form fields vertically with consistent spacing. Makes forms easier to scan and complete. Can group fields horizontally with FormLayout.Group.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | Form content (fields and field groups) |

## Examples

```jsx
import { FormLayout, TextField, Button, Text } from '@shopify/polaris';

// Basic form layout
<FormLayout>
  <TextField
    label="Store name"
    onChange={() => {}}
    autoComplete="off"
  />
  <TextField
    type="email"
    label="Account email"
    onChange={() => {}}
    autoComplete="email"
  />
  <TextField
    label="Phone"
    onChange={() => {}}
    autoComplete="tel"
  />
</FormLayout>

// With field groups
<FormLayout>
  <FormLayout.Group condensed>
    <TextField label="First name" onChange={() => {}} />
    <TextField label="Last name" onChange={() => {}} />
  </FormLayout.Group>

  <TextField
    label="Email"
    type="email"
    onChange={() => {}}
  />

  <TextField
    label="Password"
    type="password"
    onChange={() => {}}
  />
</FormLayout>

// With sections
<FormLayout>
  <Text as="h2" variant="headingMd">Account information</Text>
  <TextField label="Business name" onChange={() => {}} />
  <TextField label="Email address" onChange={() => {}} />

  <Text as="h2" variant="headingMd">Address</Text>
  <TextField label="Street address" onChange={() => {}} />
  <FormLayout.Group>
    <TextField label="City" onChange={() => {}} />
    <TextField label="Zip code" onChange={() => {}} />
  </FormLayout.Group>
</FormLayout>

// Full form with actions
<Card>
  <Box padding="600">
    <FormLayout>
      <Text as="h1" variant="headingLg">Create account</Text>

      <TextField
        label="Email"
        type="email"
        onChange={() => {}}
        autoComplete="email"
      />

      <TextField
        label="Password"
        type="password"
        onChange={() => {}}
        autoComplete="new-password"
      />

      <FormLayout.Group>
        <TextField label="First name" onChange={() => {}} />
        <TextField label="Last name" onChange={() => {}} />
      </FormLayout.Group>

      <BlockStack gap="300">
        <Button variant="primary">Create account</Button>
        <Button>Cancel</Button>
      </BlockStack>
    </FormLayout>
  </Box>
</Card>
```

## FormLayout.Group

Group fields horizontally on larger screens.

```jsx
<FormLayout.Group>
  <TextField label="First name" />
  <TextField label="Last name" />
</FormLayout.Group>

// Condensed (tighter spacing)
<FormLayout.Group condensed>
  <TextField label="City" />
  <TextField label="Zip" />
</FormLayout.Group>
```

## Best practices

- Only ask for required information
- Group related fields under section titles
- Follow logical, predictable order
- Be respectful of merchant time
- Use clear, short field labels (1-3 words)
- Provide help text for complex fields
- Label should describe what's expected, not instructions
- Use sentence case for labels

## Content guidelines

**Form section title**: Follow heading guidelines

**Field label**:
- Short and succinct (1-3 words)
- Sentence case
- Placed above or beside field
- Not instructions, just description

**Help text**:
- Extra guidance for complex fields
- Easy to ignore, don't require depending on it
- Succinct and easy to read

## Related components

- [TextField](https://polaris.shopify.com/components/textfield) - text input field
- [Layout](../layout) - page-level layout
- [BlockStack](../block-stack) - for spacing sections
- [Card](../card) - form container
