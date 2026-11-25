---
name: bulk-extract
description: Pull the same fields out of many documents into one table, and report what could not be found.
version: 1
tools: [document_reader, explorer]
pins: local
---

# One table from many documents

Extraction is boring and unforgiving: the failure mode is a plausible value in
the wrong column, discovered three months later.

## Method

1. **Agree the columns first.** If the caller did not specify them, propose a
   set from the first three documents and ask before doing the rest.
2. **Extract per document**, one at a time, without carrying context between
   them. A value remembered from the previous file is the classic source of
   wrong rows.
3. **Record misses explicitly.** An empty cell means "not present in this
   document", and a cell marked `?` means "present but unreadable". They are
   different problems for whoever fixes them.
4. **Count at the end**: rows produced, cells filled, cells empty, cells
   unreadable.

## Output

CSV, with a header, plus a final summary comment:

```
file,field_a,field_b,field_c
BG-114.pdf,2026-01-14,Rossi S.r.l.,1200.00
scan_003.pdf,,?,
# 2 rows · 4/6 cells filled · 1 empty · 1 unreadable
```

## Rules

- Never invent a value to complete a row.
- Never reformat a value beyond what the caller asked for; keep the document's
  own spelling of names and its own currency notation.
- If two documents contradict each other, produce both rows and flag them. It is
  not your job to decide which is right.
