---
name: blueprint-polish-polish
description: "Polish the next file on the list to the house style without changing what it says, keep the original, and check it."
---

# Polish one file

Take the **first** file in `.blueprint/polish.json` whose status is `"todo"`. Polish that file only; the
next round takes the next one. When the list is empty, the survey found nothing to polish: change nothing
and stop.

## First, keep the original

Copy the file to `.blueprint/originals/<the same path>` before changing anything (create the folders).
The check compares against it, and it is how the person undoes a change.

## What may change, and what may not

The document must still **say the same thing**. What changes is how it is said.

- **May change**: wording, sentence length and endings, spacing, spelling to the team's terms, splitting a
  long sentence or paragraph, removing padding.
- **May not change** — the check compares these with the original and fails on any difference:
  - the headings, in order and word for word (other documents link to them);
  - the articles, sections and items chaff reads as the document's structure (`chaff tree`), so a
    reference such as "第3条第2項" or "Section 4.2" still points at the same place;
  - code blocks, byte for byte;
  - link targets.
- Never add a fact, a number, a date or a name that is not in the original. Never drop one.

Follow `STYLE.md` when the answer `scope` includes the guide; otherwise, and when there is no `scope`, fix only what chaff reports.

## Check it

`sh <base pack>/checks/chaff.sh <the file>` — with the same `--genre` as the survey when the answer `kind`
gives one (see `<usecase pack>/kinds.json`), and `--show-baseline` when the answer `shelved` asks for the shelved
findings too — must report no warning or error, except the ones you set aside.
Set a finding aside — never change the meaning to satisfy a rule — in one of two cases, by adding it to the
file's entry in `.blueprint/polish.json`:

```json
{ "file": "guide.md", "before": 4, "status": "done",
  "dismissed": [{ "rule": "max-sentence-length", "line": 12, "because": "meaning", "why": "条文の引用で、切ると原文と違ってしまう" }] }
```

- `"because": "wrong"` — chaff misread the text (a heading it took for a sentence, a name it took for jargon).
  Each one becomes a draft report to chaff in the report step.
- `"because": "meaning"` — chaff is right, but fixing it would change what the document says.

Only a file you mark `"done"` may set findings aside. `rule` and `line` are exactly as chaff reports them now,
one dismissal per finding (two findings of a rule on one line need two); the check refuses a dismissal chaff does not report,
so update the line if your other edits moved it. `why` is one line the person can judge. Set aside only what
you cannot fix — the report shows every one to the person.

## Then read it for its kind

When the answer `kind` names a kind whose genre has viewpoints in `<usecase pack>/viewpoints.json`
(`genres` lists them; `viewpoints` says what each looks for, and whether you may fix it), read the file
for each of them once chaff is clean, and record every one in `.blueprint/viewpoints.json`, under the
file's path:

```json
{ "report.md": [
  { "id": "stacked-hedging", "verdict": "fixed", "quote": "増加する可能性があると考えられます" },
  { "id": "actionable-ask", "verdict": "writer", "quote": "ご確認をお願いします",
    "note": "誰に、いつまでに確認してもらいますか" },
  { "id": "conclusion-first", "verdict": "ok" }
] }
```

- `ok` — nothing to do. A `quote` is optional; one you give must be in the file.
- `fixed` — only for a viewpoint whose `fix` is `may`, and only when the fix adds nothing and drops no fact
  (removing a filler sentence, keeping one hedge of two). A fix takes words out; it never puts in a sentence
  of your own. When taking the sentence out would leave a heading with nothing under it, it is `writer`. `quote` is what was there, copied from the
  original; it must no longer be in the file.
- `writer` — everything else: a fix that would add a fact (who, by when, a source, a missing section), move
  a heading, or change what the writer claims. `quote` is the place in the file, word for word; `note` is
  the question to ask them, in their language. Do not guess the answer into the document.

The check refuses a missing or unknown viewpoint, a `fixed` the catalog does not allow, and a quotation that
is not where it says.

If the file cannot be polished at all without changing what it says, restore it from the original, set its
status to `"skipped"` and write a `note` saying why. Otherwise set it to `"done"`.

## Done when

`node <usecase pack>/checks/targets.mjs verify` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the
pack folders from your prompt) passes. Run `verify`, never `progress`: `progress` is the executor's check at
the end of the round and records how many files were finished, so running it yourself makes the real check
fail.
