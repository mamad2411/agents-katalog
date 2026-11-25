---
name: blueprint-summarize-summarize
description: "Summarize the named documents to the agreed length, one sentence at a time, each backed by quotations, citing every part or leaving it out with a reason — writing .blueprint/summary.json and changing no document."
---

# Summarize, sentence by sentence

`.blueprint/answers.json` names the documents (`documents`, one path per line), how long the summary may be
(`length`), who reads it (`reader`, may be empty) and what they most want to know (`focus`, may be empty). Read
every document in full. The person may not be an engineer: say what you do in plain words.

Change nothing in the repository: the documents stay exactly as they are. Write only under `.blueprint/`.

## The parts a summary answers for

Run `sh <base pack>/checks/chaff.sh tree <file> --format json` on each document. Its **parts** are its articles
(`kind` `article`) when it has any; otherwise its sections at the first level with more than one (under a single
title heading, the sections below it). Every part is either cited by some sentence of the summary or left out on
purpose, with a reason the person can judge — never dropped silently.

## Write `.blueprint/summary.json`

```json
{
  "sentences": [
    {
      "text": "経理部の確認が済んだ申請は、毎月25日に給与口座へ振り込まれる。",
      "citations": [{ "source": "keihi.md", "address": "h1.3", "quote": "毎月25日にまとめて給与口座へ振り込みます" }]
    }
  ],
  "omitted": [{ "source": "keihi.md", "address": "h1.4", "why": "例外の手続きで、この読み手には要らないため" }]
}
```

- **One claim a sentence**, in the reader's language and plain words, in the order that serves the reader —
  `focus` first when it names something.
- **Every sentence has at least one quotation** that says what the sentence says: `source` as `documents` names
  it, `address` from the tree (the paragraph or item the words are in, or the part itself), `quote` copied
  character for character. The check runs `chaff cite` on every one.
- **A number is copied, never made.** Every number a sentence states must appear in one of its quotations (or in
  the name of a place it cites, such as 第4条): the check refuses any other. Do not add up, convert or round.
- **The length** is the most sentences `length` allows (短く 5, ふつう 10; くわしく has no limit). When the parts
  outnumber the sentences, one sentence may cite several parts, or a part the reader does not need may be left
  out in `omitted` — with a reason.

## Done when

`node <usecase pack>/checks/summary.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack folders
from your prompt) passes. It writes `.blueprint/summary.txt`, the summary with where each sentence comes from,
which the person reads before the report.
