---
name: medical-svg-icons
description: Use when creating or revising SVG icons for medical imaging, DICOM viewers, radiology tools, measurement tools, overlays, or toolbar actions. This skill enforces mainstream viewer benchmarking, a consistent icon system with fixed grid, strong semantic metaphors, larger perceived size, serious workstation styling, and optional two-tone color layers so icon sets stay visually unified and readable.
---

# Medical SVG Icons

Use this skill when icon quality depends on consistency more than novelty. Goal: produce medical-imaging SVG icons that read immediately, feel like one family, and stay credible inside a dense clinical workstation UI.

## Benchmark Order

Do not redesign medical viewer icons from memory alone. Before drawing or revising:

1. Check nearby repo icons so new work matches the existing family when that family is already coherent.
2. Read [references/market-benchmarks.md](references/market-benchmarks.md) and [references/local-asset-library.md](references/local-asset-library.md) for the benchmark workflow and current asset status.
3. If browsing is available and more context is needed, benchmark mainstream viewers from official docs, screenshots, or repositories.

Preferred benchmark set: `OHIF`, `Weasis`, `RadiAnt`, and `3D Slicer` when MPR, crosshair, or pane orchestration is involved.

If browsing is not available, read [references/market-benchmarks.md](references/market-benchmarks.md).

## Bundled Assets

This skill should not assume a local vendor SVG library is present. If benchmark SVGs were removed from `assets/`, treat that as intentional and continue.

- use [assets/icon-template-24.svg](assets/icon-template-24.svg) as the only guaranteed starter asset
- use bundled references only as benchmark notes, not as geometry to paste directly into product icons
- redraw the icon in the target repo's system even when the metaphor comes from OHIF, Weasis, RadiAnt, or 3D Slicer

## Default System

Unless the user explicitly asks otherwise:

- use `viewBox="0 0 24 24"`
- target a rendered size of `18px` to `22px`, but keep source art on the 24 grid
- optimize for a larger perceived size, not maximum empty margin
- default to a serious radiology-workstation style rather than a playful app-icon style
- prefer strong outline-plus-solid-accent icons over ultra-thin pure outline icons
- primary geometry may use `stroke="currentColor"` and a selective secondary fill or accent color
- use `stroke-width="1.9"` to `2.2` when needed for legibility at toolbar sizes
- use `stroke-linecap="round"` and `stroke-linejoin="round"`
- keep all meaningful strokes inside an optical safe area of roughly `1.5..22.5`
- align endpoints and major bends to whole or half-pixels for crisp rendering
- keep visual weight balanced across the set

Default color behavior: mono is allowed, but do not default to mono if two-tone improves meaning. Keep one dominant ink color plus one restrained accent layer; the accent should separate semantic planes, not decorate. Avoid bright consumer-app colors.

If the project already uses a different grid or visual language, match the existing system instead of forcing this one.

## Mini-Viewer Repo Defaults

For `/Users/hucheng/my/github/mini-viewer`, apply these repo-specific defaults unless the user explicitly overrides them:

- keep toolbar and dropdown icons in the same family and at the same rendered size
- use the shared size variable in `app/globals.css` (`--viewer-toolbar-icon-size`) instead of sizing menu and toolbar icons separately
- when drawing new repo-local icons, prefer a `32 x 32` source grid even if intermediate code still reuses legacy `24`-grid geometry
- prefer a lighter stroke band than generic outline systems; this repo currently targets about `2.1` to `2.35` effective stroke width on the `32` grid
- use dark muted accent colors for two-tone layers, such as steel blue or desaturated teal; do not fall back to gray-only accent planes unless mono is specifically requested
- the `pan` tool should default to a four-way cross-arrow metaphor, not a hand icon
- `select` should stay a cursor metaphor
- ROI icons should not include `+` or create badges
- `fit`, `reset`, `rotate`, and `flip` icons are primary toolbar actions, not submenu-only utilities
- if the toolbar gets crowded, let it wrap to multiple rows before shrinking icon size or hiding primary tools in overflow

## Workflow

