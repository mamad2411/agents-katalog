---
name: pmjob-behavioural-answers
description: Builds a Behavioural Round Prep Sheet for one interview round with the competencies it tests, a primary and a reserve story for each, the follow-up questions each story invites with your honest answer, and the employer's values matched only where a story truly shows them. Use for "run pmjob-behavioural-answers", "prepare for a behavioural interview", "values interview prep", "leadership round next week", "my stories all say we", "tell me about a time when", "which story for which question", "match my stories to their values", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Behavioural Interview Answers

## When To Use
A values or leadership round is next and your stories all say "we". You have a story bank, but you have not decided which story answers which question in this round, or what you will say when the interviewer asks "and what was your part, exactly?". It answers: for this one round, which true story goes where, and where am I thin?

## When Not To Use
With no stories written yet, run Interview Story Bank first: this skill selects and pressure-tests stories and writes no new one. To say the answers out loud against a clock, use Mock Interview.

## Inputs
- Your Interview Story Bank (story IDs S1, S2 and so on) and the round as it stands on your Interview Loop Map, with anything the recruiter said it assesses
- The employer's values page, pasted or linked by you, and the job ad
If you have none of this, I start from three pieces of work you describe in your own words and mark the output as a first draft.

## Approach
Two public methods carry this sheet: STAR as the National Careers Service sets it out (Situation, Task, Action as the steps you personally took, Result), and the US Office of Personnel Management's description of structured interviews, where predetermined questions ask about past behaviour, a hypothetical situation, or both. The judgment: a senior candidate rarely lacks stories; they lack a decision about which story serves which competency, and an "I" inside the Action. The failure it prevents is the answer where a whole team shipped something and the interviewer still cannot tell what you did.

## Workflow
1. Ask at most three questions: which round this is and who runs it, what the recruiter said it assesses, and where the employer's values are written.
2. List the competencies for this round, each with its source: recruiter said, values page, the ad, or "my guess". A guess stays labelled as a guess and becomes a question for the recruiter.
3. For each competency, write the likely past-behaviour prompt ("tell me about a time when") and one hypothetical variant ("what would you do if"). Prepare both: a round can use either form.
4. Match a primary and a reserve story ID to each competency. One story serves at most two competencies in the round. Where no true story exists, mark "no story" and write the honest thing you would say; the cell is never filled with something close enough.
5. Run the "we" pass on each Action: mark every "we" and ask what you did. Keep "we" for what the team did and "I" for your part, with who made the final call. Public employer interview guides ask for the same thing: your direct, individual contribution.
6. For each story, write the follow-ups it invites and your honest answer in one line: what was your part, what would you do differently, who disagreed and what happened, how do you know it worked, what did it cost.
7. Values last: quote each value as a short phrase from the employer's own page and match a story only where the story truly shows it. You show a value through the story; you never recite it back to the interviewer.

## Output Format
```markdown
# Behavioural Round Prep Sheet
**Round:** [name on the loop map] · **Interviewer:** [role] · **Date:** [date] · **Length:** [minutes, as the recruiter said]
## Competencies and stories
| Competency | Source | Past-behaviour prompt | Hypothetical variant | Primary story | Reserve story |
|---|---|---|---|---|---|
| [competency] | [recruiter said / values page / ad / my guess] | [prompt] | [variant] | [S-ID or "no story"] | [S-ID or none] |
## My part in each story
| Story | What the team did ("we") | What I did ("I") | Who made the final call |
|---|---|---|---|
| [S-ID] | [team action] | [your action] | [role] |
## Follow-ups and honest answers
| Story | Follow-up | My answer in one line | Do not stretch |
|---|---|---|---|
| [S-ID] | [question] | [answer] | [fact from the evidence row] |
## Values
| Value, in the employer's words | Story that shows it | How it shows |
|---|---|---|
| [short phrase] | [S-ID or "none honestly"] | [the moment in the story] |
**Gaps:** [competency with no story]: [the honest thing I will say]
## Decision
You decide which story leads for each competency and which gaps you will name plainly, by [date, before the round].
```

## Done When
- Every competency has a source, two prompts, and either a primary story or a named gap.
- No story serves more than two competencies, every Action separates "we" from "I", and each story has at least three follow-ups answered.
- Every value is quoted from the employer's page and matched to a story, or marked "none honestly".

## Quality Bar
- Speaking notes, not a script: you say it in your own words on the day.
- Colleagues appear by role and are never judged, most of all in a disagreement or failure story.
- A number appears only if its evidence row has a source you could show; otherwise the result stays in words. The sheet describes stories and gaps and rates nothing about you.
- A competency with no true story stays marked as a gap; nothing is invented to match an employer's values.

## Next
Run pmjob-work-walkthrough (Portfolio and Project Walkthrough) to prepare the long talk on your work.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
