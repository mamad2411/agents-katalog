---
name: polaris-description-list
description: Shopify Polaris Description list component. Use to organize and explain related information. Useful for glossaries and term definitions.
---

# Description List

## When to use
Organize and explain related information. List and define terms such as in a glossary. Present merchants with items and descriptions side-by-side.

## Props
- `items` Item[] - Collection of term/description pairs
  - `term` string - Term to define
  - `description` ReactNode - Definition/explanation
- `gap?` 'tight' | 'loose' - Spacing between items. Defaults to 'loose'.

## Examples
```jsx
import { DescriptionList } from '@shopify/polaris';

<DescriptionList
  items={[
    {
      term: 'Logistics',
      description: 'The management of products or resources as they travel between origin and destination.',
    },
    {
      term: 'Sole proprietorship',
      description: 'A business structure where a single individual owns and runs the company.',
    },
    {
      term: 'Discount code',
      description: 'A series of numbers/letters entered at checkout for discounts or special offers.',
    },
  ]}
/>

// Tight spacing
<DescriptionList gap="tight" items={items} />
```

## Best practices
- Contain terms and associated explanations
- Provide non-action-oriented information
- Avoid unnecessarily complicated language
- Not for upselling features
- Use for glossaries, definitions, reference

## Content guidelines
- Terms: sentence case ("Discount code" not "Discount Code")
- Descriptions: directly related, describe benefit, 1-2 sentences
- Write in sentence case with punctuation
- Conversational (use articles: the, a, an)
- Use plain language

## Accessibility
- Produces <dl> wrapper with <dt> (term) and <dd> (definition)
- Conveys relationships to assistive tech

## Related components
- ActionList (for action-based lists)
- List (for text-only lists)
