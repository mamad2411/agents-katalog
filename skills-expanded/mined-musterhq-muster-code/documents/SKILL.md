---
name: documents
description: Create, edit and review Word documents (.docx) with Muster. Use whenever the person asks for a report, letter, memo, proposal, contract or any .docx, or to change an existing one. Writes the file with the docx library, renders it to page images with office_render and fixes the layout until every page looks right.
metadata:
  short-description: Word documents (.docx) with a render and fix loop
---

# Documents (.docx)

Use this skill for any Word document: new ones, edits to an existing .docx, and reviews of how one looks. For a
plain-text answer or a Markdown file, do not make a .docx unless the person asked for one.

## Tools

- `muster_office` `office_setup`: call it once per chat before the first script. It installs the libraries the first
  time and answers with the command that runs a script (`<node> script.mjs`). With that command,
  `import { Document } from 'docx'` works from any folder. Do not `npm install` anything into the person's project.
- `muster_office` `office_render`: renders a file to one PNG per page and shows you the first pages. The first render
  may download LibreOffice; that is expected, so wait for it.
- Libraries: `docx` to write new documents (and `patchDocument` to fill placeholders), `jszip` to edit an existing
  document's XML in place.

`example.mjs` next to this file is a tested starting point (headings, runs, bullet and numbered lists, a table, an
image, header, page numbers). Copy it into the working folder and change it rather than starting from nothing.

## The loop

1. Plan the document: sections, what goes in tables, page size (US Letter unless the person or locale says A4).
2. Write a script in the working folder (for example `make-report.mjs`) that writes the .docx. Keep content in data
   at the top of the script, so fixes are small edits.
3. Run it with the command from `office_setup`.
4. Call `office_render` on the .docx. Look at every page image, not only the first.
5. Fix what you see in the script, run it again and render again. Repeat until the checks below pass.
6. Reply with the file path and a short summary. Mention anything you could not fix.

## Quality checks (on the page images)

- Nothing runs off the page or is clipped; long words and URLs wrap; tables fit the text width.
- No empty pages, no heading alone at the bottom of a page (use `keepNext` on headings), no table row split in an
  ugly place (`cantSplit` on rows, `tableHeader` on the first row of long tables).
- Fonts are what you set and consistent; body text 10-12 pt; headings clearly larger. Stick to fonts every machine
  has (Arial, Calibri, Times New Roman, Georgia) unless the person's template uses others.
- Lists show bullets or numbers and are indented; numbering restarts where it should.
- Images are sharp, keep their aspect ratio and sit where they belong.
- Header, footer and page numbers appear on each page.

## docx rules that prevent most problems

- Sizes: page and margins in twentieths of a point (1440 = 1 inch); font `size` in half-points (22 = 11 pt).
- Tables: set `width` with `WidthType.DXA`, `columnWidths`, and the same width on each cell; the column widths must
  add up to the text width (page width minus both margins). Percent widths render differently between apps.
- Lists: define them under `numbering.config` and use `numbering: { reference, level }` on paragraphs. Do not type
  "•" or "1." into the text.
- Use `HeadingLevel.HEADING_1`... for headings so they show in the outline and a table of contents.
- Page breaks: `new Paragraph({ pageBreakBefore: true, ... })`, never runs of empty paragraphs.
- `ImageRun` needs `type` ('png', 'jpg', 'gif', 'bmp') and `transformation` in pixels; compute the height from the
  image's own aspect ratio.
- Escape nothing by hand: docx writes valid XML from plain strings.

## Editing an existing document

Keep the person's styles, numbering and section setup. Do not rebuild the document with `docx` from scratch.

- Filling a template: put `{{placeholders}}` in the document and use `patchDocument` from `docx` with
  `keepOriginalStyles: true`.
- Any other change: open it with `jszip`, change `word/document.xml` (and `word/header*.xml`, `word/footer*.xml` if
  needed) and write it back. Text in Word XML can be split across several `<w:r>` runs, so search the joined text of a
  paragraph, then edit the runs. Leave `word/styles.xml` and `word/numbering.xml` alone unless the change is about
  them.

```js
import JSZip from 'jszip';
import { readFile, writeFile } from 'node:fs/promises';
const zip = await JSZip.loadAsync(await readFile('in.docx'));
let xml = await zip.file('word/document.xml').async('string');
xml = xml.replace('Draft', 'Final');                 // a whole word that sits in one run
zip.file('word/document.xml', xml);
await writeFile('out.docx', await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
```

Render the edited file and compare it with a render of the original before you reply. Write to a new file unless
the person asked you to change theirs in place.

## Reading a document

Render it with `office_render` to see it. For its text, unzip it with `jszip` and read `word/document.xml`, or render
it and read the PDF with the pdf skill's text extraction.
