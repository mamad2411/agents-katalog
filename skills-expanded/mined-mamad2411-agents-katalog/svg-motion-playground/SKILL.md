---
name: svg-motion-playground
description: Generate a standalone no-build HTML playground that turns an input SVG into a live liquid-glass material animation using the bundled WebGL renderer and schema-driven controls.
---

# SVG Motion Playground

Generate a single self-contained `.html` playground from an SVG and an animation prompt. The output must open directly in a browser with no npm install, build step, dev server, CDN, or external runtime dependency.

## Important: Treat This Skill As Read-Only

When this skill is installed under `.claude/skills/`, `~/.claude/skills/`, `.codex/skills/`, or any other agent skill directory, do not edit the skill files themselves while using the skill. Treat `SKILL.md`, `assets/`, `references/`, and `scripts/` as read-only implementation resources.

### Fixed Skill Resources

These files are fixed implementation resources. Read them as needed, but do not modify them during normal skill use:
- `SKILL.md`
- `README.md`
- `assets/playground-template.html`
- `assets/control-kit/styles/*.css`
- `assets/control-kit/*.js`
- `assets/control-kit/components/*.js`
- `assets/parameters.json`
- `assets/renderers/webgl-fragment-material.js`
- `scripts/generate-playground.js`
- `references/*.md`
- `examples/*`

The template, renderer, controls, parameter schema, generator, examples, and references are the tool. They are not the user's output.

### Variable User Outputs

For normal use, write only project-local files requested or implied by the user:
- an optional mask-ready SVG next to the user's source SVG
- the generated standalone playground HTML
- optional notes explaining where the output was written

Good output examples:
- `camera-mask.svg`
- `camera-liquid-glass-playground.html`
- `logo-motion-playground.html`

Bad actions during normal use:
- patching `.claude/skills/svg-motion-playground/scripts/generate-playground.js`
- editing `.claude/skills/svg-motion-playground/assets/renderers/webgl-fragment-material.js`
- changing `SKILL.md` because the user named a control differently
- updating bundled examples instead of writing a project-local output

Do not patch `scripts/generate-playground.js`, renderer files, templates, references, or this `SKILL.md` to satisfy a user prompt. If the prompt asks for controls already supported by the bundled schema, use the existing schema. If the prompt asks for unsupported behavior, explain the limitation or create a separate project-local custom renderer only when explicitly requested.

## Workflow

### 1. Inspect the SVG

Parse the SVG for:
- `viewBox` dimensions
- Whether visible filled or stroked content will rasterize clearly as a mask
- Very thin strokes or tiny details that may need a larger output size
- Whether separate visible pieces touch each other

### 2. Prepare the mask shape

Before embedding the SVG, decide what visual surface should receive the material. The mask should represent the logo/object surface to coat with liquid glass, not merely every original SVG command.

Use this mask-intent classification:

- Filled logo or mark: preserve the visible filled regions and normalize them to white on transparent.
- App tile or badge: preserve the tile/background shape and any intentional foreground cutouts as transparent holes. A bird-shaped cutout inside a rounded square should stay cut out; the rounded square remains the material surface.
- Faceted or geometric logo: preserve each intended plane/band as material surface, including intentional inner voids and seams. Do not collapse a cube, prism, or polygon mark into its convex hull.
- Sliced or striped logo: preserve separate slices/stripes as separate material islands with transparent gaps between them.
- Letterform or wordmark: preserve counters and punched holes, such as the holes in `a`, `o`, `p`, or rounded vertical slots.
- Stroke-only object icon: infer the filled object silhouette only when the strokes are construction outlines for a solid thing.

If the SVG is a stroke-only line icon that outlines a solid object, do not use the stroke rails as the chrome mask unless the user explicitly asks to preserve the outline drawing. Instead, infer a filled object silhouette:
- Fill the intended object body as one white surface.
- Keep only semantic holes/counters transparent, such as a camera lens opening or letter counters.
- Do not turn inner stroke edges into extra rectangular/ring cutouts.
- Use `fill-rule="evenodd"` when a single path needs holes.

For a camera-style outline icon, the expected mask is a solid camera body with the lens cut out. A mask that looks like a hollow camera frame plus a lens ring is wrong for the default liquid-glass material because the shader will only coat those rails.

For complex logos, preserve intentional negative space:
- If the logo shows a black symbol carved out of a colored/chrome tile, keep that symbol transparent.
- If the logo is made of separated bands, facets, or strokes that are themselves the mark, keep those bands as the material and keep the gaps transparent.
- If the logo has a large outer tile plus inner holes, use `fill-rule="evenodd"` or separate white paths plus transparent holes so the mask preview matches the intended design.
- Do not fill across meaningful gaps just to make one blob. Do not preserve decorative construction strokes when the source is only an outline drawing.

When automatic conversion is ambiguous, use visual/model reasoning from the SVG path geometry to create a project-local `*-mask.svg`, then embed that mask-ready SVG in the playground. The mask preview should look like the surface the user expects to become chrome, not like construction lines from the original icon.

