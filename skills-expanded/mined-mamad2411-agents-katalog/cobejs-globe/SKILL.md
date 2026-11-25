---
name: cobejs-globe
description: "Implement a lightweight interactive WebGL globe with cobe.js — responsive canvas setup, markers, rotation, onRender callbacks, and React/Next.js integration patterns."
metadata:
  openclaw:
    emoji: "🌐"
    source: "https://github.com/MengTo/Skills"
---

# cobe.js — Lightweight WebGL Globe Skill

## When to use
- Minimal, elegant globe for hero sections or backgrounds
- Lightweight alternative to Globe.GL or full Three.js scenes
- Auto-rotating globe with optional markers

## Quick recipe
```js
import createGlobe from "cobe";

let phi = 0;
const globe = createGlobe(canvas, {
  devicePixelRatio: 2,
  width: 600 * 2,
  height: 600 * 2,
  phi: 0,
  theta: 0,
  dark: 1,
  diffuse: 1.2,
  mapSamples: 16000,
  mapBrightness: 6,
  baseColor: [0.3, 0.3, 0.3],
  markerColor: [0.1, 0.8, 1],
  glowColor: [1, 1, 1],
  markers: [
    { location: [37.7749, -122.4194], size: 0.03 },
    { location: [40.7128, -74.0060], size: 0.05 },
  ],
  onRender: (state) => {
    state.phi = phi;
    phi += 0.003;
  },
});
```

## Canvas sizing and DPR
- Set canvas width/height to `containerWidth * devicePixelRatio`
- Style canvas with CSS for display size
- Cap DPR at 2 for performance on mobile

## React/Next.js pattern
```tsx
useEffect(() => {
  let phi = 0;
  const globe = createGlobe(canvasRef.current!, {
    // ... options
    onRender: (state) => { state.phi = phi; phi += 0.003; },
  });
  return () => globe.destroy();
}, []);
```

## Resize handling
- Listen for `window.resize`
- Recalculate canvas dimensions
- Recreate or update globe instance

## Tips for AI Agents
- Ask about desired globe size and container constraints.
- Confirm marker locations if geographic data is needed.
- Consider `prefers-reduced-motion` — stop rotation for accessibility.
