---
name: ky-markdown-rebuilder
description: Rebuild visual documents into reliable Markdown by combining text extraction with page or screenshot alignment. Use when converting or cleaning up PDFs, slide decks, PPT/PPTX files, HTML pages, long screenshots, Word-like reports, whitepapers, course materials, business decks, scanned documents, or visually dense documents where plain text extraction may jumble layout, charts, timelines, diagrams, tables, screenshots, or logos.
metadata:
  short-description: Rebuild visual documents into page-aligned Markdown
---

# KY Markdown Rebuilder

Use this skill when a document should become Markdown but the visual layout matters. The goal is not just conversion; it is content reconstruction with a reliable visual source of truth.

Core principle:

> Extract text first, render visual pages second, then rebuild Markdown from a page-aligned source of truth.

Default deliverable principle:

> Use intermediate files as working evidence, but deliver only the final calibrated Markdown and, when requested, an outline Markdown.

## Host Compatibility

This package is portable across Codex, Claude Code, and Antigravity:

- Codex install path: `~/.codex/skills/ky-markdown-rebuilder/`
- Claude Code install path: `~/.claude/skills/ky-markdown-rebuilder/`
- Antigravity: copy the package into the workspace (e.g. `<workspace>/ky-markdown-rebuilder/`) and follow SKILL.md manually
- Shared assets: `scripts/` and `references/`
- Codex-only UI metadata: `agents/openai.yaml`

Both hosts should use the same workflow below. If a host cannot access one helper script or renderer, use its native browser/document tools for that step and keep the output contract unchanged.

## When To Use

Use for:

- PDF reports, PPT-style PDFs, whitepapers, course packs, proposal decks.
- PPT/PPTX decks, slide exports, Keynote-like slide files.
- Scanned documents and photographed books (Scanned-Document route, `transcribe` mode).
- HTML pages or local web pages that need Markdown reconstruction.
- Long screenshots or image-heavy documents.
- Word/document files that contain diagrams, tables, screenshots, or complex layout.

Do not use for simple text-only files where normal conversion is enough.

## Output Contract (LOCKED)

This is a hard contract, not a suggestion. `check_output.py` enforces the exact strings below. Do not invent alternative labels, languages, heading levels, or punctuation — every past "format drift" incident came from improvising here.

Language rules:

1. Structural labels are ALWAYS the exact Chinese strings defined below, regardless of the document language.
2. Body content and page titles follow the source document language (Chinese, English, Thai, or anything else). Never translate content inside the calibrated file; translation is a separate deliverable (see Filenames).
3. `## Page NN: Title` uses a half-width colon and zero-padded page numbers (minimum 2 digits). Never use a full-width colon in the heading.

Document header — the first lines of every calibrated file:

```markdown
# <文档标题>

> 重建说明：模式 <fast|page-aligned|deep-visual|transcribe>；来源 `<源文件名>`；共 <M> 页；原图逐页查看 <N>/<M> 页。
```

The `原图逐页查看 N/M` count must be TRUE: only pages opened at original resolution count. Contact-sheet thumbnails do NOT count as inspection. Never claim more inspection than actually happened; if only 10 of 50 pages were opened, write `10/50`.

Page section template — identical for `## Page NN:` / `## Region NN:` / `## Screen NN:` routes; `## Sheet: 名称` uses the same four labels:

```markdown
## Page 01: <页标题，跟随原文语言>

源图：[page-01.png](pages/page-01.png)

### 页面目的

- ...

### 布局地图

- ...

### 按区域确认内容

#### 区域 1：<位置与形态，如 左侧 2x2 卡片区>

...

### 视觉备注

- ...
```

Transcribe-mode page template (`transcribe` mode only — 1:1 content reproduction, no visual commentary):

```markdown
## Page 01: <页标题；无标题页用 第 01 页>

源图：[page-01.png](pages/page-01.png)

<该页全部内容 1:1 转写：正文按原文语言，表格转 Markdown 表，保留空单元格与 "-" 占位>
```

Contract details:

