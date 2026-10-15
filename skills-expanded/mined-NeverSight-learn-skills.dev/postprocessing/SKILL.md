---
name: postprocessing
description: "Finish a 3D scene's look with the postprocessing library — a tasteful pass (ambient occlusion, subtle bloom, tone mapping, color grading) plus the correct WebGLRenderer attributes. Use to make a scene read as a polished game rather than a raw render, or for any screen-space image effect."
---

# Post Processing via `postprocessing`

A correct render of good geometry still looks unfinished without a finishing pass — that flat, raw look. A light, tasteful pass is part of a polished game's look, not an optional extra: **ambient occlusion** to ground objects in contact shadow, a **subtle bloom** so emissive and bright things glow, and **tone mapping + a gentle color grade** to set mood. Add it once the scene reads correctly, and keep it restrained — heavy bloom or crushed grading looks worse than none.

Post processing introduces the concept of passes and effects to extend the common rendering workflow with fullscreen image manipulation tools. The following WebGL attributes should be used for an optimal post processing workflow:

```js
import { WebGLRenderer } from 'three'

const renderer = new WebGLRenderer({
  powerPreference: 'high-performance',
  antialias: false,
  stencil: false,
  depth: false,
})
```

The `EffectComposer` manages and runs passes. It is common practice to use a `RenderPass` as the first pass to automatically clear the buffers and render a scene for further processing. Fullscreen image effects are rendered via the `EffectPass`.

```js
import { BloomEffect, EffectComposer, EffectPass, RenderPass } from 'postprocessing'

const composer = new EffectComposer(renderer)
composer.addPass(new RenderPass(scene, camera))
composer.addPass(new EffectPass(camera, new BloomEffect()))

requestAnimationFrame(function render() {
  requestAnimationFrame(render)
  composer.render()
})
```

## Output Color Space

New applications should follow a linear workflow for color management and postprocessing supports this automatically. Simply set `WebGLRenderer.outputColorSpace` to `SRGBColorSpace` and postprocessing will follow suit.

Postprocessing uses `UnsignedByteType` sRGB frame buffers to store intermediate results. This is a trade-off between hardware support, efficiency and quality since linear results normally require at least 12 bits per color channel to prevent color degradation and banding. With low precision sRGB buffers, colors will be clamped to `[0.0, 1.0]` and information loss will shift to the darker spectrum which leads to noticable banding in dark scenes. Linear, high precision `HalfFloatType` buffers don't have these issues and are the preferred option for HDR-like workflows on desktop devices. You can enable high precision frame buffers as follows:

```ts
import { HalfFloatType } from 'three'

const composer = new EffectComposer(renderer, {
  frameBufferType: HalfFloatType,
})
```

## Tone Mapping

Tone mapping is the process of converting HDR colors to LDR output colors. When using postprocessing, the `toneMapping` setting on the renderer should be set to `NoToneMapping` (default) and high precision frame buffers should be enabled. Otherwise, colors will be mapped to `[0.0, 1.0]` at the start of the pipeline. To enable tone mapping, use a `ToneMappingEffect` at the end of the pipeline.

Note that tone mapping is not applied to the clear color when using only the renderer because clearing doesn't involve shaders. Postprocessing applies to the full input image which means that tone mapping will also be applied uniformly. Consequently, the results of tone mapping a clear color background with and without postprocessing will be different, with the postprocessing approach being correct.

## Performance

This library provides an `EffectPass` which automatically organizes and merges any given combination of effects. This minimizes the amount of render operations and makes it possible to combine many effects without the performance penalties of traditional pass chaining. Additionally, every effect can choose its own blend function.

All fullscreen render operations also use a single triangle that fills the screen. Compared to using a quad, this approach harmonizes with modern GPU rasterization patterns and eliminates unnecessary fragment calculations along the screen diagonal. This is especially beneficial for GPGPU passes and effects that use complex fragment shaders.

## Included Effects

- Antialiasing
- Bloom
- Blur
- Color Depth
- Color Grading
  - Color Average
  - Sepia
  - Brightness & Contrast
  - Hue & Saturation
  - LUT
- Depth of Field
  - Vignette
- Glitch
  - Chromatic Aberration
  - Noise
- God Rays
- Pattern
  - Dot-Screen
  - Grid
  - Scanline
- Pixelation
- Outline
- Shock Wave
  - Depth Picking
- SSAO
- Texture
- Tone Mapping
