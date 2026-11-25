---
name: animated-input
description: Generate input fields with floating labels, focus animations, and validation states.
---

# Animated Input Component

```css
.input-group {
  position: relative;
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 16px 18px 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 15px;
  outline: none;
  transition: all 0.2s ease;
}

.input-field:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.15);
}

.input-label {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.35);
  font-size: 15px;
  pointer-events: none;
  transition: all 0.2s ease;
}

.input-field:focus + .input-label,
.input-field:not(:placeholder-shown) + .input-label {
  top: 12px;
  transform: translateY(0);
  font-size: 11px;
  color: var(--accent);
}
```

Validation states:
- `.input-error`: border-color: #ef4444
- `.input-success`: border-color: #22c55e
