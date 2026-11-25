---
name: kdp-audit
description: >-
  Audit a book manuscript against Amazon KDP requirements: interior
  formatting, cover specs, metadata, and genre-specific checks. Handles
  technical books (LaTeX, math), fiction, and nonfiction. Produces a
  structured gap report with Critical and Warnings sections plus
  automation suggestions.
argument-hint: "[manuscript path]"
---

# KDP Manuscript Audit

Audit a book manuscript against Amazon KDP (Kindle Direct Publishing) requirements and produce a structured gap report. This skill evaluates interior formatting, cover specs, metadata completeness, and genre-specific requirements (technical vs. fiction).

## Workflow

### 1. Detect Manuscript Type

Identify manuscript files and format. Look for these file types in the current directory or specified path:

**Primary manuscript formats** (Glob tool):
- `.tex` files (LaTeX manuscripts, common for technical books)
- `.docx` files (Microsoft Word, common for fiction/nonfiction)
- `.epub` files (eBook source)
- `.md` files (Markdown manuscripts)
- `.pdf` files (final output)
- `.kpf` files (Kindle Create project)

**Manuscript type classification**:
- **Technical**: LaTeX source, math equations, code listings, index/bibliography
- **Fiction**: Structured chapters, scene breaks, dialog formatting
- **General nonfiction**: Standard chapters, images, minimal equations

If `$ARGUMENTS` names a file or directory, audit that. If no manuscript is found, ask the user which file to audit.

### 1b. Load User Config

Read `.claude/kdp.local.md` if it exists (Read tool). Its YAML frontmatter follows the schema in `${CLAUDE_PLUGIN_ROOT}/docs/user-config-template.md`, which is the only definition of the fields. This skill uses `kdp.trim_size`, `kdp.paper_type`, `kdp.target`, `kdp.genre`, `kdp.page_count`, and `author`.

If the file is missing, inform the user and offer to create one from that template. If `kdp.page_count` is empty and a compiled PDF exists, count its pages (Bash tool: `pdfinfo file.pdf | grep Pages`) and offer to save the count.

### 2. Check Interior Formatting

Verify the manuscript meets KDP interior requirements. Full specs are in `${CLAUDE_PLUGIN_ROOT}/docs/kdp-reference.md` (Interior Formatting section); read it and check the manuscript against:

- **Trim size**: look for margin or geometry declarations (Grep tool); verify it is one of KDP's paperback trims (the `trim_size` enum of `kdp_cover_specs`, or the reference doc) and that the page count is inside the range `kdp_cover_specs` reports as `page_range`
- **Margins**: inside (gutter) margin steps up with page count; check against the margin table in the reference doc
- **Fonts**: must be embedded; standard fonts preferred (Times New Roman, Garamond, Arial, Courier); minimum 7pt
- **Page numbers**: start after front matter, consistent placement
- **Table of Contents**: present and functional, hyperlinked in eBook, typically 2 to 3 levels deep

### 3. Check Cover Specifications

Verify covers meet KDP requirements. Full specs are in `${CLAUDE_PLUGIN_ROOT}/docs/kdp-reference.md` (Cover Requirements section).

**Find cover files** (Glob tool): `cover*.jpg`, `cover*.jpeg`, `cover*.tiff`, `ebook-cover.*` for eBook; `paperback-cover.pdf`, `full-cover.pdf`, `cover-print.*` for paperback.

**Verify dimensions** (kdp_validate_cover MCP tool, preferred): call `kdp_validate_cover` with the cover image path and `kind` (`ebook`, `paperback_front`, or `full_wrap`; print kinds also need `page_count`, `trim_size`, `paper_type` from the config). It returns a per-check pass/warn/fail table (dimensions, ratio, format, channels, file size, print resolution) computed from the image metadata; copy fails into Critical and warns into Warnings. It reads images, not PDFs: for a paperback cover PDF, validate the PNG it was made from (`kdp_generate_full_wrap` returns it as `wrap_png_path`) or rasterize the PDF first (`pdftoppm -r 300 -png cover.pdf cover`).

**Fallback when the MCP server is unavailable** (Bash tool): measure with `identify -format "%wx%h" cover.jpg` (ImageMagick) or `file cover.jpg`, and compare against the Cover Requirements section of the reference doc. KDP's Cover Calculator gives exact paperback wrap dimensions.

**Cover content requirements**: title readable at thumbnail size, author name present, high contrast, no prohibited content. Report actual vs. required dimensions. If cover files are absent, flag as a critical gap.

### 4. Check Metadata Readiness

Verify all required listing metadata exists in the manuscript or in `.claude/kdp.local.md`. Full field specs and constraints are in `${CLAUDE_PLUGIN_ROOT}/docs/kdp-reference.md` (Metadata section).

Grep manuscript front matter and the user config for:

- Title, subtitle (each up to 200 chars), series info
- Description or blurb (up to 4000 chars, HTML allowed)
- 3 Amazon categories per format
- Up to 7 keywords
- Author bio (100 to 200 words recommended)
- Language, pricing, territories, DRM setting, ISBN decision

Flag missing fields so the user can provide them via the KDP dashboard.

### 5. Technical Books Only

If manuscript is technical (LaTeX, math-heavy, code listings):

**LaTeX compilation** (Bash tool):
```bash
cd /path/to/manuscript && pdflatex -interaction=nonstopmode manuscript.tex
```
Verify compilation succeeds with no critical errors.

**Math rendering**:
- Check for `\usepackage{amsmath}` or equivalent
- Verify math symbols render correctly (sample PDF pages)
- Print PDF: math typeset as text is fine as long as every font, math fonts included, is embedded (`pdffonts manuscript.pdf`)
- Kindle eBook: reflowable formats do not render LaTeX math, so equations need images (with alt text) or MathML via EPUB; complex math usually argues for a print-replica or print-only edition

