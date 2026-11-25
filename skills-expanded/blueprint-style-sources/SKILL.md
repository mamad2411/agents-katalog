---
name: blueprint-style-sources
description: "Collect the texts the person wants as models into .blueprint/sources/ as Markdown, and record where each came from."
---

# Collect the models

`.blueprint/answers.json` → `sources` lists what the person wants the style taken from: files, folders
or URLs, one per line. The person may not be an engineer; tell them in plain words what you collected.

Change nothing in the repository: copies go into `.blueprint/sources/`, and the originals are only read.
The person approves the collected models before the next step writes anything of theirs.

## How

- **A file**: copy it to `.blueprint/sources/<name>.md`. A `.txt` becomes `.md` unchanged. A Word or PDF
  file: extract the text faithfully (headings as `#`, lists as `-`); say in the report that it was converted.
- **A folder**: take the documents in it (Markdown and text). Ask before taking more than about twenty.
- **A URL**: fetch the page and keep **only the article body**, as Markdown — no navigation, footer,
  cookie banner or share buttons. Those are the site's words, not the author's, and would be measured as
  the style.
- Never rewrite the text: a fixed typo in a model changes what is measured.
- Keep them in one language and one kind of document. If the list mixes them, ask which to keep.

Write `.blueprint/sources.json`, one entry per file:

```json
[{ "file": "about-us.md", "origin": "https://example.com/about" }]
```

## Done when

`node <usecase pack>/checks/sources.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack folders from your prompt) passes: every file is listed with its origin and every
listed file exists. There must be at least two documents with enough text between them to measure a
style — one short text is that text's habits, not a style. If there is too little, ask the person for more.
