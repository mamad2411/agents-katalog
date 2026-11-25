---
name: toggle-switch
description: Generate toggle switches with smooth animation and accessible markup.
---

# Toggle Switch Component

```css
.toggle {
  position: relative;
  width: 44px;
  height: 24px;
  cursor: pointer;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.toggle-track {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.toggle input:checked + .toggle-track {
  background: var(--accent);
}

.toggle input:checked + .toggle-track + .toggle-thumb {
  left: 22px;
  background: white;
}

.toggle input:focus-visible + .toggle-track {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

Rules:
- Use `<label class="toggle">` wrapping `<input type="checkbox">`
- Spring animation on thumb (cubic-bezier 0.34, 1.56, 0.64, 1)
- Focus-visible ring for keyboard accessibility
- Disabled state: opacity 0.4, cursor not-allowed