**Code listings**:
- Check for `listings` or `minted` package usage
- Verify syntax highlighting, line numbers, proper formatting
- Ensure code fits within margins (line wrapping or font scaling)

**Index and bibliography**:
- Verify `\printindex` and `\bibliography{}` commands present
- Check that index entries are defined (`\index{}`)
- Verify `.bib` file exists and is referenced
- Run `makeindex` and `bibtex` successfully

### 5b. eBook Validation

Check for eBook-specific issues that affect Kindle rendering and KDP acceptance.

**EPUB validation** (Glob tool, Bash tool):
- Check if `.epub` files exist in the project
- If `epubcheck` is available (`which epubcheck`), run it on the EPUB file and report results
- If `epubcheck` is not installed, note it as a recommendation and list common EPUB issues to manually check:
  - Broken NCX/nav table of contents
  - Missing cover image reference in OPF manifest
  - Invalid HTML entities in content
  - CSS that won't render on Kindle (floats, absolute positioning, complex grid/flexbox)
- If no EPUB exists but `.md` or `.docx` source files do, recommend conversion via Pandoc before audit:
  ```bash
  pandoc manuscript.md -o manuscript.epub --toc --metadata title="Book Title"
  ```
- Note: KDP recommends DOCX, KPF, or EPUB for eBooks (see the reference doc for the full list). EPUB gives the most control over eBook formatting.

### 5c. Kindle Format Checks

Check for issues that specifically break on Kindle devices:

**Footnotes** (Grep tool):
- Search for `\footnote` in LaTeX source, or footnote markers in DOCX/HTML
- Kindle handles footnotes poorly; recommend converting to endnotes for eBooks

**Wide tables** (Grep tool):
- Flag tables with more than 3 columns: Kindle screens are narrow and tables don't reflow well
- Recommend converting wide tables to lists or simplifying

**Complex CSS** (Grep tool):
- If CSS files exist, flag advanced layout rules: absolute positioning, floats, flexbox, grid, fixed widths in pixels
- Kindle's CSS support is limited, so flag any rules that won't render correctly

**Large images** (Bash tool):
- Flag individual images over 5MB, since they slow loading on Kindle
- Check with `ls -la` on image files or `identify` if ImageMagick is available

### 6. Fiction Only

If manuscript is fiction or narrative nonfiction:

**Chapter structure** (Grep tool):
- Body: Chapters with consistent heading styles
- Verify chapter numbering is sequential with no gaps
- Check for consistent chapter title formatting (all caps, title case, etc.)

**Front matter order validation** (Grep/Read tools):
- Expected order for fiction: title page -> copyright page -> dedication (optional) -> epigraph (optional) -> table of contents
- Flag if critical elements are missing (title page, copyright page)
- Flag if elements are out of standard order

**Back matter order validation** (Grep/Read tools):
- Expected order: acknowledgments (optional) -> about the author -> also by this author (optional) -> preview of next book (optional)
- Flag if "About the Author" section is missing entirely; readers expect it (KDP does not require it)

**Scene breaks and formatting**:
- Scene breaks marked with `* * *` or similar (not just blank lines)
- Dialog formatting: Consistent use of em-dashes vs. quotation marks
- Paragraph indentation: First line indent (0.25-0.5") except after scene breaks
- No widows/orphans (single lines at top/bottom of page)

**Scene break consistency** (Grep tool):
- Check that scene breaks use a consistent marker throughout (all `* * *`, all `---`, all `###`, etc.)
- Flag if multiple different scene break styles are used in the same manuscript
- Flag if bare blank lines (no marker) are used as scene breaks, since these can be lost in eBook conversion

**Special elements**:
- Epigraphs formatted consistently
- Letters, emails, or other narrative devices clearly distinguished
- No footnotes (not well-supported in eBooks; use endnotes or inline)

### 7. Produce Gap Report

Use the template at `${CLAUDE_PLUGIN_ROOT}/docs/audit-report-template.md` as the skeleton. Populate findings from the preceding steps. Omit sections that do not apply (for example, the Fiction checklist for a technical book).

### 8. Offer to Fix

After presenting the report, offer to fix issues that can be automated:
- Add missing front matter sections (copyright page, title page templates)
- Fix LaTeX margin settings via `geometry` package
- Generate Amazon category suggestions based on content
- Create author bio template
- Add missing TOC entries
- Fix scene break markers
- Compute paperback cover dimensions with `kdp_cover_specs`

## Reference Files

For complete KDP requirements and the audit output structure:
- `${CLAUDE_PLUGIN_ROOT}/docs/kdp-reference.md` for KDP formatting, cover, metadata, and submission specifications
- `${CLAUDE_PLUGIN_ROOT}/docs/audit-report-template.md` for the gap report skeleton

## Important Notes

- **KDP review time**: 24-72 hours for eBooks, up to 5 business days for paperbacks
- **Content guidelines**: No prohibited content (explicit sexual content requires erotica category, hate speech prohibited, public domain verification required)
- **ISBN**: Optional for eBooks (Amazon provides ASIN). Free ISBN available for paperbacks, or a custom ISBN can be provided.
- **Royalty options**: 35% (no delivery cost) or 70% (delivery cost deducted, price restrictions apply)
- **KDP Print vs. IngramSpark**: KDP is Amazon-exclusive; consider IngramSpark for wider distribution
- **Preview before publishing**: Always download and review the digital previewer or order a proof copy
- **Updates**: Manuscripts can be updated post-publication, but updates take 24-72 hours to propagate
