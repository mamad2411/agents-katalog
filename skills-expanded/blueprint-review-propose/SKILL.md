---
name: blueprint-review-propose
description: "Propose a fix for each finding and write a corrected copy of each document beside the original, leaving the original untouched."
---

# Propose fixes

The person has read the findings and approved going on. Read `.blueprint/findings.json` and
`.blueprint/answers.json`.

**Never change a document under review.** The check compares each one with the fingerprint the read step
recorded and fails on any difference.

If `proposals` is `指摘だけ` (findings only), there is nothing to write: run the check and stop.

## For each finding

Add a `proposal` string to it in `.blueprint/findings.json`: what to change, in the document's own words —
the replacement text where it is short, and which side of a contradiction you chose and why. Where the right
answer is a business decision (which of two amounts is meant), say so and propose the wording for each
choice rather than choosing silently.

## The corrected copies

For each document a finding is about, write a copy beside it named `<name>.proposed<extension>` (`contract.txt` →
`contract.proposed.txt`) with every proposal applied. A document with no finding needs no copy. Keep everything else as it is — numbering, headings,
the order of provisions — so the person can compare the two files line by line. Do not polish wording the
findings do not name.

The copy must not have more structure problems than the original: run
`sh <base pack>/checks/chaff.sh <copy> --experimental --compact` and fix any new `dangling-reference`,
`numbering-gap` or `duplicate-definition` (renumbering one article moves every reference to it).

## Done when

`node <usecase pack>/checks/findings.mjs propose` passes.
