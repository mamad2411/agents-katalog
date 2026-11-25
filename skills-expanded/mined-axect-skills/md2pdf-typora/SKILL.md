---
name: md2pdf-typora
description: >
  Convert a Markdown file to PDF that closely matches Typora's PDF export with
  the Whitey theme using pandoc and headless Chrome. Preserves MathJax math,
  code styling, and typography. Use when the user asks to convert Markdown to
  PDF, generate a PDF report from a .md file, export markdown in Typora style,
  or render styled documents to PDF.
---

# Markdown to PDF (Typora-style)

Convert a Markdown file to PDF that closely matches Typora's PDF export with the **Whitey** theme. pandoc handles MD to HTML, Chrome headless handles HTML to PDF.

**Run the bundled script. Do not reconstruct the pipeline inline.** The pipeline used to live in this file as a bash-plus-python template that the caller retyped every run, and the retyping was the instability. See "History" at the bottom for what that cost.

## Usage

```bash
bash <skill-dir>/scripts/md2pdf.sh <input.md> [options]
# e.g., bash ~/Documents/Project/AI_Project/skills/md2pdf-typora/scripts/md2pdf.sh <input.md> [options]
```

| Option | Effect |
|---|---|
| `--output <path>` | Output PDF path. Default: same directory as the input, `.pdf` extension |
| `--dropbox [subfolder]` | Also copy the PDF into `~/Dropbox/Magi/<subfolder>/` |
| `--no-toc` | Omit the table of contents. It is included by default |
| `--toc` | Accepted for compatibility; the TOC is already on by default |
| `--break-on-hr` | Force a page break at every `---`. Default is a thin rule, which is what Typora does |
| `--paper <A4\|Letter>` | Page size. Default `A4` |
| `--font <px>` | Root font size. Default `14` |
| `--keep-html` | Keep the intermediate HTML for debugging |

The script exits non-zero with a specific message on any failure, so a broken run is never mistaken for a good one.

`--send-telegram` is not a script option, because bash cannot reach the Telegram MCP tool. Run the script, then pass the printed PDF path to the `reply` tool yourself.

## What the script does

1. **Preprocess** (`scripts/preprocess_md.py`): strips Typora's `[TOC]` marker, and inserts a blank line between a `---` rule and an immediately following heading.
2. **pandoc**: standalone HTML with `--mathjax`, `--highlight-style=pygments`, `--toc --toc-depth=2`, run from the input's directory so relative image paths resolve. Reader is `markdown-yaml_metadata_block+tex_math_dollars`.
3. **Patch HTML** (`scripts/patch_html.py`): inlines the theme plus print CSS as one `<style>` block in the `<link>`'s position, rewrites MathJax to SVG, removes pandoc's duplicate title, moves the TOC below the document's H1, then asserts each of those actually happened.
4. **Chrome headless**: `--headless=new --no-pdf-header-footer --virtual-time-budget=30000 --print-to-pdf`. The browser is resolved from `google-chrome-stable`, `google-chrome`, `chromium`, `chromium-browser` in that order, matching what the repository README promises.
5. **Verify**: PDF exists, is non-empty, has at least one page. Reports size and page count.

Temp files are removed by an `EXIT` trap even when a stage fails.

## Design notes

**Why the theme CSS is inlined rather than linked.** pandoc's `--css` emits `<link rel="stylesheet" href="...">`. Chrome sometimes resolves an absolute path under `file://` and sometimes does not, and a link gives no control over cascade order. pandoc also emits its own `<style>` block *before* the link, so overrides appended to the first `</style>` land ahead of the theme and lose to it. The patcher therefore builds one block, theme first then print overrides, and puts it exactly where the link was.

**Why print overrides are needed at all.** The Whitey theme is tuned for screens: `body { max-width: 960px }` and `html { font-size: 19px }`. A4's printable width is 794px. Without overrides the body overflows the page, tables clip, and equations run past the right margin. The print CSS pins `@page { size: A4 }`, sets `body { max-width: none }`, drops the root font to 14px, and switches body text from justified to left (justified Korean in Chrome's print engine produces wide rivers).

**Why table column widths are scoped by column count.** Under `table-layout: fixed`, assigning 22%/22%/56% to the first three columns of *every* table gives those three the entire width and collapses columns 4 and beyond to nothing: a 7-column table renders as three wide columns plus a few pixels of vertically stacked single characters spilling off the page. The width hints are now scoped with `:has()` to tables that have exactly two or exactly three columns. Wider tables get `table-layout: fixed` with no hints, which distributes evenly and never overflows.

