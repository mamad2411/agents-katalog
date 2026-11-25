---
name: handle-files-frontend
description: Use when importing/exporting CSV, downloading files (single or zipped), viewing/parsing PDFs, or uploading files in a frontend app — one central file-util module covering CSV (papaparse), download (file-saver/jszip), PDF (pdf.js), and upload with magic-number MIME detection + presigned URL + image resize. React/TS reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Handle files in a frontend app

Centralize file work in **one `file.util.ts`** (+ a media/upload service), not ad-hoc per feature.
Examples React/TS; principle → **▸ Example** → **▸ Other stacks**.

## 1. CSV import/export
Export JSON → CSV with a CSV lib (e.g. papaparse `unparse`) + the download helper; import with `parse`.
```ts
export const downloadCsvFromJson = <T>(rows: T[], fileName = 'download') =>
  download({ content: unparse(rows), contentType: 'text/csv', fileName });
```

## 2. Download (single + batch zip)
One `download({ content, contentType, fileName })` wrapper over `file-saver`; batch many files into a
zip (`jszip`) for multi-download. "By URL" / "by id" variants resolve the blob, then save.
```ts
await saveMultipleFilesAndZip(files, 'export.zip');   // jszip + file-saver
```

## 3. PDF
View with a PDF component (e.g. react-pdf) — set up the **pdf.js worker once**. Read page count via
pdf.js for validation/pagination: `getPdfPageCountFromUrl(url)`.

## 4. Upload — sniff MIME, presign, resize
- **Detect the real MIME from file CONTENT (magic numbers), not the extension or `file.type`** (both
  lie / are spoofable):
  ```ts
  async function detectMimeFromContent(file: File): Promise<string> {
    const b = new Uint8Array(await file.slice(0, 12).arrayBuffer());
    // match signatures: PNG 89 50 4E 47 · JPEG FF D8 FF · PDF 25 50 44 46 · GIF 47 49 46 · ...
  }
  ```
- **Upload via a presigned URL** — the server signs, the client POSTs the blob straight to storage, so
  the app never holds storage credentials. Route image uploads through a resize subfolder when needed:
  ```ts
  const contentType = await detectMimeFromContent(file);
  const { url, fields } = await mediaService.getPresignedUrl({ contentType, isPrivate, subFolder });
  await fetch(url, { method: 'POST', body: toFormData(fields, file) });
  ```
- **Validate type + size before upload**; surface failures through the app's error handler
  (`write-frontend-code` error-handling section).
▸ *Other stacks:* same shape — one file module; content-sniff the MIME; presigned-URL upload; swap
papaparse/jszip/file-saver/pdf.js for your ecosystem's equivalents.

## Verification
- File logic lives in one util module (+ an upload service), not scattered per feature.
- Uploads detect MIME from **content** (not `file.type`) and go through a **presigned URL** (no storage
  creds client-side); images route through resize when needed.
- CSV export/import and zip-download go through the shared helpers.

## Related
- `write-frontend-code` — services + error handling · `structure-a-frontend-app`.
