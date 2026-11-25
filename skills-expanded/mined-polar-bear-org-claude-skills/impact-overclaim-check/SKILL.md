---
name: impact-overclaim-check
description: Checks a draft training report claim by claim before it is sent, producing a numbered list of every claim with the checks it fails, its strength and a verdict, a rewrite for each weak claim and a list of what must come out. Use for "run impact-overclaim-check", "check my training report before I send it", "am I overclaiming", "can I say the training caused this", "review my impact report", "fact check L&D report", "is this claim supported", "sanity check training results", part of the Claude Guide for Training Impact Pack by 90n.
---

# Overclaim Check

## When To Use
The report reads well and you are about to send it. Use this on any finished draft (a one-pager, a quarterly page, a briefing, an email with results in it) when the question is which sentences would not survive a reader from finance asking "how do you know?".

## When Not To Use
Not for building the argument: Training Contribution Analysis works out what the evidence can support, and Before-and-After Results Table computes the figures. This check only tests how a finished draft describes them. A draft with no figures and no claims does not need it.

## Inputs
- The draft, pasted in full, with who will read it and when it goes.
- The evidence behind it: the results table, the agreement, the reasoning about other explanations. Group figures only.
- The minimum reporting group, and how many data points you require before you will call something a trend.
If you have none of this beyond the draft, I start from the draft alone, mark every claim whose evidence I have not seen as "evidence not seen", and mark the output as a first draft.

## Approach
The tests come from "Communicating quality, uncertainty and change", guidance from the UK Government Analysis Function: say "estimate" where it is one, give absolute and relative change together, warn when numbers are too low for a trend, replace vague cautions with what can and cannot be concluded. Each claim then gets one of this guide's three strengths: shown, suggested or unknown. The failure this prevents is one sentence, "the programme drove the improvement", read aloud by someone who knows a new tool went live the same month; after that, nobody trusts the careful pages either. A second reader paid to doubt is cheaper before sending than after.

## Workflow
1. I ask three questions at once: who reads this draft and when it goes; which evidence files you are pasting with it; and the minimum reporting group and the fewest points you accept for a trend (you set both).
2. List every claim, numbered, in the draft's own words with where it sits: any sentence that asserts a result, a cause, a comparison or a trend. Headlines, slide titles and chart captions count; they are where claims grow.
3. Test each claim against eight checks: (A) a causal verb (caused, led to, drove, thanks to, resulted in) with no isolation method named; (B) a percentage on a small group or with no group size; (C) a missing denominator; (D) a relative change with no absolute change; (E) a benchmark, an average or a quote with no source; (F) a figure with no voucher; (G) a trend from too few points; (H) "typical" drawn from chosen cases.
4. Give each claim its strength and a verdict. Shown: a before and an after from a named source, a comparison or another named isolation method, and a voucher. Suggested: a change that fits the chain but with no comparison, other explanations open, or people's own reports only. Unknown: no data, a group under the minimum, or no baseline. Verdict: keep, rewrite or remove.
5. Rewrite each weak claim with the word that matches its strength: "the figures show", "the evidence suggests", "we do not know whether". A rewrite makes a claim smaller or more exact; it never borrows strength from a neighbouring sentence.
6. Replace vague cautions ("results should be read with care") with what the reader can and cannot conclude. Flag any sentence that turns evidence about the programme into a statement about a person or a named team: those are removed, not reworded.
7. Close with the list of what must come out before sending, and what evidence would let a removed claim back in. The check adds no claim, figure or source of its own.

## Output Format
```markdown
# Overclaim Check
Draft checked: [title, version] · Reader: [role] · Goes on: [date] · Evidence seen: [files / none] · Evidence not seen, and who holds it: [list] · Minimum reporting group: [you set] · Fewest points for a trend: [you set]
## Claims
| # | Claim as written | Where | Checks failed (A to H) | Strength | Verdict |
|---|---|---|---|---|---|
| 1 | [sentence from the draft] | [page, slide or line] | [letters / none] | [shown / suggested / unknown / evidence not seen] | [keep / rewrite / remove] |
## Rewrites
| # | As written | Rewritten | What would let the stronger wording back in |
|---|---|---|---|
| [#] | [sentence] | [sentence at its true strength] | [evidence, and who could get it] |
## Vague cautions replaced
| As written | What the reader can conclude | What the reader cannot |
|---|---|---|
| [caution] | [statement] | [statement] |
## Must come out before sending
| # | What | Why |
|---|---|---|
| [#] | [claim, figure, benchmark or quote] | [no source / no voucher / group under the minimum / about a person] |
## Decision
[Name, role] accepts or overrules each verdict and sends the report by [date]; any claim kept against a "remove" verdict carries [name]'s initials and the reason.
```

## Done When
- Every result, cause, comparison and trend in the draft is on the numbered list, titles and captions included.
- Each claim has the checks it failed, a strength and a verdict.
- Every "rewrite" has a new sentence, and every "remove" is on the final list with its reason.
- No sentence in the output says more than the sentence it replaces.

## Quality Bar
- The draft's own words are quoted exactly; a claim is never paraphrased into something easier to defend.
- "Evidence not seen" is a verdict of its own. I do not assume a figure is sound because it looks plausible.
- Thresholds are yours: the minimum group and the points for a trend are never supplied.
- The check removes claims and never adds one; whatever survives has a source, a voucher and a strength, and a named person sends the report.

## Next
Run impact-evidence-review-meeting (Evidence Review Meeting) to take the checked evidence into next period's decisions.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
