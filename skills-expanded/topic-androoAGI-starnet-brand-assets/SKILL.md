---
name: brand-assets
description: "Make images, covers and transparent cutouts that look like one family: a pinned style sheet, fixed formats, every file checked against it, and cutouts confirmed truly transparent."
license: MIT
metadata:
  title: "Brand Assets"
  category: "Creative"
  author: "StarNet"
---

A set looks like a brand when every piece follows the same written rules. image_generate takes no reference image, so consistency lives in the words: one style sheet, repeated exactly, and every result checked against it.

## Method
1. **Read what is already approved (notebook.read).** Search for the brand or project name. If a style sheet exists, use it as written; a new set that ignores the old one is a second brand.
2. **Write the style sheet.** Five to eight concrete lines: palette (named colors or hex values), rendering style (flat vector, clay 3D, film photo), lighting, line weight, composition (subject centered, wide margin), and what never appears. Concrete beats adjectives — "two colors plus white, thick rounded outlines" survives a hundred prompts; "clean and modern" does not survive one.
3. **Get it approved on one piece.** Generate a single hero image, show it, and revise until the Commander says yes.
4. **Pin the approved rules (notebook.write with `pinned: true`).** Save the style sheet and the approved file's path as a declarative fact, with `scope: stream` for this project. Pinned requirements stay in context on later runs. Read that approved file again before every new variant.
5. **Fix the formats per asset type.** Decide once and reuse: `"16:9"` for banners, `"9:16"` for stories, `"1:1"` for avatars and icons — or exact `width` + `height` when the Commander names pixels. Name files by set and role with `path`: `brand/cover-launch.png`, `brand/icon-app.png`.
6. **Generate with the sheet pasted verbatim.** Every prompt is the style sheet word for word, then one subject line. Only the subject changes. Keep one model per kind of asset: the default model for the set; the premium model the tool description names only for pieces that must carry readable text (and for all of those); and cutouts as their own sub-set, because `transparent: true` generates on its own model.
7. **Cutouts: ask for real transparency.** Set `transparent: true` for logos, stickers and icons. The tool checks the saved file and says plainly when it came back opaque. An opaque result is a failure — regenerate; never deliver a painted checkerboard as a cutout.
8. **Check every file against the sheet (image_analyze).** Ask a pointed question: "Does this use only these colors, this outline weight, this composition? List every deviation." Regenerate deviations and keep a short note of what failed and why.
9. **Review the set side by side.** Name the odd one out, if any, and redo it. Consistency is judged across the set, not file by file.

## Rules
- **Never deliver an unchecked image.** Every file has had an image_analyze pass or the Commander's own look.
- **Never call a file transparent** unless the tool's check said so.
- **Never overwrite an approved asset.** New variants get new names.
- No real company's logo or trademark and no real person's likeness unless the Commander owns or supplied it.

## Done means
Every requested asset exists at its fixed format and path, each passed the style check, every cutout is verified transparent, and the style sheet is pinned in the notebook with the approved reference path.

## Output
The style sheet, the asset list (path · format · transparent yes/no), what was regenerated and why, and the title of the pinned note.

*Needs the STUDIO object (image_generate, image_analyze) and the NOTEBOOK (the pinned style sheet).*
