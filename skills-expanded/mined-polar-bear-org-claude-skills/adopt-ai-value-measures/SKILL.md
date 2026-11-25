---
name: adopt-ai-value-measures
description: Builds the measure set for an AI pilot with four to six measures agreed with the sponsor before the start, each with a definition, a source and a baseline, at least one balancing measure for workload, and a list of what will not be measured. Use for "run adopt-ai-value-measures", "AI value measures", "how do we measure AI adoption", "measures other than hours saved", "AI pilot success measures", "what will it worked mean", "balancing measure for workload", "the sponsor wants hours saved", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Value Measures

## When To Use
The only measure anyone has proposed is "hours saved", self-reported, and the pilot starts soon. Use this before any data comes in, to agree with the sponsor what "it worked" will mean. It answers one question: how will we know that this change is an improvement, in the work and not in a survey?

## When Not To Use
Not when nobody has said what should change in the work: write that first with AI Adoption Brief. Not when the results are already in: definitions chosen after the data are a story, so read what you have with AI Adoption Evidence Review and say the measures were set late. For one team deciding where its lighter workload goes, use Freed Time Agreement.

## Inputs
- The aim and the work change per role, from your brief or in two sentences.
- What the teams already record about this work: quality checks, rework or returns, turnaround, backlog, complaints, work outside hours.
- Who the sponsor is, who owns each data source, the pilot start date, and any measure already promised to leadership, in its exact wording.
If you have none of this, I start from the aim in one sentence and the type of work, propose candidate measures marked "source to find", and mark the output as a first draft.

## Approach
Three kinds of measure, from the Institute for Healthcare Improvement's guidance on establishing measures, with the second question of its Model for Improvement: how will we know that a change is an improvement? Outcome measures say whether the work got better for the people it serves, process measures say whether the new way of working is happening, and balancing measures say whether the gain created a problem elsewhere. Self-reported time is not enough on its own: an official report on a public sector trial of an AI assistant could not say how saved time was spent, and a working paper found reported benefits alongside unchanged recorded hours. Both are single studies with limits, and neither tells you what will happen in your teams. The failure this prevents is the pilot that ends with a large hours figure, no record of where the hours went, and a team working longer days.

## Workflow
1. Ask at most three questions: what is the aim in the brief, which records of this work already exist and who owns them, and who is the sponsor and when does the pilot start?
2. Draft one or two outcome measures tied to the aim: quality, rework, turnaround, or what the team stopped doing. Prefer a measure the organisation already collects over a better one it would have to invent.
3. Draft one or two process measures at team level: is the agreed way of working happening, counted by the team as qualifying uses over eligible opportunities. A login count is not a process measure.
4. Add at least one balancing measure for workload (work outside hours, backlog age, rework downstream, quality as the next team receives it). This is the one that gets dropped when the outcome looks good, so it is fixed now.
5. Define each measure: a plain definition two people would apply the same way, numerator and denominator where it is a rate, source, baseline with its date, data owner. No baseline means "baseline to collect before the start".
6. Place self-reported time saved, if the sponsor wants it, as one labelled perception measure: never the headline, never converted into money. Set how each measure is read: plotted over time, not a single before and after, with sampling and any warning threshold you set.
7. Write the "will not be measured" list, check the total is four to six, and prepare the set for the sponsor to agree and date before the pilot starts.

## Output Format
```markdown
# AI Value Measures
**Aim (from the brief):** [what the change is for] · **Sponsor:** [name, role] · **Pilot starts:** [date]
## Measures
| # | Kind | Measure | Plain definition | Numerator / denominator | Source | Baseline and its date | Data owner |
|---|---|---|---|---|---|---|---|
| 1 | Outcome | [measure] | [definition] | [n / d, or "not a rate"] | [existing record] | [value, date, or "to collect before the start"] | [role] |
| 2 | Process (team level) | [measure] | [definition] | [qualifying uses / eligible opportunities] | [team's own count] | [value, date] | [role] |
| 3 | Balancing (workload) | [measure] | [definition] | [n / d] | [source] | [value, date] | [role] |
| 4 | Perception, self-reported | [measure, labelled as perception] | [question asked] | [answers by team, small groups merged] | [anonymous survey] | [value, date] | [role] |

## How we will read them
- Plotted over time at [interval you set], from [date] to [date]. Sampling: [what is sampled and how, set by you].
- Warning on the balancing measure: [the threshold you set, and who is told].
## Will not be measured
- Individuals, per-person usage, prompts, speed per person, any target per person. Also: [anything else ruled out, and why]
## Open points
- [Baseline to collect, source to confirm, definition still disputed]
## Decision
[Sponsor name] agrees or amends this set by [date, before the pilot starts], and [data owner] confirms each baseline by [date]. Agreed on: [date].
```

## Done When
- There are four to six measures, with at least one outcome, one process and one balancing measure for workload.
- Every measure has a definition, a source, a data owner, and a baseline with its date or the words "to collect before the start".
- Any self-reported time measure is labelled as perception and is not the first row, the "will not be measured" list is filled in, and the sponsor's agreement has a date before the pilot start.

## Quality Bar
- Every baseline is the organisation's own figure with its date, or a bracketed placeholder. I never supply a typical value.
- Definitions are fixed before the data and stay the same through the pilot and the review; a change of definition is recorded with its date.
- No return on investment calculation and no conversion of time into money.
- Small groups are merged or suppressed in any measure that counts people, and counts sit beside percentages.
- Measures describe the work at team level, never a person, and no saving is claimed that the organisation's own evidence does not show.

## Next
Run adopt-adoption-evidence (AI Adoption Evidence Review) to read what the measures show once there is data.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
