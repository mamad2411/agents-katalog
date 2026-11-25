---
name: document-triage
description: Sort a folder of documents by type, extract the fields that identify each one, and flag what needs a human.
version: 1
tools: [document_reader, explorer]
pins: local
---

# Triage a folder of documents

You are turning a pile into a table. Read, classify, extract, and be explicit
about what you could not read.

## Method

1. **Enumerate** the folder before opening anything. Report how many files, of
   what kinds, and skip nothing silently.
2. **Classify** each document by its own evidence — a heading, a form number, a
   layout — not by its filename. Filenames lie; documents do not.
3. **Extract** only the fields that identify the document: type, date, issuing
   party, receiving party, reference number, amount or deadline where present.
   Leave a field empty rather than guessing it.
4. **Flag** anything that needs a person: unreadable scans, contradictions
   between two documents, missing dates, an amount that appears twice with
   different values.

## Output

One row per document, plus a summary line:

```
FILE            TYPE              DATE        PARTY              REF          FLAG
BG-114.pdf      contratto         2026-01-14  Rossi S.r.l.       2026/114     —
scan_003.pdf    illeggibile       —           —                  —            needs a human
…
SUMMARY  <n> documents · <n> types · <n> flagged
```

## Rules

- Never merge two documents into one row because they look similar.
- Never normalise a value you had to guess. An empty cell is information; an
  invented one is a defect that will be discovered downstream.
- Dates as ISO. Amounts with their currency, exactly as written.
