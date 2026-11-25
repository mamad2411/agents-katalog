---
name: isd-branching-scenario
description: Drafts a branching scenario script a developer can build from, with numbered decision nodes, options taken from real mistakes with a consequence and feedback for each, and a path map of every route and ending. Use for "run isd-branching-scenario", "write a branching scenario", "script the decision nodes", "they pass every screen and freeze on the real call", "map every path and ending", "turn the expert's incidents into a scenario", "scenario script for the developer", "practice where a wrong choice has a consequence", part of the Claude for Instructional Designers Pack by 90n.
---

# Branching Scenario Script
## When To Use
Learners pass every screen and still freeze on the real call. They can recite the rule; nobody has ever made them choose with something at stake. Use this when the objective is a decision, the expert has given you real incidents, and you need a script with every node, option and route written out before anyone builds.

## When Not To Use
If one short decision is enough, write it as an item in Knowledge Check Questions: a scenario is a chain of linked decisions, and a chain of one is a question. If you want to try a single activity this afternoon before scripting the whole thing, use Interactive Practice Activity.

## Inputs
- The objective this scenario serves, and the expert's incidents, anonymised: the decision points, the common mistakes at each, what happened next.
- Your node budget and where it will be built (your authoring tool, paper, a live discussion).
If you have none of this, I start from one objective and one incident you describe in two lines, and mark the output as a first draft.

## Approach
Merrill's First Principles of Instruction (2002, Educational Technology Research and Development, ERIC EJ657839) hold that learning is promoted when people work on a real problem and apply what they were shown. So the script is built from one real case and the mistakes people make in it. The judgement is where to branch. The failure this prevents: a tree that doubles at every choice, lands on the developer's desk with more endings than anyone can build, and is quietly flattened into a quiz with a story pasted on top.

## Workflow
1. Ask up to three questions: which objective and which incident to build from, how many nodes you can afford to build ([node budget you set]), and who confirms the facts and by when.
2. Write the setup in the learner's work language: who they are in the story, where, what is at stake, what they can see. Mark the case and every character fictional. Activation and demonstration get one line each here; the scenario is the application.
3. Lay the spine first: the best path as a chain of nodes (N1, N2, N3), one per point where the expert's notes show a real choice. A node where everyone would do the same thing is narration, so fold it into the situation text.
4. Give each node three or four options: the right call and the real mistakes from the expert's notes, each tagged with the mistake it reflects. A mistake nobody makes is not an option. If the notes hold only one real mistake, write two options, not a filler.
5. For every option write the consequence the learner sees in the story (the customer's reply, the ticket that reopens), then feedback that says why, then a "goes to". Branch (N2a, N2b) only where the mistake changes the outcome; elsewhere show the consequence and rejoin the spine. Stay inside your budget and say where I trimmed.
6. Build the path map: every route from N1 to an ending, each ending typed good, recoverable or poor. Check for dead ends, loops and nodes no route reaches, and check the right call is not always the longest or the first option.
7. List every rule, number and step used, with its node, for the expert. Where the notes are silent I write `[to confirm with the expert]`; I never fill the gap with plausible detail.

## Output Format
```markdown
# Branching Scenario Script
Objective: [objective] | Source incident: [note ref, anonymised] | Node budget: [number you set] | Case and characters: fictional
## Setup
[Who the learner is in the story, where, what is at stake, what they can see]
Before the scenario: [one recall question] | Worked example: [one similar case with the expert's reasoning, or "none"]
## Nodes
| Node | Situation text, ready to build | Option | Mistake it reflects | Consequence shown in the story | Feedback (why) | Goes to |
|---|---|---|---|---|---|---|
| N1 | [what the learner sees and hears] | A [option text] | [right call] | [what happens] | [why] | [N2] |
| N1 | | B [option text] | [mistake, note ref] | [what happens] | [why] | [N1a, or rejoins at N2] |
## Path map
| Route | Nodes in order | Ending | Type | What the learner sees at the end | Question about their own work |
|---|---|---|---|---|---|
| R1 | [N1, N2, N3] | [E1] | [good, recoverable or poor] | [closing situation] | [how would you handle this next week?] |

Trimmed to fit the budget: [branches cut or rejoined, and why]
## Facts for the expert
| Node | Rule, number or step used | Source | Confirmed |
|---|---|---|---|
| [N1] | [claim] | [note ref or "to confirm with the expert"] | [yes, no, changed] |
## Decision
The expert, by role, confirms the facts and that each wrong option is a real mistake, by [date]. The designer decides whether the script goes to storyboard and what is trimmed, by [date].
```

## Done When
- Every option has a consequence, feedback that says why, and a "goes to".
- Every wrong option names a mistake from the expert's notes.
- The path map lists every route, with no dead end, no loop and no orphan node, inside the budget and with the trims stated.
- Every fact is listed with its node, and the case is marked fictional.

## Quality Bar
- The setup reads like a real shift, with the time pressure and the missing information left in.
- The consequence comes first and in the story; the feedback then gives the reasoning, never "Correct" or "Try again" alone.
- A recoverable ending lets the learner repair the mistake, as the job would.
- No real person, customer or incident can be recognised in the case.
- Claude drafts the branches; the mistakes come from your expert, the characters are marked fictional, and choices are practice, never a record about a learner.

## Next
Run isd-storyboard-template (E-Learning Storyboard Template) to put the scenario and the rest of the course on screens.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
