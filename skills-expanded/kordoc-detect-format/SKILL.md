---
name: kordoc-detect-format
description: Use when identifying whether a Korean document file is HWP, HWPX, PDF, or unknown with `npx` and kordoc. Trigger for triage requests such as checking file type before parsing, validating uploads, routing mixed office files, or using `kordoc:detect_format` on local documents.
---

# kordoc: detect_format

Reproduce the `detect_format` logic from `src/mcp.ts`: read only the header, then call `detectFormat`.

## Input Requirements

- Require exactly one target file.
- Require the user to attach the file or provide a concrete local path.
- Prefer supported document candidates: `.hwp`, `.hwpx`, `.pdf`.
- Do not proceed if the file is missing.

## Command

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- node <<'SCRIPT'
const p = require("path"), fs = require("fs");
const nmBin = process.env.PATH.split(p.delimiter).find(d => d.endsWith(".bin"));
const kUrl = "file:///" + p.join(p.resolve(nmBin, ".."), "kordoc", "dist", "index.js").split(p.sep).join("/");
import(kUrl).then(k => {
  const filePath = "/abs/path/document.hwpx";
  const fd = fs.openSync(filePath, "r");
  const header = Buffer.alloc(4);
  try { fs.readSync(fd, header, 0, 4, 0); } finally { fs.closeSync(fd); }
  const ab = header.buffer.slice(header.byteOffset, header.byteOffset + header.byteLength);
  console.log(k.detectFormat(ab));
}).catch(e => { console.error(e); process.exit(1); });
SCRIPT
```

## Workflow

1. Resolve the file to an absolute path.
2. Read only the first 4 bytes (the magic bytes `detectFormat` inspects).
3. Return only `hwp`, `hwpx`, `pdf`, or `unknown`.
4. If the type is supported, move to the matching kordoc skill.

## Guardrails

- Do not infer type from the filename alone.
- If the result is `unknown`, stop and report that rather than trying to parse anyway.
- Keep the answer short unless the user asked for diagnostics.
- Refuse to continue when no file was provided.
