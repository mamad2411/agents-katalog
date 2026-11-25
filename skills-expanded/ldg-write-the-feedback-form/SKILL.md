---
name: ldg-write-the-feedback-form
description: Writes the end-of-programme feedback form with four to six items on what predicts use, answer options that describe a concrete state, open prompts on barriers, and an aggregate summary template that rates the programme, never the trainer. Use for "run ldg-write-the-feedback-form", "training evaluation form", "training feedback survey", "post-training survey questions", "smile sheet", "course evaluation questions", "end of course survey", "everyone loved it and we learned nothing", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Write the Feedback Form

## When To Use
The smile sheet says everyone loved it and tells you nothing. The averages are high, nothing in them points to a change, and nobody can say whether people will use any of it on Monday. Run this before the last day of a programme to answer one question: did people leave with something they can and will apply, and what do they expect to stand in the way?

## When Not To Use
If nobody has agreed what the programme should change, a better form will not settle it: run Plan the Evaluation first. If the sponsor wants to know whether people used it at work, a form filled on the last day cannot say: run Check Use on the Job some weeks later.

## Inputs
- The programme's objectives, or the critical behaviours from your evaluation plan
- The form you use today, if there is one, and how it reaches people (paper, your LMS, your survey tool)
- The minimum group size below which you do not report results
If you have none of this, I start from the programme title and its objectives as you remember them, and mark the output as a first draft.

## Approach
The form follows LTEM, the Learning-Transfer Evaluation Model (its originator's public page): eight tiers from attendance to the effects of transfer, where learner perceptions sit at tier 3 and cannot validate learning on their own. So the form asks about what predicts use, and each answer option is a state a person can recognise in themselves, not a point on an agreement scale. The failure it prevents: a room gives the day top marks because lunch was good and the facilitator was funny, the report says "highly rated", and the one exercise nobody could follow runs unchanged next quarter.

## Workflow
1. Ask three questions: what should people be able to do after this programme, which changes are you free to make from the answers, and what is the minimum group size for reporting?
2. Audit the current form, item by item. Rates the trainer: remove. Measures satisfaction: keep one at most. Predicts use: keep and sharpen. An item you could not act on goes, however long it has been on the form.
3. Write four to six closed items, one each on relevance to the job, comprehension, realistic practice, confidence to apply, and the support people expect back at work. Fewer items answered with thought beat a long form ticked on the way out.
4. Write the answer options as concrete states ("I could do this now without help", "I would need to practise with someone first"). Never agree or disagree, and never a number with no words beside it.
5. Write two or three open prompts on barriers: what could stop you using this in the next [period], what was missing, what should be cut.
6. Add the line respondents read first: answers help fix the programme and say nothing about any person, and the form is anonymous by default.
7. Draw the summary template: counts per option, themes from comments, groups under the minimum suppressed, no quote that identifies someone. Write the limits on the summary itself, because a reader who sees only the counts will take them as proof of learning.

## Output Format
```markdown
# Programme Feedback Form
Programme: [name] | Filled on: [last day, date] | Anonymous by default
To respondents: your answers help us fix the programme. They say nothing about you or about any other person.
## Closed items
| # | Item | What it predicts | Answer options (concrete states) |
|---|---|---|---|
| 1 | How close is this to the work you do? | Relevance | [state A] / [state B] / [state C] / [state D] |
| 2 | How ready are you to [objective] at work? | Confidence to apply | [could do it now without help] / [would need practice first] / [...] |
| 3 | [comprehension, realistic practice, support back at work] | [what it predicts] | [states] |
## Open prompts
- What could stop you using this in the next [period]? / What was missing? / What should we cut?
## Audit of the previous form
- [old item] | [remove / keep one / sharpen] | [rates the trainer / satisfaction only / predicts use]
## Summary of answers
| Item | Count per option | Themes from comments | Change to the programme |
|---|---|---|---|
| [#] | [counts, or "suppressed, under [minimum]"] | [theme, no identifying quote] | [change] |
## What this form cannot show
- Perceptions on the last day only. It cannot show learning or use on the job. Where those are checked: [evaluation plan, follow-up date]
## Decision
[L&D lead name] reads the summary by [date] and decides which changes go into the next run on [date].
```

## Done When
- No item rates the trainer, the venue or a named person
- Every closed item offers concrete states, with no agreement scale left
- The summary shows counts and themes only, with the suppression threshold filled in
- The limits are written on the summary, and each item points to a change the team could make

## Quality Bar
- Four to six closed items. A seventh needs a reason stronger than "we have always asked it".
- Comments are reported as themes; a comment that would identify its author is left out
- Trainer ratings, trainer league tables and named comment reports are refused, whoever asks
- The form rates the programme, never the trainer or a learner; the L&D lead decides which changes go into the next run

## Next
Run ldg-check-use-on-the-job (Check Use on the Job) for the evidence a last-day form cannot give.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
