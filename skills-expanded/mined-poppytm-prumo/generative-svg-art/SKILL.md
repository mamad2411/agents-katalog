# Generative SVG Art

## 1. Purpose
To create procedural SVG artwork utilizing flow fields, L-systems, Voronoi tessellations, noise functions, and advanced SVG filters for dynamic and reproducible visual aesthetics.

## 2. Use When
- Generating algorithmic backgrounds or textures.
- Creating parametric design assets.
- Applying organic textures via SVG filters like `feTurbulence` and `feDisplacementMap`.

## 3. Do Not Use When
- Building highly optimized, simple UI icons.
- Working with raster-heavy image requirements (use Canvas/WebGL instead).

## 4. Required Context
- Desired visual style (e.g., organic, geometric, chaotic).
- Seed and algorithmic constraints.
- Target dimensions and performance budgets.

## 5. Procedure
1. Initialize a base SVG structure with precise dimensions.
2. Define `feTurbulence` and `feDisplacementMap` filters in `<defs>` for textures.
3. Compute path geometries using chosen algorithms (e.g., Perlin noise for flow fields, L-systems for fractals).
4. Apply parametric values and CSS custom properties for styling.
5. Render SVGs and test cross-browser filter rendering.

## 6. Decision Rules
- Use seeded random numbers to guarantee reproducibility.
- Ensure filter dimensions (e.g., `x`, `y`, `width`, `height`) extend beyond element bounds to prevent clipping.

## 7. Evidence Required
- A visually valid and properly formatted SVG output.
- Parameters explicitly mapped to CSS or SVG attributes.

## 8. Output Contract
- Valid, self-contained SVG files or snippets.
- Documentation of the seed and parameters used.

## 9. Stop Conditions
- The SVG renders correctly without performance bottlenecks or excessive DOM nodes (keep path counts reasonable).

## 10. Escalation Rules
- Escalate if computational complexity exceeds rendering limits (e.g., >10,000 paths).
