---
name: isd-sme-interview-script
description: Prepares an expert interview from start to finish, with a pre-interview note that asks for one real case, incident questions in three passes, a live notes sheet, a decision-point table and the follow-up message. Use for "run isd-sme-interview-script", "the expert sent me slides instead of answers", "SME interview script", "what do I ask the subject matter expert", "the SME sent pages an AI wrote", "prepare my expert interview", "turn my interview notes into decision points", "follow-up message to the SME", part of the Claude for Instructional Designers Pack by 90n.
---

# SME Interview Script

## When To Use
You asked the expert for answers and got a slide deck, or pages an AI wrote, and none of it says what they do when the task gets hard. Use this before you book their time, and again once your notes are on the page. It answers one question: what does the expert notice and decide that is written nowhere?

## When Not To Use
If the trouble is the pile the expert already sent, run Source Content Triage; this script is for what is not in the pile. If the expert is reading your draft and no longer telling you how the work goes, that is SME Review Round.

## Inputs
- The task the interview covers, the expert's role, the time you have with them, what they already sent (including any pages they say an AI drafted), and your raw notes if the interview has happened
If you have none of this, I start from one task and one expert role and mark the output as a first draft.

## Approach
This is an incident-based interview, a technique from research on how experts make decisions: one real case, walked through three times, each pass deeper. Experts no longer see the steps they do without thinking, so "how do you usually do it?" returns the manual, and the manual is what the slides already say. The failure it prevents is a course built on the written procedure while the floor works from four unwritten judgment calls. You run the conversation; the script only makes sure the hour is spent on the case.

## Workflow
1. Ask up to three questions: which task the interview covers, how long you have with the expert, and whether a second case or a second expert is possible.
2. Draft the pre-interview note. It asks for one real, recent case where the task went wrong or was hard, and it says what not to prepare: slides. Never ask for "the typical case". If you plan to record, the note asks first; where rules apply, check with a qualified adviser.
3. Deal with what arrived instead of answers. For slides or AI-written pages, write one opening question per claim: which case does this come from? A claim the expert cannot tie to a case goes on the list to confirm, and you decide which claims are worth interview time.
4. Write the three passes. Story: the expert tells it start to finish, and you do not interrupt. Timeline: rebuild it step by step and mark every point where a choice was made. Probes at each choice: what did you notice first, what options did you weigh, what told you which one, what would a newcomer have done, what happens if they get it wrong. Then the close: the common mistakes, then "when does the standard process not apply?". Each answer becomes a scenario seed of one line, no longer.
5. Lay out the live notes sheet you fill while listening, with the expert's own words for cues kept as said. After the interview you paste the notes; I structure them into the decision-point table with every case anonymised, and I invent nothing to fill a gap: a missing cell reads `[to confirm with the expert]`.
6. Draft the follow-up message that plays the decision points back for the expert to confirm or correct. Where two cases or two experts disagree, both versions are shown and marked, never averaged.

## Output Format
```markdown
# SME Interview Script
## Before the interview
Task: [task] | Expert role: [role] | Time: [duration you set] | Second case or expert: [yes / no]
Note to the expert: [Please bring one real, recent case where [task] went wrong or was hard. No slides needed. Recording: [asked / not recording]]
## Questions in three passes
| Pass | Question | What you listen for |
|---|---|---|
| Story | "Tell me about the last time [task] was hard, from the start." | [The case, uninterrupted] |
| Timeline | "What happened next? Was there a choice there?" | [Each decision point, in order] |
| Probes | [The five probes, per decision point] | [Cue, options, the tell, the newcomer's move, the cost] |
| Close | "Which mistakes do you see most? When does the standard process not apply?" | [Mistakes and exceptions] |
## Live notes sheet
| Time in the case | What happened | Choice made? | Expert's words for the cue | To probe |
|---|---|---|---|---|
| [Point] | [Event] | [yes / no] | [Words as said] | [Question] |
## Decision points
| Cue | Decision | Common mistake | Consequence | Source case (anonymised) | Confirmed by the expert |
|---|---|---|---|---|---|
| [Cue] | [Decision] | [Mistake] | [Consequence] | [Case A] | [yes / corrected / open] |
## Scenario seeds
1. [One line: the situation, and the mistake or exception it comes from] | Experts agree: [yes / disagree, both versions kept]
## Follow-up message
[Thank you. Here are the decision points I took from your case. Please confirm or correct each one by [date].]
## Decision
[Expert name, role] confirms or corrects every decision point by [date]; [designer name] decides which seeds go forward, and [name, role] rules where two experts disagree.
```

## Done When
- The note asks for one real, recent, hard case and tells the expert not to prepare slides
- Every decision point has a cue, a decision, a mistake, a consequence and a source case
- Every seed traces to a mistake or an exception the expert named, and every disagreement is marked

## Quality Bar
- Probes ask what the expert noticed and weighed, never "what is the rule?"
- Cases are anonymised: no colleague, customer or learner is named, and nothing is recorded without asking first
- Claude prepares the questions and structures your notes; you run the interview, and the expert confirms every decision point.

## Next
Run isd-source-content-triage (Source Content Triage) to sort the material the expert did send.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
