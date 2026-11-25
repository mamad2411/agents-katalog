---
name: documentation-pdf-operations
description: Use when working on PDF manipulation in this repo — merging multiple PDFs into one, splitting a PDF into pages, extracting/reordering pages, rotating pages, or drawing overlays. Points to the existing pdf-lib pipeline instead of reimplementing it.
---

# PDF operations in pdf-kit

All PDF manipulation here runs client-side with `pdf-lib` + `pdfjs-dist`. There is no
server-side merge/split — the worker (`worker/index.ts`) only proxies `compress` and `ocr`
to an external Stirling-PDF instance. Don't add a server endpoint for merge/split/rotate;
`pdf-lib` in the browser already does it, keeping the "processed locally" guarantee shown
in the UI.

## Merge multiple PDFs into one — already implemented, reuse it

This is not a missing feature. The existing workspace flow already merges any number of
PDFs (and images) into a single output:

1. `src/features/workspace/import-files.ts` (`importPdf` → `isolatePdfPages`) splits every
   dropped PDF into one single-page `PDFDocument` per page, so each page becomes an
   independent `WorkspacePage` with its own `source` blob and `pageIndex: 0`.
2. The pages array holds pages from every dropped file, in the order the user arranged
   them (drag-and-drop reordering, rotate, delete — see `src/features/workspace/model.ts`).
3. `src/features/image-to-pdf/generate.ts` (`generatePdf`) walks that array and, for each
   `kind: 'pdf'` page, `copyPages`s it into one output `PDFDocument`, then `output.save()`
   returns the merged bytes.

So "merge PDF A + B into one file" == drop both files on the workspace and click
**Create PDF**. Covered by the test `merges imported PDF pages in workspace order` in
`tests/pdf-generation.test.ts`.

If you need a *headless* merge (no workspace/UI involved — e.g. a script or a new
non-visual entry point), skip the isolate/thumbnail machinery and go straight to pdf-lib:

```ts
import { PDFDocument } from 'pdf-lib'

async function mergePdfs(files: Uint8Array[]) {
  const output = await PDFDocument.create()
  for (const bytes of files) {
    const source = await PDFDocument.load(bytes)
    const pages = await output.copyPages(source, source.getPageIndices())
    pages.forEach((page) => output.addPage(page))
  }
  return output.save() // Uint8Array
}
```

That's the whole operation — don't reach for a server round-trip or a new dependency.

## Split a PDF into its pages

Use `isolatePdfPages` in `src/features/workspace/import-files.ts` — it already does
"one `PDFDocument` per page" via `copyPages`. Don't rewrite it.

## Rotate / reorder / delete / duplicate pages

Handled by `src/features/workspace/model.ts` (`rotateSelected`, `reorderPages`,
`moveSelected`, `deleteSelected`, `duplicateSelected`) operating on the `WorkspacePage[]`
array before `generatePdf` runs. Rotation is composed at export time in `generate.ts`:
`page.setRotation(degrees((sourceRotation + item.rotation) % 360))` — source PDF rotation
and the user's applied rotation are added together, not overwritten.

## Overlays (text/rectangle/circle annotations)

Defined per-page in `PdfPage.overlays` (`src/types/pdf.ts`), coordinates stored as
0–1 fractions of page size. `overlayPdfRect` in `src/features/pdf-editor/model.ts`
converts a fractional rect to absolute PDF points, accounting for the *source* page's
rotation (not the export rotation) since overlays are flattened before the rotation is
applied. `generate.ts` flattens overlays with `page.drawText` / `drawRectangle` /
`drawEllipse` using `StandardFonts.Helvetica`.

## Gotchas seen in this codebase

- Cache a loaded `PDFDocument` per source `Blob` (see the `Map` in `generatePdf`) —
  don't call `PDFDocument.load` once per page when multiple pages share one source file.
- `output.save()` returns a `Uint8Array`; wrap as `new Blob([bytes as BlobPart], { type: 'application/pdf' })`
  before creating a download URL (TS needs the `as BlobPart` cast here).
- WebP images aren't embeddable by pdf-lib directly — `generate.ts` re-encodes them to
  PNG via `OffscreenCanvas` first (`imageBytes` helper). Reuse that helper for new image
  formats rather than adding a new embed path.
- Text overlay only draws if `isPdfTextSupported` (WinAnsi-encodable) — Helvetica can't
  render arbitrary Unicode.

## Where tests live

`tests/pdf-generation.test.ts` covers `generatePdf` (merge order, overlays, rotation).
`tests/workspace.test.ts` covers page array operations. `e2e/pdf-kit.spec.ts` covers the
full UI flow with Playwright. Add cases there rather than a new test file for a new
operation on the existing pipeline.
