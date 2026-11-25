---
name: accordion
description: Generate expandable accordion sections with smooth height animation.
---

# Accordion Component

```css
.accordion {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.accordion-item {
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  overflow: hidden;
}

.accordion-trigger {
  width: 100%;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.02);
  border: none;
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background 0.15s ease;
}

.accordion-trigger:hover {
  background: rgba(255, 255, 255, 0.04);
}

.accordion-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.2s ease;
}

.accordion-item.open .accordion-icon {
  transform: rotate(180deg);
}

.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.accordion-item.open .accordion-content {
  max-height: 500px;
}

.accordion-body {
  padding: 0 16px 14px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  line-height: 1.6;
}
```

Rules:
- Only one item open at a time (optional: allow multiple)
- Chevron icon rotates on open
- max-height transition for smooth expand/collapse
- Support keyboard: Enter/Space to toggle
