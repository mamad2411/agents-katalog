---
name: svg-animations
description: "Use when creating SVG animations for README files, logos, badges, or web interfaces. Covers: SMIL animations, CSS keyframes in SVG, morphing, motion paths, gradient animations, accessibility. Trigger for: animated logo, SVG badge, README animation, animated icon."
---

# SVG ANIMATIONS — Professional Animated SVG

## Core Architecture
HTML (layout) + CSS (styling) → SVG as overlay for complex animations
SVG = precision geometry + animations impossible in CSS (morphing, motion paths)

## Essential Patterns

### Blinking Eye Animation
```xml
<ellipse rx="20" ry="15">
  <animate attributeName="ry" values="15;15;1;15;15" keyTimes="0;0.3;0.5;0.7;1"
           dur="4s" repeatCount="indefinite"/>
</ellipse>
```

### Gradient Animation
```xml
<linearGradient id="grad">
  <stop offset="0%" stop-color="red">
    <animate attributeName="stop-color" values="red;blue;green;red" dur="5s" repeatCount="indefinite"/>
  </stop>
</linearGradient>
```

### Glow Filter
```xml
<filter id="glow">
  <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
  <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
```

### Pulse Ring
```xml
<circle r="35" fill="none" stroke="#COLOR" stroke-width="2" opacity="0.6">
  <animate attributeName="r" values="35;50;65" dur="3s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.6;0;0" dur="3s" repeatCount="indefinite"/>
</circle>
```

## Accessibility (MANDATORY)
```xml
<svg role="img" aria-labelledby="title-id desc-id">
  <title id="title-id">Short descriptive title</title>
  <desc id="desc-id">Detailed description</desc>
  <style>@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }</style>
</svg>
```

## Performance Rules
- File size < 50KB (< 20KB optimal for README badges)
- Use transform/opacity for GPU acceleration
- No external fonts unless necessary
- Test on dark AND light backgrounds
