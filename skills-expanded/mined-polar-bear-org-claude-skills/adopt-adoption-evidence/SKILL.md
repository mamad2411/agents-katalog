---
name: adopt-adoption-evidence
description: Reviews the evidence on an AI change at team level, with uptake as qualifying uses over eligible opportunities, five separate questions on reach, effect, take-up, delivery and lasting use, and three closing lists of what the evidence supports, contradicts and cannot show. Use for "run adopt-adoption-evidence", "AI adoption evidence review", "is AI adoption working", "do logins mean adoption", "read the AI pilot results", "what does our AI data show", "AI adoption rate by team", "review the pilot evidence", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Adoption Evidence Review

## When To Use
The dashboard says most people logged in and the sponsor reads that as adoption. Use this once the pilot or rollout has produced some data, to keep use, usefulness and side effects apart. It answers: what does our own evidence support, what does it contradict, and what can it not show?

## When Not To Use
Not before the measures are defined: without agreed definitions and baselines there is nothing to read against, so run AI Value Measures first. If what you need is the one page for leadership, write this review and then use AI Adoption Executive Update. This review produces no list of who uses AI and no comparison of people.

## Inputs
- The agreed measures with their definitions and baselines, and the work change the pilot tested.
- What the team itself provides: its count of qualifying uses and eligible opportunities, its work records for the agreed measures, the anonymous survey summary, barrier logs, any consented stories.
- The time window, the teams in scope, and the minimum group size you set.
If names appear in what you paste, I work at team level, leave the names out of the output and say so. If you have none of this, I start from the work change and whatever counts the team can give, and mark the output as a first draft with its gaps listed.

## Approach
RE-AIM, the evaluation framework published at re-aim.org, asks five separate questions: reach, effectiveness, adoption, implementation, maintenance. It was built for health programmes, so its terms are translated here: "adoption" in the framework means which teams or settings took the change up, not how many people opened a tool. The judgement is to refuse the single figure. Exposure, training attended, a try and sustained use are four different things, and a login is none of them. The failure this prevents is the slide that reports a high share of active users for a change that touched a small part of the work it was meant for, and that nobody was still doing a quarter later.

## Workflow
1. Ask at most three questions: what counts as a qualifying use and an eligible opportunity for this change, what is the window and the minimum group size, and what did the team expect to see before it looked?
2. Inventory the evidence: for each source, what it measures, its date, who provided it and what is missing. Set aside anything that exists only per person.
3. Calculate uptake per team as qualifying uses divided by eligible opportunities, with the window and the exclusions stated. Put the count beside every percentage, and merge or suppress any group below the minimum size.
4. Answer the five questions separately. Reach: of the people and teams in scope, how many took part and which groups did not. Effectiveness: did the work change on the agreed measures, negative effects included. Adoption: which teams or settings took it up, which did not and why. Implementation: was it used as agreed, what was adapted, what it cost in time and support. Maintenance: is it still in use after the period you set.
5. For each finding, write the missing data and the other explanations: case mix, timing, a changed denominator, volunteers, hard cases left out. An uncontrolled trend supports "moved alongside", never "caused".
6. Close with three lists: what the evidence supports, what it contradicts and what it cannot show. Then name the one follow-up check that would change the reading most.

## Output Format
```markdown
# AI Adoption Evidence Review
**Change reviewed:** [the work change, from the brief] · **Window:** [dates] · **Minimum group size:** [you set it; smaller groups are merged or suppressed] · **Evidence provided by the team:** [source, date], [source, date]
## Uptake
| Team or setting | Qualifying uses | Eligible opportunities | Uptake (count, then %) | Exclusions |
|---|---|---|---|---|
| [team] | [count] | [count] | [n of d, %] | [what was left out and why] |

## The five questions
| Question | What the evidence shows (counts beside percentages) | Source and date | Missing data | Other explanations |
|---|---|---|---|---|
| Reach: who took part, which groups did not | [finding] | [source, date] | [gap] | [explanation] |
| Effectiveness: did the work change, side effects included | [finding against each agreed measure and its baseline] | [source, date] | [gap] | [explanation] |
| Adoption: which teams or settings took it up | [finding] | [source, date] | [gap] | [explanation] |
| Implementation: used as agreed, adapted, at what cost | [finding] | [source, date] | [gap] | [explanation] |
| Maintenance: still in use after [period you set] | [finding, or "too early to say"] | [source, date] | [gap] | [explanation] |

## What the evidence supports, contradicts and cannot show
- **Supports:** [statement, with the row it rests on]
- **Contradicts:** [statement, with the row it rests on]
- **Cannot show:** [for example: whether the change lasts, where any saved time went, anything about individuals]
## Decision
[Decision owner name] decides by [date], using the review rule set before the pilot, whether to continue, adapt, stop or collect more. [Name] runs the follow-up check [check] by [date].
```

## Done When
- Uptake has a numerator, a denominator, a window and stated exclusions for every team shown, every percentage has its count beside it, and no group below the minimum size appears.
- Each of the five questions is answered, or marked "no evidence yet", with its source and date.
- All three closing entries are filled, and "cannot show" is not empty.

## Quality Bar
- Results are read against the measure definitions agreed before the pilot; a definition that changed is flagged with its date. Every figure is the team's own, and a gap stays a gap in brackets.
- Positive survey answers and usage counts are never offered as proof that the work improved; a consented story may be quoted as one case and never turned into a rate.
- I decline league tables, lists of non-users and causal claims from an uncontrolled trend, in one sentence, and carry on with the team-level review.
- Team level only, small groups suppressed, no usage data about individuals; the review says what the evidence cannot show.

## Next
Run adopt-ai-use-stories (AI Use Stories) to add consented accounts of real use beside the numbers.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