### 3. Use the bundled renderer

Use `assets/renderers/webgl-fragment-material.js` by default. The renderer treats the SVG as one full mask for compositing, then internally derives connected-component metadata from the rasterized alpha texture. Each component receives deterministic seed-based variation so separate pieces do not move in lockstep.

The renderer also builds a mask-field texture from the rasterized SVG. This gives the shader distance-to-silhouette, inward-normal, and coarse component-profile data, so chrome curvature follows the actual shape instead of the component bounding box.

Do not hand-code branches for a specific SVG's shape order in the default renderer. If a future project genuinely needs custom art direction, make a separate renderer file and keep the default renderer generic.

### 4. Use the bundled parameter schema

Use the bundled `assets/parameters.json` parameter schema as-is. Core V1 controls cover: preview size, motion speed, morph speed, viscosity, distortion, edge shine, highlight strength, contrast, bevel width, bevel strength, light angle, metal tint, background, mask softness, and animate noise.

If the user uses alternate names for supported controls, map them to the existing schema instead of editing the schema:
- "highlight strength", "exposure", "specular strength", and "shine strength" map to `highlightStrength`
- "tint" and "metal tint" map to `metalTint`
- "speed" maps to `motionSpeed` unless the user specifically means `morphSpeed`

### 5. Generate the standalone HTML

Prefer manual assembly without shell commands. Read the fixed resources from the installed skill directory, replace the placeholders in `assets/playground-template.html`, and write the completed HTML to the user's project/workspace.

Replace these placeholders exactly:
- `{{TITLE}}`: the requested playground title
- `{{CONTROL_CSS}}`: contents of the control-kit style files concatenated in the order listed below, indented inside the `<style>` block
- `{{SOURCE_SVG}}`: contents of the mask-ready SVG, or the user SVG only when it is already a good mask, indented inside the `source-svg` script tag
- `{{PARAMETERS_JSON}}`: contents of `assets/parameters.json`
- `{{CONTROL_JS}}`: contents of the control-kit design-system files concatenated in the order listed below
- `{{RENDERER_JS}}`: contents of `assets/renderers/webgl-fragment-material.js`
- `{{RENDERER_NAME}}`: `webgl`

Concatenate control-kit style files in this exact order:
- `assets/control-kit/styles/tokens.css`
- `assets/control-kit/styles/layout.css`
- `assets/control-kit/styles/controls.css`
- `assets/control-kit/styles/responsive.css`

Concatenate control-kit files in this exact order:
- `assets/control-kit/core.js`
- `assets/control-kit/components/panel-header.js`
- `assets/control-kit/components/panel-section.js`
- `assets/control-kit/components/slider-control.js`
- `assets/control-kit/components/toggle-control.js`
- `assets/control-kit/components/color-control.js`
- `assets/control-kit/components/xy-pad-control.js`
- `assets/control-kit/create-control-panel.js`

Before writing the output, confirm no `{{...}}` placeholders remain. The output must be one standalone `.html` file in the user's project/workspace.

### 6. Optional Node Convenience

If the user explicitly allows shell commands or wants the generator script, run the installed generator as a convenience wrapper and point `--out` at the user's project/workspace. Node is not required for normal skill use; it only assembles the same text resources described above.

```bash
node /absolute/path/to/svg-motion-playground/scripts/generate-playground.js \
  --svg /absolute/path/to/input.svg \
  --out /absolute/path/to/output.html
```

When using Claude Code, the skill directory may be inside `.claude/skills/svg-motion-playground` or `~/.claude/skills/svg-motion-playground`. Resolve the installed skill path, then run its generator. Do not copy the user's SVG into the skill directory.

The optional `--renderer` flag accepts an absolute path to a custom renderer file. Use it only for deliberate custom experiments; normal generation should omit it.

### 7. Verify

Open the output HTML directly from disk. Check:
- Animation starts immediately without a server
- Separate connected pieces do not move in perfect lockstep
- Stroke-only object icons were converted to the intended filled silhouette
- The mask does not look like hollow outline rails unless the user asked for an outline material
- No dark rounded rectangle or bounding-box artifact is visible inside shapes
- No hard ring artifacts inside shapes
- Edge silhouettes are brighter than shape interiors
- `Distortion`, `Light Angle`, and `Highlight Strength` each have an obvious visual effect

## Control Rules

- Prefer direct controls over presets.
- Every exposed parameter must visibly affect the output.
- Use bundled components only: `PillSlider`, `TogglePill`, `ColorSwatch`, `SegmentedControl`, `XYPad`, `IconButton`, and `PanelSection`.

## Renderer Rules

- The generated HTML must embed all renderer/shader code.
- Do not use Three.js, React, Vite, Tailwind, package managers, CDNs, external shader files, or network requests.
- The template, control kit, renderer, and parameter schema are reused as-is for normal V1 generation.

## References

- `references/animation-recipes.md`: liquid-glass recipe and renderer behavior notes.
- `references/control-components.md`: supported control schema.
- `references/svg-intake-checklist.md`: SVG inspection and verification checklist.
