---
name: maplibre-marker-rendering
description: Use when rendering custom icons/markers on MapLibre maps.
license: MIT
metadata:
  hermes:
    tags:
    - maplibre
    - mapbox
    - maps
    - svg
    - markers
    - z-index
    related_skills:
    - frontend-design-skills
  source_frontmatter:
    version: 1.0.0
    author: Hermes
  imported_from: hermes
---

# MapLibre icon & marker rendering

## When to Use

Trigger when the task involves MapLibre GL JS (or Mapbox GL) rendering: custom SVG/PNG icons, markers layered above/below other map elements, z-order conflicts between markers and canvas layers, or outlined icon styling. Also useful when debugging a MapLibre layer that silently renders nothing.

Render custom vehicle/POI icons on MapLibre GL JS maps with correct loading, z-order, and outlined-icon styling. Proven on the CUpedia campus-bus map (bus icon above station markers, gold fill + white outline).

## Icon loading: avoid `map.loadImage` for SVG data URLs

MapLibre 5.x `loadImage`'s internal Image path is unreliable for `data:image/svg+xml` — its own error string says "Note that SVGs are not supported". A bare `<img src=svgDataUrl>` loads fine in browsers, so the failure is inside MapLibre's fetch/Image pipeline.

**Working pattern — offscreen canvas → ImageData → `addImage`:**
```ts
const canvas = document.createElement("canvas");
canvas.width = 24; canvas.height = 24;
const ctx = canvas.getContext("2d")!;
const img = new Image();
img.onload = () => {
  ctx.drawImage(img, 0, 0);
  const imageData = ctx.getImageData(0, 0, 24, 24);
  if (!map.getImage("bus-icon")) map.addImage("bus-icon", imageData);
};
img.src = BUS_ICON_DATA_URL; // encodeURIComponent of the SVG string
```
Then a `symbol` layer with `layout: { "icon-image": "bus-icon", "icon-size": 1.4 }`.

## Layering: DOM markers always beat canvas layers

- Symbol/line layers render inside the WebGL canvas. **DOM markers (`new maplibregl.Marker({element})`) always paint above the canvas**, regardless of layer order.
- To put an icon *above* another marker (e.g. bus over station circle): render BOTH as DOM markers and give the top one a higher CSS `z-index`. A canvas symbol layer can never sit above a DOM marker.
- DOM marker element class must be on the element you pass to `Marker({element})`; style `pointer-events: none` on non-interactive icons so they don't block clicks.
- Track markers in a `Map<departureAt, Marker>` ref; on each position update call `marker.setLngLat(...)`, create on first sight, `marker.remove()` + delete for departed; clear all in effect cleanup.

## Two-layer SVG for outlined icons (user-corrected pattern)

User rule (CUpedia): solid gold fill `#d4a538` with a **thin white outline that must NOT cover the fill**. A single path with `fill` + wide `stroke` paints the stroke half-inside, eating the fill.

**Working pattern — draw the same path twice:**
```svg
<svg viewBox="0 0 24 24">
  <path d="…" fill="#ffffff" stroke="#ffffff" stroke-width="4" stroke-linejoin="round"/>
  <path d="…" fill="#d4a538"/>
</svg>
```
White layer first (fill+stroke expands silhouette outward), gold layer second covers the white interior; only the outer ~2px white ring remains. `fill-rule="evenodd"` keeps interior holes (windows/wheels) transparent. This SVG renders directly in a DOM marker via `element.innerHTML = BUS_ICON_SVG` — no data URL needed at all.

## Pitfalls

- `map.loadImage` + SVG: failure is silent-ish (layer renders nothing); check `map.getImage()` / console rather than assuming the layer is wrong.
- External raster basemaps (e.g. HK Lands Dept tiles) fail offline → whole map looks blank gray. Verify tile network before blaming your own layer code (browser reload often fixes it; dev server also periodically hangs — restart it).
- Next.js dev: `tsconfig.json` gets auto-reformatted on dev-server boot; `git checkout tsconfig.json` before committing.
- 1s UI refresh + hot reload can wedge the dev server (HTTP 000); kill and restart (`lsof -ti:3000 | xargs kill -9`).

## Verification (no reliable vision in headless)

- Screenshot → cluster pixels by target color (gold ≈ RGB 190-235/145-185/40-80) to locate the icon, crop around the cluster, then `vision_analyze` the crop to confirm the shape.
- Check docking/selected states via `data-*` attributes in the DOM rather than pixel-hunting.
