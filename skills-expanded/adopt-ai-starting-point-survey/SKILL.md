---
name: adopt-ai-starting-point-survey
description: Writes an anonymous AI starting point survey of 10 to 15 questions, with a minimum group size you set, a never-asked list and a team-level summary template. Use for "run adopt-ai-starting-point-survey", "AI starting point survey", "survey before AI training", "ask people where they are with AI", "anonymous AI survey", "why are people not using AI survey", "AI adoption baseline questions", "AI readiness survey", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Starting Point Survey

## When To Use
You are about to plan training for people you have never asked, and the only data on offer is a licence count. A licence count says who was given a seat. It says nothing about whether the tool is useful for their work, whether their manager has ever mentioned it, or why some people have decided not to use it. This skill gives you the questions, the protections and the summary to find out.

## When Not To Use
Not for explaining why one specific use is not happening in one team: AI Adoption Barrier Diagnosis works from real episodes and tests explanations, which a survey cannot do. Not in a group so small that any answer points at its author: hold a conversation instead, and say openly that it is not anonymous.

## Inputs
- The roles or teams in scope and roughly how many people are in each group.
- What your survey tool records about respondents (login, email, device, time stamp), or "I do not know".
- Who will see the raw answers and the summary, what you intend to do with the results, and your organisation's AI rules if they exist.
If you have none of this, I start from the roles in scope and mark the output as a first draft.

## Approach
The questions rest on two plain ideas: people take up a tool when they find it useful for their own work and easy enough to use. To those I add the conditions that go with frequent use in Gallup's 2026 workplace surveys (a manager who actively supports it, fit with existing work, room to experiment, clear policies) and the reasons non-users give there (preferring the current way, privacy and compliance worries, doubt that it helps their work, ethical objection). Those surveys are correlational: they show what goes together, not what causes what. The failure this prevents is the "anonymous" survey of a team of four, broken down by role and tenure, that everyone can decode and nobody answers honestly again.

## Workflow
1. Ask up to three questions: which groups are in scope and how large is the smallest, what does your survey tool record about respondents, and who sees the raw answers and what happens to the results by when.
2. Set the protections before any question. You set the minimum group size; any group below it is merged with a neighbour or suppressed. I draft the never-asked list: name, email, employee number; combinations that identify a person in a small team (team plus tenure plus role); self-rated skill used to compare people; anything about a named colleague; anything used for performance review.
3. Draft 10 to 15 questions across eight blocks, one or two each: current use (by task, in bands you set, never a count), usefulness for my work, ease, manager support, clarity of the rules, time to learn, concerns, reasons for not using. Scales are agreement or frequency bands in words. No question produces a personal score.
4. Write "reasons for not using" as legitimate options, including "I do not think it helps my work", "I prefer the way I do it now", "I am not sure what I am allowed to put in" and "I have objections", with a free text line. If the options read like excuses, people who hold them will skip the question.
5. Write the cover note: who sees what, what the survey tool itself records, what will happen with the results and by when. It promises no anonymity the tool cannot give. If the tool logs identity, say so and offer a route that does not.
6. Build the summary template by team or role group: counts beside percentages, top reasons for not using, the conditions that are missing, open questions. No row per person. Free text is paraphrased when it could identify someone. When results come back, I summarise only at or above the minimum group size; I do not guess who wrote an answer, and I do not break a result down further on request.

## Output Format
```markdown
# AI Starting Point Survey
Status: [first draft / approved by [name] on [date]] · Groups in scope: [roles or teams]
## Cover note
[Why we ask. Who sees raw answers: [role]. Who sees the summary: [roles]. What the survey tool records: [as stated by the user]. What happens with the results, and by [date]. Taking part is a choice.]
## Protections
- Minimum group size: [number you set]. Groups below it are [merged with / suppressed].
- Never asked: [name, email, employee number; identifying combinations; self-rated skill used to compare people; anything about a named colleague; anything used for performance review]
## Questions
| No. | Block | Question | Answer scale |
|---|---|---|---|
| [1] | Current use | [question by task] | [frequency bands in words] |
| [2] | Usefulness for my work | [question] | [agreement bands] |
| [..] | [Ease / Manager support / Clarity of the rules / Time to learn / Concerns / Reasons for not using] | [question] | [bands or options, plus free text] |

## Team-level summary template
| Group | Responses (count) | Block | Result (count and %) | Reading |
|---|---|---|---|---|
| [role group at or above the minimum] | [n] | [block] | [count, %] | [one line] |

- Top reasons for not using: [reason, count]. Conditions that are missing: [manager support / fit with work / room to experiment / clear rules]
- Open questions the survey cannot answer: [list]. Groups merged or suppressed: [list]
## Decision
[Name of the survey owner] decides by [date] whether the survey goes out as written, and [sponsor name] decides by [date] what is done with the results and how they are reported back to the people who answered.
```

## Done When
- There are 10 to 15 questions and each of the eight blocks has one or two.
- The minimum group size is a number the user set, and the rule for smaller groups is written.
- The cover note states what the survey tool records, and the summary template has no row, column or cut that could single out a person.

## Quality Bar
- One idea per question, in the words people use about their own work, and "reasons for not using" read as reasonable positions, never as deficits.
- No readiness or maturity score, for a person or for a team: the summary describes conditions, it does not rate anyone.
- Counts sit beside every percentage. No benchmark and no figure from any external survey appears anywhere.
- The survey measures no result of the work, and it says so under open questions. What you may collect and keep: check with a qualified adviser.
- Anonymous, team level, small groups suppressed: the survey never becomes a list of who uses AI.

## Next
Run adopt-ai-use-case-map (AI Use Case Map) to turn "I do not see what I would use it for" into tasks per role.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
