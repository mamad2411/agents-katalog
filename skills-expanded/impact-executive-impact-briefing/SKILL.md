---
name: impact-executive-impact-briefing
description: Drafts a briefing on one flagship programme for the executive team and finance, producing five slides or two pages (the business result, the chain of evidence, the cost, the limits, the decision asked), speaker notes and the hard questions with answers drawn only from the evidence. Use for "run impact-executive-impact-briefing", "executive briefing on training impact", "present training results to executives", "training impact presentation", "L&D slides for the leadership team", "show the business impact of training", "questions finance will ask about training", part of the Claude Guide for Training Impact Pack by 90n.
---

# Executive Impact Briefing

## When To Use
You have ten minutes with the executive team and one chance to be taken seriously. Use it for one flagship programme whose evidence is in, when the readers did not sign the agreement and care about three things: the result, the cost and the risk. It answers what they will ask before they ask it.

## When Not To Use
Not for the sponsor who signed the agreement: Sponsor Impact One-Pager reports measure by measure for that reader. Not for the whole function: use Quarterly L&D Report. And this skill does not test its own wording; Overclaim Check does that before the room sees it.

## Inputs
- The programme's results table and the reasoning about what else could explain the change, with claim strengths.
- The cost, fully loaded, including participants' time away from work, from finance or with finance's agreement; the return as a range if one was worked out; and the one-pager for the sponsor, if it exists.
If you have none of this, I start from the agreement and whatever figures you can paste, and mark the output as a first draft with every missing cell left blank.

## Approach
Bottom line up front, from the US Army's writing standard (Army Regulation 25-50): the main point at the beginning, understood in a single rapid reading. Key caveats sit with the key findings, as the UK Government Analysis Function's guidance "Communicating quality, uncertainty and change" asks, and the audience and the action wanted are fixed first (the CDC evaluation reporting guide). The failure this prevents: nine slides of method, the result on slide eight, and finance finding the weak spot in the cost while you are still on slide three. Build it in Claude Slides (beta) or Claude Docs (beta), in the same conversation as the one-pager so the two match; slides export to PowerPoint or PDF, and you tell it your house rules for slides.

## Workflow
1. I ask three questions at once: which programme, and what decision you want from the room; who is in the room (roles) and how many minutes you have; and slides or two pages, with which evidence files you are pasting.
2. Lay out five parts in this order, one message each: the business result and the ask; the chain of evidence; the cost; the limits; the decision asked. The ask appears in part one and again in part five, in the same words.
3. Write each title as the finding in one sentence, not a topic label: a reader who sees only the five titles has the whole briefing. The verb matches the claim strength: "the figures show", "the evidence suggests", "we do not know whether".
4. The chain of evidence in one picture: programme, behaviour on the job, leading indicator, result, each link with its evidence and strength. The other explanations that were weighed get a line here, not a footnote.
5. The cost, all in, with participants' time. Finance's figures or a blank cell. A return appears only as the low to high range already worked out, with the share credited to the programme named, never a single point and never a new calculation.
6. The limits: what we can conclude and what we cannot, and the caveat that would change the decision, which also goes on slide one. This part is never cut for time; if minutes run short, the chain shrinks.
7. Speaker notes per slide (what to say in under two minutes, the source of each figure), then the hard questions: how do you know it was the programme; what did it cost, all in; what did not work; what would you stop; plus what this room is known to ask. Answers come from the evidence only, and "we do not know yet" is allowed, with what it would take to know. Last, the figure check against the results table and the one-pager, to the digit.

## Output Format
```markdown
# Executive Impact Briefing
Programme: [name] · Audience: [roles] · Time: [minutes] · Format: [five slides / two pages] · Presented by: [name, role] · Status: [first draft / checked] · Figures match the results table and the one-pager: [yes / no, fix before the meeting]
## The five parts
| # | Part | Title as a finding (one sentence) | On the slide | Figures, each with its source |
|---|---|---|---|---|
| 1 | Result and ask | [finding] | [the result, the key caveat, the ask] | [your figure, source] |
| 2 | Chain of evidence | [finding] | [link by link, with strength; other explanations weighed] | [your figure, source] |
| 3 | Cost | [finding] | [fully loaded cost, including participants' time; return as a range or blank] | [finance's figure, source] |
| 4 | Limits | [finding] | [what we can conclude; what we cannot] | [none / your figure, source] |
| 5 | Decision asked | [finding] | [continue, change, stop or scale; what it needs] | [your figure, source] |
## Speaker notes
| Slide | What to say (under two minutes) | Source of each figure | Voucher |
|---|---|---|---|
| [#] | [notes] | [source] | [name / no voucher yet] |
## Hard questions
| Question | Answer from the evidence | Evidence it rests on | If we do not know yet: what it would take |
|---|---|---|---|
| How do you know it was the programme? | [answer] | [evidence, strength] | [what, who, by when] |
| [What did it cost, all in? / What did not work? / What would you stop? / this room's own question] | [answer] | [evidence, strength] | [what, who, by when] |
## Decision
[Name, role, for the executive team] decides to [continue / change / stop / scale] [programme] by [date]; [name, role] presents and answers for the figures.
```

## Done When
- The five titles, read alone, give the result, the evidence, the cost, the limits and the ask.
- Every figure matches the results table and the one-pager to the digit, with its source in the notes.
- The limits part is present, and the caveat that changes the decision is on slide one.
- Each hard question has an answer from the evidence or an honest "we do not know yet" with what it would take.

## Quality Bar
- One message per slide, the rest in an annex; the cost is finance's figure or it is blank, and the slide says who is working on it.
- No individual or team is held up as proof or as the problem; evidence is about the programme.
- The briefing is a draft until a person has rehearsed it aloud and timed it.
- Answers come only from the evidence, including "we do not know"; no result, comparison or quote is added to make the story land.

## Next
Run impact-overclaim-check (Overclaim Check) to test every claim before the room does.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
