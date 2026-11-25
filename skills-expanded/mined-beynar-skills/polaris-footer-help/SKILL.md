---
name: polaris-footer-help
description: Shopify Polaris Footer help component. Use to display helpful, contextual information at bottom of page or form.
---

# Footer Help

## When to use
Display helpful, contextual information at bottom of page or section. Provide additional guidance or resources. Usually appears in page footer.

## Props
Core text and optional link:
- `children?` ReactNode - Help text content
- `link?` { url, label } - Optional help link

## Examples
```jsx
import { FooterHelp } from '@shopify/polaris';

// Basic text
<FooterHelp>
  Save your work by clicking the Save button at the top of the page.
</FooterHelp>

// With link
<FooterHelp>
  Learn more about
  <Link url="https://help.shopify.com">managing inventory</Link>
</FooterHelp>

// In form
<Form onSubmit={handleSubmit}>
  <FormField label="Email">
    <TextField value={email} onChange={setEmail} />
  </FormField>
  <FooterHelp>
    We'll send confirmations to this email address.
  </FooterHelp>
</Form>
```

## Best practices
- Use for non-critical guidance
- Place at bottom of related section/form
- Keep concise and helpful
- Link to detailed docs when needed
- Not for errors (use Banner or InlineError)

## Content guidelines
- Write clearly and conversationally
- Provide actionable information
- Link to relevant documentation
- Keep brief

## Accessibility
- Provides additional context for screen readers
- Text is read automatically
- Links keyboard accessible

## Related components
- Banner (for critical information)
- InlineError (for form field errors)
