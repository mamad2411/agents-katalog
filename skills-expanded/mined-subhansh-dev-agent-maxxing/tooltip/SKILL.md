---
name: tooltip
description: Generate tooltips with arrow, delays, and smart positioning.
---

# Tooltip Component

```css
.tooltip-wrapper {
  position: relative;
  display: inline-block;
}

.tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) translateY(4px);
  padding: 6px 12px;
  background: rgba(16, 18, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.85);
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: all 0.15s ease;
  z-index: 1000;
}

.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: rgba(16, 18, 30, 0.95);
}

.tooltip-wrapper:hover .tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
```

Rules:
- Delay 300ms before showing (prevents flicker)
- Smart position: flip if too close to viewport edge
- Max-width 200px for long text, allow wrapping