1. Inspect nearby repo icons and benchmark notes before drawing so the new work fits local chrome.
2. Write the intended meaning in plain language: what should an operator understand in under one second?
3. Reduce the concept to 1 primary metaphor plus at most 1 supporting cue.
4. Draw the strongest recognizable silhouette first, then add only the detail needed to disambiguate it.
5. Redraw the geometry in the repo's icon system instead of pasting vendor SVG paths directly.
6. Normalize proportions, occupied area, and accent usage against peers before delivering.
7. Return the SVG plus a short note covering benchmark influences, metaphor, color logic, and assumptions.

## Style Direction

Bias toward:

- serious
- clinical
- instrument-like
- stable
- deliberate
- professional workstation UI

Avoid:

- cute or playful metaphors
- overly airy line art
- consumer mobile-app icon language
- decorative flourishes that do not strengthen meaning
- over-rounded shapes that make tools feel toy-like
- “designy” originality that weakens industry-recognizable metaphors

## Size And Readability Rules

If an icon feels too small, first:

- enlarge the main silhouette
- reduce unused outer margin
- increase stroke weight slightly
- simplify inner detail
- promote one key shape to a filled or accented plane

Do not fix smallness by making the icon visually noisy.

## Borrowing Policy

Borrowing established medical-viewer icon ideas is preferred over inventing new metaphors.

- Favor benchmarked ideas over novelty, but redraw the geometry yourself.
- Stay close to mainstream viewer metaphors when they are already clear and professional.
- It is acceptable to echo proportions, silhouette strategy, or pane logic from OHIF, Weasis, RadiAnt, or 3D Slicer.
- Do not paste vendor SVGs directly into the product icon set unless the user explicitly asks for that.
- Do not drift toward generic SaaS iconography when the function is radiology-specific.

## Medical Viewer Heuristics

For DICOM and radiology tooling, prefer these metaphors:

- series, stack, study: layered frames, strips, or tiled panels
- measurement: ruler, caliper, segment, angle, ellipse, rectangle, or plotted handles
- MPR or layout: orthogonal panes, slice planes, tri-view grids, or crosshair axes
- window/level: grayscale ramp, contrast window, histogram-like split, or tone bracket
- annotations: mark, text leader, measured callout, or anchored note
- segmentation: contour, filled region edge, mask slab, or highlighted anatomy region
- sync/link: chain, paired panes, mirrored markers, or synchronized slice indicators
- settings: control panel, sliders, or structured parameters rather than a generic playful gear when context allows

Avoid:

- photoreal anatomy details
- too many tiny internal strokes
- ambiguous metaphors that could mean several commands
- icons whose center of mass is too small for the button they sit in
- relying on letters unless the product already does that
- ambiguous crosses that read as “close” instead of “medical”

## Output Contract

For mono icons, prefer:

```svg
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

For two-tone icons, prefer:

```svg
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." fill="var(--icon-accent, #4C6FFF)" opacity="0.18"/>
  <path d="..." stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

Two-tone guidance:

- use the accent plane sparingly
- keep contrast readable in dark clinical UI
- the icon must still work if accent collapses to grayscale
- prefer structural accent areas such as a pane, mask, slice plane, or focus target

If React/TSX is needed, convert the SVG cleanly without changing geometry.

## Consistency Checks

Before finalizing, verify:

- same `viewBox` across the set
- same stroke width band across the set
- same cap and join rules across the set
- no accidental fills unless intentional
- similar visual margin on all sides
- center of mass feels aligned with adjacent icons
- icon still reads at `18px`
- the metaphor is recognizable without reading the tooltip
- if two-tone is used, the accent improves meaning rather than merely styling
- dropdown menu icons and toolbar icons feel like the same set, not two different scales

## References

- For current bundled asset status and benchmark workflow, read [references/local-asset-library.md](references/local-asset-library.md).
- For the concrete icon spec and dos/don'ts, read [references/system-spec.md](references/system-spec.md).
- For benchmark synthesis without browsing, read [references/market-benchmarks.md](references/market-benchmarks.md).
- For reusable prompting language, read [references/prompt-template.md](references/prompt-template.md).
- For a starter SVG shell, reuse [assets/icon-template-24.svg](assets/icon-template-24.svg).
