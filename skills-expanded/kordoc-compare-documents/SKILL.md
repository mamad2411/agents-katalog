---
name: kordoc-compare-documents
description: Use when diffing two Korean documents with `npx` and kordoc. Covers HWP, HWPX, and cross-format comparisons for requests such as 신구대조표 preparation, change review between document versions, block-level additions and removals, or invoking `kordoc:compare_documents` on two local files.
---

# kordoc: compare_documents

Reproduce the `compare_documents` logic from `src/mcp.ts` with the public `compare` export.

## Input Requirements

- Require exactly two target documents.
- Require the user to attach both documents or provide two concrete local paths.
- Accept only supported formats: `.hwp`, `.hwpx`, `.pdf`.
- Do not proceed if either document is missing.
- Preserve the user-provided ordering so source and target are not swapped implicitly.

## Command

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- node <<'SCRIPT'
const p = require("path"), fs = require("fs");
const nmBin = process.env.PATH.split(p.delimiter).find(d => d.endsWith(".bin"));
const kUrl = "file:///" + p.join(p.resolve(nmBin, ".."), "kordoc", "dist", "index.js").split(p.sep).join("/");
import(kUrl).then(async (k) => {
  const fileA = "/abs/path/old.hwpx";
  const fileB = "/abs/path/new.hwpx";
  const rawA = fs.readFileSync(fileA);
  const rawB = fs.readFileSync(fileB);
  const bufA = rawA.buffer.slice(rawA.byteOffset, rawA.byteOffset + rawA.byteLength);
  const bufB = rawB.buffer.slice(rawB.byteOffset, rawB.byteOffset + rawB.byteLength);
  const result = await k.compare(bufA, bufB);
  console.log(JSON.stringify(result, null, 2));
}).catch(e => { console.error(e); process.exit(1); });
SCRIPT
```

## Workflow

1. Resolve both files to absolute paths.
2. Run `compare`.
3. Read `stats` first: `added`, `removed`, `modified`, `unchanged`.
4. Summarize the major deltas instead of repeating unchanged blocks.
5. Keep source and target ordering explicit.

## Guardrails

- Call out when the comparison is cross-format.
- Do not overstate semantic meaning from block-level diffs.
- Separate added, removed, and modified content in the final explanation.
- Refuse to continue when fewer than two supported documents were provided.