- The only accepted section labels are `### 页面目的`, `### 布局地图`, `### 按区域确认内容`, `### 视觉备注` — exact spelling, H3 level, no colon suffix. English labels (`Page purpose` etc.) and bare-text labels (`页面目的:`) are contract violations. (`transcribe` mode omits the four sections entirely — never mix the two shapes in one file.)
- Region subsections under 按区域确认内容 use `#### 区域 N：<位置>` (full-width colon inside this label is correct).
- Source line: during validation use `源图：[page-NN.png](pages/page-NN.png)`. In the final deliverable (screenshots removed) replace with `源页：第 N 页` (PDF/scan), `源页：Slide NN` (PPT), or `源图：<原始输入文件名>` (single-image input). Every section has exactly one 源图/源页 line, directly under the `##` heading.
- Screenshot links are always RELATIVE paths (`pages/page-01.png`). Absolute paths become dead links the moment the work folder moves or is cleaned; if the pages directory will not survive delivery, use 源页 notes instead of links.
- Title/transition pages may keep each section to a single bullet, but all four sections stay present in page-aligned/deep-visual outputs.
- 视觉备注 must be page-specific. The checker fails when the identical note line appears on 3+ pages. Do not rotate canned sentences.
- Never wrap page body in a full-page code fence. Code fences are only for actual code or verbatim ASCII art. Tables become Markdown tables; the checker fails oversized fences.
- Every table needs a blank line before it. A table glued to the preceding text line (`หน่วย : ล้านบาท` directly above `| ... |`) renders as plain text, not a table. `scripts/fix_tables.py` inserts the missing blank lines; the checker fails glued tables.
- Chemistry/math notation uses `<sub>`/`<sup>` (e.g. H<sub>2</sub>O, Zn + H<sub>2</sub>SO<sub>4</sub>), never code fences, never bare-text approximations.
- Never use HTML whitespace entities (`&nbsp;`, `&emsp;`, `&ensp;`, `&thinsp;`) to imitate the source's indentation or alignment — they render as garbage in plain-Markdown viewers. Visual indentation is layout, not content: drop it, or express structure with lists/blockquotes/tables. The checker fails any occurrence.
- If the source page has no readable title, use `## Page NN: 第 NN 页` — never paste raw OCR garbage as the title.
- Do not invent an H1 title. If the document has no visible title, derive one and mark it: `# <自拟标题>（自拟）`.

Filenames:

- Calibrated: `<source name>.calibrated.md`
- Outline (only when requested): `<source name>.outline.md`
- Translated deliverable (only when requested): `<source name>.calibrated.<lang>.md` (e.g. `.zh.md`). Structural labels stay Chinese, `## Page NN:` keeps the English word "Page" and the half-width colon; only body content and page titles are translated. A translated deliverable is generated from the calibrated file AND spot-checked against original page images — never from the calibrated file alone.

## Output Modes

Choose the smallest mode that satisfies the user, and state it verbatim in the reconstruction note. The only legal mode names are `fast`, `page-aligned`, `deep-visual`, `transcribe`, `reading` — never invent hybrid names.

| Mode | Use when | Output |
| --- | --- | --- |
| `fast` | The document is mostly linear text | raw conversion plus light cleanup |
| `page-aligned` | Default for decks, PDFs, reports, or mixed text/visual pages | one Markdown section per page/slide/screen |
| `deep-visual` | High-stakes, visually dense, or sales/solution deck material | page-aligned Markdown with per-page original-resolution inspection |
| `transcribe` | Scanned books, forms, budget/reference documents where the user wants the CONTENT 1:1, not layout commentary | per-page 1:1 transcription (text + tables), no four-section template |
| `reading` | User wants a readable article/report | generate only after a page-aligned source exists |

For scanned documents choose between `transcribe` and `deep-visual` by asking what the user will do with the file: reading/searching/quoting the content → `transcribe` (the common case for 100+ page scans); analyzing the page design itself → `deep-visual`. Do not apply the four-section template to hundreds of pages of tables — that is bloat, not rigor.

Important: never generate a `reading` version directly from raw extraction when the source is visually complex. First create or verify the page-aligned source.

## Document Routing

Route by observed structure, not only by file extension. A file extension is a hint; the screenshot/rendered view and extracted structure are the source of truth.

