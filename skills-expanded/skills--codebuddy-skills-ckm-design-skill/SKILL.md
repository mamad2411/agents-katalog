---
name: ckm:design
description: "Design hub: brand, tokens, UI, logo, CIP, slides, banners, social, icons. Actions: logo, CIP, mockups, slides, banner, icons, social photos."
---

# Design

Hub for brand, UI, and marketing assets.

## Routing
| Task | Sub-skill | CMD / Info |
|------|-----------|------------|
| Brand / Voice | `brand` | External |
| Tokens / CSS | `design-system` | External |
| UI styling | `ui-styling` | External (shadcn/Tailwind) |
| Logo | Built-in | `scripts/logo/search.py` |
| CIP Mockups | Built-in | `scripts/cip/search.py` |
| Slides | Built-in | `references/slides.md` |
| Banners | Built-in | `references/banner-sizes-and-styles.md` |
| Social Photos | Built-in | `references/social-photos-design.md` |
| SVG Icons | Built-in | `scripts/icon/generate.py` |

## Built-in Tools
### Logo & CIP
```bash
# Logo: Brief, Search (style/color/industry), Generate
python3 .../logo/search.py "query" --design-brief -p "Name"
python3 .../logo/generate.py --brand "Name" --style minimalist --industry tech
# CIP: Brief, Search (deliverable/mockup), Generate, Render HTML
python3 .../cip/search.py "query" --cip-brief -b "Name"
python3 .../cip/generate.py --brand "Name" --logo /path --set
python3 .../cip/render-html.py --brand "Name" --images /path
```

### Banners & Social
- **Sizes**: FB (820x312), X (1500x500), LI (1584x396), YT (2560x1440), IG Story (1080x1920), IG Post (1080x1080), Ads (300x250), Hero (1920x1080).
- **Styles**: Minimalist, Bold Typo, Gradient, Photo, Geometric, Glass, Neon.
- **Rules**: Safe zones (central 80%); 1 CTA (min 44px); Max 2 fonts; Text < 20% for ads; Print (300 DPI, 3mm bleed).
- **Workflow**: Ask -> Research -> Design (HTML/CSS) -> Export (Screenshot) -> Verify -> Report.

### SVG Icons
```bash
python3 .../icon/generate.py --prompt "gear" --style outlined --color "#hex"
python3 .../icon/generate.py --prompt "icon" --batch 4 --sizes "16,24,32"
# Styles: outlined, filled, duotone, rounded, sharp, flat, gradient.
```

## References
Files: `logo-design.md`, `cip-design.md`, `slides-create.md`, `banner-sizes-and-styles.md`, `social-photos-design.md`, `icon-design.md`.

## Setup
`pip install google-genai pillow`. Requires `GEMINI_API_KEY`.
