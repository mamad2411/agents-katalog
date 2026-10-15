---
name: redbook-render-skills
description: Redbook (Xiaohongshu) material rendering and publishing skill. Used to convert markdown text into stunning, natively formatted image cards (cover + content pages) and optionally publish them automatically to the platform. Supports 8 gorgeous CSS themes and 4 smart pagination modes.
---
# 🌟 Redbook Render Engine & Publisher
## Overview
This skill takes processed copy and transforms it into highly aesthetic visual cards ready for Redbook. It functions as the "printer" and "delivery boy" of the automation pipeline.
> *See `references/params.md` (if available) for detailed parameter configurations.*
---
## Workflow
### Step 1: Generate the Markdown Render Source
**Note: This Markdown format is strictly designed for image rendering. It is NOT the raw copy.**
Save the content to be visualized into a local `.md` file structured with YAML frontmatter:
```markdown
---
emoji: "🚀"
title: "Cover Main Title (≤15 chars)"
subtitle: "Cover Subtitle (≤15 chars)"
---
Body content for the first card...
---
Second card content... (When using --- for manual separation)
```
**Pagination Strategies:**
- For precise cutting → Manually separate with `---` and use `-m separator`.
- For unpredictable length → Do not use `---`, let the system auto-split using `-m auto-split`.
---
### Step 2: Render Image Cards
Execute the underlying Python rendering script via CLI.
```bash
python scripts/render_xhs.py <markdown_file> [options]
```
**Defaults:**
- Theme: `sketch` (Hand-drawn sketch style)
- Pagination: `separator` (Splits strictly by `---`)
**Common Execution Examples:**
```bash
# Default (sketch theme + manual pagination)
python scripts/render_xhs.py content.md
# Auto-split (Recommended when text length varies)
python scripts/render_xhs.py content.md -m auto-split
# Change theme to playful geometric
python scripts/render_xhs.py content.md -t playful-geometric -m auto-split
# Auto-fit text into a fixed single card dimension
python scripts/render_xhs.py content.md -m auto-fit
```
**Generation Artifacts:** 
Produces `cover.png` (The Cover) + `card_1.png`, `card_2.png`... (The Body sequence).
**Available Themes (`-t`):** 
`sketch`, `default`, `playful-geometric`, `neo-brutalism`, `botanical`, `professional`, `retro`, `terminal`.
---
### Step 3: Publish to Redbook (Optional Action)
**Prerequisite:** Requires a valid `XHS_COOKIE` configured in the `.env` file.
```bash
# Default behavior: Published as 'Private/Only me' (highly recommended for previewing)
python scripts/publish_xhs.py --title "Your Note Title" --desc "Your Note Body..." \
  --images cover.png card_1.png card_2.png
# Publish Publicly (Once reviewed and verified)
python scripts/publish_xhs.py --title "Your Note Title" --desc "Your Note Body..." \
  --images cover.png card_1.png card_2.png --public
```
---
## Skill Architecture
### Core Scripts
- `scripts/render_xhs.py`: The Main Rendering Engine (Browser automation backed).
- `scripts/render_xhs_v2.py`: The Backup Rendering Engine.
- `scripts/publish_xhs.py`: The API Publishing script.
### Assets & Templates
- `assets/cover.html` & `assets/card.html`: Base DOM structures.
- `assets/themes/`: CSS injecting engines defining the visual aesthetics.
