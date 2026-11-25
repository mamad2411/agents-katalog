---
name: reviewer
description: Simulated ARR review of the paper along the current official review form, plus a guidelines check. Writes review.md and report items.
disable-model-invocation: true
argument-hint: "[reviewer persona or focus, e.g. 'skeptical about the evaluation']"
---

This skill is ARR-only. When `paper.config.json` has `venue` `semeval`, say that SemEval has no ARR review form and stop.

Review the paper as an ARR reviewer would, so the authors see the weaknesses before real reviewers do. The review form and reviewer guidelines change between cycles; every run fetches them.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

## 1. Fetch the form

```
PK guidelines reviewer
```

It downloads the ARR review form and reviewer guidelines into a temp folder. On ⚠️: tell the user what is missing and stop, since a review against a remembered form would mislead. Read both in full: the form fields, the score scales with their descriptions, and what the guidelines tell reviewers to do and to avoid (the guidelines list common unhelpful review patterns; a useful review avoids them too).

## 2. Context

Ask with AskUserQuestion what changes the review and is not in the project: the track or area the paper is submitted to, long or short, and whether it is a resubmission. For a resubmission, ask for the previous reviews and meta-review (offer `reviews/`): a reviewer of a resubmission checks whether the earlier weaknesses were addressed, so the review must do the same.

## 3. Compliance first

Load and run the `guidelines-check` skill, carrying over the answers from step 2 so it asks only what is still open. Its findings (including the Responsible NLP checklist) go to `report.md` as usual and inform the review's soundness and ethics fields.

## 4. Read like a reviewer

Read the whole paper in reading order, including appendices, once without writing. Then review it:

- What is the claim, and does the evidence carry it? Baselines, ablations, statistical significance, data splits, contamination, number of runs.
- Is it reproducible from the paper (hyperparameters, prompts, data, code)?
- Related work: is the closest prior work present? Search with the `acl-anthology` and `arxiv` skills for work the paper should compare to, and read what you name (the `literature` skill) before saying the paper misses it.
- Clarity: could a reader in the area reimplement it?

Apply the persona or focus from the argument if one was given; otherwise review as a competent, fair reviewer from the paper's area.

## 5. Write review.md

Fill every field of the fetched form in `review.md` in the project root, in the form's order and with its field names: summaries, strengths, weaknesses, comments, every score with a one-line justification using the scale's own wording. Each weakness names the place in the paper and what would fix it. Where a weakness rests on a reviewer guideline or a form criterion, name its identifier and the document's URL as `PK guidelines` prints it. Overwrite an earlier `review.md` only after asking; otherwise number it (`review-2.md`).

## 6. Report items

Each weakness that the authors can fix before submission becomes an item in `report.md`, category `Review`, severity by how much it would move the score, with **Rule:** where the weakness rests on a guideline. Weaknesses that need new experiments are 🔴 or 🟠 with the experiment named.

Report in chat: the overall assessment with its score, the three weaknesses most likely to sink the paper, and what fixes them.
