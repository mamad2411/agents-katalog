---
name: polaris-link
description: Shopify Polaris Link component. Use for navigation and clickable text. Semantic alternative to buttons for navigation.
---

# Link

## When to use
Navigate to different page or external resource. Use semantically correct element for links (not buttons). Preferred over Button for navigation.

## Props
- `url` string - Href for navigation
- `children?` ReactNode - Link text content
- `external?` boolean - Open in new tab
- `download?` string | boolean - Download file
- `accessibilityLabel?` string - Aria-label for screen readers
- `className?` string - CSS class

## Examples
```jsx
import { Link } from '@shopify/polaris';

// Basic link
<Link url="/products">View products</Link>

// External link
<Link url="https://example.com" external>
  External site
</Link>

// Download link
<Link url="/file.pdf" download="myfile.pdf">
  Download PDF
</Link>

// With accessibility label
<Link url="/order/123" accessibilityLabel="View order #123">
  Order #123
</Link>
```

## Best practices
- Use for navigation, not actions
- Clear, descriptive link text
- Use Button for actions
- Prefer Link over styled button for navigation
- Include context in link text

## Content guidelines
- Clear about destination
- "Order #001" not "Order"
- Consistent labeling (Orders not "Finance section")
- Use consistent navigation labels

## Accessibility
- Semantic <a> element
- Descriptive link text
- Use accessibilityLabel if text isn't descriptive
- Keyboard: Tab to focus, Enter to follow
- External links indicate new window

## Related components
- Button (for actions)
- NavigationLink (for app navigation)
