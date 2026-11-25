---
name: pmjob-app-critique
description: Run a practice critique of an app you choose and produce the critique in order (users, business, flows walked, what works and fails against the usability heuristics, one change and its cost), notes on your answer against a rubric you can see and a practice log line. Use for "run pmjob-app-critique", "practise an app critique", "app critique interview practice", "critique this app with me", "pick a product you like and improve it", "heuristic review of these screenshots", "product thinking interview practice", part of the Claude Guide for Product Interviews Pack by 90n.
---

# App Critique

## When To Use
You practise by criticising random apps and it never turns into a method. A critique or product thinking round is coming, for a design or a product role, and you want to walk one live product aloud in a fixed order and see which parts of your critique held up. It answers: was that a point of view on a product, or a list of dislikes?

## When Not To Use
Not for an open question with no product in front of you: use Product Sense Case. Not for presenting your own work: use Portfolio and Project Walkthrough. This practice is for someone else's live product, seen through its flows.

## Inputs
- The app you choose, and screenshots of the flows you upload, or the app open beside the chat while you describe each screen.
- The round as the recruiter described it, the length they gave you, and your role, product manager or product designer, so the weight on visual craft is right.
If you have none of this, I start from an app you know well, described from memory, with a time box you set, and mark the output as a first draft.

## Approach
The lens is the 10 Usability Heuristics from NN/g, used inside a users, business, flows, change order that is common practice with no single originator. NN/g's guidance on design critiques adds two rules: tie every observation to the goal of the design, and say what works as well as what does not. Public employer interview guides describe product thinking follow-ups that ask how well you understand products you use and the business value they provide, craft follow-ups on design proficiency, and workshops on how you weigh trade-offs when constraints change. Product managers meet the same round as "pick a product you like and improve it", with less on visual craft. The failure this prevents: opening at screen three with ten labels read aloud and no view on which one matters.

## Workflow
1. I ask up to three questions: which app and how I will see it, your role, and what time box the recruiter gave (you set it, I never assume one). This is practice only, never for use during a real interview.
2. I play a stand-in interviewer and stay quiet while you critique in full, in writing or aloud. I do not operate the app; a screen you have not shown or described is noted as "not seen", never guessed. Work in this order: users and the job the app does for them; the business, meaning how it earns its place and what it must protect; two or three flows chosen for a reason (first run, the core task, one edge such as an error or an empty state), walked step by step; what works and what fails; the one change you would argue for, what it costs, who would object and how you would check it helped.
3. Each observation names the screen, what happens, the heuristic it touches and why it matters for this user. The ten: visibility of system status; match between the system and the real world; user control and freedom; consistency and standards; error prevention; recognition rather than recall; flexibility and efficiency of use; aesthetic and minimalist design; help users recognize, diagnose and recover from errors; help and documentation. Three or four well-argued observations beat ten labels. Rank the problems and commit to one change. "I do not like it" is not an observation; the critique is of the product, never of the people who made it.
4. I ask two or three follow-ups: challenge the priority, change a constraint, ask "why that one".
5. I show the rubric, each row marked present, thin or missing with your words quoted. You redo the one weakest part in your own reasoning; I give no model answer to memorise. I add a log line: date, app, what to practise again.

## Output Format
```markdown
# App Critique Practice Notes
App: [app] | Seen through: [screenshots / described live / memory] | Role: [role] | Time box: [minutes you set] | Date: [date]
Users and the job the app does for them: [your words] | How it earns its place, and what it must protect: [your words]
## Flows walked
| Flow, and why you chose it | Screen | What happens | Heuristic touched | Works or fails, and why it matters for this user |
|---|---|---|---|---|
| [first run / core task / edge] | [screen, or "not seen"] | [observation] | [heuristic name] | [your words] |
## The one change
- Priority among the problems: [your ranking and reason] | Change you would argue for: [change] | Cost: [cost] | Who would object: [role] | How you would check it helped: [check]
## Notes on the answer
| Rubric row | Status | Your words as evidence |
|---|---|---|
| Users and their goal | [present / thin / missing] | [quote] |
| Business model or purpose | [status] | [quote] |
| Flows chosen with a reason | [status] | [quote] |
| Observations tied to a screen and a heuristic | [status] | [quote] |
| Something that works | [status] | [quote] |
| Priority among the problems | [status] | [quote] |
| One change with its cost and who would object | [status] | [quote] |
| How you would check it | [status] | [quote] |
## What to practise again
[Date] | [App] | [The one part redone, and what to repeat next time]
## Decision
You decide whether to repeat the critique on a second app or move to the next round's practice, by [date].
```

## Done When
- Users and business come before any observation, in your words.
- Each observation has a screen, a heuristic by name and a reason tied to this user, and at least one says what works.
- One change is chosen with its cost, every rubric row has a status and a quote, the weakest part is redone, and the log line is written.

## Quality Bar
- Heuristics are a lens for your argument, not a checklist to complete. Unused heuristics are simply left out.
- Nothing is recorded about a screen you did not show or describe.
- The rubric is a stand-in built from public guides, not any employer's scoring sheet. Notes describe the answer, with no number and no verdict on you.
- Practice only: you walk the flows and form the view yourself, and Claude is never used during a real interview.

## Next
Run pmjob-behavioural-answers (Behavioural Interview Answers) to move from cases to conversations.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
