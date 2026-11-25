---
name: blueprint-write-draft
description: "Write the next part of the outline to the house style, check it with chaff, cite what came from the sources, and mark it done."
---

# Write one part

Take the **first** part in `.blueprint/outline.json` whose status is `"todo"`. Write that part only; the
next round writes the next one.

## Before writing

Read `.blueprint/brief.md`, the part's `points`, and — when the folder has one — `STYLE.md`. Read the parts
already written, so terms, tone and numbering continue rather than restart.

## Write

- Write the part to its `file`, beginning with its title as a heading.
- Follow `STYLE.md`: voice, sentence endings, terms, structure. It is the part of the style a machine
  cannot check, and the reason it exists.
- Cover every one of the part's `points`.
- **State a fact only if it is in the brief's facts from sources**, or is common knowledge. Anything else is
  an open question for the report, not a sentence.

## Cite what came from the sources

For each sentence that states something taken from a source, record the source passage in
`.blueprint/citations/<part id>.json`:

```json
[{ "source": "annual-report.md", "address": "h1.2", "quote": "売上は前年比 12% 増えた" }]
```

`address` is where the passage sits in the source's tree: `sh <base pack>/checks/chaff.sh tree
.blueprint/sources/<file>` prints it (a heading's `h1.2`, an article's `3.2`). `quote` is the source's own
words, copied, not your paraphrase. The check runs `chaff cite` on each source.

## Check it yourself

`sh <base pack>/checks/chaff.sh <the part's file>` must report no warning or error. Fix the text, not the
style. Set a finding aside only in one of two cases, by adding it to the part in `.blueprint/outline.json`:

```json
{ "id": "intro", "file": "01-intro.md", "status": "done",
  "dismissed": [{ "rule": "max-sentence-length", "line": 8, "because": "meaning", "why": "資料の一文をそのまま引用している" }] }
```

- `"because": "wrong"` — chaff misread the text (a heading it took for a sentence, a name it took for jargon).
  Each one becomes a draft report to chaff in the report step.
- `"because": "meaning"` — chaff is right, but fixing it would change what must stay exact (a quotation).

`rule` and `line` are exactly as chaff reports them now, one dismissal per finding; the check refuses a
dismissal chaff does not report.
`why` is one line the person can judge. Never silence a rule in `chaff.yaml` or with `stet` to get past it.

Then set the part's status to `"done"`.

## Done when

`node <usecase pack>/checks/parts.mjs verify` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the
pack folders from your prompt) passes: every done part is written, raises no finding it did not set aside, and quotes its
sources faithfully. Run `verify`, never `progress`: `progress` is the executor's check at the end of the
round and records how many parts were done, so running it yourself makes the real check fail.
