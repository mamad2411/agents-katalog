---
name: vantajs-background
description: "Add animated WebGL background effects with Vanta.js — setup, parameters, resizing, performance considerations, and integration patterns in React/Next.js."
metadata:
  openclaw:
    emoji: "🌊"
    source: "https://github.com/MengTo/Skills"
---

# Vanta.js — Animated WebGL Backgrounds Skill

## When to use
- Decorative animated backgrounds behind hero sections
- Quick "wow" factor without building a full Three.js scene
- Lightweight integration into static sites or React/Vue

## Key APIs
- **Init**: `const effect = VANTA.WAVES({ el: "#hero", ...options })`
- **Update**: `effect.setOptions({ color: 0xff88cc })`
- **Resize**: `effect.resize()` (if container size changes)
- **Cleanup**: `effect.destroy()` (important in SPAs)

## Quick recipe — Waves background
```html
<div id="hero" style="height: 70vh;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta/dist/vanta.waves.min.js"></script>
<script>
  const effect = VANTA.WAVES({
    el: "#hero", color: 0x0b1220,
    shininess: 40, waveHeight: 16, zoom: 0.9
  });
</script>
```

## React cleanup pattern
```js
useEffect(() => {
  const effect = VANTA.WAVES({ el: heroRef.current, ... });
  return () => effect.destroy();
}, []);
```

## Common pitfalls
- Container has no size → nothing visible
- Multiple WebGL canvases → GPU load (keep to 1-2/page)
- Mobile/older GPU issues → provide fallback background
- Bundling: some builds require `window.THREE` or passing `THREE` in options

## Tips for AI Agents
- Ask which effect (waves, birds, fog, net, etc.) and brand colors.
- Confirm mobile support requirements.
- Check if effect is behind text (readability concerns).
