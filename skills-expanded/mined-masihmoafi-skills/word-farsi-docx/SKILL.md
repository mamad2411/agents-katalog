---
name: word-farsi-docx
description: Build a clean, editable Persian (Farsi) Word .docx in B Nazanin from a report, PDF or TeX source with python-docx. Use for Persian Word output, RTL or font problems in .docx, or converting a Persian report to Word.
---

# Persian Word documents

Produce a Word-native, RTL-correct Persian `.docx` in B Nazanin that keeps a clean academic layout.

## Goal

- Real Word objects (paragraphs, tables, images), not PDF pages pasted into Word.
- The template's margins, spacing and headings preserved.
- RTL punctuation and alignment correct.
- B Nazanin everywhere, including English inside Persian text.
- Tables, bullets, headings, page breaks and images supported.

## Tools

- `python-docx` for generation and styling.
- Optionally, PDF text extraction or page images as a reference; rebuild the content as Word objects.
- For validation, render the final document with a Word-compatible renderer and compare its pages with the reference. If no renderer is available, report the visual check as incomplete.

## Steps

1. Start from the bundled template `perfect-farsi-word.docx` in this skill's folder, which already has the right margins, spacing and headings, because styling Word from scratch is fragile.
2. Clear the body but keep `w:sectPr`, which holds page size, margins and layout; deleting it changes the page geometry.
3. Set every paragraph to right alignment and add `w:bidi = 1`, since Persian can look right while punctuation, numbering and Latin tokens behave wrongly without the RTL flag.
4. Set B Nazanin on every run in all four `w:rFonts` channels (`w:ascii`, `w:hAnsi`, `w:cs`, `w:eastAsia`) and in `run.font.name`, because mixed-script runs fall back to other fonts unless all channels are set.
5. Rebuild the content as Word structures: headings, normal paragraphs, bullet and numbered lists, `Table Grid` tables and captioned images, so the document stays editable and its layout consistent.
6. Set `w:spacing` explicitly on key paragraphs and headings (for example `after = 120`), since Word's defaults inflate spacing around Persian text.
7. Build tables with `doc.add_table`, bold the header row and apply RTL and B Nazanin to every cell paragraph and run, because tables show direction and font bugs first.
8. Insert `doc.add_page_break()` after the cover, after the abstract and between major sections so Word does not reflow them unpredictably.
9. After all content is added, walk every paragraph and run and reapply RTL and B Nazanin, keeping centred cover paragraphs centred, because some operations add runs with default fonts or drop the bidi flag.
10. If the client cannot download Persian filenames, also save an ASCII-named copy and optionally a `.zip`.

## Quality checklist

- Persian punctuation (، ؛ ؟) is correct and stays RTL.
- English terms sit in parentheses and do not break the sentence flow.
- No empty placeholder squares.
- Headings are bold and consistently sized.
- Bullets align correctly in RTL.
- Tables are readable, aligned and do not overflow.
- Images are undistorted and captioned.
- Page breaks fall where intended.

## Failures and fixes

| Symptom | Fix |
| :--- | :--- |
| Wrong font | Set `w:rFonts` in all four channels |
| RTL looks right but punctuation is wrong | Add `w:bidi = 1` to the paragraph properties |
| Layout changed after editing | `sectPr` was removed; keep it |
| Download fails | Save an ASCII-named copy or zip it |
