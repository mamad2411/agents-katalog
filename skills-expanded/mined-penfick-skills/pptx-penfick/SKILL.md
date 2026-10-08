---
name: pptx-penfick
description: >
  Generate PowerPoint decks from a structured JSON outline (page-by-page types,
  titles, bullets). Use when the user asks to create, build, or export a PPT/PPTX/
  演示文稿/幻灯片/deck/presentation. CLI: pptx-penfick (alias pptskill). Produces local
  .pptx plus structural QA. Does not invent logos or real product photos.
---

# pptx-penfick

Deterministic PPT renderer: **JSON outline → `.pptx` + QA**. Agent owns research and outline content; CLI owns layout, CJK fonts, and validity.

> CLI command: **`pptx-penfick`** (alias `pptskill` if installed that way). Requires the CLI package installed (see skill README).

## Iron laws (follow every deck job)

1. **Output only under the current project/workspace** (`cwd` or the project the user named). Never `%USERPROFILE%` / Desktop unless the user asks.
2. **User materials first** — if facts/structure/numbers are provided, do **not** web-search; fill gaps by asking one question or marking 示意.
3. **Never copy facts/numbers/segments/people from example outlines** into another topic. **Do not open `examples/` during generation jobs** when you already know the schema.
4. **Before render**: `pptx-penfick validate` then `pptx-penfick content-check` (use `--expect-pages` when the user asked for N pages; `--allow` only if the topic truly includes a deny term).
5. **Deliver the `.pptx`**: say `PPT 已生成` + absolute path + one-line summary; call `present_files` (or attach) with the `.pptx` first if the host has it. Never end on outline/QA only.
6. If you cannot inspect PNGs, still run `qa --visual` and say **「仅结构/几何 QA，未做像素级目检」** in the reply.

## Workflow

1. **Clarify** topic, page count, audience, language, theme (发布会→dark-keynote；汇报→light-corporate；课件→education-blue；路演→pitch-green）.
2. **Output dir** under the project: `<project>/<slug>/` (outline, assets, qa, pptx).
3. **Research policy**: materials first (Iron laws). Unverified numbers → 示意.
4. **Draft outline JSON** — one thesis per slide; prefer `chart`/`image_text`/`compare`/`kpi`; every slide `notes`.
5. **Assets** (if `image_text`): local files → `pptx-penfick assets import …` → `assets check`.
6. **Validate + content-check**:
   ```
   pptx-penfick validate outline.json
   pptx-penfick content-check outline.json --expect-pages 15
   ```
7. **Render**: `pptx-penfick render outline.json -o <path>.pptx` (optional `--ensure-contrast`).
8. **QA**: `pptx-penfick qa out.pptx --visual --json qa-report.json` then `export-png` if needed; `update-slide` to fix.
9. **Deliver** per Iron law 5.

### Slide types (summary)

`cover` · `agenda` · `section` · `title_body` · `two_col` · `timeline` · `data_cards` · `chart` · `image_text` · `compare` · `kpi` · `quote` · `closing`

Themes: `dark-keynote` · `light-corporate` · `education-blue` · `pitch-green` · `minimal-mono` · `finance-navy` · `warm-editorial`

Custom theme JSON / per-slide `theme` / `theme_tokens` / logo extract / `theme fix` — see CLI: `pptx-penfick --help`, `pptx-penfick themes`.

## CLI reference

```
pptx-penfick validate <outline.json>
pptx-penfick content-check <outline.json> [--expect-pages N] [--allow terms]
pptx-penfick render <outline.json> -o out.pptx [--theme …] [--ensure-contrast]
pptx-penfick qa <out.pptx> [--visual] [--json report.json]
pptx-penfick export-png <out.pptx> --out-dir qa/
pptx-penfick update-slide <outline.json> --index N --patch patch.json
pptx-penfick assets check|import …
pptx-penfick theme extract|fix …
pptx-penfick themes
```

Exit codes: `0` ok · `2` schema · `3` render/export · `4` QA / content-check failed.

MCP: `pptskill-mcp` / `python -m pptskill.mcp_server`.

## Out of scope

- CLI image download/generation (agent may fetch then `assets import`)
- Vision auto-fix loop
- In-place edit of existing `.pptx`
