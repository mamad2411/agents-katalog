---
name: review-page
description: "Build process. Review a finished page of an element against its approved design: screenshots and the element's page guard without a model first, then a verdict in the owner's three grades with named sections — 1 «replace X → Y», 2 «move X and Z», 3 «looks great» — recorded next to the owner's verdict. Load it when the owner asks to assess, review or check a page of an element, a landing after an element agent's work («look at what the agent built», «grade this page»), and before any verdict on whether a page's sections are right. The rule that changes behaviour: a review by a model costs tokens and runs only after the owner's yes with a price counted for this page; the instrument (screenshots, the guard) is free and runs first."
---

# review-page

**Process: build.** A hint, not a law, in HOW you review. Not in the price: a review by a model — only after the owner's yes.

## 1. The instrument — zero tokens, always first

```
node .claude/skills/review-page/shots.mjs --element <element folder> --page en [--page ru] --out <folder>
node .claude/skills/review-page/shots.mjs --url http://127.0.0.1:<port> --page en --out <folder>
```

- `--element` serves the element's installed build on a spare port of `127.0.0.1` (block 25500–25679) and stops it at the end; a turned-off
  element is not turned on. It prints the map «screen → sections» (`kind·address`) and, verbatim, the element's page guard
  (`scripts/check-page-sequence.mjs`).
- A page goes **without the leading slash** (`en`, `ru/docs`): Git Bash rewrites `/en` into a Windows path and the instrument refuses it.
- Screenshots: 1440 and 500 px, by screens of 900 px. The build, not the source: an edit after the build is not on the screenshots.
- A red guard means the verdict is already grade 1 or 2 by its lines; no model is needed for that.

## 2. The price — named before the yes

An image 1440×900 ≈ 1 700 tokens, 500×900 ≈ 600. A page of three screens at 1440 and four at 500 ≈ 7–8 thousand per language; the element's
`DESIGN.md` and the approved test page's screenshots ≈ 3 thousand; the rubric below ≈ 2 thousand; the verdict ≈ 1–2 thousand. It
is an estimate, not a measurement — say so. A second language adds only its screenshots.

## 3. The rubric — what to look at on the screenshots

Three sources, in order:
1. **The element's approved design:** its `DESIGN.md` (composition, rhythm, imagery, «do» and «don't») and the screenshots of the
   approved test page (`prototypes/_pages/<id>/shots/` or the core's Design tab) — does this page speak the same language; a section's
   card (`components/blocks/<block>.card.json`, when the element keeps cards): `use` and `avoid`, the page's mode (a landing persuades).
2. **`craft-floor` of the impeccable skill** (`.claude/skills/impeccable/reference/craft-floor.md` of any element) — «Verify» (contrast,
   spacing, type, motion, states, language) and «Refuse» (identical cards as the skeleton, an eyebrow over the heading, gradient text…).
3. **`critique.md` of the same skill — parts only:** «Design Specificity Verdict» (made for this product or fits any), «Priority Issues»
   P0–P3, the mode rule (on a landing heuristics 7 and 10 are `n/a`). The full critique report is not written. 🛑 Critique wants two
   subagents; they are forbidden here — the review is always «DEGRADED: single-context», and that is its first line.

## 4. The verdict — exactly one of three grades, with named sections

| Grade | When | What is named |
|---|---|---|
| **1** «does not meet the standard — replace X → Y» | the section is not for this place or task; another section of the element, or a new one, is better | `X → Y` by section names |
| **2** «better, but out of place — move X and Z» | the sections are right, their order or neighbours are not | which sections and where |
| **3** «looks great» | no complaint that changes sections | — (small things in a line; they do not lower the grade) |

- A complaint about the **words** inside a right section is not a replacement: it is a line under the verdict.
- The needed section does not exist yet — grade 1 with `X → (new)`; the element's design pass writes it (a task to its agent:
  `npm run task -- <id> "Build process, design: …"`).
- No false complaints: on a right page do not invent a replacement for the sake of a grade.

## 5. The record

```
node .claude/skills/review-page/verdict.mjs add --element <id> --page en --grade <1|2|3> --by model:<model id> \
     [--replace "block-a>block-b"] [--move block-x] [--fine block-y] [--note "…"]
node .claude/skills/review-page/verdict.mjs add … --by owner                      # the owner's verdict — next to it
node .claude/skills/review-page/verdict.mjs add … --copy "<what is spoiled>"      # a review of a spoiled copy — not compared
node .claude/skills/review-page/verdict.mjs list [--element <id>]                # how often the model agrees with the owner
```

The file is `data/node/page-verdicts.jsonl` of the core (outside git). The owner's verdict is recorded in his words in `--note` —
that measures how far the reviewer agrees with his eye. Fixes after a verdict go as a task to the element's agent, not by your hands.

## 6. What the skill does not do

It does not review every build by itself (no timers, no autostart) · it does not edit the page · a review on another model in a separate
context — only by the owner's word.
