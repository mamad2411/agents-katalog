---
name: impact-post-training-survey
description: Writes the end-of-programme survey that rates the programme and never the trainer, producing an audit of your current form, four to six closed items with concrete answer options, open prompts on barriers, an item-to-measure map, a three-person pretest and a group-level summary template. Use for "run impact-post-training-survey", "post-training survey", "training evaluation form", "training feedback survey", "smile sheet", "end of course survey", "our satisfaction form tells us nothing", "course feedback questions", part of the Claude Guide for Training Impact Pack by 90n.
---

# Post-Training Survey

## When To Use
The satisfaction form says everyone loved it and tells you nothing you can act on. Use this before the last day of a programme, to replace that form with a short one that answers a narrower question: are people ready to use this at work, and what do they expect to stand in the way?

## When Not To Use
A form filled in on the last day cannot tell you whether anyone used anything; for that, run Training Follow-Up Survey some weeks later. If no measures have been agreed with the sponsor, the items have nothing to map to: run Success Measures Agreement first.

## Inputs
- The agreed measures and critical behaviours from your Success Measures Agreement
- Your current form, pasted as it is, how it reaches people (paper, your LMS, your survey tool), and the minimum reporting group
If you have none of this, I start from the programme title and what people should be able to do afterwards, and mark the output "no agreement on file: first draft".

## Approach
The frame is LTEM, the Learning-Transfer Evaluation Model from Work-Learning Research: eight tiers, where the lower ones, learner perceptions included, cannot validate learning on their own. So this survey makes no claim about learning; it asks about the things that predict use. The wording follows Pew Research Center's "Writing survey questions": one concept per question, a choice between alternative statements instead of agree or disagree, short option lists, open questions in a pilot to find the options, and a pretest. The failure it prevents: a wall of top marks for "the facilitator was engaging", which is a verdict on a colleague and gives you nothing to change.

## Workflow
1. Ask three questions at once: which agreed measures and behaviours does this programme serve, what could you change in the next run based on the answers, and what minimum reporting group do you set?
2. Audit the current form item by item. Each item gets one verdict: rates the trainer (remove), measures satisfaction or reputation (keep one at most), or measures something that predicts use (keep and sharpen). Say plainly how many items survive; it is often very few.
3. Draft four to six closed items, one each on relevance to the job, comprehension, realistic practice, confidence to apply, and the support people expect back at work. Never ask whether people have used it: on the last day nobody has. Write the answer options as concrete states a person recognises in themselves ("I could do this tomorrow on my own", "I could do it with a job aid beside me"), never "agree" or "strongly agree". Four or five options at most, one idea per item, and any question holding an "and" is split in two.
4. Add two or three open prompts on barriers: what could stop you using this in the next [period you set], what was missing, what to cut.
5. Map every item to an agreed measure and to a change you could make. An item that maps to neither is cut, however interesting the answer would be.
6. Write the pretest and the summary template. Three people take each item as an open question first and think aloud; you note what they understood it to mean, and the closed options are rebuilt from their words. The summary reports counts per option for groups at or above the minimum, with the number invited beside the number who answered.

## Output Format
```markdown
# Post-Training Survey
Programme: [name] | Run on: [last day, date] | Anonymous | These answers help fix the programme and say nothing about any person | Perception data from the last day: it cannot show learning or use
## Audit of the current form
| Current item | Verdict (remove / keep one / keep and sharpen) | Why |
|---|---|---|
| [item as written] | [verdict] | [reason] |
## Closed items
| # | Item | Answer options (concrete states) | Agreed measure it serves | Change it could trigger |
|---|---|---|---|---|
| 1 | [item on relevance to the job] | [state A] / [state B] / [state C] / [state D] | [measure] | [change] |
## Open prompts
What could stop you using this in the next [period you set]? | [prompt on what was missing] | [prompt on what to cut]
## Pretest record (three people, filled by you)
| Item | What the person understood it to mean | Words they used | Revision |
|---|---|---|---|
| [#] | [your note] | [their words] | [new wording or "none"] |
## Group summary template
| Item | Invited | Answered | Count per option | Reported or suppressed (minimum [you set]) |
|---|---|---|---|---|
| [#] | [your figure] | [your figure] | [your figures] | [reported / suppressed] |
## Decision
[L&D lead name] approves the final wording after the pretest by [date], and decides by [date] which changes go into the next run.
```

## Done When
- No item rates the trainer, a learner or any named person, none asks whether people have used the training, and at most one measures satisfaction
- Every closed item offers concrete states, and every item maps to an agreed measure and a possible change
- The pretest record is blank for you to fill, and the summary carries your minimum reporting group

## Quality Bar
- Options come from what pretest participants said, not from what reads well to the designer
- Requests for trainer ratings, trainer league tables or named comment reports are refused in one line, with the group-level summary offered instead
- Whether the form may be anonymous in your survey tool, and how long answers are kept: check with a qualified adviser
- The survey rates the programme, never the trainer or a learner; results are reported for groups, and no response figure is ever made up

## Next
Run impact-training-follow-up-survey (Training Follow-Up Survey) to ask later whether anyone used it.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
