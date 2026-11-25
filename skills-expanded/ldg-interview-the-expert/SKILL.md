---
name: ldg-interview-the-expert
description: Prepares an expert interview built on one real incident, with questions in three passes, then turns your notes into a decision-point table, a common-mistakes list, exceptions and scenario seeds. Use for "run ldg-interview-the-expert", "SME interview", "SME interview questions", "subject matter expert interview", "get the know-how out of the expert", "what questions do I ask the SME", "the expert only gives me the standard process", "structure my expert interview notes", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Interview the Expert

## When To Use
The expert gives you the standard workflow but solves real cases with years of intuition, and the intuition is the part a newcomer needs. Use this once you know which actions the training must change and before anyone writes a scenario. It answers one question: what does the expert see and decide that the procedure leaves out?

## When Not To Use
If nobody has agreed what people must do differently on the job, run Map the Actions first, or the interview has no target and the expert's hour is spent on a tour of the subject. If you need every task of the role listed and sorted, that is Break Down the Task; this skill goes deep on the hard decisions inside a few of them.

## Inputs
- The task or action the interview covers, taken from your action map or task list
- The expert's role, the time you have with them, and whether a second expert can be asked
- Documents the expert already shared and, after the interview, your raw notes or transcript
If you have none of this, I start from one task and one expert role and mark the output as a first draft.

## Approach
Incident-based expert interviewing, described from cognitive task analysis research: ask about one real, recent case and walk through it several times, each pass deeper. Experts no longer hear themselves think, so a general question returns the procedure, tidy and incomplete. A specific case returns the detail that mattered: the reading that looked slightly off, the option they dropped, the shortcut a newcomer takes. The failure this prevents is the course that passes every review and still leaves a new person frozen at the first case that does not match the flowchart. Projects (redesigned, beta on select plans) is optional to keep interview notes and sources together.

## Workflow
1. Ask up to three questions: which task the interview covers, how long you have with the expert, and whether a second expert is available.
2. Write the opening request: one specific, recent, real incident on that task that went wrong, was hard, or would trip a newcomer. Never "the typical case", which is how you get the manual read back to you.
3. Pass one, the story: the expert tells it start to finish and you stay quiet. Pass two, the timeline: rebuild it in order together and mark every point where a choice was made, including the ones the expert calls obvious.
4. Pass three, the probes, asked at each marked point: what did you notice first, what options did you weigh, what told you which one, what would a newcomer have done, what happens if they get it wrong. Drop a probe when the answer turns into policy; go back to the case.
5. Close with common mistakes and exceptions ("when does the standard process not apply?"). Each one becomes a one-line scenario seed.
6. Plan the repeats: more incidents on the same task and, where possible, the same questions with a second expert. Where two experts disagree, mark it and record both; do not average them.
7. After the interview a person ran, paste your notes. I sort them into the decision-point table, remove every colleague and customer name, flag gaps as questions to take back, and leave the "confirmed" column empty for the expert.

## Output Format
```markdown
# Expert Interview Guide and Notes
## Set-up
Task: [task or action] | Expert role: [role] | Time: [duration] | Second expert: [yes / no] | Interviewer: [name]
## Questions in three passes
| Pass | Question | What it is for |
|---|---|---|
| Story | "Tell me about the last time [task] [went wrong / was hard]." | [A real case, told whole] |
| Timeline | [Question that rebuilds the order and marks the choices] | [Finds the decision points] |
| Probes | [Question per decision point] | [Cue, options, newcomer's move, consequence] |
## Decision points
| Cue the expert noticed | Decision | What a newcomer does instead | Consequence | Source incident | Confirmed by the expert |
|---|---|---|---|---|---|
| [Cue] | [Decision] | [Mistake] | [Consequence] | [Incident ref, anonymised] | [Yes / changed / open] |
## Mistakes, exceptions and scenario seeds
| Common mistake or exception | Scenario seed | Experts agree? |
|---|---|---|
| [Mistake, or when the process does not apply] | [One-line situation] | [Yes / disagree, both views noted] |

Still to ask the expert: [each gap in the notes, as a question]
## Decision
[Expert name] confirms or corrects every decision point by [date]; [L&D lead name] decides which seeds go forward and who settles any disagreement between experts.
```

## Done When
- Every question asks about a real incident, none about the usual way of working
- Each decision point has a cue, a decision, a newcomer's mistake, a consequence and a source incident
- Every scenario seed traces to a mistake or an exception said in an interview
- No row is marked confirmed unless the expert confirmed it

## Quality Bar
- Probes ask what the expert noticed and weighed, never "what is the rule"
- Nothing is added to the notes: a gap becomes a question, never a plausible guess
- Incidents are anonymised; no colleague or customer is named
- Claude prepares the questions and structures your notes; a person runs the interview, and the expert confirms every decision point

## Next
Run ldg-break-down-the-task (Break Down the Task) to place these decisions in the full list of what the role does.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
