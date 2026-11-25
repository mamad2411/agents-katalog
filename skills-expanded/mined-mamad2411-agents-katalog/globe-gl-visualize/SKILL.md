---
name: globe-gl-visualize
description: "Implement Globe.GL for 3D globe data visualization with WebGL/Three.js — setup, data layers (points, arcs, polygons, labels), and integration patterns in plain HTML or React."
metadata:
  openclaw:
    emoji: "🌍"
    source: "https://github.com/MengTo/Skills"
---

# Globe.GL — 3D Globe Data Visualization Skill

## When to use
- Interactive 3D globe with data overlays
- Visualize geographic data (connections, locations, heatmaps)
- Impressive hero sections with globe animations

## Quick start (ESM)
```html
<script type="module">
  import Globe from 'globe.gl';
  const myGlobe = new Globe(document.getElementById('globe'))
    .globeImageUrl(myImageUrl)
    .pointsData(myData);
</script>
```

## Quick start (CDN)
```html
<script src="//cdn.jsdelivr.net/npm/globe.gl"></script>
<script>
  const myGlobe = new Globe(document.getElementById('globe'))
    .globeImageUrl(myImageUrl)
    .pointsData(myData);
</script>
```

## Common layers
- **Points**: Location markers with size/color
- **Arcs**: Connections between locations
- **Polygons**: Country/region highlights
- **Paths**: Route visualizations
- **Heatmaps/Hex bins**: Density visualization
- **Labels/HTML**: Custom overlays
- **3D objects**: Custom layer objects

## Practical tips
- Size the container with CSS; the globe fills its parent element.
- Reduce point count or size for mobile performance.
- Use a darker globe texture for neon-style data overlays.
- React bindings available via `react-globe.gl`.

## Tips for AI Agents
- Ask which layers are needed (points, arcs, polygons, labels).
- Confirm desktop vs mobile sizing requirements.
- Check if drag/rotate interactions or static globe is preferred.
