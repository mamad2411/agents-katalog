---
name: glass-card
description: Generate a glassmorphism card component with backdrop blur, translucent backgrounds, and specular highlights.
---

# Glass Card Component

Generate a premium glassmorphism card using this exact pattern:

```css
.glass-card {
  background: linear-gradient(
    135deg,
    rgba(16, 18, 30, 0.75) 0%,
    rgba(10, 12, 22, 0.82) 35%,
    rgba(18, 20, 35, 0.75) 65%,
    rgba(12, 14, 26, 0.82) 100%
  );
  backdrop-filter: blur(80px) saturate(2.2) brightness(1.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  box-shadow:
    0 40px 120px rgba(0, 0, 0, 0.65),
    0 2px 0 rgba(255, 255, 255, 0.08) inset,
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    inset 0 -1px 0 rgba(255, 255, 255, 0.04);
  position: relative;
  overflow: hidden;
}
```

Add a specular highlight that follows the mouse:

```css
.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(
    ellipse 350px 250px at var(--mouse-x, 50%) var(--mouse-y, 50%),
    rgba(255, 255, 255, 0.05) 0%,
    transparent 100%
  );
  pointer-events: none;
  transition: background 0.1s ease-out;
}
```

Rules:
- Pure black backgrounds (#010103, #06060a), NEVER grey
- Bright specular edges: rgba(255,255,255,0.12-0.2)
- Max 1 accent color, saturation < 80%
- No emoji in UI, use SVG icons
