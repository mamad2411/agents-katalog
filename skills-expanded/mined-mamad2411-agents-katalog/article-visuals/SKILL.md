---
name: article-visuals
description: 'Use to make an article 图文并茂 — generate publish-ready figures (data charts, flow/structure diagrams) and a cover, SEO/GEO-friendly. 配图/图表/插图/封面/流程图/数据图/visuals/figures/diagrams/charts'
version: "1.0.0"
license: Apache-2.0
homepage: "https://github.com/weitzu-com/ai-article-factory"
when_to_use: "Use at the figures stage (P6) of article production, or whenever a draft needs charts/diagrams/a cover. Renders Mermaid + matplotlib to PNG and prepares an AI-cover prompt; enforces image SEO/GEO rules."
argument-hint: "<article-dir>"
metadata:
  author: weitzu-com
  tags: [visuals, figures, charts, diagrams, mermaid, matplotlib, image-seo, cover]
---

# article-visuals (P6 — 图文并茂)

Make figures that serve three readers at once: humans (understanding), search engines (image SEO / rich results), and AI engines (multimodal citation). **≥3 figures per article: 1 cover + ≥2 content figures.** This skill is self-contained — it uses the bundled scripts, no external pack needed.

## Type decision tree (pick type → tool)
| To express | Type | Tool | Source file |
|---|---|---|---|
| flow / structure / relationship | diagram | **Mermaid** | `assets/src/*.mmd` |
| data / comparison / trend | chart | **matplotlib** (`import figlib`) | `assets/src/*.py` |
| concept / cover | illustration | **AI image** (prompt → human fills) | `assets/src/cover-prompt.md` → `assets/img/cover.png` |
| real UI / object | screenshot/photo | manual | — |
| tabular comparison | **Markdown table** (preferred — AI-extractable) | in prose | — |

**Rule:** if data fits a Markdown table, use a table; only draw when relationships/trends need it.

## Workflow
1. From the outline's figure intent, write figure sources into `assets/src/` and log `assets/图清单.md` (caption + alt + placement).
2. Render:
   ```bash
   bash <repo>/scripts/render-figures.sh <article-dir>      # mermaid + matplotlib → assets/img/
   ```
   `figlib.py` provides the brand palette (`scripts/palette.json`) + registered CJK fonts (Chinese won't box) + `save()` / `bar_compare()` helpers. If `mmdc` is missing, `.mmd` is skipped gracefully.
3. Embed with `![keyworded-alt](assets/img/x.png)` + a caption carrying the source `[C#]`.
4. Cover: a placeholder is used so it never blocks; generate the real one from `cover-prompt.md` and drop it at `assets/img/cover.png`.

## Image SEO + GEO checklist (each figure must pass)
- Descriptive English kebab-case filename with keywords (not `image1.png`).
- Alt text describing the figure + naturally containing the keyword.
- Caption is a complete sentence with the data source.
- Compressed (<200KB chart / <400KB cover).
- **Every data figure has an equivalent sentence/table nearby** (AI reads text; the figure corroborates).
- Don't rely on color alone (color-blind safe); in-figure font ≥ body.

Full detail: `../../references/visuals-spec.md` (the repo-root `references/` folder).
