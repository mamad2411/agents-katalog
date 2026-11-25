---
name: build-office-docs
description: Generates and edits Office documents (DOCX/PPTX) programmatically from data or templates, including styled reports, tables, headers/footers, tracked changes, and slide decks.
when_to_use: When the user asks to create or edit a Word document or PowerPoint deck — generate a report, fill a DOCX/PPTX template, mail-merge data into letters/memos, build slides from an outline, or apply tracked-changes edits to an existing .docx.
---

## When to Use

Trigger this skill when the task produces or modifies a `.docx` or `.pptx` file:

- Generate a Word report/letter/memo from data or a written outline.
- Fill a DOCX/PPTX **template** that has `{{placeholder}}` fields or named shapes.
- **Mail-merge** one template over a row set (one output file per row, or one file with repeated sections).
- Build a slide deck from a structured outline (title + bullets + notes per slide).
- Edit an **existing** `.docx`: find-replace, insert/restyle tables, add headers/footers/page numbers, or apply **tracked changes**.

Do NOT use this for: plain `.txt`/`.md`/`.csv` output, PDFs (use a PDF/HTML-to-PDF path), or `.doc`/`.ppt` legacy binary formats (convert to OOXML first via LibreOffice `soffice --headless --convert-to docx`).

## Steps

1. **Classify the job along two axes before writing code:**
   - Format: `docx` (Word) vs `pptx` (PowerPoint). Decide from the request, not the extension alone.
   - Mode: `from-scratch` (build a new file) · `template` (fill placeholders in an existing file) · `edit-existing` (mutate a real document, preserving its styles).
   Print the chosen `{format, mode}` before proceeding — the library and approach differ per cell.

2. **Pick the library by {format, mode}. Do not invent a new dependency if one is already in the repo:**
   - docx, from-scratch / edit-existing → `python-docx`.
   - docx, template with `{{fields}}`/Jinja loops → `docxtpl` (renders Jinja2 inside a real .docx, keeps styles).
   - pptx, any mode → `python-pptx`.
   - Low-level changes these libraries can't express (tracked changes `w:ins`/`w:del`, custom XML, content controls, theme colors) → edit the OOXML directly: a `.docx`/`.pptx` is a **zip** of XML parts (`word/document.xml`, `ppt/slides/slideN.xml`). Unzip, edit XML via `lxml`, re-zip.
   Confirm the package is installed (`pip show python-docx docxtpl python-pptx`); install into the project env, not globally, if missing.

3. **DOCX — from scratch (`python-docx`):**
   - Structure with real styles, not manual formatting: `doc.add_heading(text, level=N)`, `doc.add_paragraph(text, style='List Bullet'|'List Number')`. Reuse `doc.styles` / a base template (`Document('template.docx')`) so output inherits the org's fonts and theme.
   - Tables: `t = doc.add_table(rows, cols)`, set `t.style = 'Light Grid Accent 1'` (must be a style that exists in the doc, else it errors). Cell styling lives on the **run** inside the cell paragraph: `cell.paragraphs[0].add_run(text).bold = True`; widths need `tblLayout` fixed (`t.autofit = False` + set each `cell.width`).
   - Headers/footers/page numbers: `section.header` / `section.footer`; a page-number field requires a `fldSimple`/`w:instrText PAGE` XML run (`python-docx` has no helper — inject the XML via `run._r.append(...)`).
   - Images: `doc.add_picture(path, width=Inches(...))`; missing files raise, so check the path first.

4. **DOCX — template fill & mail-merge (`docxtpl`):**
   - Author the template with Jinja in real Word text: `{{ customer_name }}`, `{% for row in items %}...{% endfor %}` (use `{%tr ... %}` to repeat **table rows**, `{%p ... %}` to repeat paragraphs). Tag names must match the context dict keys exactly.
   - Render: `tpl = DocxTemplate('tpl.docx'); tpl.render(context); tpl.save(out)`.
   - Mail-merge = loop the data rows: render one output per row → `out_{i}.docx` (or `_{key}.docx`), OR pass a list into one template and use a `{%tr%}`/`{%p%}` loop for a single combined file. Decide which the user wants up front.
   - Insert images/rich runs via `tpl.new_subdoc()` / `InlineImage`, not raw strings, so styling survives.

