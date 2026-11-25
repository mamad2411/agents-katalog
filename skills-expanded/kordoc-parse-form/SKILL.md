---
name: kordoc-parse-form
description: Use when extracting structured label-value fields from Korean forms with `npx` and kordoc. Trigger for requests involving applications, government forms, personnel sheets, contact fields, or any HWP, HWPX, or PDF document that should be processed with `kordoc:parse_form`.
---

# kordoc: parse_form

Reproduce the `parse_form` logic from `src/mcp.ts`: parse the document, then run `extractFormFields`.

## Input Requirements

- Require exactly one target document.
- Require the user to attach the document or provide a concrete local path.
- Accept only supported formats: `.hwp`, `.hwpx`, `.pdf`.
- Prefer form-like or table-heavy office documents.
- Do not proceed if the document is missing.

## Command

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- node <<'SCRIPT'
const p = require("path"), fs = require("fs");
const nmBin = process.env.PATH.split(p.delimiter).find(d => d.endsWith(".bin"));
const kUrl = "file:///" + p.join(p.resolve(nmBin, ".."), "kordoc", "dist", "index.js").split(p.sep).join("/");
import(kUrl).then(async (k) => {
  const filePath = "/abs/path/form.hwpx";
  const raw = fs.readFileSync(filePath);
  const buffer = raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.byteLength);
  const result = await k.parse(buffer);
  if (!result.success) throw new Error(result.error);
  console.log(JSON.stringify(k.extractFormFields(result.blocks), null, 2));
}).catch(e => { console.error(e); process.exit(1); });
SCRIPT
```

## Workflow

1. Resolve the document path to an absolute path.
2. Parse the file once.
3. Run `extractFormFields(result.blocks)`.
4. Return structured JSON and preserve confidence if present.

## Guardrails

- Keep the output structured.
- Do not invent missing field values.
- If the document is not form-like, say so and suggest a normal parse instead.
- Refuse to continue when no supported document was provided.
