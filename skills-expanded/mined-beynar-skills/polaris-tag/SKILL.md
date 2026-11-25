---
name: polaris-tag
description: Shopify Polaris Tag component. Use this skill when displaying keywords, labels, categorization tags, removable tags, clickable tag buttons. Interactive keywords that help label, organize, and categorize objects.
---

# Tag

## When to use

Display a set of interactive, merchant-supplied keywords that help label, organize, and categorize objects. Tags can be added or removed by merchants.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | React.ReactNode | - | Content of the tag (required) |
| `onClick` | () => void | - | Callback on click (for clickable tags) |
| `onRemove` | () => void | - | Callback on remove (for removable tags) |
| `url` | string | - | URL for tag link (for link tags) |

Note: Either `onClick` or `onRemove`/`url` can be provided, but not both.

## Examples

```jsx
import { Card, Tag } from '@shopify/polaris';

// Basic tag
function BasicTagExample() {
  return (
    <Card>
      <Tag>Wholesale</Tag>
    </Card>
  );
}

// Removable tag
import { useState } from 'react';

function RemovableTagExample() {
  const [tags, setTags] = useState(['Wholesale', 'Bulk']);

  const handleRemove = (index) => {
    setTags(tags.filter((_, i) => i !== index));
  };

  return (
    <Card>
      {tags.map((tag, index) => (
        <Tag
          key={tag}
          onRemove={() => handleRemove(index)}
        >
          {tag}
        </Tag>
      ))}
    </Card>
  );
}

// Clickable tag
function ClickableTagExample() {
  const [selected, setSelected] = useState(null);

  return (
    <Card>
      <Tag onClick={() => setSelected('tag1')}>
        Marketing
      </Tag>
    </Card>
  );
}

// Tag as link
function TagLinkExample() {
  return (
    <Card>
      <Tag url="/collections/wholesale">
        Wholesale
      </Tag>
    </Card>
  );
}
```

## Best practices

- Be presented close to or within the input control that allows merchants to add and remove tags

## Accessibility

- Button to remove tag automatically given label via aria-label
- Distinguishes which tag will be removed for screen readers
- Keyboard: Tab to focus, Enter/Space to activate
- When removing tag, manage focus by moving to next element

## Related components

- Badge: for showing status of an object
- Text field: for adding and removing tags
