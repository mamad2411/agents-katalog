---
name: docx
description: "Use whenever the user wants to create, read, edit, redact, merge, split, extract from, or otherwise manipulate Word documents (.docx / .doc / .dotx). Triggers include: any mention of 'Word doc', 'Word document', '.docx', '.doc', 'Microsoft Word'; producing professional deliverables in Word format such as memos, letters, MSAs, DPAs, NDAs, security questionnaires, SOC 2 evidence packs, board memos, customer notification letters, policy documents, runbooks delivered as Word, bilingual (Spanish/English) Puerto Rico business correspondence; styled output with TOC, headings, page numbers, headers/footers, footnotes, tables, comments, tracked changes, find-and-replace, redaction of names/PII inside Word; converting PDF→Word for editing; converting Markdown/HTML→Word; extracting Word content (text, tables, comments, tracked-change history) for downstream use. ALSO use when the deliverable is a .docx even if the substantive content was drafted by a sibling skill — packaging into Word is in this skill's scope. Do NOT use when: the deliverable is a PDF (use pdf), spreadsheet (use xlsx), slide deck (use pptx), or when the user wants substantive content drafted in a domain owned by another skill (use marketing:draft-content for blog/email/landing copy, legal:review-contract for clause-by-clause contract redlining strategy, legal:legal-response for templated legal replies, operations:runbook for runbook authoring logic, finance:financial-statements for P&L narratives) — in those cases the sibling skill drafts and this skill packages the final .docx."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX — Create, Edit, Redact, Extract

## Overview

A .docx file is a ZIP archive of XML files. This skill handles all Word-format work end-to-end: new documents (via `docx-js`), edits to existing documents (unpack → edit XML → repack), conversion in/out of Word, redaction, tracked changes, comments, find-and-replace, and bilingual (Spanish/English) typography for Puerto Rico business contexts.

## When to use vs. defer

| User asks for... | Use this skill? | Notes |
|---|---|---|
| ".docx", "Word doc", "Word document", "MS Word" | YES | Format-driven trigger |
| Word memo, letter, MSA, DPA, NDA, policy, board memo | YES | Word is the natural deliverable |
| Convert PDF → Word | YES | Word-from-PDF lives here |
| Convert Word → PDF | NO → `pdf` | PDF-from-Word lives in `pdf` |
| Redact a Word doc | YES | True redaction = find/replace + remove + flatten (see Redaction below) |
| Redact a PDF | NO → `pdf` | PDF redaction is high-stakes; that skill enforces black-box overlay |
| Marketing blog/email/landing copy as .docx | CHAIN | `marketing:draft-content` writes; this skill packages |
| Contract redline strategy / playbook deviation analysis | NO → `legal:review-contract` | That skill owns clause-by-clause logic; this skill applies the redlines as tracked changes |
| Runbook authoring | NO → `operations:runbook` | That skill drafts; this skill packages if Word output is requested |
| Financial statement narratives | NO → `finance:financial-statements` | That skill drafts; this skill packages |
| Slide deck | NO → `pptx` | |
| Spreadsheet | NO → `xlsx` | |
| Google Docs (live, in-cloud) | NO | Out of scope; suggest export to .docx first |

**Rule of thumb:** sibling skills draft *substance*; this skill packages *Word format*. If the user just says "write me X as a Word doc" and X falls in a sibling's domain, briefly chain (sibling drafts → this skill packages) rather than draft from scratch.

## Quick Reference

