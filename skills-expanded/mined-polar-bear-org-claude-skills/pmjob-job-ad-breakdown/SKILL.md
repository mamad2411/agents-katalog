---
name: pmjob-job-ad-breakdown
description: Reads one job ad line by line and writes a Job Ad Breakdown with the problem the role exists to fix, must-haves against nice-to-haves, level signals, the AI ask, the rounds it implies and your evidence for each line with gaps stated as gaps. Use for "run pmjob-job-ad-breakdown", "break down this job ad", "which requirements really matter", "what level is this role", "is this a senior or a lead role", "what does this ad want on AI", "what rounds should I expect", "do I have evidence for this ad", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Job Ad Breakdown

## When To Use
The ad lists twenty requirements and you cannot tell which three decide the hire. Run this on one ad you intend to apply to, to answer: what problem is this role there to fix, which lines carry the decision, what level does the text read as, and where do I have evidence and where do I not?

## When Not To Use
To compare the vocabulary of several ads or set your own criteria, use Target Role Brief. Once the recruiter has told you the real rounds, use Interview Loop Map; this skill only reads likely rounds from the text.

## Inputs
- The full ad pasted as text, including the title, the team paragraph and any "about you" list
- Your Career Evidence Inventory (rows E1, E2 and so on)
- Your Target Role Brief, if you have one
If you have none of this, I start from the ad alone, leave the evidence column open, and mark the output as a first draft.

## Approach
A skills-by-level reading with evidence matching. The Government Digital and Data Profession Capability Framework describes each product manager skill at four levels (awareness, working, practitioner, expert), which gives a public vocabulary for the verbs in an ad. It is one framework and level names do not transfer between employers, so the output says "reads as", never "is". The failure this prevents: treating all twenty lines as equal, spending the cover note on a tool named once, and missing the outcome the ad opened with.

## Workflow
1. Ask up to three questions: is the pasted text the whole ad; which lines worry you; when do you plan to apply.
2. Number every line. Give each a type (outcome, responsibility, skill, tool, quality), a must-have or nice-to-have call, and the signal behind that call: placed first, repeated, in the title, under "required", or tied to the stated problem. The call is a reading of the text and is labelled as one.
3. Write the problem behind the role in two sentences from the ad's own words, then what the ad does not say. Mark the second part "inferred" and turn each inference into a question for the recruiter.
4. Read the level from the verbs: explains or supports reads as awareness; applies and delivers as working; chooses approaches and influences as practitioner; sets direction and coaches as expert. Add scope, team size if stated, and who the role reports to.
5. Quote the AI line and sort it: use AI tools in your own work (AI Fluency Answer for the spoken answer, AI Work Sample for something to show), build AI features (the evidence rows where you shipped one, told in Portfolio and Project Walkthrough), or lead AI adoption in a team (a story in Interview Story Bank). A line too vague to sort becomes a recruiter question. No AI line is also a finding.
6. Map lines to likely rounds: metrics wording to an analytical round, "prioritise" to an execution round, a portfolio request to a walkthrough. Mark each "likely, confirm with the recruiter".
7. Match every line to your inventory: shown (row ID), partly (row ID plus what is missing), not yet. For each gap, write the honest sentence you would say about it.

## Output Format
```markdown
# Job Ad Breakdown
Role: [title] · Ad read on: [date] · Status: [full / first draft]
## The problem behind the role
[Two sentences, in the ad's words]
Inferred, to confirm: [what the ad does not say] · Question for the recruiter: [question]
## Line by line
| No. | Line (short) | Type | Must-have or nice-to-have | Signal behind that reading | Evidence | Match | Likely round, to confirm with the recruiter |
|---|---|---|---|---|---|---|---|
| [1] | [line] | [outcome / responsibility / skill / tool / quality] | [must / nice] | [first / repeated / title / "required" / tied to problem] | [E4] | [shown / partly / not yet] | [round, or none] |
## Level signals
Reads as: [awareness / working / practitioner / expert] · Verbs: [verbs quoted] · Scope: [scope] · Team: [size if stated, or "not stated"] · Reports to: [role, or "not stated"]
## The AI ask
"[line quoted]" · Kind: [use in own work / build AI features / lead adoption / none stated] · Prepare with: [skill]
## Gaps, stated as gaps
| Line no. | What is missing | The honest sentence you would say |
|---|---|---|
| [n] | [gap] | [sentence in your words] |
## Decision
You decide whether to apply, and which three lines to lead with, by [date].
```

## Done When
- Every line of the ad is numbered, typed and called, with the signal named
- The problem statement uses the ad's words, and every inference has a recruiter question
- The level line says "reads as" and quotes the verbs it rests on
- Every line has a match status; every gap has a sentence you would be comfortable saying aloud

## Quality Bar
- Must-have calls and likely rounds are readings of the text, labelled as readings; only the recruiter can confirm them.
- The level reading describes the ad, never you. There is no fit score and no match percentage.
- Pay is recorded only if the ad states a range, quoted with the date read.
- A gap is written as a gap; no evidence is stretched or invented to cover a line of the ad.

## Next
Run pmjob-company-research (Company Research Brief) to learn the company behind the ad.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).