---
name: kordoc-parse-metadata
description: Use when extracting document metadata with `npx` and kordoc instead of reading the full document text. Trigger for requests about title, author, created date, or quick inspection of local HWP, HWPX, and PDF files through `kordoc:parse_metadata`.
---

# kordoc: parse_metadata

`src/mcp.ts` uses internal metadata-only helpers, but the public `npx kordoc` surface does not expose that fast path. With `npx` only, emulate the tool by parsing JSON and returning just the metadata fields.

## Input Requirements

- Require exactly one target document.
- Require the user to attach the document or provide a concrete local path.
- Accept only supported formats: `.hwp`, `.hwpx`, `.pdf`.
- Do not proceed if the document is missing or the path is ambiguous.

## Command

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- node <<'SCRIPT'
const p = require("path"), fs = require("fs");
const nmBin = process.env.PATH.split(p.delimiter).find(d => d.endsWith(".bin"));
const kUrl = "file:///" + p.join(p.resolve(nmBin, ".."), "kordoc", "dist", "index.js").split(p.sep).join("/");
import(kUrl).then(async (k) => {
  const filePath = "/abs/path/document.hwpx";
  const raw = fs.readFileSync(filePath);
  const buffer = raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.byteLength);
  const result = await k.parse(buffer);
  if (!result.success) throw new Error(result.error);
  console.log(JSON.stringify({
    fileType: result.fileType ?? null,
    pageCount: result.pageCount ?? null,
    metadata: result.metadata ?? null,
    outline: result.outline ?? null,
    warnings: result.warnings ?? null
  }, null, 2));
}).catch(e => { console.error(e); process.exit(1); });
SCRIPT
```

## Workflow

1. Resolve the target file to an absolute path.
2. Parse the file using the library API.
3. Return only metadata-oriented fields.
4. Say clearly that this path performs a full parse because metadata-only internals are not exposed through the public CLI.

## Guardrails

- Keep the answer focused on metadata.
- Do not invent missing fields.
- If the user truly needs the fastest possible metadata-only path, note that the source tree has a private implementation but this skill is intentionally `npx`-only.
- Refuse to continue when no supported document was provided.
