---
name: article-export
description: 'Use to export a finished article to Word (.docx) with images embedded, plus clean Markdown — brand-templated. 导出/Word/docx/转Word/MD转Word/export/word-export/双格式'
version: "1.0.0"
license: Apache-2.0
homepage: "https://github.com/weitzu-com/ai-article-factory"
when_to_use: "Use at the export stage (P9), or whenever the user wants a Markdown article as a Word .docx (for review, clients, or offline). Embeds figures and applies the brand reference template."
argument-hint: "<article-dir> [slug]"
metadata:
  author: weitzu-com
  tags: [export, word, docx, pandoc, markdown, deliverable]
---

# article-export (P9 — MD + Word)

Produce two deliverables from one master draft: **Markdown** (for the website) and **Word .docx** (for review/clients/offline), with figures embedded. Self-contained — uses the bundled script + pandoc; no external pack needed.

## Workflow
1. The final draft is `<article-dir>/<slug>-final.md`, with figures referenced as `![](assets/img/...)`.
2. Export to Word:
   ```bash
   bash <repo>/scripts/export.sh <article-dir> <slug>      # → <slug>-final.docx
   ```
   - Applies the brand template `templates/reference.docx` (swap it for your own corporate VI; or edit and save back).
   - `--resource-path` points at `assets/img/` so every `![](...)` is **embedded into the .docx**.
   - Adds a table of contents and a `zh-CN` lang tag; macOS bash-3.2 safe.
   - If the brand template is absent, falls back to pandoc defaults (warns, doesn't crash).
3. Website version: also keep `<slug>-wp.md` (the Markdown the site/CMS ingests).

## Requirements & graceful degradation
- Needs `pandoc` (`brew install pandoc`). If absent, you still have the Markdown; install pandoc to get .docx.
- A Markdown article needs **zero** dependencies — Word is the optional extra.

## Verify
After export, confirm the `.docx` opens, the cover + content figures are embedded, the TOC is correct, and Chinese renders (not boxes).
