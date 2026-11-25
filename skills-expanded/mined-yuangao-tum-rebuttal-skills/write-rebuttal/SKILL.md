---
name: write-rebuttal
description: Write conference/journal author-response rebuttals that clarify and convince, following Parikh–Batra–Lee's "How we write rebuttals" method (two-audience mindset, itemize→brain-dump→draft→revise, 18 tactics, the neutral-third-party test). Use when responding to peer reviews, writing an author response / rebuttal / reviewer reply for NeurIPS, ICLR, ICML, CVPR/ICCV/ECCV, AAAI, ACL/ARR/EMNLP, or any venue, planning rebuttal experiments, or when the user says "rebuttal", "author response", "respond to reviewers".
---

# Write Rebuttal

Distilled from Devi Parikh, Dhruv Batra & Stefan Lee, *How we write rebuttals*
(https://deviparikh.medium.com/how-we-write-rebuttals-dc84742fece1).

A rebuttal exists to **clarify and convince** — it is one stage in a deliberative
scientific process, not a fight to win. Optimize it for the reader, not for venting.

## The one idea that governs everything

**Two audiences, and beginners forget the second one:**

1. **Reviewers** — read your paper, may have forgotten details. Goal: clarify doubts,
   correct misunderstandings, push back on mischaracterizations, incorporate feedback.
2. **Area Chair / meta-reviewer** — likely has *not* read your paper closely and won't
   re-read it. Goal: show good-faith effort, give a fair summary, make it obvious each
   concern was addressed, flag bad-faith reviewing, and **help them decide.**

> Most new researchers write only for (1). Writing for (2) is what moves decisions.
> Think of it like debate: you convince the *judges* (AC), not your opponents.

**The acceptance test for every response — the "neutral third-party" test:**
Could someone who has *not* read your paper or the reviews tell, from your rebuttal
alone, that the concern was addressed? If not, rewrite it (self-contained; Tip 8).

## Process (do these in order)

1. **Itemize** — put every reviewer comment/question/concern in a spreadsheet, one row
   each, columns per reviewer. Do this *first, ASAP*: it guarantees nothing is missed,
   surfaces shared concerns to consolidate, and **identifies needed experiments early**
   while there's still time to run them.
2. **Brain-dump** — rough responses in the sheet, no style/length worry. Collaborative.
3. **Draft** — turn the consensus into concise responses covering every point.
4. **Revise** — reread the reviews, check completeness, prioritize the majors, fit the
   space limit. Run the neutral-third-party test on each response.

See [references/rebuttal-skeleton.md](references/rebuttal-skeleton.md) for a ready
structure (summary → common concerns → per-reviewer → note to AC), micro-templates,
and two AC "dashboard" summary tables.
[assets/rebuttal-template.tex](assets/rebuttal-template.tex) is the compilable
LaTeX implementation — use it only where free-form PDF responses are accepted.

## The 18 tactics (apply while drafting)

Full detail + examples in [references/eighteen-tips.md](references/eighteen-tips.md).
The load-bearing ones:

- **Start positive** (1) — open with a short recap of the praise; don't let strengths be forgotten.
- **Order by strength, not by reviewer** (2) — lead with the *biggest concerns you have good answers for*; trail minor/weaker points.
- **Quote → direct answer → detail** (3) — quote the concern, answer **Yes/No/one line in bold** first, then elaborate.
- **Stats speak louder than words** (12) — whenever you disagree with a reviewer, back it with a number, not an argument. Ask "can I establish this with data?"
- **Don't promise, *do*** (13) — compute the number/analysis *now* and put it *in the rebuttal*; then say you'll fold it into the paper. Never leave "we will add X" as the whole answer.
- **Get credit for what's already there** (9) — if they asked for something in the paper, cite the line/section *and restate it*.
- **Be transparent** (15) — venue bars new experiments? no clean intuition? out of GPUs? result is null? **Say so honestly** and reframe — do not overclaim.
- **Answer the intent, not just the literal question** (5), be **self-contained** (8), **consolidate shared concerns** (10), **thank real effort** (17), and **remember the humans** (18) — seek common ground unless a reviewer is bad-faith (16).

## Applying it to rebuttal *experiments*

The guide shapes what you run, not just how you write:

- **Itemize first (Step 1)** to derive the experiment list from concerns, then map each
  experiment to the exact sentence/slot it will fill.
- **Tip 2 + 13**: prioritize experiments that will *reliably* yield a clean, defensible
  number inside the response window over high-variance gambles. A promised experiment
  that doesn't land is worse than a transparent limitation (Tip 15).
- **Tip 12**: prefer designs that end in a statistic (effect size, CI, p-value, a
  baseline delta) — that is the currency of a rebuttal.
- **Tip 14** (be receptive): when a reviewer proposes a baseline/ablation, *try it* —
  "maybe it will work" — rather than arguing why it wouldn't.
- **Never pre-write the outcome.** If a response sentence already asserts a result
  ("the increase is significant") before the experiment is run, that violates Tips 13
  and 15 — fill it only with the computed value, or reframe to what the data supports.

## Anti-patterns (auto-reject in review)

- A response that fails the neutral-third-party test (needs the paper to make sense).
- "We will add / we plan to" with no number in the rebuttal itself (violates 13).
- Ordered reviewer-by-reviewer with the weakest answer first (violates 2).
- Arguing a point you could have measured (violates 12).
- Combative tone, litigating instead of clarifying (violates 4, 18).
- Silent overclaim of a result the data doesn't yet support (violates 13, 15).
- Ignoring the AC entirely — no decision-oriented summary (the core miss).

## Optional check

`python scripts/lint_rebuttal.py <rebuttal.tex|.md>` flags promise-language
("we will add", "in the final version"), unfilled placeholders (`\Rtodo`, TODO,
`[\ldots]`), outcomes asserted next to unfilled slots, a missing AC section, a
missing opening thanks, and the absence of any statistics. Advisory only —
judgment still yours.
