---
name: cesium-skills
description: >-
  Writes native CesiumJS demos for the latest stable Cesium API (async terrain,
  3D Tiles, imagery, WebGL2 shaders/effects). Use when creating or migrating
  Cesium Viewer, layers, terrain, Cesium3DTileset, models, CustomShader,
  PostProcessStage, materials, particles, or when old Cesium 1.x / WebGL1 demos
  break. Do not use for non-Cesium GIS or mars3d/SuperMap wrappers.
---

# Cesium Skills (native, latest API)

Generate **native CesiumJS** code aligned with the [official ref-doc](https://cesium.com/learn/cesiumjs/ref-doc/).

This skill ships **~185 modernized demo scripts** (`.js` only, no HTML) under [`examples/`](examples/), converted from Cesium-Examples `examples/cesiumEx` with async terrain/tileset, `baseLayer`, and WebGL2-oriented rewrites.

## Hard rules

1. **Native only** — call `Cesium.*` directly. No mars3d / SuperMap / custom SDK wrappers.
2. **Latest stable Cesium** — Ion CDN or `npm cesium`. Do not default to Cesium 1.98 paths.
3. **Modern async API** — prefer `fromUrl` / `fromGltfAsync` / `createWorldTerrainAsync` / `Terrain.fromWorldTerrain`. Never recommend `readyPromise` or `new Cesium3DTileset({ url })` / `new CesiumTerrainProvider({ url })` as the primary path.
4. **WebGL2 default** — never set `requestWebgl1: true`. Custom shaders follow [webgl2.md](webgl2.md).
5. **Container** — `div#map` unless the host project already differs.
6. **No default Ion basemap noise** — `baseLayer: false` + `baseLayerPicker: false`, then add imagery yourself. Do **not** use deprecated `imageryProvider: false`.
7. Prefer **Chinese section comments** when writing demos for Chinese users.
8. Prefer **Tianditu XYZ** as the sample imagery (placeholder `tk=`).
9. **Read `examples/<demo>.js` before inventing** non-trivial demos. Auto-migrated files may need small cleanup; apply [migration.md](migration.md) / [webgl2.md](webgl2.md) if anything still looks legacy.

## Workflow

```
- [ ] Identify feature (catalog.md / examples/README.md)
- [ ] READ examples/<matching>.js  (required for non-trivial features)
- [ ] Cross-check patterns.md / webgl2.md / scripts/ as needed
- [ ] Emit runnable HTML for the user (templates.md) using modern Cesium CDN
- [ ] Replace tokens/URLs; frame camera on the feature
```

Full index: [examples.md](examples.md) → [examples/README.md](examples/README.md).

Regenerate from upstream HTML (maintainers): `node _build-examples.mjs`

## Default Viewer bootstrap

```javascript
const viewer = new Cesium.Viewer('map', {
  baseLayer: false,
  baseLayerPicker: false,
  animation: false,
  timeline: false,
  geocoder: false,
  homeButton: false,
  sceneModePicker: false,
  navigationHelpButton: false,
  fullscreenButton: false,
  infoBox: false,
  selectionIndicator: false,
});

viewer.imageryLayers.addImageryProvider(
  new Cesium.UrlTemplateImageryProvider({
    url: 'https://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=YOUR_TIANDITU_TOKEN',
  })
);
```

World terrain (Ion token required):

```javascript
const viewer = new Cesium.Viewer('map', {
  baseLayer: false,
  baseLayerPicker: false,
  terrain: Cesium.Terrain.fromWorldTerrain(),
});
```

Helper: [scripts/createViewer.js](scripts/createViewer.js).

## Feature routing

| User asks for… | Read first |
| --- | --- |
| Any concrete demo (水波纹 / 地形 / 3D Tiles…) | Matching file in [examples/](examples/) |
| Viewer / camera / events / coords | `examples/1.*.js` + [patterns.md](patterns.md) |
| Imagery | `examples/2.1.*.js` |
| Terrain | `examples/2.2.*.js` + [migration.md](migration.md) |
| Entity / GeoJSON | `examples/2.3.*.js` |
| glTF / 3D Tiles / CustomShader | `examples/2.4.*.js`, `examples/3.1.*.js` |
| Analysis / measure / video | `examples/4.*.js` |
| Fog / particles / radar / fence | `examples/5.*.js` + [webgl2.md](webgl2.md) |
| Materials / wave / flow | `examples/7.*.js` + [scripts/](scripts/) |
| Heatmap / wind / isosurface | `examples/8.*.js` |
| Old demo broke after upgrade | [migration.md](migration.md) |

## Output expectations

- Emit a **complete runnable HTML** for the user (skill package itself has **no** `.html`).
- Load **latest** Cesium (see [templates.md](templates.md)), not `Cesium1.98`.
- Full-bleed `#map`; native APIs only; placeholder tokens.
- Effects must be WebGL2-safe.

## Quality checklist

- [ ] Started from `examples/*.js` when a matching demo exists
- [ ] No `imageryProvider: false` / `readyPromise` / `requestWebgl1`
- [ ] Terrain / tileset / model use async factories
- [ ] WebGL2-safe custom GLSL
- [ ] Tokens/URLs placeholders; camera framed

## Additional resources

- [examples.md](examples.md) / [examples/README.md](examples/README.md)
- [migration.md](migration.md) · [patterns.md](patterns.md) · [webgl2.md](webgl2.md)
- [templates.md](templates.md) · [catalog.md](catalog.md)
- [scripts/](scripts/)
