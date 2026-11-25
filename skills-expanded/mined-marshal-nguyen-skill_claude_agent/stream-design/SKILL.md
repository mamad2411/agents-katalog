---
name: stream-design
description: Use this skill to generate well-branded interfaces and assets for STREAM (a Verge-inspired editorial dark system), either for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. Always link `colors_and_type.css` for tokens; prefer Lucide via CDN for icons. Never use light backgrounds, gradients, or drop shadows — the system is strictly `#131313` canvas + 1px hazard borders + saturated color-block tiles.

If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

Key files:
- `README.md` — full system overview (content fundamentals, visual foundations, iconography)
- `colors_and_type.css` — CSS variables + semantic element styles
- `colors.json` — machine-readable palette
- `preview/` — minimal live specimens of every token cluster
- `ui_kits/homepage/` — StoryStream homepage recreation with JSX components
- `assets/` — wordmark + logo mark SVGs
