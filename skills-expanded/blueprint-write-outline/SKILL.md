---
name: blueprint-write-outline
description: "Split the document into parts — each with its file, the points it must cover and a length — without touching any existing file."
---

# The outline

The person approved the brief. Now decide the parts, in `.blueprint/outline.json`:

```json
{ "parts": [
  { "id": "intro", "title": "はじめに", "file": "guide/01-intro.md", "points": ["何のための手引きか", "読み方"], "length": "800 字", "status": "todo" }
] }
```

- **How many parts.** A short piece is one part, one file. A long document is a part per chapter or
  section, each its own file, so each round writes and checks one of them. A book: a part per chapter.
- **Every key point of the brief lands in some part's `points`.** A point nobody owns is a point the
  document will miss.
- **Files are new.** Choose paths that do not exist yet: the check refuses an outline that would overwrite
  a file the person already has. Keep them inside this folder, outside `.blueprint/`.
- **The order is the reading order**, and `id`s are short lowercase words (`intro`, `ch-02-setup`).
- Every part starts as `"todo"`.

Write nothing else in this step. The person reads the outline and approves it before any part is written.

## Done when

`node <usecase pack>/checks/parts.mjs outline` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the
pack folders from your prompt) passes.
