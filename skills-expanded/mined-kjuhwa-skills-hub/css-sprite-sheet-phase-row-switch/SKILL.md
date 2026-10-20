---
name: css-sprite-sheet-phase-row-switch
description: Single CSS sprite sheet animated via steps() on X, with inline-style row switch on Y for phase-specific animations
category: design
triggers:
  - css sprite animation
  - sprite sheet phase
  - pixel art character animation
  - game-style sprite
tags:
  - css
  - animation
  - sprite-sheet
  - pixel-art
version: 1.0.0
---

# CSS Sprite Sheet — Phase-Based Row Switching

Use one sprite sheet (N cols × M rows) and let CSS handle the X-axis walk cycle via `steps()`, while inline style or per-phase class overrides the Y-axis to switch between animation states (idle, walking, working, celebrating, etc).

## Core pattern

```css
.char {
  width: 48px; height: 48px;
  background-image: url('sheet.png');
  background-repeat: no-repeat;
  background-position: 0 0;
  image-rendering: pixelated;
  transform: scale(4);
  animation: walk 1.1s steps(12) infinite;
}
@keyframes walk {
  from { background-position-x: 0 }
  to   { background-position-x: -576px }   /* -(cols × frame_width) */
}
/* Phase rows override Y + speed */
.char.thinking { background-position-y: -48px;  animation-duration: 1.6s; }
.char.working  { background-position-y: -96px;  animation-duration: .55s; }
.char.sending  { background-position-y: -144px; animation-duration: .7s;  }
.char.reading  { background-position-y: -192px; animation-duration: 1.4s; }
```

## Why this works

- `background-position-x` is **separately animatable** from `-y`. The keyframe animates only X, so the Y set via class/inline-style isn't overwritten.
- `steps(N)` where N = column count gives frame-perfect transitions (no blur).
- `image-rendering: pixelated` + integer scale (`transform: scale(4)`) preserves crisp pixels at display size.
- Adding a class like `.working` simultaneously switches row AND speed — one line defines an entire animation state.

## Layering extra motion

Don't replace the spritesheet animation when adding overlay motion (bounce, jump). Put the character inside a wrapper and animate the wrapper instead:

```css
.char-wrap { animation: bob 1.1s steps(4) infinite; }
@keyframes bob { 0%,100% { margin-top: 0 } 50% { margin-top: -6px } }
```

Wrapper motion composes with sprite frame animation without conflict.

## Gotchas

- Never animate the full `background-position` shorthand — it overwrites both axes. Use `-x` and `-y` separately.
- JPEG sprite sheets with white backgrounds won't blend into dark UI. Preprocess with canvas chroma-key (see `canvas-chromakey-bg-removal`) or use PNG with alpha.
- Don't forget integer scaling or pixel art gets blurred by interpolation.
