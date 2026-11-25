---
name: polaris-resource-item
description: Shopify Polaris Resource item component. Use to represent specific objects in collection. Contextual info and link to detail page.
---

# Resource Item

## When to use
Represent specific objects within collection like products or orders. Provide contextual information on resource type. Link to object's detail page.

## Props
Complex union type with either url or onClick:
- `id` string - Unique identifier
- `url?` string - URL to navigate to (or use onClick)
- `onClick?` () => void - Click handler (or use url)
- `name?` string - Resource name/title
- `accessibilityLabel?` string - Aria-label for link
- `media?` ReactNode - Media (icon/image) to display
- `shortcutActions?` Array - Quick action buttons
- `persistentShortcutActions?` boolean - Always show actions
- `children?` ReactNode - Custom content

## Examples
```jsx
import { ResourceList, ResourceItem, Text } from '@shopify/polaris';

const items = [
  { id: '1', url: 'posts/1', title: 'How to Blog' },
];

<ResourceList
  resourceName={{ singular: 'post', plural: 'posts' }}
  items={items}
  renderItem={(item) => (
    <ResourceItem
      id={item.id}
      url={item.url}
      accessibilityLabel={`View details for ${item.title}`}
      name={item.title}
    >
      <Text variant="bodyMd" fontWeight="bold">
        {item.title}
      </Text>
    </ResourceItem>
  )}
/>
```

## Best practices
- Tailor to specific resource type
- Perform action when clicked (navigate to detail)
- Use shortcut actions for frequent operations
- Each item must have unique name prop
- AccessibilityLabel should convey link purpose

## Shortcut actions
- Quick access to frequent detail page actions
- Don't need full verb+noun formula
- Keep concise

## Accessibility
- Functions as link to detail page
- Unique name prop for each
- accessibilityLabel for unique aria-label
- Custom controls need keyboard support
- Logical focus order
- Visible focus indicator

## Keyboard support
- Enter/Return activates link by default
- Custom controls need keyboard support
- Tab through in logical order
- Visible focus indicator

## Related components
- ResourceList (required wrapper)
- List (for simple lists)
