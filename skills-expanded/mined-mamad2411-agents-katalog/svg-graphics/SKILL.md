---
name: "svg-graphics"
description: Create scalable, accessible, theme-aware SVG graphics and animations for the web — icons, banners, diagrams, illustrations, badges, and interactive visuals. Use this skill when building SVG files, animating SVG with CSS or SMIL, doing path morphing, motion path tracking, creating interactive SVG that responds to clicks without JavaScript, drawing real-world subjects (animals, people, objects) as vector illustrations, or producing documentation diagrams. Also triggers on "SVG animation", "animate SVG", "SMIL", "path morph", "animateMotion", "SVG icon", "SVG banner", "SVG diagram", "script-free SVG interaction", "CSS SVG", or any request to produce a self-contained scalable graphic.
---

# SVG Graphics Skill

> Scalable, accessible, theme-aware visuals.

## Why SVG

- Scales infinitely (retina, print)
- Text is searchable/accessible
- CSS-styleable (dark mode!)
- Small file size
- Version control friendly

## Banner Template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300">
  <!-- Background -->
  <rect width="100%" height="100%" fill="#1a1a2e"/>

  <!-- Title -->
  <text x="50" y="100" font-size="48" fill="#fff" font-family="system-ui">
    Project Name
  </text>

  <!-- Tagline -->
  <text x="50" y="150" font-size="24" fill="#888">
    One-line description
  </text>

  <!-- Feature pills -->
  <g transform="translate(50, 200)">
    <rect rx="12" width="100" height="24" fill="#4a4a6a"/>
    <text x="50" y="17" text-anchor="middle" fill="#fff" font-size="12">Feature 1</text>
  </g>
