---
name: creative-visual-production
description: "Use when producing visual creative artifacts: ASCII art/video, diagrams, comics, article illustrations, pixel art, p5.js/Manim animations, HTML mockups, design systems, ComfyUI media, or style-guided web visuals."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Creative Visual Production

Umbrella skill for visual and motion output. Pick the subsection by artifact class, load supporting references only when needed, and verify the produced file or render.

## Text and ASCII visuals
- `ascii-art`: banners, cowsay/boxes, image-to-ASCII stills.
- `ascii-video`: colored ASCII MP4/GIF, terminal-style animations, audio-reactive ASCII.
- `pretext`: DOM-free text layout, kinetic typography, text-as-geometry browser demos.

## Diagrams and sketches
- `excalidraw`: hand-drawn `.excalidraw` architecture, flow, and sequence diagrams.
- `sketch`: throwaway HTML mockups with 2–3 variants for comparison.
- `claude-design`: one-off polished HTML artifacts, landing pages, decks, prototypes.
- `design-md`: DESIGN.md design-token specs for coding agents.
- `popular-web-designs`: real brand/style templates for web UI direction.

## Illustration and comics
- `baoyu-article-illustrator`: article illustrations with type × style × palette consistency.
- `baoyu-comic`: knowledge comics, educational explainers, biographies, tutorials.
- `pixel-art`: retro pixel-art conversion/generation using era palettes.

## Programmatic animation and media generation
- `p5js`: creative coding, canvas, interactive visualization, shaders, WebGL.
- `manim-video`: mathematical/algorithmic explainers and 3Blue1Brown-style animations.
- `comfyui`: image/video/audio generation via ComfyUI workflows and API.

## Verification
- For files: confirm output exists and has the expected extension/size.
- For browser demos: open or render a screenshot if possible.
- For generated media: report exact path(s), workflow used, and any model/API limitations.

## Common pitfalls
- Do not flatten large package references; preserve support files under this skill if absorbed.
- Avoid one giant prompt for multi-frame/multi-scene work; separate style, storyboard, and render parameters.
- If a generator or dependency is unavailable, state the blocker and offer a fallback artifact type.
