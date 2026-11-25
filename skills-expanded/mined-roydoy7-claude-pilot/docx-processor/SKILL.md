---
name: docx-processor
description: Create, edit, inspect, and convert professional Word documents (.docx). Use for reports, letters, policies, manuals, forms, contracts, template-based documents, formatting-preserving edits, document automation, and DOCX quality review.
---

# DOCX Processing

## Choose the workflow

1. Inspect an existing document with `mcp__docx__docx` using `get-info` before changing it.
2. Use the TypeScript `docx` library to create a new document from structured content.
3. Use Word desktop automation for layout-sensitive edits to an existing document.
4. Edit OOXML only for narrow, well-understood changes that desktop automation cannot perform reliably.
5. Use `mcp__convert__convert` for DOCX/PDF/TXT/HTML conversion.

Never imply that the `docx` library can load an arbitrary existing DOCX and append to it. Never overwrite the source unless the user explicitly requests it.

## Build new documents safely

Separate content from rendering. Draft and validate sections as data, then perform one deterministic final render. Split helper functions by component instead of repeatedly reopening the generated DOCX.

```typescript
import {
  Document, HeadingLevel, Packer, Paragraph, TextRun,
} from 'docx';
import { writeFile } from 'node:fs/promises';

const sections = [
  { heading: 'Executive Summary', paragraphs: ['State the decision and key evidence.'] },
  { heading: 'Findings', paragraphs: ['Present findings in a logical order.'] },
];

const children = sections.flatMap(({ heading, paragraphs }) => [
  new Paragraph({ text: heading, heading: HeadingLevel.HEADING_1 }),
  ...paragraphs.map((text) => new Paragraph({ children: [new TextRun(text)] })),
]);

const doc = new Document({ sections: [{ children }] });
await writeFile('report.docx', await Packer.toBuffer(doc));
```

For long documents, keep section content in JSON or TypeScript data, validate each section independently, and render only after the full structure is coherent.

## Apply professional document design

- Select page size, margins, language, and fonts for the audience and locale.
- Define reusable title, heading, body, caption, quote, and table styles.
- Use heading levels semantically; do not simulate headings with bold text.
- Keep body typography restrained and readable. Use spacing and hierarchy before decoration.
- Add headers, footers, page numbers, metadata, and a table of contents when the document warrants them.
- Keep tables readable across page breaks; repeat header rows and avoid crowded cells.
- Use numbered and bulleted lists through document numbering, not typed symbols.
- Preserve template styles and branding when a source template exists.
- Add descriptive alternative text or captions for meaningful images when supported.

Adapt density to the artifact. A formal Japanese application form may need precise borders and compact fields; a narrative report needs comfortable reading rhythm and clear hierarchy.

## Edit existing documents conservatively

- Copy the source to a new output path first.
- Preserve styles, section breaks, headers, footers, fields, comments, tracked changes, and embedded objects unless the task targets them.
- Prefer text replacement inside existing runs only when formatting boundaries are understood.
- Use desktop Word for pagination, tracked changes, comments, fields, or complex template interaction.
- Reinspect structure after editing and report any feature that could not be preserved.

## Validate before delivery

1. Confirm the output exists and opens successfully.
2. Run DOCX `get-info` and check expected pages, paragraphs, tables, images, comments, and tracked changes.
3. Convert the result to PDF and visually inspect representative pages, including the first, last, dense tables, and section transitions.
4. Check clipped text, blank pages, widows/orphans, broken numbering, table overflow, font substitution, and inconsistent headings.
5. Confirm that temporary files were not delivered and the original remained unchanged.
