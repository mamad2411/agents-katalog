---
name: blueprint-glossary-apply
description: "When the person asked, put the glossary's spellings and jargon into the folder's chaff.yaml without losing what it had; then write the glossary up for them."
---

# Put it into chaff.yaml, and report

`.blueprint/glossary.json` is the glossary the person approved. The documents stay exactly as they are.

## chaff.yaml — only when `write` is 「このフォルダの chaff.yaml に入れる」

Add to the folder's `chaff.yaml` (create it if there is none, with the documents' `language`, and a `genre` from
`chaff genres`):

```yaml
prefer:                # the spelling not to use: the one to use
  サーバ: サーバー
  ユーザ: ユーザー
jargon:                # words only understood inside
  - 横展開
rules:
  preferred-term: normal
```

- One `prefer` line for every spelling of a term other than its `preferred`.
- `jargon` lists every term marked `jargon: true`.
- `preferred-term` is experimental: it runs only when named under `rules`.
- **Creating the file for documents of different kinds** (a policy and its guide), give each kind its genre: the
  kind most documents are goes in `genre`, and each other document gets its own under `by_path`, so a guide is not
  measured as a policy:

  ```yaml
  genre: legal/statute
  by_path:
    - files: ["tebiki.md"]
      genre: docs/manual
  ```

  `files` are globs relative to `chaff.yaml`. An existing file's `genre` and `by_path` are the person's: keep them.
- **Keep everything the file already had.** Add to its `prefer`, `jargon` and `rules` rather than replacing them;
  the check refuses a line of the old file that is gone.

The check then runs chaff on every document that still writes an avoided spelling, and expects `preferred-term` to
report it: that is the proof the file works. When `write` is 「入れない」, do not touch `chaff.yaml` at all.

## The report

Write `.blueprint/glossary-report.md` for the person, in their language and in plain words:

- `## 用語集` / `## Glossary` — a table: each term (the check looks for every one), its definition and where, the
  spellings found and the one to use, and whether it is jargon.
- `## 二重定義` / `## Defined twice` — when any term is defined more than once: each such term, every definition
  quoted with its place, and what differs. Deciding which is right is the person's.
- `## 確かめたこと` / `## What was checked` — every quotation is in its document, every term the documents define
  is in the glossary, and, when `chaff.yaml` was written, what went into it and that chaff now reports the spellings
  still in the documents. Say that the documents were not changed: making them use one spelling is 「文書を整える」's
  work, which will follow this `chaff.yaml`.

## Done when

`node <usecase pack>/checks/glossary.mjs apply` and then `node <usecase pack>/checks/report.mjs` (with
`BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set) pass.
