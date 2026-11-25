---
name: blueprint-verify-report
description: "Report every problem the machine found in the extracted facts, in plain words, with where it is and how to fix it."
---

# Report what the machine found

A person has read the extracted table in `.blueprint/facts.json`. If they asked for a correction, make it and
run the extract check again before this step, because the report step refuses facts changed since that check.

Run `node <usecase pack>/checks/report.mjs` once first. It decides by machine what is wrong with
`.blueprint/facts.json` and writes the list to `.blueprint/verification.json`. It fails until the report
exists. The machine's rules are these:

- `weekday-mismatch`: the weekday written beside a date is not that date's weekday.
- `end-before-start`: an event ends before it starts.
- `out-of-order`: an event comes later in the document but earlier in time than the one before it.
- `overlap`: on one day, an event starts before the previous one ends.
- `total-mismatch`: a total is not the sum of its parts. Its `detail` says which way: `writtenIs` is
  `"more"` when the written total is larger than the sum of the parts, `"less"` when smaller, by `by`. Say it
  that way round (「書かれた合計は、内訳を足した額より 500円 多い」) — never work the direction out yourself.
- `unit-mismatch`: a total and its parts are in different units.
- `product-mismatch`: an amount is not the product it claims to be (単価 × 数量, 小計 × 税率), even allowing for
  rounding to the digits it is written to. `detail` gives `written`, the true `product`, and `writtenIs` / `by` the
  same way as a total. Say that way round, and propose the product; for a tax, say the fraction may be rounded
  either way (1,234円 or 1,235円) and that the issuer decides.

You cannot add or drop a problem. Explain each one; if you think one is not really wrong (an overnight
leg read as ending before it starts, say), say so under that problem, but still name it.

Write `.blueprint/verify-report.md` for the person, in their language and in plain words:

- `## 見つけたこと` / `## Problems`: every problem by its `id` from `verification.json`. Say what is wrong in
  the document's own words, quote where it is (the event's or amount's quotation, and the place named as the document does — a
  section's heading in 「」, "…" in an English report — not chaff's index such as `h1`), and propose a fix (the
  weekday that date really is, the sum the parts really make). When there are none, say that the machine
  found none.
- `## 確かめたこと` / `## What was checked`: how many events, amounts, totals and products were extracted. Each value
  was found in its quotation, and each quotation in the document (`chaff cite`). Then name the rules that ran.
- `## 確かめきれなかったこと` / `## Not checked`: what a machine cannot confirm. That the extraction is
  complete; a product the document gives no factor for (a line with no quantity); travel time between places; time zones; dates written as `MM-DD` because no year was known (their
  weekdays were not checked); prices, availability and anything outside these files.

## Done when

`node <usecase pack>/checks/report.mjs` passes. The originals are unchanged.
