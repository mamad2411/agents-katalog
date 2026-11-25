---
name: badge-tag
description: Generate badges, tags, and status indicators with multiple color variants.
---

# Badge & Tag Component

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.badge-default {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.6);
}

.badge-primary {
  background: rgba(var(--accent-rgb), 0.12);
  color: var(--accent);
}

.badge-success {
  background: rgba(34, 197, 94, 0.12);
  color: #22c55e;
}

.badge-warning {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
}

.badge-danger {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.tag-removable::after {
  content: '×';
  margin-left: 4px;
  cursor: pointer;
  opacity: 0.5;
}

.tag-removable:hover::after {
  opacity: 1;
}
```

Rules:
- Badges: pill shape, small, for counts/status
- Tags: rounded rectangle, for labels/categories
- Badge colors: map to semantic meaning (success=green, warning=yellow, danger=red)
