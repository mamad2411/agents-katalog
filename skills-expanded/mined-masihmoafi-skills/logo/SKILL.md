---
name: logo
description: Generate logos, icons, ornaments, illustrations, badges and diagrams with the image tool, then keep the chosen artwork as real SVG paths through SVG Studio. Use for an image-first visual-to-SVG request or /logo.
---

# Image first, then SVG

Generate a high-quality image, turn it into SVG paths with SVG Studio, then animate it or use it as an icon. That is the whole job. Bad image prompts are what break it.

## 1. Prompt well

Write each prompt in five parts, and keep the prompts the user approved in one file so new ones copy their shape:

- **One concrete, recognizable subject that carries the meaning:** two offset robot heads for many agents; a crane whose wing folds around a sun for a tea house. Never abstract planes, plain letters or generic geometry.
- **Describe it part by part:** pose, shapes, cutouts, and where the empty space falls.
- **Name its use and size:** "toolbar icon, unmistakable at 20 px, no detail smaller than one eighth of its width, fills 85% of the square canvas".
- **One flat ink colour (a hex code) on genuine transparency.**
- **A short no-list:** gradients, shading, outlines, text, badge, mockup.

Use the built-in image tool only, one image per call, and make three distinct directions for a new design. Save each exact prompt beside its image. The user picks one; a recommendation is not a choice.

## 2. Turn it into SVG

Use SVG Studio's MCP tools: `vectorize_multicolour_image` for colour art, `vectorize_image` for one ink. Without the MCP tools, run the CLI wrapper from this folder:

```sh
SVG_STUDIO_MODULE=/path/to/svg/mcp-server/dist/vectorize.js node scripts/trace.mjs source.png output.svg 24
```

Keep the holes, and frame the viewBox to the mark. Output only real paths with explicit fills: no embedded raster, script, foreignObject or font. Never redraw the design by hand.

## 3. Check, then use

```sh
SVG_STUDIO_MODULE=/path/to/svg/mcp-server/dist/vectorize.js node scripts/proof.mjs proof.png source.png output.svg
```

Look at source and SVG side by side, on light and on dark, at the size they will be used. Visible damage fails even when the numbers look good. Then animate it (SVG or CSS) or place it as the icon. The wrapper's own checks: `node --test test/pipeline.test.mjs`, with the same `SVG_STUDIO_MODULE`.
