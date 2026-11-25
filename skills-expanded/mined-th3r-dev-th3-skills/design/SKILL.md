---
name: design
description: >-
  Design toolkit, one skill with sub-skills. (1) core: shared design principles (composition, interface
  writing, quality baseline, taste pass, reference-first cook loop scored by a fresh critic, picture-to-3D
  cutaway); (2) flow: real screens captured into Figma with their flowchart beside them, bound to the file's
  variables and styles; (3) banner-design: a banner with the brand on one side and four steps of what the product
  does, built at the exact platform size, exported to PNG and benched for crop, contrast and phone width; (4)
  thumbnail-keyart: a game thumbnail or key art that shows what the game is, what you do and the goal, from a
  TOON brief, benched and read back by a fresh vision critic.
  Use WHENEVER the user designs or reviews a screen, page, component, flow or UI copy ("review this design",
  "looks generic", "looks AI-made", "หลักการออกแบบ", "ตรวจงานดีไซน์"), designs from references or Inspo /
  Awwwards, wants a cook loop or three variants, a cutaway / exploded view of a picture, shares a
  figma.com/design URL to add or check flows ("flowchart next to the screen", "ออกแบบหน้าพร้อม flow"), or
  wants a banner, cover, header, social preview, README hero or ad ("ทำแบนเนอร์", "GitHub social preview",
  "X header"), or a game thumbnail, Roblox thumbnail, key art or update thumbnail ("ทำ thumbnail เกม", "ทำปกเกม
  Roblox"). Read the sub-skill's SKILL.md before acting.
---

# design: sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| "review this design", "looks generic", design principles, UI copy, reference-first variants, a cook loop, a cutaway | [`core/SKILL.md`](core/SKILL.md) | `core/cutaway/check_page.mjs`, `core/assets/hero.py` |
| a figma.com/design URL, "flow beside the screen", capture a page into Figma, screens lacking a flow | [`flow/SKILL.md`](flow/SKILL.md) + [`flow/README.md`](flow/README.md) Part 3 | `flow/scripts/*.py` (bridge, capture, flow_review) |
| a banner, cover, header, social preview, hero image, ad, "which size for X" | [`banner-design/SKILL.md`](banner-design/SKILL.md) | `banner-design/scripts/banner.py` (spec → SVG), `banner-design/scripts/bench.py` (export + checks) |
| a game thumbnail, Roblox thumbnail, key art, update thumbnail, thumbnail variants, "match this app's look" | [`thumbnail-keyart/SKILL.md`](thumbnail-keyart/SKILL.md) | `banner.py` (`.keyart.toon` → SVG), `bench.py --bottom --max-kb`, `thumbnail-keyart/scripts/critic.py` (vision critic) |

They chain: `core` sets the rules and the review table; `flow`, `banner-design` and `thumbnail-keyart` apply
them, and their checks feed the same score. A Roblox game's interface applies them through game-dev's
`design-ui` (when that skill is installed).

## Rules every sub-skill keeps

- **The product's own system first.** Its components, tokens, fonts, brand and terms win over any
  default here. Report gaps instead of restyling over them.
- **Copy before layout.** Every string is written and grounded before anything is placed.
- **A check the author didn't run decides when it's done:** core's fresh-context score, flow's
  `flow_review.py`, banner-design's `bench.py`, thumbnail-keyart's `critic.py`.
- **No real client data** in any example, commit or public artifact; mock labels only.
