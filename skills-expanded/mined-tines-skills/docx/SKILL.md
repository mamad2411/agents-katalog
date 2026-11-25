---
name: docx
description: Create, edit, and read Word documents (.docx) with python-docx. Use whenever the user wants a Word file as output — a report, memo, letter, contract, proposal, or template fill — or uploads a .docx to summarize, review, comment on, redline, or rewrite, even if they only say “document” or “Word”.
license: Apache-2.0
compatibility: Tines 3B
---

# Word documents

Work with `.docx` files in Python through `execute`, adding `python-docx==1.2.0` to a `requirements.txt` in `files`. In a workflow step, add it to the step’s `requirements.txt` instead.

User uploads arrive under `/3b/uploads/<id>/<file>`, which every execution can read. Write output to a persistent volume, such as `volumes: ["documents"]` and `/storage/documents/report.docx`, then call `showStorageFile` so the user can preview and download it. Never overwrite the user’s upload: save edits as a new file, and call `showStorageFile` again after each change.

## Reading

Walk the body in order so paragraphs and tables stay interleaved as the author wrote them:

```python
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

doc = Document("/3b/uploads/abc/contract.docx")
for block in doc.iter_inner_content():
    if isinstance(block, Paragraph) and block.text.strip():
        print(f"[{block.style.name}] {block.text}")
    elif isinstance(block, Table):
        for row in block.rows:
            print(" | ".join(cell.text for cell in row.cells))
```

python-docx skips text inside tracked insertions (`w:ins`), text boxes, and footnotes. If the document has redlines or the output looks incomplete, read `word/document.xml` from the zip as well.

## Creating

Structure first, styling second. Use the built-in styles rather than hand-formatting each paragraph: Word builds its navigation pane and table of contents from real headings, and a restyle then changes the whole document at once.

```python
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(section, side, Inches(1))

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)

doc.add_heading("Quarterly access review", level=0)
doc.add_paragraph("Summary of findings for Q3.")
doc.add_heading("Findings", level=1)
doc.add_paragraph("Three dormant admin accounts", style="List Bullet")
doc.add_paragraph("Disable dormant accounts", style="List Number")

table = doc.add_table(rows=1, cols=3, style="Light Grid Accent 1")
for cell, label in zip(table.rows[0].cells, ("System", "Owner", "Status")):
    cell.text = label
for values in (("Okta", "IT", "Done"), ("AWS", "Platform", "Open")):
    for cell, value in zip(table.add_row().cells, values):
        cell.text = value

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
    run = footer.add_run()
    if kind:
        field = OxmlElement("w:fldChar")
        field.set(qn("w:fldCharType"), kind)
    else:
        field = OxmlElement("w:instrText")
        field.text = text
    run._r.append(field)

doc.save("/storage/documents/access-review.docx")
```

- `Document()` defaults to US Letter. Use A4 (`Mm(210)` × `Mm(297)`) when the user or their organization is outside North America.
- Add images with `doc.add_picture(path, width=Inches(6))`. Render charts to PNG with matplotlib first, at 200 DPI or more.
- Start a new page with `doc.add_page_break()`, not a run of empty paragraphs.
- Python-docx has no table-of-contents builder. Insert a `TOC \o "1-3" \h` field the same way as the page number above, and tell the user to update fields in Word to fill it.
- Keep tables to five or six columns in portrait. Switch the section to landscape (`section.orientation`, then swap width and height) for wider tables.

## Editing an existing document

Load the user’s file and change it in place, so their styles, numbering, headers, and section settings survive. Rebuilding a similar document from scratch loses formatting the user cares about.

Word splits text into runs wherever formatting, spell-check, or revision history changes, so one sentence can span several runs. To replace text, edit only the runs the match overlaps: the replacement takes the formatting of the run where the match starts, and every other run keeps its own. Setting `paragraph.text` collapses every run into one and drops bold, italics, and links.

```python
def replace_in_runs(runs, old, new):
    """Replace the first match of `old` across `runs`, touching only the runs it overlaps."""
    start = "".join(run.text for run in runs).find(old)
    if start == -1:
        return False
    end = start + len(old)
    position = 0
    for run in runs:
        run_start, text = position, run.text
        position += len(text)
        if position <= start or run_start >= end:
            continue
        after = text[end - run_start:] if position > end else ""
        run.text = text[:start - run_start] + new + after if run_start <= start else after
    return True

replace_in_runs(paragraph.runs, "Acme Ltd", "Globex Corp")
for link in paragraph.hyperlinks:
    replace_in_runs(link.runs, "Acme Ltd", "Globex Corp")
```

`paragraph.runs` excludes text inside hyperlinks, which `paragraph.text` includes, so handle each hyperlink’s runs separately as above. The helper replaces one match per call, so call it again until it returns `False`, unless the replacement contains the search text. Search table cells, headers, and footers as well as `doc.paragraphs`. For a template with placeholders like `{{client_name}}`, check that no placeholder remains after filling it.

## Comments and redlines

To review a document, attach comments rather than rewriting text:

```python
paragraph = doc.paragraphs[4]
doc.add_comment(paragraph.runs, text="Should this be 30 days?", author="3B", initials="3B")
```

When the user asks for tracked changes, read [references/tracked-changes.md](references/tracked-changes.md): python-docx can’t write them, so they need direct XML edits.

## Check the result

Reopen the saved file and print its headings, table count, and the first lines of each section to confirm it says what you intended. Then call `showStorageFile` so the user can see the rendered layout. Tell them what you produced and anything the preview can’t show, such as fields that update only when the file opens in Word.
