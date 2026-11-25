---
name: blueprint-glossary-collect
description: "Collect the terms the documents define, the ways each word is spelled, and the jargon, each quoted where it was found, into .blueprint/glossary.json — changing no document."
---

# Collect the terms

`.blueprint/answers.json` names the documents (`documents`, one path per line) and whether what you find goes into
the folder's `chaff.yaml` (`write`). Read every document in full. The person may not be an engineer: say what you do
in plain words.

Change nothing in the repository: the documents stay exactly as they are, and `chaff.yaml` is the next step's.
Write only under `.blueprint/`.

## What to collect

- **Every term a document defines.** `sh <base pack>/checks/chaff.sh tree <file> --format json` shows chaff's
  reading: every node of `kind` `definition` names a defined term in `attrs.term` (「社員」とは…, (以下「甲」という)).
  Each must be in the glossary with its definition from that document; the check refuses the glossary otherwise.
  Add any definition chaff missed.
- **A term defined more than once**, in one document or across them — list every definition. That two definitions
  disagree is exactly what the person needs to see.
- **A word spelled more than one way** (サーバー / サーバ, ユーザー / ユーザ, 問い合わせ / 問合せ): every spelling
  found, each quoted, and the one to use in `preferred` — the one the documents use most, unless a definition or
  the person's style says otherwise; say why in `note`.
- **Jargon**: a word only understood inside the organisation (`jargon: true`).

## Write `.blueprint/glossary.json`

```json
{ "terms": [
  { "term": "社員",
    "definitions": [
      { "source": "kitei.txt", "address": "2", "quote": "「社員」とは、会社と雇用契約を結んでいる者をいう" },
      { "source": "tebiki.md", "address": "h1.1", "quote": "「社員」とは、正社員と契約社員をいいます" } ],
    "spellings": [{ "spelling": "社員", "citations": [{ "source": "kitei.txt", "address": "3", "quote": "社員は、テレワークをする日の前日までに" }] }] },
  { "term": "サーバー",
    "spellings": [
      { "spelling": "サーバー", "citations": [{ "source": "tebiki.md", "address": "h1.2", "quote": "会社のサーバーに接続できたら" }] },
      { "spelling": "サーバ", "citations": [{ "source": "kitei.txt", "address": "4", "quote": "VPN を通してサーバに接続する" }] } ],
    "preferred": "サーバー", "note": "定義の条がサーバーと書くため" }
] }
```

Every quotation is copied character for character from the place its `address` names; the check runs `chaff cite`
on every one. A definition's quotation contains the term; a spelling's quotation contains that spelling.

## Done when

`node <usecase pack>/checks/glossary.mjs collect` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack
folders from your prompt) passes. It writes `.blueprint/glossary.txt`, which the person reads before the next step.
