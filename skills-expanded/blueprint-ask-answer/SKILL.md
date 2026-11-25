---
name: blueprint-ask-answer
description: "Answer each question from the named documents only, quoting where the answer is written, or saying plainly that the documents do not say — changing nothing yet."
---

# Answer from the documents

`.blueprint/answers.json` names the documents (`documents`, one path per line), the questions
(`questions`, one per line) and whether to keep the answers (`keep`). The person may not know the
documents well: answer in their language and in plain words.

Change nothing in the repository: this step only reads. Write only under `.blueprint/`; the person reads
the answers before anything is kept.

## How to answer

- **Only from the documents.** Not from general knowledge, not from what such documents usually say. If the
  documents do not answer a question, the answer is that they do not — and what they do say nearby, if it
  helps.
- **Find where it is written.** `chaff tree <document>` (through the base pack's wrapper,
  `sh <base pack>/checks/chaff.sh tree <document>`) shows the document's addresses — articles, sections,
  items — so an answer can say "第4条第2項" or "Section 3.1". Read the whole relevant part, including
  exceptions and definitions elsewhere that change its meaning.
- **When provisions disagree**, say so and quote both rather than choosing one.

## Write `.blueprint/replies.json`

```json
{
  "replies": [
    {
      "question": "委託料はいつまでに払う？",
      "found": true,
      "answer": "検収後30日以内です（第4条第2項）。",
      "citations": [{ "source": "contract.txt", "address": "第4条第2項", "quote": "成果物の検収後30日以内に" }]
    },
    {
      "question": "消費税は含まれる？",
      "found": false,
      "answer": "文書には書かれていません。第4条第1項は「金50万円」とだけ定めています。",
      "citations": [{ "source": "contract.txt", "address": "第4条第1項", "quote": "委託料として金50万円を支払う" }],
      "searched": ["消費税", "税", "税込", "税別"]
    }
  ]
}
```

- `question`: the question exactly as it is in `questions`. One reply per question, none extra.
- `found`: `true` when the documents answer it. Then at least one citation.
- `citations`: `source` is the document's path as `documents` names it; `address` is where; `quote` is
  copied character for character — the check runs `chaff cite` on every one. **Name every cited place in
  the `answer` text** so the person can open the document there: an article or item as the document numbers it
  (第4条第2項, Section 3.1), and a section of a Markdown document by its heading, word for word, in 「」 (「作業用フォルダを信頼しておく」;
  in an English answer, "Getting started") — the check looks for it in those marks.
  chaff's index for a section (`h1.3`) goes in `address` only — it means nothing to the person.
- `searched`: when `found` is `false`, the words and places you looked for.

Also write `.blueprint/replies.md` for the person: each question as a heading, the answer, and the quotations,
each with its place named as in the answer (never `h1.3`).

## Done when

`node <usecase pack>/checks/replies.mjs answer` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the
pack folders from your prompt) passes. It also records a fingerprint of the documents and of `FAQ.md`.
