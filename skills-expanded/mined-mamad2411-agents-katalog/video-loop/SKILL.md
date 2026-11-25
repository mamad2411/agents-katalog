---
name: video-loop
description: Create seamless infinite loops from video clips using forward-reverse-crossfade technique. Perfect for hero backgrounds, ambient loops, and any video that needs to play continuously without visible jumps.
---

# Video Loop Skill

Transform any video into a mathematically seamless infinite loop. Uses the forward-reverse-crossfade technique to eliminate the jarring "jump" when videos restart.

## How It Works

1. Takes the original video
2. Creates a reversed copy
3. Crossfades the end of the original into the start of the reversed
4. Crossfades the end of the reversed back to match the original start
5. Result: A video that flows forward, then backward, creating perfect continuity

## Prerequisites

Requires `ffmpeg` installed:

```bash
brew install ffmpeg
```

## Usage

Run the script with input video and output path:

```bash
./scripts/create-loop.sh input.mp4 output-loop.mp4
```

### Options

```bash
./scripts/create-loop.sh input.mp4 output.mp4 [crossfade_duration]
```

- `input.mp4` - Source video file
- `output.mp4` - Output seamless loop file
- `crossfade_duration` - Optional, default 0.5 seconds (range: 0.25-2.0)

### Examples

```bash
# Basic usage - 0.5s crossfade (default)
./scripts/create-loop.sh hero-background.mp4 hero-loop.mp4

# Longer crossfade for smoother transition
./scripts/create-loop.sh hero-background.mp4 hero-loop.mp4 1.0

# Quick crossfade for faster-paced content
./scripts/create-loop.sh product-spin.mp4 product-loop.mp4 0.25
```

## Output

The output video will be approximately `(2 * input_duration) - (2 * crossfade_duration)` in length.

Example: 6 second input with 0.5s crossfade = ~11 second seamless loop

## HTML Implementation

Use the seamless loop in your hero section:

```html
<video
  autoplay
  muted
  loop
  playsinline
  class="hero-background"
>
  <source src="hero-loop.mp4" type="video/mp4">
</video>
```

```css
.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
}
```

## When to Use

- **Hero backgrounds** - Ambient motion behind text/CTAs
- **Product showcases** - Rotating/floating products
- **Ambient loops** - Atmospheric content for displays
- **Loading states** - Smooth visual feedback

## Tips

- **Shorter crossfades (0.25-0.5s)** work better for videos with subtle motion
- **Longer crossfades (0.75-1.5s)** smooth out videos with more dynamic movement
- Videos with symmetrical or abstract content loop most naturally
- Avoid videos with directional motion (walking, scrolling text) - they look odd reversed
