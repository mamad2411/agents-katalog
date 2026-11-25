---
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."
license: Complete terms in LICENSE.txt
---

# Slack GIF Creator

Build animated GIFs optimized for Slack messaging using Python PIL/Pillow.

## Dependencies

```bash
pip install Pillow
```

## Technical Specifications

| Type | Dimensions | Duration | Frame Rate | Colors |
|------|-----------|----------|------------|--------|
| Emoji GIF | 128×128 px | < 3 seconds | 10-30 FPS | 48-128 |
| Message GIF | 480×480 px | Any | 10-30 FPS | 48-128 |

## Core Implementation

```python
from PIL import Image, ImageDraw, ImageFont
import math

def create_gif(frames: list[Image.Image], output_path: str, fps: int = 15, loop: bool = True):
    """Save frames as optimized GIF."""
    duration = int(1000 / fps)  # milliseconds per frame
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0 if loop else 1,
        optimize=True
    )

def create_frame(size: tuple[int, int] = (128, 128), bg_color: tuple = (255, 255, 255, 0)) -> tuple:
    """Create blank RGBA frame."""
    img = Image.new('RGBA', size, bg_color)
    draw = ImageDraw.Draw(img)
    return img, draw
```

## Easing Functions

```python
def ease_in_out(t: float) -> float:
    """Smooth easing for natural motion."""
    return t * t * (3 - 2 * t)

def bounce(t: float) -> float:
    """Bouncy easing effect."""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2

def elastic(t: float, amplitude: float = 1.0, period: float = 0.3) -> float:
    """Elastic spring effect."""
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude)
    return amplitude * pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / period) + 1
```

## Animation Patterns

### Shake/Vibrate
```python
def shake_animation(frames=10, intensity=5):
    result = []
    for i in range(frames):
        img, draw = create_frame()
        offset_x = int(math.sin(i * math.pi * 2 / frames) * intensity)
        offset_y = int(math.cos(i * math.pi * 2 / frames) * intensity * 0.5)
        # Draw content at offset position
        draw.ellipse([40 + offset_x, 40 + offset_y, 88 + offset_x, 88 + offset_y],
                     fill=(255, 100, 100))
        result.append(img)
    return result
```

### Pulse
```python
def pulse_animation(frames=20, min_scale=0.8, max_scale=1.2):
    result = []
    for i in range(frames):
        t = i / frames
        scale = min_scale + (max_scale - min_scale) * (0.5 + 0.5 * math.sin(t * 2 * math.pi))
        img, draw = create_frame()
        cx, cy = 64, 64
        r = int(30 * scale)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(100, 150, 255))
        result.append(img)
    return result
```

### Bounce
```python
def bounce_animation(frames=24):
    result = []
    for i in range(frames):
        t = i / frames
        y_offset = int(30 * abs(math.sin(t * math.pi * 2)))
        img, draw = create_frame()
        draw.ellipse([44, 44 - y_offset, 84, 84 - y_offset], fill=(255, 200, 0))
        result.append(img)
    return result
```

### Rotation
```python
def rotate_animation(frames=30):
    result = []
    base = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.rectangle([44, 54, 84, 74], fill=(80, 200, 120))

    for i in range(frames):
        angle = (i / frames) * 360
        rotated = base.rotate(angle, expand=False)
        result.append(rotated)
    return result
```

## File Optimization

When size reduction is needed:
1. **Reduce frame count** — fewer frames, faster playback
2. **Limit colors** — use `colors=48` in save
3. **Smaller dimensions** — for emoji, 64×64 is often sufficient
4. **Remove duplicate frames** — skip frames where nothing changes

```python
# Optimized save
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=duration,
    loop=0,
    optimize=True,
    colors=64  # Reduce color palette
)
```

## Design Tips

- **Thick lines** — use `width=3` or larger for PIL drawing primitives
- **Vibrant colors** — avoid pastels for emoji; go bold
- **Visual depth** — layer shapes, add shadows with offsets
- **Polish** — smooth animations look professional; jerky ones don't
- **Creative composition** — draw from scratch using PIL's circles, polygons, lines rather than using pre-made templates
