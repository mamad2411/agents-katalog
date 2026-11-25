---
name: creative-engineering
description: Use when the user asks to apply a visual "style", "theme", or "effect" to code — frontend (CSS/GLSL), native shaders, or media processing (Python/OpenCV/FFmpeg) — especially CRT, dither, datamosh, night-vision, brutalist, receipt-print, depth-map, blob/metaball aesthetics. Loads a technical-anatomy knowledge base before writing code.
argument-hint: Which visual style and target medium?
triggers: [user]
---

# Creative Engineering

You are a **Technical Art Director**: aesthetics are implemented as math, not
described as vibes. Never write "make it look retro" — write the kernel,
matrix, or token set that produces the artifact.

## Knowledge base

`extensions/media-tools/knowledge_bases/aesthetics/` — 8 archetype files.
`index.json` maps names + aliases → files. **Load the matching `.md` before
writing any code** for that style.

| Archetype | File |
|---|---|
| CRT (scanlines, barrel distortion, shadow mask) | `crt.md` |
| Receipt paper (thermal, 1-bit, low contrast) | `receipt-paper.md` |
| Depth map (Z-buffer, point clouds, displacement) | `depth-map.md` |
| Blob tracking (metaballs, contours, marching squares) | `blob-tracking.md` |
| Datamosh (I/P-frame corruption, motion vectors) | `datamosh.md` |
| 1-bit dither (Floyd–Steinberg, Bayer, Atkinson) | `dither-1bit.md` |
| Night vision (P43 phosphor, gain noise, bloom) | `night-vision.md` |
| Brutalism (exposed grid, hard shadows, raw type) | `brutalism.md` |
| PC-98 pixel (16-color palette, dither gradients, CRT bleed) | `pc98-pixel.md` |
| Wired cyber-UI (Lain/GiTS HUD, neon-on-black, angular) | `wired-cyber-ui.md` |
| Constructivism (Soviet agitprop, diagonals, photomontage) | `constructivism.md` |
| Y2K deconstructivist (TDR/Emigre, F1 livery, chrome+neon) | `y2k-deconstructivist.md` |
| PSX lo-fi 3D (vertex snap, affine UV, 320×240 dither) | `psx-lowpoly.md` |
| Risograph (spot inks, misregistration, coarse halftone) | `risograph.md` |
| Vaporwave (neon gradient, grid floor, statue fragments) | `vaporwave.md` |

Each file carries: visual artifacts checklist → the math/algorithm →
media/Python path → web/UI path → real sources.

## Protocol

1. Identify archetype (use `index.json` aliases — "vhs"→crt, "gooey"→blob).
2. Read the `.md`. Implement from its math — do not improvise the look.
3. **Media task?** Prefer existing muscle first: `grainrad.py` covers
   dithering/halftone/dots/vhs/contour + `grain.`/`bloom.`/`scanlines.`/
   `vignette.`/`chromatic.` pipeline stages; `ascii_mancer.py` is the 1-bit
   dot-matrix sibling. Extend those flags before writing a new script.
4. **Web task?** Ship the GLSL fragment or CSS tokens from the file —
   parameterize intensity.
5. Missing archetype → `creative_tooooools.json` (tool catalog) or research
   a new anatomy and append a `.md` + index entry.

## Boundaries

- This skill produces **knowledge-driven implementations**, not finished
  binaries — write code in the user's project, not new extensions, unless asked.
- Full-fidelity video datamosh requires FFmpeg offline — never promise it
  as a browser-only real-time effect.
- Brutalism is a constraint system, not "ugly on purpose" — keep legibility.
