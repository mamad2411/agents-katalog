---
name: product-mock
description: Add, change or re-export an HTML-rendered product mock for a project with tools/product-mocks and pnpm mocks:build. Use for a new product screen, changes to an existing one, or fresh PNGs for Sanity.
---

# Product mock

The generator lives in `tools/product-mocks/` and the root script `pnpm mocks:build`
runs it. If that directory is missing, this skill does not apply; product images
are ordinary Sanity image assets.

```bash
test -d tools/product-mocks && echo "product mocks: yes" || echo "product mocks: no"
```

The product images on the site are HTML mocks in `tools/product-mocks/`, rendered on
the **product** tokens (the dashboard, `product.py`) and placed on the tinted dune
panel (`mocks.py`). `pnpm mocks:build` writes the gallery
`tools/product-mocks/out/index.html`; each panel has a **Save PNG** button that
renders it at the Sanity asset size. The full guide, with the rules, is
`docs/guides/product-mocks.md`. Read it first.

## Input

What the user wants: a new screen (which capability, which numbers), a change to an
existing one, or just a re-export. Which split-section row it is for decides the
alignment (`right` when the image sits on the right of the row, `left` otherwise)
and the tint (peach, sage, rose, cycling with the row index).

## Steps

1. **Read** `tools/product-mocks/mocks.py` and, for dashboard changes,
   `tools/product-mocks/dashboard.py`. Find the closest existing screen; `winloss()`
   is the simplest template.
2. **Write the screen** as `name(pins=True, align="right")` from the existing atoms
   (`frame`, `metric`, `hbar`, `area`, `tag`, the `.app` utility classes). Product
   tokens only (`--p-*`); never a marketing token, never a new colour. Real copy, no
   lorem ipsum, and only names from the invented Meridian world in `BRAND.md` (no
   real companies or people). Two pins naming the capabilities the site's bullet
   list mentions, right-side pins kept inside the panel (`right:.75rem`).
3. **Register** it in `DIVES` and `GALLERY`. New lucide icon? Run
   `node tools/product-mocks/extract-icons.mjs <name>` (needs `web/node_modules`).
4. **Build and check**: `pnpm mocks:build`, open the gallery in a browser, look at
   both variants at a normal window width. Content must fit the 4:3 panel at the
   export width (680px); if the gallery says the panel is taller, cut a row.
5. **Export**: click Save PNG for each variant. Files are named
   `meridian-<slug>-<right|left>-1360x1020.png` (hero/dashboard: `…-2880x1605.png`).
   The export drops the outer hairline and corners on purpose: the site draws them
   in code (`HeroSection`, `SplitSections`). Never add a border to the PNG.
6. **Hand over**: tell the user which Sanity field each file goes to (row `image`,
   hero `productImage`, CTA `image`) and the alt text to use. In local dev, deleting
   `web/.next/dev/cache/fetch-cache` and restarting shows the new asset.

## Don't

- Don't restyle a screen with the marketing palette, Mona Sans or the card-frame
  double border. Screens look like the product, the panel looks like the site.
- Don't bake the panel's outer border or rounded corners into the PNG.
- Don't export at the window's size; the button already renders at a fixed design
  width so the file is exactly 1360×1020 or 2880×1605.
- Don't use real brand logos in a screen. `tools/product-mocks/assets/` holds
  fictional integration marks; add new ones the same way.
- Don't commit `tools/product-mocks/out/` (git-ignored).