**Why MathJax SVG, not CHTML.** CHTML needs STIX-Web webfonts loaded from a CDN before printing. Under Chrome headless this fails quietly: Greek letters render as empty boxes and inline math like `$\theta_{\mathrm{UV}}$` wraps with the base on one line and the subscript on the next. SVG renders every glyph as path data with no font dependency. The patcher rewrites any `tex-*.js` reference, from either pandoc's older `mathjax@3/es5/` URL or the newer `mathjax@4/` one, to the v3 `tex-svg-full.js`, and fails if a MathJax script survives unrewritten. SVG output is 10 to 30 percent larger and immune to font-cache state.

**Why `code` no longer uses `word-break: break-all` in body text.** `break-all` breaks even when the token would have fitted, so `` `morton` `` came out as `mort` / `on` mid-sentence. Body code now uses `overflow-wrap: break-word` (break only when necessary); table and pre code keep the aggressive rule, where narrow cells need it.

**Why `---` no longer forces a page break.** Typora renders `---` as a thin rule and does not break the page. Documents that use `---` as a section separator every few paragraphs turned into bloated PDFs with many half-empty pages. Use `--break-on-hr` for the old behaviour.

## Fonts

**IBM Plex Serif** (Latin) plus **MaruBuri** (Korean) for body, **Roboto Slab** for headings, **JetBrains Mono** for code, all pulled from CDNs by four `@import` rules at the top of `typora-whitey.css`. Chrome needs network access while rendering. The body stack falls back to Palatino, Times and generic serif when offline, so text still renders, just not in the intended faces. For fully offline use, download the font CSS and MathJax `tex-svg-full.js` locally and point the `@import` rules and `MATHJAX_RE` replacement at the local copies.

## Failure modes the pipeline defends against

Each of these was observed in production and is handled by default now.

1. **Quoted heredoc swallowed the paths.** The python stage was pasted under `<< 'PYEOF'`, so `css_path = "$CSS_PATH"` reached python as literal text and the stage died on `FileNotFoundError`. Under `set -e` the run aborted; without it, the HTML kept pandoc's `<link>` and *none* of the print CSS applied, so PDFs came out Letter-sized with a 19px body and 960px max-width crushed onto the page. Fixed structurally: paths now arrive as `argv` in real script files, and step 3 asserts the CSS was inlined.
2. **`---` followed immediately by a heading, no blank line.** pandoc parses `---\n## X` as a setext-style table fragment and swallows the heading plus following paragraphs into one `<table><td>` cell. Symptom: the TOC entry disappears and the section body renders as a run-on paragraph. Common when chunked translations are `cat`-merged. Fixed by the preprocessor.
3. **`YAML parse exception at line N, column M`.** pandoc's default markdown reader reads an early-line `:` as a YAML key, so Korean documents opening with `> **도메인**: 물리학` abort before producing HTML. Fixed by `-f markdown-yaml_metadata_block+tex_math_dollars`.
4. **Wide tables destroyed by the column-width hints.** See "Design notes". Fixed by `:has()` scoping.
5. **TOC silently deleted.** The old code cut the TOC out and reinserted it after the first `</h1>`; a document with no `# heading` has no `</h1>`, so the reinsertion no-oped and the TOC vanished. Now it falls back to just after `<body>`, and an assertion fires if it went missing.
6. **Duplicate title.** pandoc emits `<h1 class="title">` from `--metadata title` inside a `<header id="title-block-header">` wrapper, on top of the body `<h1>`. Both the h1 and the wrapper are removed; leaving the wrapper kept its margins as stray whitespace.
7. **Equations, blockquotes, code blocks split across page breaks**, and **headings stranded at the bottom of a page**. Handled by `page-break-inside: avoid` and `page-break-after: avoid`.

## Files

- `scripts/md2pdf.sh`: the pipeline. Run this.
- `scripts/preprocess_md.py`: `[TOC]` stripping, `---`-then-heading separation.
- `scripts/patch_html.py`: CSS inlining, print layout, TOC placement, MathJax SVG, plus the assertions.
- `typora-whitey.css`: the theme, unmodified screen CSS. Print concerns live in `patch_html.py`, not here.

## History

Before 2026-07-28 this file carried the whole pipeline as a "Complete Script Template" to copy. Three latent bugs (1, 4 and 5 above) shipped inside that template, and bug 1 meant the print CSS never applied at all. Keeping the pipeline in executable files removes the transcription variance that made the skill unreliable.
