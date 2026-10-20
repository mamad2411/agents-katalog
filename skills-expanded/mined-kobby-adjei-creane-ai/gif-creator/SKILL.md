---
name: gif-creator
description: Knowledge and utilities for creating animated GIFs. Use when users request animated GIFs for messaging apps, social media, or any context. Provides constraints, animation concepts, and PIL-based creation workflow. Trigger when user asks to make a GIF, animate something, or create a short animation.
---

# GIF Creator

Create animated GIFs optimized for various platforms.

## Platform Requirements

| Platform | Dimensions | Notes |
|----------|-----------|-------|
| Emoji/Sticker | 128x128 | Keep under 3 seconds |
| Messaging | 480x480 | Standard message GIF |
| Social media | 600x600+ | Higher quality |

**Parameters:**
- FPS: 10-30 (lower = smaller file size)
- Colors: 48-128 (fewer = smaller)
- Duration: Keep short for messaging, flexible otherwise

## Core Workflow

```python
from PIL import Image, ImageDraw
import imageio

frames = []
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)
    # Draw your animation using PIL primitives
    frames.append(frame)

# Save as GIF
imageio.mimsave('output.gif', [f for f in frames], fps=10)
```

## Drawing Graphics

### From Scratch with PIL
```python
draw = ImageDraw.Draw(frame)

# Circles/ovals
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# Polygons (stars, triangles, etc.)
draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=(r, g, b))

# Lines
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b))
```

### Working with User Images
```python
uploaded = Image.open('file.png')
# Use directly or as reference for colors/style
```

### Making Graphics Look Good

- **Use thicker lines** — width=2 or higher. Thin lines look choppy.
- **Add visual depth** — gradients for backgrounds, layered shapes
- **Make shapes interesting** — add highlights, rings, patterns
- **Use vibrant colors** — complementary colors with contrast
- **Complex shapes** — combine polygons and ellipses for hearts, snowflakes, etc.

## Animation Concepts

### Shake/Vibrate
Use `math.sin()` or `math.cos()` with frame index. Add small random variations for natural feel.

### Pulse/Heartbeat
`math.sin(t * frequency * 2 * math.pi)` for smooth pulse. Scale between 0.8 and 1.2 of base size.

### Bounce
Apply gravity by increasing y velocity each frame. Use easing for natural landing.

### Spin/Rotate
`image.rotate(angle, resample=Image.BICUBIC)` — use sine wave for wobble instead of linear.

### Fade In/Out
Create RGBA image, adjust alpha. Or use `Image.blend(image1, image2, alpha)`.

### Slide
Start position outside frame, end at target. Use ease_out for smooth stop.

### Explode/Particle Burst
Generate particles with random angles and velocities. Add gravity (`vy += gravity`). Fade out over time.

## Easing Functions

```python
import math

def ease_out(t):
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    return 3 * t**2 - 2 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def bounce_out(t):
    if t < 1/2.75:
        return 7.5625 * t * t
    elif t < 2/2.75:
        t -= 1.5/2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5/2.75:
        t -= 2.25/2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625/2.75
        return 7.5625 * t * t + 0.984375
```

## Optimization (when file size matters)

1. Fewer frames — lower FPS or shorter duration
2. Fewer colors — 48 instead of 128
3. Smaller dimensions
4. Remove duplicate frames
5. Use `optimize=True` in PIL's GIF save

```python
frames[0].save('output.gif', save_all=True, append_images=frames[1:],
               optimize=True, duration=100, loop=0)
```

## Dependencies

```bash
pip install pillow imageio numpy
```

Combine concepts — bouncing + rotating, pulsing + sliding. Be creative with PIL's full capabilities.