</svg>
```

## Key Techniques

| Technique | Use Case |
| --------- | -------- |
| `viewBox` | Responsive scaling |
| `<defs>` + `<use>` | Reusable components |
| `<linearGradient>` | Modern backgrounds |
| `<clipPath>` | Shaped containers |
| CSS variables | Theme switching |

## Dark/Light Mode

```xml
<style>
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a2e; }
    .text { fill: #ffffff; }
  }
  @media (prefers-color-scheme: light) {
    .bg { fill: #ffffff; }
    .text { fill: #1a1a2e; }
  }
</style>
```

## Icon Guidelines

| Size | Use |
| ---- | --- |
| 16x16 | Favicon, small UI |
| 32x32 | Tab icon, lists |
| 128x128 | App icon |
| 512x512 | Store listing |

## SMIL Animation

### Delayed Fade-In Pattern

Elements that should appear after load (hero text, feature pills, etc.):

```xml
<!-- Element starts invisible, fades in after delay -->
<g opacity="0">
  <text x="50" y="100" font-size="48" fill="#fff">Title</text>
  <animate
    attributeName="opacity"
    from="0" to="1"
    dur="0.8s"
    begin="0.5s"
    fill="freeze"
  />
</g>
```

**Key attributes**:

| Attribute | Purpose | Values |
|-----------|---------|--------|
| `begin` | Delay before start | `"0.5s"`, `"1s"`, `"click"` |
| `dur` | Animation duration | `"0.3s"` to `"2s"` typical |
| `fill` | State after animation | `"freeze"` (keep end state) or `"remove"` (revert) |
| `repeatCount` | Repetitions | `"1"`, `"3"`, `"indefinite"` |

### Staggered Entrance

Multiple elements appearing in sequence:

```xml
<g opacity="0">
  <rect rx="12" width="100" height="24" fill="#4a4a6a"/>
  <text x="50" y="17" text-anchor="middle" fill="#fff" font-size="12">Feature 1</text>
  <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.3s" fill="freeze"/>
</g>
<g opacity="0">
  <rect rx="12" width="100" height="24" fill="#4a4a6a"/>
  <text x="50" y="17" text-anchor="middle" fill="#fff" font-size="12">Feature 2</text>
  <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.6s" fill="freeze"/>
</g>
<g opacity="0">
  <rect rx="12" width="100" height="24" fill="#4a4a6a"/>
  <text x="50" y="17" text-anchor="middle" fill="#fff" font-size="12">Feature 3</text>
  <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.9s" fill="freeze"/>
</g>
```

**Pattern**: Increment `begin` by `0.3s` per element for smooth staggering.

### SMIL Compatibility

| Platform | Support |
|----------|---------|
| Chrome/Edge | Full SMIL |
| Firefox | Full SMIL |
| Safari | Full SMIL |
| GitHub README | **No animation** (static render) |
| npm/PyPI README | **No animation** (static render) |

**Rule**: For README badges/banners, set initial `opacity="1"` as fallback — animated SVGs render as static first frame in non-animated contexts.

### CSS vs SMIL: Choosing the Right Tool

| Goal | Use | Why |
|------|-----|-----|
| `opacity`, `fill`, `stroke` loops | CSS | Hardware-accelerated, lower battery |
| `transform` (rotate, scale, translate) | CSS | Composited on GPU |
| `:hover` / `:focus` states | CSS | Cannot be done with SMIL |
| Path morphing (`d` attribute) | SMIL | CSS cannot animate `d` portably |
| `viewBox` animation | SMIL | No CSS equivalent |
| Click/event-triggered sequences | SMIL | `begin="el.click"` without JS |
| Following a bezier motion path | SMIL | `<animateMotion>` + `<mpath>` |

**General rule**: use CSS for anything it can reach (visual properties, transforms); fall back to SMIL for attributes CSS cannot touch and for event-driven interaction without JavaScript.

### Path Morphing

To animate a shape changing form, both `from` and `to` paths must have the **same number of points and the same command types** — otherwise the browser can't interpolate between them.

```xml
<svg viewBox="0 0 100 100">
  <!-- Square that morphs into a diamond on click -->
  <path id="shape" d="M10,10 L90,10 L90,90 L10,90 Z" fill="crimson">
    <animate
      attributeName="d"
      begin="shape.click"
      dur="0.5s"
      fill="freeze"
      to="M50,10 L90,50 L50,90 L10,50 Z"
    />
  </path>
</svg>
```

**Tip**: When designing morph pairs, trace both shapes with the same number of anchor points in the same winding direction. Tools like Inkscape's node editor make this easy to verify.

### Motion Path

Move an element along any arbitrary curve using `<animateMotion>` referencing a `<path>` via `<mpath>`:

```xml
<svg viewBox="0 0 200 200">
  <!-- The path to follow (can be invisible) -->
  <path id="track" d="M20,100 Q60,20 100,100 T180,100" fill="none" stroke="#ddd"/>

  <!-- Element that travels the path -->
  <circle r="6" fill="#4a90d9">
    <animateMotion dur="3s" repeatCount="indefinite" rotate="auto">
      <mpath href="#track"/>
    </animateMotion>
  </circle>
</svg>
```

`rotate="auto"` keeps the element tangent to the curve as it moves. Use `rotate="auto-reverse"` to flip the orientation 180°.

### Interactive Event Chaining

SMIL `begin` and `end` can reference element events and other animation endpoints — enabling click-driven state machines with zero JavaScript:

```xml
<svg viewBox="0 0 200 100">
  <!-- Button: click to start sequence -->
  <rect id="btn" x="10" y="35" width="80" height="30" rx="6" fill="#4a90d9" cursor="pointer"/>
  <text x="50" y="55" text-anchor="middle" fill="#fff" font-size="12" pointer-events="none">Play</text>

  <!-- Step 1: slide in on click -->
  <circle id="dot" cx="-20" cy="50" r="10" fill="#cf4040">
    <animate
      id="slide"
      attributeName="cx"
      begin="btn.click"
      dur="0.4s"
      to="150"
      fill="freeze"
    />
    <!-- Step 2: pulse after step 1 ends -->
    <animate
      attributeName="r"
      begin="slide.end + 0.1s"
      dur="0.3s"
      values="10;16;10"
      fill="freeze"
    />
  </circle>
</svg>
```

**Chaining syntax**:
- `begin="anim1.end"` — starts when anim1 finishes
- `begin="anim1.end + 0.5s"` — starts 0.5 s after anim1 finishes
- `begin="el.click"` — starts on element click
- `begin="el.mouseover"` — starts on hover

### Spline Easing (Professional Timing)

SMIL's default `calcMode="linear"` produces robotic motion. For natural easing, use `calcMode="spline"` with cubic bezier `keySplines`:

```xml
<animate
  attributeName="cy"
  from="20" to="180"
  dur="1s"
  calcMode="spline"
  keyTimes="0;1"
  keySplines="0.4 0 0.2 1"
  fill="freeze"
/>
```

`keySplines` uses the same cubic bezier format as CSS `cubic-bezier()`. Common presets:

| Feel | keySplines value |
|------|------------------|
| Ease-in-out (Material) | `0.4 0 0.2 1` |
| Ease-out (decelerate) | `0 0 0.2 1` |
| Ease-in (accelerate) | `0.4 0 1 1` |
| Bouncy | `0.34 1.56 0.64 1` |

For multi-step animations, provide one `keySplines` entry per interval (n-1 entries for n `keyTimes`).

## CSS Transform Patterns

### The Nested Group Pattern

**Problem**: Combining position transforms (`translate`) with animation transforms (`rotate`, `scale`) on the same element causes conflicts — the animation resets position.

**Solution**: Use nested `<g>` groups to separate concerns:

```xml
<!-- Outer group: POSITION (static) -->
<g transform="translate(600, 150)">
  <!-- Inner group: ANIMATION (dynamic) -->
  <g>
    <animateTransform
      attributeName="transform"
      type="rotate"
      from="0" to="360"
      dur="10s"
      repeatCount="indefinite"
    />
    <!-- The actual shape -->
    <circle r="20" fill="#4a90d9"/>
  </g>
</g>
```

**Rule**: Never mix static positioning and animated transforms on the same element. Always wrap in a positioning group.

**CSS alternative**: When using CSS `@keyframes` instead of `<animateTransform>`, add `transform-box: fill-box; transform-origin: center;` to the element's CSS — this makes `rotate` and `scale` pivot from the shape's own centre rather than the SVG canvas origin, avoiding unexpected orbits.

### Scale from Center

```xml
<g transform="translate(100, 100)">
  <!-- transform-origin doesn't work reliably in SVG; 
       use translate to center, then scale -->
  <g>
    <animateTransform
      attributeName="transform"
      type="scale"
      from="0.8" to="1.0"
      dur="0.5s"
      fill="freeze"
    />
    <!-- Shape centered at origin (0,0) -->
    <circle cx="0" cy="0" r="30" fill="#d3f5db"/>
  </g>
</g>
```

### Pulse Effect

```xml
<circle cx="50" cy="50" r="10" fill="#cf222e">
  <animateTransform
    attributeName="transform"
    type="scale"
    values="1;1.2;1"
    dur="1.5s"
    repeatCount="indefinite"
  />
</circle>
```

## ClipPath Container Layering

### The 3-Layer Pattern

For shaped containers with content and visible borders:

```xml
<defs>
  <clipPath id="container-clip">
    <rect x="50" y="50" width="400" height="200" rx="16"/>
  </clipPath>
</defs>

<!-- Layer 1: BACKGROUND (fill behind clip) -->
<rect x="50" y="50" width="400" height="200" rx="16" fill="#f6f8fa"/>

<!-- Layer 2: CLIPPED CONTENT (stays inside shape) -->
<g clip-path="url(#container-clip)">
  <!-- Content that may overflow is safely clipped -->
  <image href="photo.jpg" x="50" y="50" width="400" height="200"/>
  <text x="70" y="120" font-size="24" fill="#fff">Overlay Text</text>
</g>

<!-- Layer 3: BORDER OUTLINE (drawn last, on top) -->
<rect x="50" y="50" width="400" height="200" rx="16" 
      fill="none" stroke="#d1d9e0" stroke-width="2"/>
```

**Draw order matters**:
1. Background fill (behind everything)
2. Clipped content group (contained within shape)
3. Border outline (on top, `fill="none"`)

### Rounded Card Pattern

```xml
<defs>
  <clipPath id="card">
    <rect width="300" height="180" rx="12"/>
  </clipPath>
</defs>

<g transform="translate(20, 20)">
  <!-- Card background -->
  <rect width="300" height="180" rx="12" fill="#ffffff"/>
  
  <!-- Card content (clipped) -->
  <g clip-path="url(#card)">
    <!-- Header band -->
    <rect width="300" height="48" fill="#0550ae"/>
    <text x="16" y="32" fill="#fff" font-size="16" font-weight="bold">Card Title</text>
    <!-- Body -->
    <text x="16" y="80" fill="#1f2328" font-size="14">Card content here</text>
  </g>
  
  <!-- Card border -->
  <rect width="300" height="180" rx="12" fill="none" stroke="#d1d9e0"/>
</g>
```

## SVG Optimization

### SVGO Configuration

```json
{
  "plugins": [
    "preset-default",
    { "name": "removeViewBox", "active": false },
    { "name": "removeDimensions", "active": true },
    { "name": "removeTitle", "active": false }
  ]
}
```

**Critical**: Never remove `viewBox` (breaks scaling) or `<title>` (breaks accessibility).

### Size Budget

| SVG Type | Target Size | Max |
|----------|-------------|-----|
| Icon | < 1 KB | 2 KB |
| Badge/shield | < 2 KB | 5 KB |
| Banner | < 10 KB | 25 KB |
| Complex diagram | < 25 KB | 50 KB |

### Common Optimization Wins

| Technique | Savings |
|-----------|---------|
| Remove editor metadata (Inkscape, Illustrator) | 20-50% |
| Simplify paths (reduce decimal precision) | 10-20% |
| Remove empty groups/unused defs | 5-15% |
| Convert shapes to paths | 5-10% |
| Gzip on server | 60-80% additional |

## Accessibility

- `role="img"` on the `<svg>` element for meaningful graphics
- `<title>` — short name read by screen readers (first child of `<svg>`)
- `<desc>` — longer description for complex diagrams; linked via `aria-labelledby="title-id desc-id"`
- `aria-hidden="true"` on purely decorative SVGs
- Sufficient contrast (4.5:1 minimum for text, 3:1 for UI components)
- `pointer-events="none"` on text inside interactive shapes to prevent event conflicts

```xml
<svg role="img" aria-labelledby="svg-title svg-desc" viewBox="0 0 400 200">
  <title id="svg-title">Monthly revenue chart</title>
  <desc id="svg-desc">Bar chart showing revenue rising from $12k in January to $18k in March.</desc>
  <!-- chart content -->
</svg>
```

## Tools

| Tool | Purpose |
| ---- | ------- |
| SVGO | Optimize/minify |
| Inkscape | Visual editing |
| svg-to-png | Rasterization |

## SVG for Documentation Illustrations

SVG isn't just for branding — it's the best format for **polished documentation visuals** that need more control than Mermaid provides.

### When to Choose SVG Over Mermaid

| Scenario | Use SVG | Use Mermaid |
|----------|---------|-------------|
| Architecture overview for README | ✅ Branded, polished | ❌ Too generic |
| Internal dev docs flow | ❌ Overkill | ✅ Quick, accurate |
| Marketing / landing page | ✅ Full design control | ❌ Unbranded |
| Infographic with custom layout | ✅ Arbitrary positioning | ❌ Auto-layout only |
| Dark/light theme required | ✅ CSS media queries | ⚠️ Limited theming |
| Print / high-DPI output | ✅ Infinitely scalable | ⚠️ Rasterized at render |

### Illustration Template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Architecture Overview</title>
  <style>
    @media (prefers-color-scheme: dark) {
      .bg { fill: #1e1e1e; }
      .text { fill: #d4d4d4; }
      .box { fill: #2d2d2d; stroke: #444; }
      .accent { fill: #0078d4; }
    }
    @media (prefers-color-scheme: light) {
      .bg { fill: #ffffff; }
      .text { fill: #1a1a1a; }
      .box { fill: #f5f5f5; stroke: #ddd; }
      .accent { fill: #0078d4; }
    }
    .label { font-family: system-ui, sans-serif; font-size: 14px; }
    .title-text { font-family: system-ui, sans-serif; font-size: 20px; font-weight: 600; }
    .connector { stroke-width: 2; stroke-dasharray: 4 4; }
  </style>

  <rect class="bg" width="100%" height="100%"/>

  <!-- Title -->
  <text class="title-text text" x="400" y="30" text-anchor="middle">Architecture Name</text>

  <!-- Boxes with rounded corners -->
  <g transform="translate(100, 60)">
    <rect class="box" rx="8" width="200" height="80" stroke-width="1.5"/>
    <text class="label text" x="100" y="45" text-anchor="middle">Component A</text>
  </g>

  <!-- Connector arrow -->
  <line class="connector accent" x1="300" y1="100" x2="400" y2="100"/>
  <polygon class="accent" points="400,95 410,100 400,105"/>

  <g transform="translate(420, 60)">
    <rect class="box" rx="8" width="200" height="80" stroke-width="1.5"/>
    <text class="label text" x="100" y="45" text-anchor="middle">Component B</text>
  </g>
</svg>
```

### Key Principles for Illustrations

1. **Always include dark/light mode** via `@media (prefers-color-scheme: ...)` — GitHub renders both
2. **Use semantic class names** (`.box`, `.accent`, `.connector`) not inline styles
3. **Center with `text-anchor="middle"`** — more maintainable than manual x positioning
4. **Group with `<g transform="translate()">`** — move entire components by adjusting one value
5. **Keep `viewBox` ratio consistent** — 800×400 (2:1) for wide illustrations, 600×600 (1:1) for square

## Illustrating Real-World Subjects (Animals, Objects, People)

### The Snowman Problem

**Problem**: When asked to draw a dog, cat, person, or any real-world subject, AI defaults to stacking circles and rectangles — producing geometric snowmen with accessories instead of recognizable illustrations.

**Root Cause**: The model uses primitive shapes (`<circle>`, `<rect>`, `<ellipse>`) as building blocks. Real-world subjects have **organic, asymmetric silhouettes** that require `<path>` elements with Bezier curves.

**The Snowman Test**: If you remove all color, texture, and small details — does the **silhouette alone** identify the subject? A circle on a circle is always a snowman, no matter how many ears/tails you add.

### Mandatory Rules for Subject Illustrations

| # | Rule | Why |
|---|------|-----|
| 1 | **Start with the silhouette** — sketch the outer `<path>` outline FIRST | The outline makes or breaks recognition. If the outline looks wrong, details won't fix it. |
| 2 | **Use `<path>` with Bezier curves** for ALL organic shapes | `<circle>` and `<ellipse>` produce geometric/robotic results. Real animals have no perfect circles. |
| 3 | **Pass the squint test** — outline alone must be identifiable | Remove all fill colors and details. If the outline doesn't read as the subject, redo the outline. |
| 4 | **Get proportions right before adding details** | Head-to-body ratio, limb length, and placement matter more than eyes/nose/accessories. |
| 5 | **Count limbs correctly** — quadrupeds have 4 legs, birds have 2 + wings | The most common error. Don't draw 2 legs on a 4-legged animal. In side view, show at least 3 legs (near pair + 1 far). |
| 6 | **Differentiate species by key anatomical features** | A dog is not a cat is not a bear. See the feature table below. |

### Feature Differentiation Table

What makes each animal **visually distinct** — the features to exaggerate:

| Animal | Key Silhouette Features | Common AI Mistakes |
|--------|------------------------|--------------------|
| **Dog** | Snout/muzzle protruding from head, floppy or pointed ears (SIDE of head, not top), 4 legs, wagging tail, body longer than tall | Flat face (no snout), cat ears on top, 2 legs, perfect circle head |
| **Cat** | Pointed ears on TOP of head, round face, long curved whiskers, slender body, long curving tail, 4 legs with small paws | No whiskers, dog-like snout added, thick stocky body |
| **Bird** | Beak (triangular), wings (large relative to body), 2 thin legs, tail feathers, no arms | 4 legs, no beak, arms instead of wings |
| **Fish** | Streamlined oval body, tail fin, dorsal fin, NO legs | Legs added, round body (balloon), no fins |
| **Person** | Head on neck on shoulders, 2 arms with hands, 2 legs with feet, torso taller than wide | Snowman stack, no neck, T-pose arms |
| **Horse** | Long neck, elongated head with flat front, 4 long thin legs, mane, flowing tail | Dog-like proportions, short legs, round head |
| **Rabbit** | LONG upright ears (longer than head), round body, short front legs, large hind legs, cotton tail | Short ears (looks like a bear), same-length legs |

### The Path-First Approach

**Never build an animal from primitive shapes.** Build from a single continuous `<path>` outline.

#### Step-by-Step: Drawing a Dog (Side View)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img">
  <title>Dog illustration</title>
  
  <!-- Step 1: BODY OUTLINE - single path defining the entire silhouette -->
  <!-- Start at chest, go along back, tail, rear leg, belly, front leg, up to chin, head, ear, back to start -->
  <path d="
    M 120,180
    C 120,140 140,110 180,105
    C 210,100 250,100 280,110
    Q 300,118 310,135
    L 330,115
    L 320,140
    Q 315,160 310,180
    L 305,220
    L 290,220
    L 290,185
    Q 260,195 220,195
    L 180,220
    L 165,220
    L 170,185
    Q 140,180 120,180
    Z
  " fill="#c89050" stroke="#6b4226" stroke-width="2"/>

  <!-- Step 2: HEAD - overlapping path with snout protruding forward -->
  <path d="
    M 130,160
    C 120,130 100,110 85,100
    Q 70,92 60,100
    C 50,110 55,130 60,140
    L 65,148
    Q 80,160 100,165
    Q 115,168 130,160
    Z
  " fill="#c89050" stroke="#6b4226" stroke-width="2"/>
  
  <!-- Step 3: SNOUT/MUZZLE - the feature that makes it a dog, not a snowman -->
  <path d="
    M 72,130
    C 60,125 50,128 48,135
    C 46,142 52,148 62,148
    Q 70,145 72,138
    Z
  " fill="#e8c690" stroke="#6b4226" stroke-width="1.5"/>
  
  <!-- Step 4: EAR - floppy, attached to SIDE of head (not on top!) -->
  <path d="
    M 100,105
    C 105,85 115,75 120,80
    C 125,88 118,105 110,112
    Z
  " fill="#a0703c" stroke="#6b4226" stroke-width="1.5"/>
  
  <!-- Step 5: Details LAST - eye, nose, mouth -->
  <circle cx="82" cy="115" r="4" fill="#2c1810"/>  <!-- Eye -->
  <ellipse cx="52" cy="135" rx="5" ry="4" fill="#2c1810"/>  <!-- Nose -->
  <path d="M 55,142 Q 62,148 68,144" fill="none" stroke="#6b4226" stroke-width="1.5"/>  <!-- Mouth -->
  
  <!-- Step 6: TAIL - curved upward, characteristic dog pose -->
  <path d="M 325,120 Q 345,90 350,100 Q 348,115 330,125" 
        fill="#c89050" stroke="#6b4226" stroke-width="2"/>
</svg>
```

**Why this works**: 
- Silhouette reads as "dog" even without color (elongated body, protruding snout, floppy ear)
- Snout is the dominant facial feature — face is NOT flat
- 4 legs visible (2 front, 2 back in side view)
- Body is longer than tall (dog proportions, not snowman proportions)
- ALL shapes use `<path>` with curves — no perfect circles

### Proportion Guide

For side-view quadrupeds (dog, cat, horse):

```text
┌──────────────────────────────────────────┐
│         HEAD    NECK    BODY             │
│        ┌───┐   ┌─┐   ┌──────────┐      │
│   ear→ │   │───│ │───│          │ ←tail │
│        │ • │   │ │   │          │  /    │
│  snout→│ ▪ │   └─┘   │          │ /     │
│        └───┘         │          │/      │
│                      └──┬──┬──┬─┘       │
│                         │  │  │  │      │
│                     legs (4, not 2!)    │
│                                         │
│  HEAD:BODY ratio ≈ 1:2.5 (dog)         │
│  HEAD:BODY ratio ≈ 1:2   (cat)         │
│  HEAD:BODY ratio ≈ 1:4   (horse)       │
│  LEG length ≈ body height (dog, horse)  │
│  LEG length ≈ 0.7× body height (cat)   │
└──────────────────────────────────────────┘
```

### Color Guidelines for Illustrated Subjects

| Subject | Natural Palette | Avoid |
|---------|----------------|-------|
| Dog | Browns (#c89050, #a0703c, #6b4226), Golden (#e8c690), Black, White, Gray | Green, blue, purple (unnatural) |
| Cat | Gray (#8e8e8e), Orange (#d68c45), Black, White, Siamese (#c4a882) | Bright green, neon colors |
| Bird | Species-specific; blue (#4a90d9), red (#cf4040), yellow (#e6b422), green (#5ab05a) | All one color (usually multi-toned) |
| Person | Skin tones, clothing colors | Geometric shapes for body parts |
| Tree | Green canopy (#4a8c3f, #6aad5a), brown trunk (#6b4226, #8b6914) | Blue leaves, gray trunk |

**Rule**: Use **realistic base colors** unless the user specifically requests a stylized/cartoon palette.

### Common Failure Modes

| Failure | Cause | Fix |
|---------|-------|-----|
| "Snowman with ears" | Using stacked circles for body | Use one continuous `<path>` for body outline |
| "Cat ears on everything" | Triangles placed on top of circular head | Place ears on SIDE of head (dogs), check species table |
| "Floating face" | Features placed on a perfect circle with no jaw/chin structure | Give head a distinct shape — snout, jawline, not a circle |
| "Stick figure animal" | Rectangles for legs attached to circles | Legs should taper, connect to body organically with curves |
| "2-legged quadruped" | Forgetting rear or front leg pair | Always count: is this animal 2-legged or 4-legged? |
| "Psychedelic colors" | Using brand/branding palette instead of natural colors | Real animals have earthy, natural tones — check color table |
| "Giant head, tiny body" | No proportion reference | Check proportion guide — head is usually smaller than body |

### Workflow for Subject Illustrations

1. **Identify** — What species/object? What view? (side/front/3-quarter)
2. **Reference proportions** — Check the proportion guide and feature table
3. **Draw silhouette** — Single `<path>` for body outline. Apply squint test.
4. **Add major features** — Head shape, ears at correct position, limbs (count them!)
5. **Add details last** — Eyes, nose, mouth, texture, color
6. **Squint test** — Remove all color. Is the silhouette recognizable?

---

## Related Skills

### svg (svg-animation-expert)
Deep-dive JS-free animation expertise: complex path morphing workflows, motion path nuances, sophisticated SMIL event chains, and hybrid CSS+SMIL architecture decisions. The svg-graphics skill covers the animation techniques needed for most work; consult svg-animation-expert for advanced animation-only projects.

**Use svg-animation-expert instead when:** the entire project is a complex interactive animated SVG with multiple chained events, intricate morphing sequences, or motion-path choreography as its primary purpose.

### animation-specialist
Broad motion design expertise spanning CSS animations, Web Animations API, spring physics, canvas, GSAP timelines, and the mathematics behind choreography. Useful when the problem isn't specifically SVG or when the right animation approach hasn't been decided.

**Use alongside this skill when:** an SVG animation needs to coordinate with non-SVG page elements, or the user is deciding between SVG/SMIL and a JavaScript-based animation approach.

### css-design
Expert CSS including `@keyframes`, transitions, `animation-timeline`, CSS scroll-driven animations, and modern selectors. CSS is the right tool for SVG property animations that don't require SMIL — opacity, fill, stroke, and transforms.

**Use alongside this skill when:** SVG animation is driven by CSS `@keyframes` or you need `prefers-reduced-motion` media queries to respect accessibility preferences.

### gsap
Professional JavaScript animation using GSAP — tweens, timelines, Flip, Observer, and MorphSVG plugin. MorphSVG can morph between paths that have *different* point counts, which SMIL cannot do.

**Use instead of this skill when:** path morphing between incompatible shapes is required, or the SVG animation must be precisely coordinated with JavaScript-driven page animations.

### web-visual-effects
GPU-accelerated visual effects: WebGL/WebGPU shaders, post-processing, and particle systems. Useful when SVG's rendering ceiling isn't enough.

**Use instead of this skill when:** the visual complexity (thousands of animated particles, real-time shader effects, 3D scenes) exceeds what SVG can efficiently render in the DOM.

### p5js-creative-coding
Generative and creative coding using p5.js — drawing loops, particle systems, Perlin noise, and interactive canvas sketches.

**Use instead of this skill when:** the output is a live generative/procedural canvas experience rather than a self-contained SVG file.

### accessibility-patterns
Comprehensive WCAG guidance: semantic HTML, ARIA roles, keyboard navigation, colour contrast, and screen-reader testing strategies.

**Use alongside this skill when:** the SVG is part of a larger accessible UI and needs thorough ARIA integration, keyboard focus management, or WCAG audit coverage beyond the basics listed here.

### frontend-design
Creative direction and full interface implementation — layout, typography, colour systems, and component design.

**Use before this skill when:** the SVG is one component of a larger designed page and the overall visual direction hasn't been established yet.