| Kind | Typical inputs | Default calibrated structure |
| --- | --- | --- |
| `deck` | PPT/PPTX, proposal PDFs, slide-style PDFs | `## Page NN:` with the locked four-section template |
| `report` | Word/PDF reports, whitepapers, manuals | document headings plus page anchors where visual layout matters |
| `scanned` | CamScanner PDFs, photographed books, image-only PDFs | Scanned-Document route (below), `transcribe` template |
| `spreadsheet` | XLS/XLSX/CSV, finance models, dashboards | `## Sheet: Name`, then tables, formulas, charts, dashboard regions |
| `image` | single images, long screenshots, scanned pages | `## Region NN:` with the locked four-section template |
| `html` | web pages, local HTML exports | `## Screen NN:` or `## Section: Name` with DOM/visual region structure |
| `mixed` | files with multiple strong forms | combine the relevant structures; do not force one template |

Flexible routing rules:

- Upgrade a spreadsheet to visual/dashboard treatment when it contains charts, KPI cards, slicers, pivot tables, dashboards, screenshots, or complex merged-cell layouts.
- Upgrade a Word/PDF report to page-aligned treatment when it contains diagrams, tables, sidebars, screenshots, forms, or page-specific visual meaning.
- Treat PPT/solution decks as `deep-visual` by default when they include product imagery, callouts, case studies, comparison matrices, or contact pages.
- If one document contains multiple forms, use section-level routing. Example: a workbook may have a dashboard sheet, raw data sheets, and formula/model sheets.
- Never let routing block output. If classification is uncertain, choose `mixed` and state the chosen structure in the reconstruction note.

## Scanned-Document Route (no text layer)

Trigger: `pdfinfo`/pypdf shows no text layer, or extraction yields ~0 characters for a visibly full page. Default mode: `transcribe`.

Engine priority — vision model first, tesseract second:

1. **Vision-model direct reading (preferred).** If the host model or its subagents can read images (Claude, Gemini/Antigravity, GPT-vision), render pages at high DPI and transcribe directly from the original-resolution page images. This beats tesseract decisively on Thai, handwriting, small fonts, and complex tables. Proven pattern for 100+ page documents: split into batches of ~10 pages, one parallel subagent per batch, each instructed to transcribe 1:1 — preserve Thai/original text exactly; convert every table to a Markdown table keeping empty cells and dash-only (`-`) placeholders; handle merged cells by the LOCKED rules (跨列=每列重复内容, 跨行=只写首行其余留空, 多行表头=第一行做表头其余行做正文首行 — see `references/visual-transcription-rules.md`) — then concatenate batches in page order and run `scripts/fix_tables.py` to normalize ragged table rows. Give every subagent an ABSOLUTE output path under `.ky-md-work/<source-name>/` (e.g. `/full/path/.ky-md-work/doc/batch_01_10.md`); relative or improvised batch paths scatter fragments that the parent must hunt down and reassemble.
2. **Tesseract fallback.** Only when no vision-capable model is available: check `tesseract --list-langs` first; if the document language pack is missing, tell the user and ASK before installing anything (e.g. `brew install tesseract-lang`) — never silently install software. OCR output must still be reconciled against original-resolution images for every page with tables, forms, or money amounts.
3. **Neither available: STOP and report.** Do not deliver a thumbnail-based "reconstruction" and do not transcribe from low-resolution contact sheets.

Rules for both engines:

- Tables become Markdown tables — never dump a page into a code fence. Unreliable readings (amounts, units, small labels) are marked `[?]` inline rather than silently guessed.
- Degraded pages must be declared: if quota exhaustion, a crashed batch, or any fallback means some pages were NOT transcribed from original-resolution images (e.g. rebuilt from a reference file or a text dump), list those page numbers in the reconstruction note (`> 补充：第 91-99 页因配额耗尽由脚本兜底，未经视觉核对。`) and reduce the `原图逐页查看 N/M` count accordingly. Silent fallback is the single biggest trust-killer in past runs.
- If a reference/companion document is provided by the user, transcribing it is NOT reconstruction: every page taken from the reference instead of the image must be flagged as `内容来自参考文件，未逐页核图`.

## Workflow

1. Preflight once per session: `python3 scripts/preflight.py`. It reports which tools exist (markitdown, pdftoppm, pdfinfo, soffice, tesseract + language packs, PIL/pypdf) so the pipeline never discovers missing tools mid-run. Plan around what is actually available; use `python3`, never `python`.
2. Establish deliverables and output path before conversion:
   - default: create `source.calibrated.md`;
   - if the user mentions `outline`, `大纲`, `大纲版`, `two files`, `两个文件`, or asks to generate a version based on the calibrated Markdown, create both `source.calibrated.md` and `source.outline.md`;
   - do not finish the task until every requested deliverable exists.
