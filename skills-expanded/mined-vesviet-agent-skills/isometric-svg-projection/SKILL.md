---
name: isometric-svg-projection
description: Use when generating precision isometric vector diagrams, engineering schematics, and CAD projections with standardized SVG millimeter coordinates and stroke weights.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build]
---

# Isometric SVG Projection

Generate publication-grade 2D vector technical drawings from 3D coordinate geometry using standardized isometric transformation matrices, millimeter units, and ISO drafting line weights.

## When to Use

- Generating isometric exploded assembly diagrams or technical product schematics
- Rendering scale-accurate architectural or mechanical illustrations in SVG
- Transforming 3D bounding geometry and part vertices into clean 2D vector paths
- Standardizing line weight hierarchies, dimension callouts, and projection ellipses
- Producing publication-ready vector figures for technical reports and user manuals

## Core Rules

- **Millimeter Coordinate Space**: Map $1\text{ SVG user unit} = 1\text{ mm}$ on standard sheets. Default standard sheet is Landscape A3 ($420 \times 297\text{mm}$, `viewBox="0 0 420 297"`). Never use unitless pixels or non-metric scaling.
- **Isometric Transformation Matrix**: Project 3D $(x,y,z)$ coordinates to 2D $(x_{\text{proj}}, y_{\text{proj}})$ via $\pm 30^\circ$ isometric mapping:
  $$x_{\text{proj}} = \text{ox} + \text{scale} \cdot \frac{\sqrt{3}}{2}(x - y), \quad y_{\text{proj}} = \text{oy} + \text{scale} \cdot \left(0.5(x + y) - z\right)$$
  - $+x$ projects down-right at $+30^\circ$ below horizontal
  - $+y$ projects down-left at $+30^\circ$ below horizontal
  - $+z$ projects vertically upwards at $90^\circ$
- **4-Tier Stroke Hierarchy (ISO 128 / ISO 5456)**: Strictly enforce line weights:
  - Tier 1 (Heavy, `0.35mm`): Silhouettes, cutting planes, primary perimeters
  - Tier 2 (Medium, `0.22mm`): Visible component edges, internal contours
  - Tier 3 (Light, `0.16mm`): Dimension lines, extension lines, leader callouts
  - Tier 4 (Fine, `0.13mm`): Centerlines, hatching patterns, explode trails
- **Dash Array Standards**: Hidden edges use `stroke-dasharray="2 1"`; centerlines use `stroke-dasharray="6 1 1 1"`; explode trails use `stroke-dasharray="4 1.5 1 1.5"`.
- **Ellipse Orientation**: Project circular features on isometric planes as ellipses with aspect ratio $\sqrt{3} : 1 \approx 1.732 : 1$:
  - Top plane ($xy$): Major axis is horizontal ($0^\circ$)
  - Right plane ($xz$): Major axis is tilted at $+60^\circ$
  - Left plane ($yz$): Major axis is tilted at $-60^\circ$ ($120^\circ$)
- **Structured Grouping**: Every SVG output must group paths by semantic role (`<g id="silhouettes">`, `<g id="visible-edges">`, `<g id="hidden-edges">`, `<g id="dimensions">`, `<g id="annotations">`).

## Suggested Process

### 1. Establish Sheet Geometry and Framing
- Define the SVG root element with Landscape A3 millimeter dimensions (`viewBox="0 0 420 297"`).
- Insert standard outer border with $12\text{mm}$ margins (`x="12" y="12" width="396" height="273"`).
- Construct the $24\text{mm}$ title block band across the bottom inner border (`y="261"`).
- Calculate uniform scale factor and origin offsets $(\text{ox}, \text{oy})$ to center model geometry.

### 2. Transform 3D Geometry and Compute Projections
- Convert all 3D mesh vertices $(x,y,z)$ to projected 2D coordinates using the isometric matrix.
- Calculate outward surface normal vectors $\mathbf{n} = (n_x, n_y, n_z)$ for each planar polygon.
- Compute view dot product $V = \mathbf{n} \cdot \mathbf{v}_{\text{cam}}$ to classify visible versus back-facing surfaces.
- For circular holes and cylindrical faces, compute conjugate diameters and project oriented SVG `<ellipse>` or path arcs.

### 3. Layer and Style Vector Paths
- Render visible object contours using Tier 2 stroke weight (`0.22mm`, `stroke="currentColor"`).
- Render boundary silhouettes using Tier 1 stroke weight (`0.35mm`).
- Trace hidden structural features with Tier 3 stroke weight (`0.16mm`) and `stroke-dasharray="2 1"`.
- Add symmetry centerlines with Tier 4 stroke weight (`0.13mm`) and `stroke-dasharray="6 1 1 1"`.

