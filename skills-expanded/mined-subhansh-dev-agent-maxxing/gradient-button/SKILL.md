---
name: gradient-button
description: Generate gradient buttons with hover states, press feedback, and glow effects.
---

# Gradient Button Component

```css
.btn-gradient {
  padding: 12px 28px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--accent), var(--accent-deep));
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 20px rgba(var(--accent-rgb), 0.3);
  position: relative;
  overflow: hidden;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(var(--accent-rgb), 0.4);
}

.btn-gradient:active {
  transform: scale(0.97);
}

.btn-gradient::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.2s;
}

.btn-gradient:hover::after {
  opacity: 1;
}
```

Use CSS custom properties for theming:
- `--accent`: primary color
- `--accent-deep`: darker shade
- `--accent-rgb`: RGB values for rgba()
