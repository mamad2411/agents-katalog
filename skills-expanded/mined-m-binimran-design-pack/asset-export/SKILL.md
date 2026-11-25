---
name: asset-export
description: Produce a clean export/delivery spec - right formats, sizes, densities, naming, color profile, optimization - for a set of assets. Use when delivering assets to a client or developer.
---

# asset-export

Deliverables that drop straight into production: correct format, size, name, and weight.

## Process
1. **Map each asset to its use:** logo -> SVG (+ PNG fallback); icons -> SVG; raster -> WebP/AVIF or optimized
   PNG/JPG; print -> PDF/CMYK with bleed; video -> MP4/WebM.
2. **Densities:** @1x/@2x/@3x for raster UI assets; responsive sizes for web heroes.
3. **Name** lowercase kebab-case with density suffix (`hero-banner@2x.webp`) - the `asset-naming-guard` hook checks.
4. **Optimize:** compress, strip metadata bloat; keep heroes lean (don't ship 8MB images).
5. **Colour profile:** sRGB for screen, CMYK for print; embed where needed.
6. **Manifest:** list file -> format -> size -> source -> license (`templates/ASSET-MANIFEST.md`).

## Output
- The export spec / manifest (file, format, dimensions, density, profile, optimization, license) ready for handoff.

## Guardrails
- Lowercase kebab-case names; right format per use; optimized weights.
- Don't embed big binaries in text or commit large exports to git (the `large-asset-guard` hook).
