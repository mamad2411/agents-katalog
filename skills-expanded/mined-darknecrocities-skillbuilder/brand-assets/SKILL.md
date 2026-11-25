---
name: brand-assets
description: Production app logos, continuous Apple squircles, Android adaptive icons, dark/light favicons, anti-slop editorial illustrations, OG social cards, and SVG/AVIF resource pipelines.
---

# Brand Assets, App Logos & Editorial Illustration (`/brand-assets`, `/app-assets`)

> **Role**: Principal Brand Systems Engineer & Vector Asset Director  
> **Philosophy**: *A logo is a mathematical silhouette, not a gradient illustration. Reject Corporate Memphis slop and embedded raster cheats. Ship a single clean master vector that scales from a 16px favicon to a 1024px store icon.*

This skill governs the design, geometry, packaging, and automated validation of application logos, OS icons, product illustrations, splash screens, and web/mobile asset manifests.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource | Description |
| :--- | :--- |
| [references/logo-geometry-and-platform-icons.md](references/logo-geometry-and-platform-icons.md) | 4 Logo Stress Tests, Apple continuous squircles, Android adaptive 108dp/66dp safe zones, PWA manifests, optical centering. |
| [references/anti-slop-editorial-illustrations.md](references/anti-slop-editorial-illustrations.md) | Replacing Corporate Memphis & AI plastic blobs with 4 authentic vector art systems (CAD, Swiss Risograph, Isometric, Ink). |
| [references/asset-pipeline-and-svg-optimization.md](references/asset-pipeline-and-svg-optimization.md) | SVGO rules, inline gradient ID collision defense, AVIF/WebP budgets, OpenGraph `1200x630` specs, zero-CLS image sizing. |
| [templates/adaptive-favicon.svg](templates/adaptive-favicon.svg) | Theme-adaptive `<svg>` favicon responding to `prefers-color-scheme: dark`. |
| [templates/og-card-template.svg](templates/og-card-template.svg) | High-contrast Swiss editorial `1200x630` OpenGraph card vector template. |
| [templates/pwa-icons-manifest.json](templates/pwa-icons-manifest.json) | Complete PWA icon & maskable manifest blueprint (`192`, `512`, `maskable`). |
| [scripts/generate_svg_squircle_kit.py](scripts/generate_svg_squircle_kit.py) | Generates Apple squircle master icon, adaptive `favicon.svg`, and Android foreground/background SVGs from one mark. |
| [scripts/verify_brand_assets.py](scripts/verify_brand_assets.py) | Audits SVGs for `<30` logo nodes, `viewBox`, embedded rasters, duplicate IDs, and editor metadata bloat. |

---

## 2. The 4 Mandatory App Logo Stress Tests

Every app mark must pass all four gates before shipping:
1. **Pure Silhouette Test**: Instantly recognizable in 100% solid `#000` on `#fff` and `#fff` on `#000` (zero reliance on gradients or drop shadows).
2. **16px Favicon Test**: Key negative-space cuts remain clear at `16x16px` (`>= 1.5px` stroke equivalent at 16px).
3. **5-Second Memory Sketch Test**: Simple geometric construction (`<= 3–5` primitives) recallable after 5 seconds.
4. **Vector Cleanliness Test**: Primary glyph path uses `< 30` Bezier commands on an integer `viewBox` (`0 0 512 512`), aligned to $0^\circ / 45^\circ / 90^\circ$ angles and optical mass center.

---

## 3. Cross-Platform App Icon Matrix

| Platform Target | Canvas Size | Safe Area | Mandatory Mask / Format |
| :--- | :--- | :--- | :--- |
| **Apple iOS / macOS** | `1024x1024` (`512` SVG master) | `384x384` centered on `512` | Continuous curvature squircle ($\|x/a\|^4 + \|y/b\|^4 = 1$) |
| **Android Adaptive** | `108dp x 108dp` | `66dp` centered circle | Split foreground + opaque background layers |
| **Web / Browser** | `32x32` / `vector` | `10%` padding | Theme-adaptive `favicon.svg` + `apple-touch-icon` (`180x180`) |
| **PWA / Web App** | `192x192` & `512x512` | `80%` maskable safe zone | `purpose: "any"` and `purpose: "maskable"` PNG/SVG |
| **OpenGraph / Social** | `1200x630` | `80px` outer margin | High-contrast Swiss/CAD card, zero noisy gradients |

---

## 4. Generating & Verifying App Asset Kits

```bash
# Generate Apple squircle, adaptive favicon, and Android foreground/background SVGs
python3 skills/brand-assets/scripts/generate_svg_squircle_kit.py --out-dir ./public/icons --title "App"

# Audit all project brand/icon SVGs for AI slop, bloat, or missing viewBox
python3 skills/brand-assets/scripts/verify_brand_assets.py --path . --strict
```
