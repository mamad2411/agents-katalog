---
name: case-timeline
description: Build a dated chronology from a folder of documents, with a source for every entry.
version: 1
tools: [document_reader, explorer]
min_context: 16000
pins: local
---

# Chronology from a set of documents

A timeline whose entries cannot be traced back to a document is a story. Every
line here carries its source.

## Method

1. Read every document before writing anything. A chronology assembled as you go
   is a chronology in the order the files happened to be listed.
2. Extract each dated event: what happened, when, who acted, where it is
   recorded.
3. Order by date. Undated events go in a separate section — never guessed into
   place.
4. Mark **contradictions** explicitly: two documents that date the same event
   differently is the single most useful thing you will find.

## Output

```
DATE        EVENT                                   ACTOR        SOURCE
2026-01-14  contract signed                          both parties BG-114.pdf p.1
2026-02-03  first notice sent                        Rossi S.r.l. lettera.pdf
…
UNDATED
  - <event> · <source> · <why it could not be dated>
CONFLICTS
  - <what two documents disagree about, and which they are>
```

## Rules

- One line per event. If a document describes three events, that is three lines.
- Never infer a date from context ("presumably that spring"). Undated is a valid
  and useful answer.
- Quote at most a few words from any document; this is an index, not a copy.
