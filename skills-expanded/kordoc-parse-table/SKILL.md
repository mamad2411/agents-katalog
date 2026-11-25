---
name: kordoc-parse-table
description: Use when extracting a specific table from a Korean document with `npx` and kordoc. Trigger for requests such as pulling the first or Nth table from HWP, HWPX, or PDF, isolating tabular content for review, or using `kordoc:parse_table` with a zero-based table index.
---

# kordoc: parse_table

Reproduce the `parse_table` logic from `src/mcp.ts` with a one-off Node run inside the `npx` package context.

## Input Requirements

- Require exactly one target document.
- Require the user to attach the document or provide a concrete local path.
- Accept only supported formats: `.hwp`, `.hwpx`, `.pdf`.
- Require a table index or a clear ordinal such as "first table".
- Do not proceed if the document or table target is missing.

## Command

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- node <<'SCRIPT'
const p = require("path"), fs = require("fs");
const nmBin = process.env.PATH.split(p.delimiter).find(d => d.endsWith(".bin"));
const kUrl = "file:///" + p.join(p.resolve(nmBin, ".."), "kordoc", "dist", "index.js").split(p.sep).join("/");
import(kUrl).then(async (k) => {
  const filePath = "/abs/path/document.hwpx";
  const tableIndex = 0;
  const raw = fs.readFileSync(filePath);
  const buffer = raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.byteLength);
  const result = await k.parse(buffer);
  if (!result.success) throw new Error(result.error);
  const tables = result.blocks.filter(b => b.type === "table" && b.table);
  if (tables.length === 0) throw new Error("문서에 테이블이 없습니다.");
  if (tableIndex >= tables.length) {
    throw new Error("테이블 인덱스 초과: " + tableIndex + " (총 " + tables.length + "개 테이블)");
  }
  console.log(k.blocksToMarkdown([tables[tableIndex]]));
}).catch(e => { console.error(e); process.exit(1); });
SCRIPT
```

## Workflow

1. Resolve the file path to an absolute path.
2. Convert the user request into a zero-based `tableIndex`.
3. Parse the document once.
4. Filter `result.blocks` to table blocks only.
5. Render the selected table back to Markdown.

## Guardrails

- Convert "first table" to `0`, "second table" to `1`.
- Report the table count when the requested index is out of range.
- Do not silently fall back to another table.
- Refuse to continue when no supported document was provided.
