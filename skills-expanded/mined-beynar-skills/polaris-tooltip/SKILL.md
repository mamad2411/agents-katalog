---
name: polaris-tooltip
description: Shopify Polaris Tooltip component. Use to display helpful information on hover/focus. Explain UI elements, keyboard shortcuts, or provide tips.
---

# Tooltip

## When to use
Display helpful information on hover or focus. Explain UI elements, keyboard shortcuts, or provide contextual tips. Keep explanations brief.

## Props
- `children` ReactNode - Element tooltip appears on
- `content` string | ReactNode - Tooltip text/content
- `preferredPosition?` 'above' | 'below' | 'left' | 'right' - Position preference
- `activationDelay?` number - Delay before showing (ms). Defaults to 1000.
- `dismissOnMouseOut?` boolean - Close on mouse leave. Defaults to true.

## Examples
```jsx
import { Tooltip, Button, Icon } from '@shopify/polaris';
import { QuestionMarkIcon } from '@shopify/polaris-icons';

// Basic button tooltip
<Tooltip content="Save your changes">
  <Button primary>Save</Button>
</Tooltip>

// Icon tooltip
<Tooltip content="Learn more about this feature">
  <Icon source={QuestionMarkIcon} />
</Tooltip>

// With keyboard shortcut
<Tooltip content="Keyboard shortcut: Cmd+S">
  <Button>Save</Button>
</Tooltip>

// Custom delay
<Tooltip content="Hover me" activationDelay={500}>
  <span>Slow tooltip</span>
</Tooltip>
```

## Best practices
- Use for additional help/context only
- Keep text brief (1-2 sentences max)
- Don't hide critical info in tooltips
- Avoid on mobile (hover doesn't exist)
- Use for keyboard shortcuts
- Don't use for repeated info

## Content guidelines
- Brief and helpful text only
- Explain purpose or provide tip
- For buttons with icons, explain icon
- Keyboard shortcuts: "Shortcut: Cmd+S"
- Avoid redundancy with visible text

## Accessibility
- Shows on hover and focus
- Screen readers can access aria-describedby
- Keyboard users can trigger with Tab
- Escape key to dismiss
- Touch devices may not see tooltips

## Related components
- Popover (for more content)
- Banner (for critical info)
- KeyboardKey (for shortcuts)
