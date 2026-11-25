---
name: finding-rewriter
description: Rewrites each auto-extracted Finding cell in a Fetchproof project's research/EVIDENCE.md into a real claim - what the cached page establishes, with the number or rule that proves it and a word-for-word [quote: ...] from the capture - keeping the Raw cell pointing at the capture. Use on a collector after research.mjs collects, when preflight reports quote or finding problems, or when the user asks to rewrite or review the findings.
---

# Finding rewriter

`research.mjs` fills each `Finding` cell with an extracted sentence. It is a pointer into
the page, not a claim. Rewriting it is the second review step of phase 1.

## Each row

1. Open the capture the `Raw` cell names, under `research/raw/`.
2. Write what the page **establishes** for the unknown it was collected for - the
   number, the rule, the field, the limit - in your own words, concretely.
3. Add the sentence it rests on as `[quote: ...]`, copied from the capture **word for
   word, on one line** of the capture. The gate checks it occurs there (ADR-0087); a
   sentence that wraps across two lines in the capture fails - quote the part on one line.
4. Say what the page does **not** establish, when a reader would assume it does.
5. Never put a `|` in the cell; it breaks the table.

## Rules

- Never edit the capture, the `Raw` cell, or `research/raw/.fetches.jsonl`. An edited
  capture fails the gate and blocks every commit.
- A thin or client-rendered capture (`raw-thin`) is not cited for the fact. Say so in its
  Finding, and collect the page that owns the fact as text.
- A claim the page does not support is not written, however likely it is.