3. Extract a raw text Markdown draft using MarkItDown or the best local extractor. If the text layer is empty, switch to the Scanned-Document route above.
4. Render visual references into `.ky-md-work/<source-name>/pages/`:
   - PDF: render pages to images.
   - PPT/PPTX: convert to PDF, then render pages.
   - HTML: capture screenshots of the relevant page or viewport.
   - Images/long screenshots: use the source image directly or split if needed.
5. Create a manifest with page number, screenshot path, extracted title, text length, and visual-check priority (`make_manifest.py` understands both form-feed and `<!-- Slide number: N -->` page breaks).
6. Visual inspection — real rules, not theater:
   - contact sheets / thumbnail grids are for TRIAGE ONLY (deciding what to look at); transcribing content from a thumbnail is a contract violation;
   - every page ranked high or medium priority in the manifest must be opened at ORIGINAL resolution before its section is written;
   - in `deep-visual` and `transcribe` modes, every page with tables, diagrams, KPI numbers, or dense text must be opened at original resolution (in `transcribe` the transcription itself must come from the original-resolution image);
   - keep a running count of pages actually opened — it goes into the reconstruction note as `原图逐页查看 N/M 页`, truthfully.
7. Rebuild Markdown using the locked Output Contract templates. Write pages in batches after inspecting them; do not write the whole document in one pass before inspection is complete. Convert visual structures using `references/visual-transcription-rules.md`.
8. Validate with `scripts/check_output.py`:
   - always pass `--expected-pages N` when the page count is known and `--pages-dir` while screenshots exist;
   - for `page-aligned` and `deep-visual` outputs also pass `--require-visual-sections` (`transcribe` outputs must NOT pass it — they have no four-section template);
   - paste the checker output into your reply; a failing check blocks delivery.
9. If an outline was requested in step 2, generate `source.outline.md` from the calibrated version and re-check that both final files exist.
10. Finalize the deliverable: if the user wants no screenshot links, replace every `源图：[...](...)` line with the matching `源页：` note, then rerun `check_output.py` on the final file.
11. Cleanup — timing matters:
    - NEVER delete rendered pages before the deliverable message is sent; premature cleanup has forced full re-renders when the user pushed back;
    - after delivering, keep `.ky-md-work/<source-name>/` in place and tell the user: 中间截图与工作文件保留在 `.ky-md-work/<name>/`，确认内容无误后可以删除（或让我删除）;
    - delete only after the user confirms or explicitly asks.

## Page Manifest

Prefer creating a manifest before spending tokens on visual inspection. Use:

```bash
python3 scripts/make_manifest.py --raw raw.md --pages-dir pages --out manifest.md
```

The manifest should help decide which pages need visual checks. Typical fields: page number, screenshot path, extracted title, extracted text length, visual-check priority, reason.

When rendering into an existing directory, prefer:

```bash
python3 scripts/render_pages.py deck.pdf --out-dir deck.pages --clean
```

## Artifact Policy

By default, the user should see only final deliverables next to the source file:

```text
source.calibrated.md
source.outline.md   # only when requested
```

Deliverable location is a hard rule: calibrated/outline files go NEXT TO THE SOURCE DOCUMENT, never inside the skill package folder (the directory containing SKILL.md/scripts/references). The skill folder gets overwritten wholesale on updates — any deliverable stored inside it will be destroyed. If the host copied the skill into the workspace (e.g. Antigravity), treat that folder as read-only tooling and write all outputs elsewhere.

Treat the outline as a first-class requested deliverable, not as an optional summary. If requested, it must be generated in the same run as the calibrated Markdown unless the user explicitly asks to postpone it.

Intermediate evidence (raw extraction, rendered pages, manifest, split pages, draft calibration files) lives in the hidden work folder:

```text
.ky-md-work/<source-name>/
```

Cleanup follows the timing rules in Workflow step 11: keep the work folder through delivery, announce it, delete only on user confirmation. If the final calibrated Markdown keeps local screenshot links, the pages directory must stay as long as the file references it.

When the user asks for "only the final file", "only two files", or similar, do not leave raw, manifest, split, or rendered-page artifacts beside the final Markdown files — but the hidden `.ky-md-work/` folder still stays until confirmation.

## Outline Output

