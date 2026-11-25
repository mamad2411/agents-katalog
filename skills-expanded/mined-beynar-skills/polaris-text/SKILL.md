---
name: polaris-text
description: Shopify Polaris Text component. Use for typography establishing hierarchy and communicating important content. Replaces DisplayText, Heading, Caption.
---

# Text

## When to use
Establish hierarchy and communicate important content via typography. Create clear visual patterns. Replaces legacy DisplayText, Heading, Subheading, Caption, TextStyle, VisuallyHidden.

## Props
- `alignment?` 'start' | 'center' | 'end' | 'justify' - Horizontal text alignment
- `as` 'dt' | 'dd' | 'h1'-'h6' | 'p' | 'span' | 'strong' | 'legend' - Semantic element type
- `breakWord?` boolean - Prevent text overflow
- `children` ReactNode - Text content
- `tone?` 'base' | 'disabled' | 'inherit' | 'success' | 'critical' | 'caution' | 'subdued' | 'text-inverse' | 'text-inverse-secondary' | 'magic' | 'magic-subdued'
- `fontWeight?` 'regular' | 'medium' | 'semibold' | 'bold'
- `id?` string - HTML id attribute
- `numeric?` boolean - Use numeric monospace variant
- `truncate?` boolean - Truncate with ellipsis
- `variant?` heading | body variants (see below)
- `visuallyHidden?` boolean - Visually hide text
- `textDecorationLine?` "line-through" - Add strikethrough

## Variants (Heading)
- `heading3xl` (36px, bold) - Responsive
- `heading2xl` (30px, bold) - Responsive
- `headingXl` (24px, bold) - Responsive
- `headingLg` (20px, semibold) - Responsive
- `headingMd` (14px, semibold)
- `headingSm` (13px, semibold)
- `headingXs` (12px, semibold)

## Variants (Body)
- `bodyLg` (14px, regular)
- `bodyMd` (13px, regular)
- `bodySm` (12px, regular)
- `bodyXs` (11px, regular)

## Examples
```jsx
import { Text } from '@shopify/polaris';

// Headings
<Text variant="heading3xl" as="h1">Main title</Text>
<Text variant="headingLg" as="h2">Section heading</Text>

// Body text
<Text variant="bodyMd" as="p">Regular paragraph text</Text>

// With styling
<Text tone="subdued" variant="bodySm">Secondary text</Text>
<Text fontWeight="semibold">Bold text</Text>
<Text tone="critical">Error message</Text>

// Alignment
<Text alignment="center" variant="bodyMd">Centered text</Text>

// Numeric
<Text numeric>1,234.56</Text>

// Truncate
<Text truncate variant="bodyMd">Long text...</Text>

// Visually hidden
<Text visuallyHidden as="h2">Hidden from view</Text>
```

## Best practices
- Headings: clearly describe section, highlight important info, sit at top
- Captions: use bodySm for secondary labels, timestamps (few words only)
- Text styles: enhance meaning, use subdued for less important, warning for attention-needed
- Semibold for input fields or row totals
- Pair with symbols (arrows, $) for success/critical

## Accessibility
- Nested Text inherits properties from parent
- visuallyHidden: for extra context when semantic markup insufficient
- Use semantic element (as prop) for proper HTML structure
- Don't use visuallyHidden to hide critical info

## Migration from legacy
- DisplayText small → headingLg
- DisplayText medium → headingXl
- DisplayText large → heading2xl
- Heading → headingMd
- Subheading → headingSm
- Caption → bodySm
- TextStyle subdued → tone="subdued"
- TextStyle positive → tone="success"
- TextStyle critical → tone="critical"

## Related components
- Use appropriate `as` prop for semantic HTML
