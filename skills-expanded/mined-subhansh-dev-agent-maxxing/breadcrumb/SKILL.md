---
name: breadcrumb
description: Generate breadcrumb navigation with separators and current page indicator.
---

# Breadcrumb Component

```css
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.breadcrumb-item {
  color: rgba(255, 255, 255, 0.4);
  text-decoration: none;
  transition: color 0.15s ease;
}

.breadcrumb-item:hover {
  color: rgba(255, 255, 255, 0.8);
}

.breadcrumb-item.current {
  color: rgba(255, 255, 255, 0.85);
  pointer-events: none;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.2);
  font-size: 10px;
}

.breadcrumb-separator svg {
  width: 12px;
  height: 12px;
}
```

Rules:
- Separator: chevron-right or slash
- Last item is always plain text (current page)
- Truncate middle items if too many: `Home / ... / Current`
