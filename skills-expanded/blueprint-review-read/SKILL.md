---
name: blueprint-review-read
description: "Read the named documents closely, address every structure problem chaff reports, find contradictions and ambiguities, and quote the text for each finding — changing nothing yet."
---

# Read the documents and write the findings

`.blueprint/answers.json` names the documents (`documents`, one path per line), what kind they are
(`kind`), what the person is worried about (`focus`) and how far to go (`proposals`). The person may not be
a lawyer or an engineer: write for them in plain words, in their language.

Change nothing in the repository: this step only reads. The documents are the person's originals and stay
exactly as they are — the next check fails if one of them changes. Write only under `.blueprint/`.

## First, what chaff finds by machine

For each document run, from the folder, `sh <base pack>/checks/chaff.sh <document> --experimental --compact`.
Three rules read the document's structure (`chaff tree <document>` shows the addresses they use):

- `dangling-reference` — a reference such as "第12条" or "Section 4.2" to a provision that does not exist;
- `numbering-gap` — articles, paragraphs or items numbered with a gap or out of order;
- `duplicate-definition` — the same term defined twice.

Every one of these must appear in the findings as a finding with a `machine` field
(`{ "rule", "file", "line" }`: the rule and line as chaff reported them, the file as `documents` names it), or in `dismissed` with the same fields and a
`why` — for example, a reference into another law that the document names. Do not claim a machine result
chaff did not report. Other chaff findings (style) are not the subject of this review; leave them.

## Then, what only reading finds

Read the whole of every document, starting with `focus`. Look for:

- **contradiction** — two provisions that cannot both hold (different amounts, periods, parties, conditions;
  one permits what another forbids);
- **ambiguity** — a provision a reasonable reader could apply two ways, a term used but never defined, a
  deadline without a start;
- **omission** — something the rest of the document relies on but never says (who pays, what happens when a
  condition fails).

Report only what the text supports. A finding you cannot quote is not a finding.

## Write `.blueprint/findings.json`

```json
{
  "findings": [
    {
      "id": "payment-deadline",
      "kind": "contradiction",
      "severity": "high",
      "summary": "支払期限が二か所で違う",
      "explanation": "第4条第2項は検収後30日以内、第9条は検収後60日以内としている。どちらで支払えばよいか決まらない。",
      "citations": [
        { "source": "contract.txt", "address": "第4条第2項", "quote": "成果物の検収後30日以内に" },
        { "source": "contract.txt", "address": "第9条", "quote": "検収後60日以内に" }
      ]
    }
  ],
  "dismissed": []
}
```

- `id`: lower-case letters, digits and `-`, unique.
- `kind`: `dangling-reference`, `numbering-gap`, `duplicate-definition`, `contradiction`, `ambiguity`,
  `omission` or `other`. `severity`: `high` (changes who owes what, or makes a provision unenforceable),
  `medium`, or `low` (wording).
- `citations`: at least one. `source` is the document's path exactly as `documents` names it; `address` is
  where it is (use `chaff tree`'s addresses); `quote` is copied character for character from the document —
  the check runs `chaff cite` on every one. For a contradiction, quote both sides.

An empty `findings` array is a valid answer when nothing is wrong. Say so; do not invent findings.

## Done when

`node <usecase pack>/checks/findings.mjs read` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the
pack folders from your prompt) passes. It also records a fingerprint of each document, which the next step
uses to prove the originals were not changed.
