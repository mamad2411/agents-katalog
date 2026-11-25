---
name: adopt-ai-pilot-plan
description: Drafts an AI pilot plan with the one question the pilot answers, a prediction written before the start, the measures it will read, and the stop, rollback and review rules. Use for "run adopt-ai-pilot-plan", "AI pilot plan", "design an AI pilot", "pilot before rolling out AI", "what should our AI pilot test", "stop rule for the AI pilot", "plan a small test of AI on real work", "our pilot proved nothing", part of the Claude Guide for AI Adoption Pack by 90n.
---
# AI Pilot Plan
## When To Use
The choice on the table is between rolling out to everyone at once and running a pilot that proves nothing. You have a work change in mind for one or two teams and a sponsor who wants "a pilot". The question this answers: what exactly will this test tell us, and what did we agree to do with the answer before we saw it?

## When Not To Use
Not when the measures themselves are still undefined: agree them first with AI Value Measures, because this plan only points to them. Not once the pilot has run and the sponsor is asking who goes next: that is the AI Rollout Decision.

## Inputs
- The work change being tested, per role, and the teams or work proposed for the pilot, with how they were chosen.
- The agreed measures with their sources and baselines, the sponsor and the date a decision is needed.
If you have none of this, I start from one sentence on the change and the team, and mark the output as a first draft.

## Approach
This is Plan-Do-Study-Act, the test cycle inside the Model for Improvement from the Institute for Healthcare Improvement: plan a small test, run it, compare the result with what you predicted, act on the rule you set. The judgement is in what gets written down before the start. A pilot run by the keenest volunteers, on their easiest work, with success defined afterwards, always "goes well", and then the rollout meets people who are nothing like them.

## Workflow
1. Ask at most three questions: what do you expect to improve and what could go wrong, which real work and which teams are in scope and why those, and who is the sponsor and when must they decide.
2. Plan the question. Reduce the pilot to one uncertainty it can answer. A pilot that tests the tool, the training and the process at once cannot say which one worked. Park the rest in a "not tested here" list.
3. Set the scope: a bounded set of real work, who takes part, where, for how long (you set it). Include one difficult but safe case, or the pilot only shows the change works where it was always going to. Write how volunteers may differ from everyone else. Taking part is a choice and people can leave.
4. Write the prediction before anything starts, then list the measures by reference: name, source, baseline. I do not redefine them here. If a measure has no baseline, the plan says "collect before the start".
5. Describe what the results are compared with (the same team's earlier work, comparable work running alongside) and the limits of that. Name the other explanations in advance: novelty, a quiet month, different work.
6. Plan the Do and the Study: the support, the check-in dates, where problems and surprises get noted as they happen, and the date results are read against the prediction. Then fix the Act rule now, before any result exists: what leads to continue, adapt, stop or collect more, and the stop and rollback conditions, including harm even when use is high. These thresholds are local: the sponsor sets them. Say that a short pilot cannot show durability.

## Output Format
```markdown
# AI Pilot Plan
**Change tested:** [role, action, task] · **Sponsor:** [name] · **Runs:** [start] to [end] · Draft status: [first draft / agreed on date]
## The question and the prediction
[The one question this pilot answers.] Not tested here: [list].
Prediction, written on [date] before the start: [what we expect to see, and what would surprise us].
## Scope and selection
| Work covered | Teams and roles | Why these | How they may differ from the rest | Difficult but safe case |
|---|---|---|---|---|
| [bounded set of real work] | [team, roles] | [reason] | [volunteers, workload, type of work] | [case] |

## Measures (defined elsewhere, listed here by reference)
| Measure | Kind (outcome, process, balancing) | Source | Baseline and its date |
|---|---|---|---|
| [measure, team level] | [kind] | [source] | [baseline or "collect before the start"] |

## Comparison and limits
Compared with: [earlier work / comparable work]. Other explanations to rule out: [novelty, a quiet month, different work]. What this pilot cannot show: [durability, other teams, people who did not volunteer].
## Support and check-ins
Support: [who helps, with what]. Check-ins: [dates]. Problems and surprises are noted in: [place]. Results read on: [date].
## Stop, rollback and review rule
| Condition | What it triggers (stop, roll back, adapt, continue, collect more) | Who calls it |
|---|---|---|
| [condition the sponsor set] | [action and how work returns to the old way] | [name] |

## Decision
[Sponsor name] approves the question, the prediction and the stop rule by [date], before the pilot starts, and decides continue, adapt, stop or collect more on [review date].
```

## Done When
- The pilot answers one question, and the prediction carries a date earlier than the start.
- Every measure has a source and a baseline, or is marked to collect before the start.
- Each stop and rollback condition names who calls it and how work goes back, and the plan says what the pilot cannot show.

## Quality Bar
- Real work only: no demonstration tasks, no sandbox exercises standing in for the job.
- Measures are read at team level from the team's own records. No per-person usage, no list of who took part how much.
- A before and after comparison is called what it is, never proof of cause.
- Failed attempts and surprises stay in the record, and no expected figure is written unless it is your own prediction, labelled as one.
- The pilot tests a change in the work at team level; taking part is a choice and the sponsor owns the stop rule.

## Next
Run adopt-team-involvement-plan (Team Involvement Plan) to decide what the people in the pilot can still change.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
