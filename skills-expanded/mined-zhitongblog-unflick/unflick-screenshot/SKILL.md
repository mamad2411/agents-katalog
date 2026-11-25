---
name: unflick-screenshot
description: >-
  Capture the current video frame as an image with the unflick player, and tune
  the picture (brightness, contrast, saturation, gamma, hue). Use when the user
  asks to "screenshot", "grab this frame", "save a still", or adjust the image.
  Requires the unflick MCP server (or CLI).
license: MIT
---

# unflick: screenshot & picture tuning

## Screenshot

`screenshot(output?)` captures the current frame. With no `output` a path is
auto-generated; report it back. To screenshot a specific moment, `seek()` there
first, then `screenshot()`.

```bash
unflick seek 42
unflick screenshot --output frame.png
```

## Picture filters

Adjust the live image with the `filter_*` tools (values −100..100, 0 = neutral):

- `filter_list()` — current brightness/contrast/saturation/gamma/hue.
- `filter_set(name, value)` — `name` ∈ {brightness, contrast, saturation, gamma, hue}.
- `filter_reset()` — back to neutral.

## Looking at the frame yourself

`describe_frame(position?, max_edge?)` returns the frame as an **image block**
rather than a path, so a multimodal model can answer "what is on screen right
now" without a round trip through the filesystem. `max_edge` caps the long side
— keep it modest (768–1024) unless detail is the point.

```bash
unflick frame capture --position 42 --max-edge 1024
```

## Geometry

Separate from the colour filters below: `video_transform_get()` /
`video_transform_set(name, value)` / `video_transform_reset()` cover `aspect`,
`rotate`, `zoom`, `panscan` and `deinterlace` — the answers to "this is
squashed", "this was filmed sideways" and "this is combing".

## Flows

- **"Save the current frame"** → `screenshot()` → return the path.
- **"What's happening in this scene?"** → `describe_frame()` and answer from
  the image.
- **"This looks washed out"** → bump `filter_set("contrast", +20)` and/or
  `filter_set("saturation", +15)`; offer `filter_reset()` to undo.

## Guidance

- Filters affect on-screen playback live; a screenshot taken afterward reflects
  them. Mention this if the user wants a *clean* still.
- Keep filter nudges modest (±10–25) and report the resulting values.