5. **PPTX (`python-pptx`):**
   - Start from `Presentation('template.pptx')` to inherit master/layouts; `Presentation()` alone gives the default theme only.
   - Per slide: pick a layout (`prs.slide_layouts[idx]`), `slide = prs.slides.add_slide(layout)`, then fill **named placeholders** by index/type (`slide.placeholders[0].text = title`) — do not assume placeholder 1 is always the body; inspect `[ph.placeholder_format.idx for ph in slide.placeholders]`.
   - Bullets: write into the body placeholder's `text_frame`, one `paragraph` per bullet, set `paragraph.level` for indent.
   - Speaker notes: `slide.notes_slide.notes_text_frame.text = notes`.
   - Charts/tables: `slide.shapes.add_chart(...)` with a `CategoryChartData`, or `add_table(rows, cols, x, y, w, h)`.

6. **Edit-existing without nuking styles:** open the real file, mutate only target nodes. For find-replace in `python-docx`, replace at the **run** level (text can be split across runs — naive `paragraph.text = ...` drops formatting); join/split runs carefully or use a known replace helper.

7. **Tracked changes** are not in `python-docx`'s API — do it at the XML layer: an insertion is a `<w:ins w:author w:date>` wrapping the new run; a deletion wraps the old run in `<w:del>` with the text in `<w:delText>`. Set author/date attributes. Verify Word shows them under Review → Track Changes after opening.

8. **Render to the requested path, then validate (step into ## Verify) before declaring done.** Report the absolute output path and confirm the file opens.

## Common Errors

- **Corrupt file after manual XML edits** — re-zipping with wrong compression/structure, missing `[Content_Types].xml`, or a stray byte breaks the package and Word says "needs repair". Always round-trip through `zipfile` (preserve all parts), and re-open with the library after writing to catch corruption early.
- **Style does not exist → exception or silent no-op.** `t.style = 'Some Style'` / `add_paragraph(style=...)` only works if that style is defined in the document. Build from a template that contains the style, or add the style definition first. Style names are case- and space-sensitive.
- **Fonts/styles "not embedded" → output looks wrong on another machine.** OOXML references fonts by name; it does not embed them. If a specific font is required, embed it (`<w:embedRegular>` font part) or restrict to fonts the consumer has. Theme colors only resolve if the theme part is present (another reason to start from a real template).
- **Merge-field / placeholder mismatch.** A `{{tag}}` with no matching context key renders empty or raises (`jinja2.UndefinedError`); a key with no tag is silently ignored. Diff the template's tag set against the context dict keys before rendering. Word sometimes splits `{{ tag }}` across runs so `docxtpl` can't see it — keep each tag typed in one run (retype it cleanly in Word).
- **find-replace drops formatting** because Word stores one logical word across multiple `<w:r>` runs. Replacing `paragraph.text` collapses runs and loses bold/italic/links. Operate run-by-run or use a run-aware replacer.
- **PPTX placeholder index assumption** — layouts differ; index 1 is not always the content body. Always enumerate `slide.placeholders` and match by `placeholder_format.type`/`idx`.
- **`add_picture`/template path is relative** and the working dir differs at run time → `FileNotFoundError`. Use absolute paths.
- **Tracked changes invisible** because `w:author`/`w:date` are missing or the run wasn't wrapped in `w:ins`/`w:del` — Word then shows the edit as a normal change. Confirm the wrapping nodes and attributes exist.

## Verify

A generated/edited Office file is done only when ALL hold:

- [ ] The file exists at the reported absolute path and has non-trivial size (> a few KB; a 0-byte or tiny file means the write failed).
- [ ] **It is a valid OOXML package:** `unzip -l <file>` lists parts including `[Content_Types].xml` and `word/document.xml` (docx) or `ppt/presentation.xml` (pptx) — no zip error.
- [ ] **It re-opens with the library** without exception: `Document(out)` (docx) or `Presentation(out)` (pptx) loads, and a spot-check reads back expected content (a heading's text, a known cell value, slide count == expected).
- [ ] For templates/mail-merge: no `{{` / `}}` / `{%` literals remain in the output (`unzip -p <file> word/document.xml | grep -c '{{'` returns 0), and one output file exists per data row when per-row mode was chosen.
- [ ] For tracked changes: `word/document.xml` contains the expected `<w:ins>`/`<w:del>` nodes with author+date; opening in Word shows them under Review.
- [ ] If a specific font/style/theme was requested, it is present (style name resolves; theme/font part exists in the zip).

If validation cannot run (no Word/LibreOffice available and the library re-open is the only check), state that the file passed structural+library validation but was not opened in a real Office client.