### 4. Layout Dimensions, Explode Trails, and Callouts
- Trace exploded assembly guide trails between separated components using Tier 4 dashed lines.
- Position dimension lines offset by at least $8\text{mm}$ from visible geometry.
- Draw leader lines with $0.8\text{mm}$ terminal markers (filled dots or $30^\circ$ closed arrows) and horizontal shoulders.
- Format dimension values in system sans-serif typography ($1.8\text{mm}$ text height).

### 5. Annotate Title Block and Review Quality
- Populate title block fields: Project Name, Part Number, Drawing Scale, Projection Symbol, and Date.
- Validate that all vector paths remain within sheet margins and zero stroke clipping occurs.
- Verify stroke weights and colors adhere strictly to calibrated ISO token classes.

## Output Format

Outputs should include the generated SVG document and an engineering metadata brief:

```markdown
# <Part/Assembly Name> - CAD Projection Brief

## Drawing Specifications
- Sheet standard: ISO Landscape A3 (420 x 297 mm)
- Coordinate scale: 1 unit = 1 mm (Scale 1:1 or calibrated ratio)
- Center origin: (ox, oy)
- Stroke weight tiers applied: Tier 1 (0.35mm), Tier 2 (0.22mm), Tier 3 (0.16mm), Tier 4 (0.13mm)

## Geometry Summary
- Total transformed vertices: <count>
- Projected components: <list of parts>
- Isometric planes utilized: Top (xy), Right (xz), Left (yz)

## SVG Artifact
[Embedded or referenced SVG vector drawing]
```

## Failure Modes

- **Unitless pixel scaling**: Arbitrary pixel dimensions cause scale degradation during print or high-DPI zoom. **Mitigation**: Bind SVG canvas to metric millimeter viewBox with $1:1$ physical mapping.
- **Occlusion inversions**: Drawing occluded edges with solid strokes creates ambiguous optical illusions. **Mitigation**: Perform back-face culling and style hidden lines with distinct dash arrays.
- **Distorted circular features**: Drawing unrotated circles on tilted isometric planes breaks perspective. **Mitigation**: Compute exact elliptical major and minor axes from isometric surface plane normals with $\sqrt{3}:1$ ratio.
- **Floating-point path bloat**: Unrounded float values in path data bloat SVG file size. **Mitigation**: Round coordinate strings to 2 decimal places ($0.01\text{mm}$ precision).
- **Unstructured SVG hierarchy**: Emitting ungrouped path tags prevents post-processing and styling. **Mitigation**: Structure paths into semantic `<g>` layers.

## Output Contracts

When producing technical drawing packages or component specs, emit:

- Standalone, valid SVG document formatted with ISO sheet frame, calibrated stroke tiers, and title block metadata.
- If accompanying a 3D configurator or UI feature, record deliverable in `contracts/schemas/implementation-result.json`.

## Security Guardrails (OWASP ASI)

- **ASI05 Code Injection Guard**: Never embed unescaped user-supplied strings or external scripts directly into SVG `<script>` or `<foreignObject>` tags.
- **ASI07 Safe Asset Generation**: All generated SVG vector coordinates must derive from sanitized numeric geometry arrays; reject unbounded vertex counts ($> 100{,}000$ points) that cause client DOM exhaustion.

## Checklist

- [ ] SVG canvas initialized with Landscape A3 millimeter dimensions (`viewBox="0 0 420 297"`).
- [ ] Sheet border ($12\text{mm}$ margin) and title band ($24\text{mm}$ height) accurately positioned.
- [ ] Isometric projection matrix applied consistently to all 3D vertices ($x_{\text{proj}}, y_{\text{proj}}$).
- [ ] 4-tier stroke weight hierarchy enforced (`0.35mm`, `0.22mm`, `0.16mm`, `0.13mm`).
- [ ] Hidden edges and centerlines use calibrated dash arrays (`2 1` and `6 1 1 1`).
- [ ] Circular features projected as oriented isometric ellipses with $\sqrt{3}:1$ aspect ratio.
- [ ] Exploded assembly trails use calibrated dash arrays (`4 1.5 1 1.5`).
- [ ] Dimension callouts and leader lines terminate with valid arrowheads or dots.
- [ ] Text annotations styled with standardized font sizes (`3.5mm`, `2.5mm`, `1.8mm`).
- [ ] All coordinates rounded to 2 decimal places to prevent SVG payload bloat.
- [ ] Paths grouped into semantic `<g>` layers (`silhouettes`, `visible-edges`, `hidden-edges`, `dimensions`).

## Related Skills

- **debug-3d-scene**: Trace 3D transformations, scene graphs, and camera matrices before 2D projection
- **optimize-3d-assets**: Simplify source 3D polygon meshes and extract clean edge geometry
- **design-ux-flow**: Incorporate technical schematics into interactive user experience workflows
- **review-code**: Audit vector generation algorithms and SVG DOM performance
- **frontend-testing**: Validate SVG rendering across diverse screen resolutions and container bounds
