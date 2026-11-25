---
name: blueprint-summarize-report
description: "Write the checked summary up for the person: the summary, where each sentence comes from, and what was left out."
---

# The summary, finished

`.blueprint/summary.json` is the summary the person approved. Write `.blueprint/summary-report.md` for them, in
their language and in plain words:

- `## 要約` / `## Summary` — every sentence of the summary, **word for word** and in its order (the check looks
  for each one). A short heading line or paragraph breaks may be added; the sentences themselves may not be
  reworded here.
- `## 出どころ` / `## Sources` — for each sentence, the document and the place it comes from, named as the
  document does (第4条, a section's heading in 「」 — "…" in an English report — never chaff's `h1.3`), with the
  quotation.
- `## 省いた部分` / `## Left out` — when anything was left out: each part by its name, with the reason. Write the
  name in 「」 ("…" in an English report) or set off by punctuation (「支払い」: 理由, 第4条（委託料）): the check looks
  for each name as a whole word, so 「支払いは」 or a name inside a longer word is not counted.
- A line saying what was checked by machine (every quotation is in its document, no part was dropped silently,
  every number is in a quotation) and what was not (whether each quotation really supports its sentence is a
  reading, which the person approved).

## Done when

`node <usecase pack>/checks/report.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set) passes.
