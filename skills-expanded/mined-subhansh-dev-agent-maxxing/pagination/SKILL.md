---
name: pagination
description: Generate pagination with page numbers, prev/next, and active state.
---

# Pagination Component

```css
.pagination {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.page-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.page-btn.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-ellipsis {
  color: rgba(255, 255, 255, 0.3);
  padding: 0 4px;
}
```

Rules:
- Show max 7 page buttons: `1 2 3 ... 8 9 10`
- Prev/Next with chevron icons
- Active page gets accent color background
- Disabled state for prev on page 1, next on last page