| Task | Approach |
|------|----------|
| Read / extract text | `pandoc document.docx -o output.md` |
| Read with tracked changes | `pandoc --track-changes=all document.docx -o output.md` |
| Read raw XML | `python scripts/office/unpack.py document.docx unpacked/` |
| Create new document | `docx-js` (see Creating New Documents) |
| Edit existing | unpack → edit XML → repack (see Editing Existing Documents) |
| Convert .doc → .docx | `python scripts/office/soffice.py --headless --convert-to docx document.doc` |
| Convert .docx → PDF | DEFER to `pdf` skill (uses LibreOffice) |
| Convert PDF → .docx | `python scripts/office/soffice.py --headless --convert-to docx file.pdf` (verify layout; OCR first if scanned via `pdf` skill) |
| Convert .docx → images | `soffice --convert-to pdf` then `pdftoppm -jpeg -r 150 file.pdf page` |
| Accept all tracked changes | `python scripts/accept_changes.py input.docx output.docx` |
| Find & replace (string) | unpack → `Edit` tool on `word/document.xml` → repack |
| Compare two .docx versions | `pandoc` both to .md, then `diff` (or use Word's compare via LibreOffice) |
| Redact text content | See Redaction section — true removal, not visual cover |

## Default Professional Preset (use as the baseline for all new docs)

Apply this preset to every new document unless the user specifies otherwise. It produces consistent, professional output suitable for client/board/regulator delivery.

- Page size: US Letter (12240 x 15840 DXA); 1-inch margins (1440 DXA).
- Default font: Arial 11pt (24 half-points). Universal, renders in Google Docs and on PR-government systems.
- Headings: H1 16pt bold, H2 14pt bold, H3 12pt bold, all Arial, with `outlineLevel` set (required for TOC).
- Smart quotes ON for body text (use XML entities when editing raw XML — see table below).
- Header: company / document title, right-aligned date via tab stop.
- Footer: "Page X of Y" centered.
- Hyperlinks: built-in `Hyperlink` style, blue underline.
- Tables: 1px solid `#CCCCCC` borders, `ShadingType.CLEAR` headers in `#D5E8F0`, cell padding `{top:80, bottom:80, left:120, right:120}`.

A complete preset block is provided in the Creating New Documents section.

## Bilingual (Spanish / English) typography for PR contexts

Many PR business documents are bilingual. Use these rules:

| Char | XML entity | When |
|---|---|---|
| ñ Ñ | `&#xF1;` `&#xD1;` | Always (Spanish names, "España", "señor") |
| á é í ó ú | `&#xE1;` `&#xE9;` `&#xED;` `&#xF3;` `&#xFA;` | Always (use precomposed, never combining) |
| Á É Í Ó Ú | `&#xC1;` `&#xC9;` `&#xCD;` `&#xD3;` `&#xDA;` | Always |
| ¿ ¡ | `&#xBF;` `&#xA1;` | Open Spanish question/exclamation |
| « » | `&#xAB;` `&#xBB;` | Spanish-style quotes (optional; smart quotes also acceptable) |
| ° | `&#xB0;` | Degree (e.g., "Art. 3°") |

- **Font**: Arial, Calibri, Times New Roman, Liberation Sans all render Spanish diacritics correctly. AVOID Helvetica (some weights drop diacritics on some viewers).
- **Bilingual section pattern**: header in both languages separated by ` / ` (e.g., "Confidentiality / Confidencialidad"). Use the same paragraph + soft-break (`<w:br/>`) for tight pairing, or two paragraphs with H2 styling for distinct sections.
- **Date format**: spell out month for formal letters ("25 de abril de 2026" / "April 25, 2026"). Locale-set date fields are unreliable across viewers — render as static text.

## Workflow Recipes (most common the operator jobs)

### R1. Create-from-Markdown (policy, memo, runbook in Word)
1. Receive Markdown source.
2. Quick path: `pandoc input.md -o draft.docx --reference-doc=reference.docx` (if a styled reference exists) — fast but limited control.
3. Full-control path: parse the MD structure, generate via `docx-js` using the Default Professional Preset, programmatic TOC, headers/footers, page numbers.
4. Validate: `python scripts/office/validate.py draft.docx`.

### R2. Edit-in-place with tracked changes (vendor MSA redlines)
1. `unpack.py contract.docx unpacked/`.
2. Use the `Edit` tool on `word/document.xml`. Replace whole `<w:r>` blocks with `<w:del>...</w:del><w:ins>...</w:ins>` siblings. Preserve `<w:rPr>` for formatting.
3. Author = "Claude" (unless user names another).
4. `pack.py unpacked/ redlined.docx --original contract.docx`.

### R3. Redline-an-MSA against playbook (CHAINED with `legal:review-contract`)
1. Call `legal:review-contract` for clause-level deviation analysis and proposed redlines.
2. Apply each proposed redline as a tracked change per R2 above.
3. Add a Claude-authored comment per material change explaining the rationale (use `scripts/comment.py`).

### R4. Redact-and-export-PDF (SOC 2 evidence sharing, customer references)
1. **List every term to redact** (names, emails, IP addresses, account IDs, customer logos in images).
2. unpack the .docx.
3. For each term: in `word/document.xml` and `word/header*.xml`, `word/footer*.xml`, `word/comments.xml`, `word/footnotes.xml`, `word/endnotes.xml` — replace text inside `<w:t>` with `[REDACTED]` (or fixed-width block `█████`). Match in `<w:delText>` too if tracked changes exist.
4. **Strip metadata**: blank `core.xml` `dc:creator`, `dc:title`, `lastModifiedBy`; remove `app.xml` `Company`, `Manager`.
5. **Remove all comments and tracked changes** (these often leak the original text). Run `accept_changes.py` first, then strip `word/comments.xml`, `commentsExtended.xml`, `commentsIds.xml` and the related `[Content_Types].xml` entries.
6. **Remove embedded images** that contain identifiable info (replace with placeholder rectangles or delete).
7. repack → then HAND OFF to `pdf` skill to flatten to PDF (PDF flattening eliminates any residual Word-layer recoverability). Do NOT just visually cover text with white boxes — the underlying string survives extraction.

### R5. Extract tables to spreadsheet (CHAINED with `xlsx`)
1. `pandoc document.docx -o tables.html` (preserves table structure better than .md).
2. Or, unpack and parse `<w:tbl>` from `word/document.xml`.
3. Hand off rows/columns to `xlsx` skill for final spreadsheet generation.

### R6. Bilingual customer letter (PR-typical)
1. Use Default Professional Preset.
2. Letterhead: company name + PR address (street, municipio, ZIP).
3. Two-language body: English left column / Spanish right column via two-column section, OR sequential blocks separated by H2 dividers ("English Version" / "Versión en Español").
4. Signature block: name, title in both languages, optional bilingual notary block for formal letters.

## Find-and-Replace (string-level)

For one-off replacements, prefer unpack → Edit tool on `word/document.xml`. For programmatic batch replace across many files:

```bash
python scripts/office/unpack.py file.docx unpacked/
# Edit document.xml, header*.xml, footer*.xml, comments.xml, footnotes.xml as needed
python scripts/office/pack.py unpacked/ out.docx --original file.docx
```

Watch out for:
- Text split across multiple `<w:r>` runs because of formatting. `unpack.py` merges adjacent runs by default (`--merge-runs true`) — keep this on for find-and-replace.
- Smart quotes: source may have `&#x2019;` instead of `'`. Search for both.
- Case sensitivity: XML editing is case-sensitive; if user wants case-insensitive, write a small Python pass.

## Redaction (Word-format)

True redaction in .docx requires: (1) remove the underlying text, (2) strip metadata, (3) strip comments/tracked-changes history, (4) flatten images, (5) export to PDF for delivery (PDF flattening prevents text-layer recovery). Visual cover (white box on top) is NOT redaction — the text remains in the XML and is trivially extracted. See Recipe R4. For PDF redaction proper, defer to the `pdf` skill which enforces black-box overlay + content-stream removal.

---

## Creating New Documents

Generate .docx files with JavaScript, then validate. Install: `npm install -g docx`.

### Setup
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### Default Professional Preset (drop-in)
```javascript
const doc = new Document({
  creator: "Claude",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } }, // 11pt body
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: { default: new Header({ children: [new Paragraph({ children: [new TextRun({ text: "Document Title", bold: true })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] }),
                 new TextRun(" of "), new TextRun({ children: [PageNumber.TOTAL_PAGES] })],
    })]}) },
    children: [/* content */],
  }],
});
```

### Validation
```bash
python scripts/office/validate.py doc.docx
```
If validation fails, unpack, fix the XML, repack.

### Page Size

`docx-js` defaults to A4. Set US Letter explicitly for US/PR documents:

| Paper | Width (DXA) | Height (DXA) | Content Width (1" margins) |
|---|---|---|---|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 (default) | 11,906 | 16,838 | 9,026 |
| Legal | 12,240 | 20,160 | 9,360 |

**Landscape:** pass portrait dimensions and let docx-js swap:
```javascript
size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
```

### Lists (NEVER use unicode bullets)

```javascript
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
    ],
  }],
});
```
Same `reference` continues numbering; different `reference` restarts.

### Tables (dual widths required)

```javascript
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [4680, 4680],
  rows: [
    new TableRow({ children: [
      new TableCell({
        borders,
        width: { size: 4680, type: WidthType.DXA },
        shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun("Cell")] })],
      }),
    ]}),
  ],
})
```

Rules: ALWAYS `WidthType.DXA` (PERCENTAGE breaks Google Docs); table width = sum of `columnWidths`; cell `width` matches its column; `ShadingType.CLEAR` not SOLID; never use tables as horizontal rules — use a paragraph border instead.

### Images
```javascript
new ImageRun({
  type: "png", // REQUIRED: png, jpg, jpeg, gif, bmp, svg
  data: fs.readFileSync("image.png"),
  transformation: { width: 200, height: 150 },
  altText: { title: "T", description: "D", name: "N" }, // all three required
})
```

### Page Breaks, Hyperlinks, Footnotes, Tab Stops, Multi-Column, TOC, Headers/Footers

(See original patterns — preserved unchanged. Key rules below.)

- `PageBreak` must be inside a `Paragraph`.
- External link via `ExternalHyperlink`; internal via `Bookmark` + `InternalHyperlink`.
- Footnotes via `footnotes: { 1: { children: [...] } }` plus `FootnoteReferenceRun(1)` in body.
- Tab stops for right-aligned same-line text; `PositionalTab` with `PositionalTabLeader.DOT` for TOC-style dot leaders.
- Multi-column via `properties.column`; force column break with `SectionType.NEXT_COLUMN`.
- TOC: `new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })` — headings MUST use `HeadingLevel` only.
- Headers/footers via `headers.default` and `footers.default` per section.

### Critical Rules for docx-js

- Set page size explicitly (default is A4).
- Landscape: pass portrait dims + `orientation: PageOrientation.LANDSCAPE`.
- Never `\n`; use separate `Paragraph` elements.
- Never unicode bullets in plain `TextRun`; use `LevelFormat.BULLET` numbering.
- `PageBreak` must be inside `Paragraph`.
- `ImageRun` requires `type` and full `altText` `{title, description, name}`.
- Tables: `WidthType.DXA` only, dual widths must match, `ShadingType.CLEAR`, never as dividers.
- TOC requires `HeadingLevel` only on heading paragraphs (no custom style IDs interfere).
- Override built-in heading styles with exact IDs `Heading1` / `Heading2` / `Heading3` and include `outlineLevel`.

---

## Editing Existing Documents

Three steps in order: Unpack → Edit XML → Pack.

### Step 1: Unpack
```bash
python scripts/office/unpack.py document.docx unpacked/
```
Pretty-prints, merges adjacent runs, converts smart quotes to XML entities so they survive editing. `--merge-runs false` to skip.

### Step 2: Edit XML

Edit files in `unpacked/word/`. Use the `Edit` tool directly for string replacement — do not write Python scripts unless doing batch transforms.

Author for tracked changes / comments = `"Claude"` unless the user specifies otherwise.

**Smart quotes for new content** (entities table earlier in this skill).

**Adding comments:**
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"
```
Then add markers to `document.xml` (see XML Reference below).

### Step 3: Pack
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
Validates with auto-repair (fixes oversized `durableId`, missing `xml:space="preserve"`). Won't fix malformed XML, bad nesting, missing relationships.

### Common Pitfalls (Editing)

- Replace whole `<w:r>` blocks for tracked changes; don't inject `<w:del>`/`<w:ins>` inside a run.
- Preserve `<w:rPr>` (bold, font, size) by copying it into your replacement runs.
- For find-and-replace across split runs, rely on `unpack.py --merge-runs true` (default).

---

## XML Reference

### Schema Compliance

- `<w:pPr>` element order: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` last.
- Add `xml:space="preserve"` on any `<w:t>` with leading/trailing spaces.
- RSIDs: 8-digit hex (e.g., `00AB1234`).

### Tracked Changes

**Insertion:**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2026-04-25T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**Deletion:**
```xml
<w:del w:id="2" w:author="Claude" w:date="2026-04-25T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

Inside `<w:del>`: use `<w:delText>` (not `<w:t>`) and `<w:delInstrText>` (not `<w:instrText>`).

**Selective accept/reject of another author's changes:**

Reject Jane's insertion → nest a Claude deletion inside her insertion:
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

Restore Jane's deletion → leave hers, add a Claude insertion after:
```xml
<w:del w:author="Jane" w:id="5"><w:r><w:delText>x</w:delText></w:r></w:del>
<w:ins w:author="Claude" w:id="10"><w:r><w:t>x</w:t></w:r></w:ins>
```

**Deleting whole paragraphs/list items** — also mark the paragraph mark as deleted so it merges into the next paragraph:
```xml
<w:p>
  <w:pPr><w:rPr><w:del w:id="1" w:author="Claude" w:date="..."/></w:rPr></w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="...">
    <w:r><w:delText>...</w:delText></w:r>
  </w:del>
</w:p>
```

### Comments

`<w:commentRangeStart>` and `<w:commentRangeEnd>` are siblings of `<w:r>`, never inside `<w:r>`.

```xml
<w:commentRangeStart w:id="0"/>
<w:r><w:t>commented text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

Replies nest the child range markers inside the parent's range markers, then both `commentReference` elements follow.

### Images

1. Add file to `word/media/`.
2. Add relationship in `word/_rels/document.xml.rels`.
3. Add content type in `[Content_Types].xml`.
4. Reference in `document.xml` via `<w:drawing><wp:inline>...<a:blip r:embed="rIdN"/>...`.

(EMU units: 914400 = 1 inch.)

---

## Document QA Checklist (run before delivery)

- [ ] Font consistent throughout (no stray Calibri/Times mixed in).
- [ ] No orphan headings (heading on its own at end of page).
- [ ] Smart quotes used (no straight `'` or `"`).
- [ ] Spanish diacritics render (open in `pandoc -o check.md` and grep for `?` artifacts).
- [ ] All images have `altText`.
- [ ] Page numbers present (or explicitly omitted by user).
- [ ] No tracked changes / comments left over (unless intentional).
- [ ] Metadata (Author, Company) appropriate for the audience.
- [ ] `validate.py` passes.

---

## Dependencies

- **pandoc**: text extraction, MD↔DOCX conversion.
- **docx (npm)**: `npm install -g docx` for new document generation.
- **LibreOffice**: PDF and legacy `.doc` conversion (auto-configured via `scripts/office/soffice.py`).
- **Poppler**: `pdftoppm` for image rendering.
- **Python**: `scripts/office/unpack.py`, `pack.py`, `validate.py`, `accept_changes.py`, `comment.py`.
