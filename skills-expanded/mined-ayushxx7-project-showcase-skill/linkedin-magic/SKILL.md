---
name: linkedin-magic
description: "LinkedIn post generation and asset bundling for project launches. Depends on project-showcase."
---

# LinkedIn Magic

Transforms showcased projects into LinkedIn engagement.

## Workflows

### 1. Prep
Run the main `project-showcase` skill first to ensure screenshots, health score, and README are ready.

### 2. Content Generation
4 post variants:
- **🚀 Viral Hype** — Short, punchy, emoji-driven
- **🏗️ Deep Dive** — Technical architecture focus
- **📈 Health Audit** — Trust and quality metrics
- **💡 Story** — Problem/solution narrative

Templates: `references/post_templates.md`

### 3. Asset Bundling
```bash
python3 linkedin-magic/scripts/bundle_assets.py
```
Copies best assets to `linkedin_launch/` with descriptive names.

### 4. Hashtag Strategy
Core: `#BuildingInPublic #AIAgents #OpenSource`
Tech: `#Python #React #AI` (match your stack)

## Checklist
- [ ] Showcase skill run (README updated, health score present)
- [ ] At least 2 high-res screenshots or 1 GIF
- [ ] 3 post variants generated
- [ ] Repo URL + Live App URL verified
- [ ] `linkedin_launch/` folder ready

## Pro Tips
- **First Comment Rule** — Post links in the first comment
- **Lead with visuals** — Images > text on LinkedIn
- **Human-first tone** — Avoid robotic AI language
