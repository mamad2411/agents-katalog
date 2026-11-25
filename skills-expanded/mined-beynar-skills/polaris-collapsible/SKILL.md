---
name: polaris-collapsible
description: Shopify Polaris Collapsible component. Use for show/hide long sections. Merchants can expand or collapse content.
---

# Collapsible

## When to use
Hide long sections under expandable block. Merchants expand or collapse as needed. Use for lower priority or optional information not always needed.

## Props
- `id` string - Unique ID for collapsible (required for accessibility)
- `expandOnPrint?` boolean - Show content when printing. Defaults to false.
- `open` boolean - Toggle expanded state
- `variant?` 'inline' | 'block' - Collapse direction. Defaults to 'block'.
- `transition?` boolean | Transition - Animation config. Defaults to ease-in-out 150ms.
  - Pass false to disable transition
  - Or customize: `{ duration: '500ms', timingFunction: 'ease-in' }`
- `onAnimationEnd?` () => void - Complete animation callback
- `children?` ReactNode - Collapsible content

## Examples
```jsx
import { Collapsible, Button } from '@shopify/polaris';
import { useState } from 'react';

function CollapsibleExample() {
  const [open, setOpen] = useState(true);

  return (
    <div>
      <Button
        onClick={() => setOpen(!open)}
        ariaExpanded={open}
        ariaControls="content-collapsible"
      >
        Toggle
      </Button>

      <Collapsible
        open={open}
        id="content-collapsible"
        transition={{ duration: '500ms' }}
      >
        <div>
          Your mailing list lets you contact interested customers
          with exclusive offers.
        </div>
      </Collapsible>
    </div>
  );
}

// With custom transition
<Collapsible
  open={open}
  id="custom-transition"
  transition={{ duration: '300ms', timingFunction: 'ease-out' }}
>
  Content
</Collapsible>

// No animation
<Collapsible open={open} id="no-transition" transition={false}>
  Content
</Collapsible>
```

## Best practices
- Use for lower priority information
- Not for errors/critical info (show always)
- Place content immediately after trigger button
- Use id prop for accessibility
- Pair with Button component
- Show/hide with controlled state

## Content guidelines
- Organize optional/secondary information
- Clear expand/collapse labels on trigger
- Provide context for collapsed content

## Accessibility
- Required id prop for unique identification
- Use button with ariaExpanded prop for toggle
- Use ariaControls to link button to collapsible
- Clear indication of expanded/collapsed state
- Keyboard accessible (Tab to button, Space to toggle)

## Related components
- Button (to control collapsible)
- Scrollable (for scrollable long content)