When requested, create an outline file from the calibrated Markdown, not from raw extraction. This is mandatory when the prompt asks for an outline, a second Markdown, or two final files.

Locked outline skeleton (headers always these Chinese strings; body language follows the source):

```markdown
# <文档标题> - 大纲

> 来源：`source.calibrated.md`（校准版）；原始文档 `source.ext`。

## 1. 核心主线

- ...

## 2. 结构地图

| 章节 | 来源页/表 | 作用 |
| --- | --- | --- |

## 3. 详细大纲

### 3.1 ...

## 4. 关键证据

| 证据 | 来源 | 为什么重要 |
| --- | --- | --- |
```

The outline preserves the document's logic without duplicating all details: top-level sections/pages/sheets, key claims or findings, important tables/charts/diagrams and their role, open uncertainties only if the calibrated source marked them. For decks and proposals, group pages by narrative function, not merely page titles. For spreadsheets, group sheets by purpose: dashboard, raw data, assumptions, calculations, outputs, charts.

## Helper Scripts

Use scripts as mechanical helpers; do not load their source unless you need to edit or troubleshoot them. Always invoke with `python3`.

- `scripts/preflight.py`: report which pipeline tools exist and which are missing, with install hints. Run once per session before planning.
- `scripts/render_pages.py`: render PDF/PPT/PPTX inputs into page screenshots (`--clean` removes stale images first). Handles LibreOffice headless-profile crashes internally and normalizes zero-padding to at least 2 digits.
- `scripts/split_markdown_pages.py`: split raw Markdown on page breaks.
- `scripts/make_manifest.py`: build a page/slide manifest from raw Markdown and screenshots. Understands form-feed and `<!-- Slide number: N -->` breaks.
- `scripts/check_output.py`: enforce the Output Contract. Key flags: `--expected-pages N`, `--pages-dir DIR`, `--require-visual-sections` (page-aligned/deep-visual only).
- `scripts/fix_tables.py`: pad ragged Markdown table rows to the table's max column count. Run on `transcribe` outputs after concatenating batches.

## Quality Gate

A page-aligned output is not acceptable if it only summarizes each page. For visual decks and solution proposals, each page section must include enough visual guidance that a reader can reconstruct the slide's information architecture.

Minimum contract per page: the locked four sections, one 源图/源页 line, region-grouped confirmed text, visual relationships (highlighted columns, center nodes, arrows, callouts, before/after areas, image roles), and an uncertainty note only when text or logos are not reliably legible.

Before final delivery, verify:

- Does every page section follow the locked template exactly (labels, levels, source line)?
- Is the `原图逐页查看 N/M` claim in the header truthful?
- Could a reader tell where the text appeared on the slide?
- Are product images, diagrams, callouts, and highlighted areas described?
- Are dense pages structured as tables, region groups, or ordered steps instead of loose bullets?
- Did the output avoid merging adjacent slide content?
- Did it avoid generic filler ("主体区域承载段落、卡片或图示信息") when the actual regions are visible?
- Did it avoid rotating canned 视觉备注 sentences across pages?

For `page-aligned` and `deep-visual` outputs, run:

```bash
python3 scripts/check_output.py --md deck.calibrated.md --pages-dir deck.pages --expected-pages N --require-visual-sections
```

## References

Load references only when needed:

- `references/visual-transcription-rules.md`: how to convert diagrams, timelines, tables, screenshots, and logos to Markdown.
- `references/output-formats.md`: locked templates for all routes and deliverables.
- `references/token-control.md`: strategies for minimizing context use on large documents.

## Reliability Rules

- Treat page-aligned Markdown as the source of truth.
- Do not merge adjacent pages unless the output mode is explicitly `reading`.
- Do not invent unreadable small text, logos, chart labels, or screenshot details.
- Mark uncertain visual details as `无法可靠辨认` or omit them.
- Never claim inspection that did not happen: reconstruction notes report the true original-resolution page count, and reference-file transcription is flagged per page.
- Keep screenshot links for visual verification while intermediate evidence is retained; in deliverable-only mode, use the locked 源页 notes instead.
- Prefer tables for timelines, matrices, repeated item grids, and comparison layouts.
- Prefer module + relationship lists for architecture diagrams.
- If you correct an OCR/reference error (e.g. a garbled patent number), list every correction in 视觉备注 so the user can audit it.
