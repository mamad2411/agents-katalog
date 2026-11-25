---
name: design-banner-design
description: Design a banner that puts the brand on one side and shows what the product does in four steps beside it, built in SVG or HTML at the exact platform size, exported to PNG and checked with the two-second, crop, contrast and grayscale tests. Use WHENEVER the user wants a banner, cover, header, social preview, README hero, ad or poster ("make a banner for this repo", "GitHub social preview", "X header", "LinkedIn cover", "YouTube channel art", "hero image", "ทำแบนเนอร์", "ปกโซเชียล", "แบนเนอร์โปรโมต"), wants a banner reviewed ("is this banner readable", "does it crop"), or asks which size or style a placement needs. Not for full pages (design-core) or video.
---

# Banner

A banner gets two seconds. In that time it has to say whose it is and what the product does.
This sub-skill always uses one structure: the brand on one side and four steps of what the product
does beside it, read in order and ending on the call to action. Five layouts arrange it.

Rules come from [references/principles.md](references/principles.md); the five layouts and where
each was seen from [references/layouts.md](references/layouts.md); sizes and the 22 art directions
from [references/sizes-and-styles.md](references/sizes-and-styles.md). The product's own
brand (logo, colors, fonts) always wins over both, the same order of authority as
[`../core/SKILL.md`](../core/SKILL.md).

## The layout: brand side, four steps

```
┌──────────────┬───────────┬───────────┬───────────┬───────────┐
│ logo         │ 01        │ 02        │ 03        │ 04        │
│              │ Verb      │ Verb      │ Verb      │ Verb      │
│ NAME         │ one line  │ one line  │ one line  │ one line  │
│ one-line     │           │           │           │           │
│ promise      │ [proof:   │ [proof:   │ [proof:   │ [proof:   │
│              │  icons,   │  names,   │  numbers] │  ...]     │
│              │  names]   │           │           │           │
│              ├───────────┴───────────┴───────────┴───────────┤
│              │                       CTA: verb + command/URL │
└──────────────┴───────────────────────────────────────────────┘
  brand ~30%                 four steps ~70%
```

- **Brand side** (left in LTR, right in RTL): logo, name as the largest type on the canvas, one
  promise line and at most one line of facts. It is the core zone, so it has to survive every crop.
