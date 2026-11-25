---
name: pdf
description: Create, read, fill and review PDF files with Muster. Use whenever the person asks for a PDF, to pull text or tables out of one, to fill or make a form, or to merge, split or stamp PDFs. Writes PDFs with pdf-lib, reads them with pdfjs-dist, renders pages to images with office_render and fixes the layout until every page looks right.
metadata:
  short-description: PDFs with pdf-lib and pdfjs-dist, checked page by page
---

# PDF

Use this skill to make a PDF, to read text and tables from one, to fill or create form fields, and to merge, split,
rotate or stamp pages. If the person wants a document they will keep editing, make a .docx with the documents skill
and render it to PDF at the end instead.

## Tools

- `muster_office` `office_setup`: call it once per chat before the first script. It answers with the command that
  runs a script (`<node> script.mjs`); with it `import { PDFDocument } from 'pdf-lib'` works from any folder. Do not
  `npm install` anything into the person's project.
- `muster_office` `office_render`: renders a PDF's pages to PNGs and shows you the first ones. It also turns a
  .docx, .xlsx or .pptx into a PDF (the `PDF:` line of its answer), which is often the easiest way to make a
  well-typeset PDF.
- Libraries: `pdf-lib` creates and changes PDFs (text, shapes, images, forms, merging, page copying); `pdfjs-dist`
  reads text and its position from any PDF.

`example.mjs` next to this file is a tested starting point (wrapped text that flows onto new pages, a table, an image,
form fields, page numbers). Copy it into the working folder and change it.

## The loop

1. Plan the pages: size (US Letter or A4), margins, sections.
2. Write a script in the working folder that builds the PDF, run it with the command from `office_setup`.
3. Call `office_render` on the PDF and look at every page image.
4. Fix, run and render again until the checks pass. Reply with the path and a short summary.

## Quality checks (on the page images)

- Text stays inside the margins and wraps; nothing is drawn below the bottom margin (start a new page instead).
- No overlapping text, no empty pages, no orphan heading at the bottom of a page.
- Tables line up; numbers are right-aligned when in a column.
- Images keep their aspect ratio (`image.scaleToFit`).
- Page numbers are right on every page; the title and author are set.

## pdf-lib rules that prevent most problems

- Units are points (72 per inch) with the origin at the bottom left: `y` counts up from the bottom of the page.
- pdf-lib does not wrap or paginate: measure with `font.widthOfTextAtSize` and move to a new page yourself (see
  `wrap` and `room` in the example).
- The standard fonts (`StandardFonts.Helvetica`, Times, Courier) only cover WinAnsi characters. For other characters
  (accents beyond Latin-1, CJK, emoji) embed a TrueType font file the person has, with `pdf.registerFontkit` and a
  fontkit build, or make the document as a .docx and render it to PDF.
- `embedPng` and `embedJpg` only; convert other image types first.

## Reading text and tables

```js
import { readFile } from 'node:fs/promises';
import { getDocument } from 'pdfjs-dist/legacy/build/pdf.mjs';
const doc = await getDocument({ data: new Uint8Array(await readFile('in.pdf')), useSystemFonts: false }).promise;
for (let number = 1; number <= doc.numPages; number++) {
  const page = await doc.getPage(number);
  const { items } = await page.getTextContent();
  // Each item has str and transform ([a, b, c, d, x, y]): group by y for lines, sort by x within a line.
  const lines = new Map();
  for (const item of items) { const y = Math.round(item.transform[5]); lines.set(y, [...(lines.get(y) ?? []), item]); }
  for (const y of [...lines.keys()].sort((a, b) => b - a)) console.log(lines.get(y).sort((a, b) => a.transform[4] - b.transform[4]).map(item => item.str).join(' | '));
}
```

For a table, group items into rows by `y` and into columns by the `x` where each header starts; check the result
against a render of the page. A scanned PDF has no text items: say so, render it and read the page images instead.

## Forms

```js
import { PDFDocument } from 'pdf-lib';
const pdf = await PDFDocument.load(await readFile('form.pdf'));
const form = pdf.getForm();
console.log(form.getFields().map(field => `${field.constructor.name} ${field.getName()}`)); // what can be filled
form.getTextField('approver.name').setText('Ada Lovelace');
form.getCheckBox('approver.approved').check();
// form.flatten();   // only if the person wants the answers fixed into the page
await writeFile('form-filled.pdf', await pdf.save());
```

Render the filled form to check every answer shows in its box.

## Other changes

- Merge: `const out = await PDFDocument.create(); for (const src of docs) (await out.copyPages(src, src.getPageIndices())).forEach(page => out.addPage(page));`
- Split, reorder, rotate (`page.setRotation(degrees(90))`), stamp text or a watermark on each page, set metadata.
- Write to a new file unless the person asked you to change theirs in place.
