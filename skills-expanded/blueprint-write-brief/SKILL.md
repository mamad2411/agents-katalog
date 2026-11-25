---
name: blueprint-write-brief
description: "Turn the interview into a brief — purpose, audience, key points, facts from the sources, open questions — and collect the sources."
---

# The brief

`.blueprint/answers.json` holds what the person asked for. The person may not be a writer or an engineer:
say what you do in plain words.

Change nothing in the repository: this step writes only inside `.blueprint/`. The person reads the brief
and approves it before anything of theirs is written.

## Collect the sources (when `sources` is not empty)

Copy each file, or fetch each page's **article body only**, as Markdown into `.blueprint/sources/`, and
list them in `.blueprint/sources.json` as `[{ "file", "origin" }]`. Never rewrite a source: a later check
compares quotations against it word for word.

## Write `.blueprint/brief.md`

In the language the document will be written in, with these sections (either name works):

- `## 目的` / `## Purpose` — what the document is for, in one or two sentences.
- `## 読者` / `## Audience` — who reads it and what they can do after reading.
- `## 要点` / `## Key points` — every point from the answer `points`, plus what the topic needs.
- `## 資料から取る事実` / `## Facts from sources` — each fact the document will state, with the source file
  it comes from. With no sources, write "資料なし — 事実は書き手の知識による" and say which facts need checking.
- `## 決まっていないこと` / `## Open questions` — what you would ask the person. Write "なし" if there is none.

**Do not invent facts.** A number, a name, a date or a quotation that is not in the sources goes under
open questions, not under facts.

## Which style

If the answer `style` is the folder's style, read `STYLE.md` and `chaff.yaml` now and note anything in them
that shapes this document. If they are missing, stop: the check tells the person to make the style first
or to choose chaff's defaults.

## Done when

`node <usecase pack>/checks/brief.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack
folders from your prompt) passes.