- **Four steps**, numbered 01-04, each a **verb** (Design, Build, Test, Ship) or the product's
  own four names when it has them (a person's four layers: Interface, Services, Data, Platform),
  one line of what it does, and the proof under it (the parts, a number, an icon). Four because a viewer holds about
  four things at once; fewer than three reads as a list, more than five as a menu.
  The steps are a sequence when the product is a pipeline, or four jobs when it is a toolkit:
  say which in the line under the name.
- **CTA** bottom-right, where the eye lands after step 04. One per banner, starts with a verb.
- The diagram above is `columns`. `rail`, `stairs`, `bento` and `stack` arrange the same parts
  differently; [layouts.md](references/layouts.md) says which fits which kind of four steps.
- Other ratios (square, story, leaderboard): [sizes-and-styles.md](references/sizes-and-styles.md#brand-side-layout-per-ratio).

## Workflow

1. **Brief.** Placement (it sets the exact size), audience, goal, the one idea. Gather the brand's logo,
   colors and fonts; if there are none, say so and use the core skill's defaults.
2. **Copy first.** Name, promise line (6-12 words), four verbs with one line each, proof per
   step, CTA. Ground every claim in the product: a step names what it really does.
3. **Art direction.** Keep the brand's look if it has one. Otherwise pick 2-3 styles from the
   table and build each as a variant. With Inspo or Awwwards available, collect 3-5 references
   first (`../core/references/reference-first.md`).
4. **Build** at the exact pixel size as SVG, text as live text, fonts subset and embedded. Write
   the banner as a spec (`<campaign>.banner.json`: size, brand, four steps, CTA, custom styles,
   variants) and render it with `uv run scripts/banner.py <spec>`. The spec is the file to save
   and share: anyone with the repo rebuilds every variant from it. Hand-written SVG works too. Critical content in the placement's safe zone (principles.md: central 80% under
   platform UI, otherwise 50px+ from every edge and outside the crop). Tag it `data-zone="core"`
   and each dark panel `data-bg` so the bench can measure it.
5. **Export** to PNG at 1× and 2×. Under the platform's limit (GitHub: 1 MB).
6. **Bench**: run every test in principles.md (two-second at ~400px, crop to the safe zone,
   contrast ≥ 4.5:1, grayscale, spelling). `uv run scripts/bench.py <banner.svg> [--margin 64]`
   exports the PNGs (1×, 2×, 400px, 1.91:1 crop) and measures safe zone, contrast, type size and
   file size; exit code = failures. It works on any SVG carrying the `data-zone` / `data-bg`
   markers. Grayscale and spelling stay eye checks on the exported PNGs.
7. **Hand over** each variant: style name, preview, the bench results, file path and size.
   Name files `{campaign}/{style}-{w}x{h}.png`.

## The spec

```json
{
  "size": [1920, 1080],
  "brand": {"name": "…", "mark": "logo.svg", "promise": ["line", "line"], "facts": "…"},
  "steps": [{"num": "01", "verb": "…", "line": ["…", "…"], "items": [{"name": "…", "icon": "x.svg"}]}, …],
  "through": "what carries the request (stack only: a label along its line)",
  "cta": {"verb": "Hire", "detail": "url or command"},
  "styles": {"mine": {"bg": "#…", "panel": "#…", "on_panel": "#…", "fg": "#…", "fg2": "#…", "fg3": "#…",
                      "rule": "#…", "cta": "#…", "on_cta": "#…", "edge": null,
                      "pattern": "grid|dots", "pattern_color": "#…", "shadow": "#…", "accent": "#…"}},
  "variants": ["stack-mine", "columns-flat"]
}
```

Where a platform crops the image, `"content_ratio": [4, 3]` keeps all content inside the centred
4:3 area of the canvas (the brand panel colour still reaches the edge), and `bench.py --safe-ratio 4:3`
checks the crop and writes a `-safe.png` preview. A spec can list `"sizes": [[1200, 630], [1920, 1080]]` instead of one `size`; every variant renders at
each. `"fonts"` maps text roles to `family-weight` (`"title": "kanit-700"`); the Thai families are
Kanit, Anuphan and Mali, since Archivo and JetBrains Mono have no Thai. The `cover` layout takes a
`cover` block (kicker, title lines, note, author, motif) instead of `brand`, `steps` and `cta`, and the
`step` layout a `step` block (number, title, caption, a picture). A spec with `pages` renders several
images, each with its own layout and size; the social-media skill's blog-cover sub-skill documents both.
A game thumbnail is a `<game>.keyart.toon` brief rendered by the `keyart` layout (scene full-bleed, block
title, ribbon, callouts); [`../thumbnail-keyart/SKILL.md`](../thumbnail-keyart/SKILL.md) documents it.
`bench.py --bottom N` keeps text out of a band the platform covers, `--max-kb` sets the PNG limit.

Paths are relative to the spec. `mark`, `icon`, `facts`, `through`, `detail` and the last four style tokens are
optional; presets `flat`, `dark`, `minimal` need no `styles` entry. Layouts are drawn on a 1280-wide
grid and scaled, so any size from 2:1 to 16:9 renders. Text marked `data-zone="decor"` (a misregistered
duplicate, a watermark) is skipped by the bench.

## Worked examples

- [examples/th3-skills](examples/th3-skills/README.md): this repo's GitHub social preview, the nine
  skills as four jobs, every layout in flat, dark and minimal (1280 × 640).
- [examples/th3r-fastwork](examples/th3r-fastwork/README.md): a freelancer's first Fastwork post
  (1920 × 1080, measured from Fastwork's 16:9 image boxes), the `stack` layout in two custom styles
  (blueprint, paper) and flat.

## Done when

- Every string is grounded and spelled right; one CTA.
- The bench passes: nothing core outside the safe zone, every text color ≥ 4.5:1 (≥ 3:1 for
  large bold), the PNG under the platform limit, readable at phone width.
- The variant set exists if the placement needs it (primary, tight crop, text-light).
