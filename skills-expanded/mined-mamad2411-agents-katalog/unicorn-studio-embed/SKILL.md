---
name: unicorn-studio-embed
description: "Embed Unicorn Studio interactive WebGL designs into websites — embed patterns, attributes, performance knobs (scale/dpi/fps/lazyload), and common site-builder pitfalls."
metadata:
  openclaw:
    emoji: "🦄"
    source: "https://github.com/MengTo/Skills"
---

# Unicorn Studio — Embed Skill

## When to use
- Embedding Unicorn Studio interactive designs into web pages
- Adding animated, interactive hero sections without custom code
- Integrating no-code WebGL designs into production sites

## Embed patterns
```html
<!-- Basic embed -->
<div data-us-project="YOUR_PROJECT_ID" style="width: 100%; height: 400px;"></div>
<script src="https://cdn.unicorn.studio/v1.3.2/unicornStudio.umd.js"></script>
<script>
  UnicornStudio.init();
</script>
```

## Key attributes
- `data-us-project`: Your project ID from Unicorn Studio
- `data-us-scale`: Render scale (0.5 = half resolution for performance)
- `data-us-dpi`: Device pixel ratio override
- `data-us-fps`: Max frames per second cap
- `data-us-lazyload`: Enable lazy loading (`true`/`false`)

## Performance knobs
- **Scale**: Lower `data-us-scale` for less GPU load
- **DPI**: Cap at `1` on mobile for better performance
- **FPS**: Cap at `30` for subtle animations
- **Lazyload**: Enable for below-fold content

## React integration
```tsx
useEffect(() => {
  const script = document.createElement('script');
  script.src = 'https://cdn.unicorn.studio/v1.3.2/unicornStudio.umd.js';
  script.onload = () => UnicornStudio.init();
  document.head.appendChild(script);
  return () => UnicornStudio.destroy();
}, []);
```

## Common pitfalls
- Container has no explicit size → nothing renders
- Multiple embeds on one page → heavy GPU usage
- Site builders (Webflow, Framer) may block third-party scripts
- Not destroying on route changes in SPAs → memory leaks

## Tips for AI Agents
- Ask for the Unicorn Studio project ID.
- Confirm performance requirements (mobile, low-end devices).
- Check if lazy loading is appropriate for the embed placement.
