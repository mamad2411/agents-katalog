---
name: pmjob-execution-case
description: Run a practice prioritisation and execution case on a trade-off question and produce the options with what each costs and who pays, your call and cut written out, notes on your answer against a rubric you can see and a practice log line. Use for "run pmjob-execution-case", "practise a prioritisation question", "execution interview practice", "five things and room for two", "what would you cut", "practise a trade-off question", "the deadline moved, what do you drop", "use RICE in an interview", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Prioritisation and Execution Case

## When To Use
The question is "you have five things and room for two" and you answer by listing all five. An execution or case study round is coming, and you want to practise making the call aloud: what goes ahead, what is cut, who pays for it and what you would watch. It answers: did I decide, or did I describe?

## When Not To Use
Not for an open question about who the user is and what to build: use Product Sense Case. Not for choosing measures or explaining a moved metric: use Metrics Case. This practice starts from options that already exist.

## Inputs
- The round as the recruiter described it, the length they gave you, and a scenario: a real prioritisation call from your own work with details you may share, or "give me a generic one".
- The constraint you find hardest to answer under: less time, fewer people, a dependency, a stakeholder who objects.
If you have none of this, I start from a generic set of options and one constraint, with a time box you set, and mark the output as a first draft.

## Approach
The method is a named trade-off with an owner, supported by RICE from Intercom's public article as one input and never as the answer. That article says scores are not a hard and fast rule: a lower score can go first when it is a dependency or a must-have for certain customers. Public employer interview guides describe a case that covers execution interactively and listen for how you prioritised and on what evidence, a plan built on impact and feasibility, respect for engineering effort, how you balance technical debt against growth, what you do when engineers are stuck, and, for senior designers, how you handle trade-offs with engineering and product counterparts. The failure this prevents: a tidy scoring table, a long justification, and no decision.

## Workflow
1. I ask up to three questions: which scenario, which constraint, and what time box the recruiter gave (you set it, I never assume one). This is practice only, never for use during a real interview.
2. I play a stand-in interviewer: I give the options and the constraint, answer clarifying questions briefly, then stay quiet while you answer in full, in writing or aloud. Work in this order: restate the constraint and the goal it serves; lay the options out; say what each costs and who pays (users, the team, another team, the business, later you); make the call; say what is cut or deferred and how you would tell the people affected; name who you bring in; name the risk you accept and the signal that would make you revisit. The call comes before the long justification.
3. Use RICE only to expose the trade-off: Reach (people or events in a set period), Impact (massive 3, high 2, medium 1, low 0.5, minimal 0.25), Confidence (high 100%, medium 80%, low 50%), Effort in person-months; reach times impact times confidence, divided by effort. Reach is usually unknown in an interview, so say each assumption aloud. Then say one trade-off sentence: "I am choosing [A] over [B], which costs [whom] [what], because [reason]; I would revisit if [signal]." Every cut has an owner who is told.
4. I ask two or three follow-ups, and one always changes a constraint: less time, a dependency slips, a stakeholder objects. Say what changes in your call and what does not.
5. I show the rubric, each row marked present, thin or missing with your words quoted. You redo the one weakest part in your own reasoning; I give no model answer to memorise. I add a log line: date, question, what to practise again.

## Output Format
```markdown
# Prioritisation and Execution Practice Case
Question: [question] | Constraint: [constraint] | Goal it serves: [goal] | Time box: [minutes you set] | Date: [date]
## Options and who pays
| Option | What it costs | Who pays | Your assumptions (labelled as assumptions) |
|---|---|---|---|
| [option] | [cost] | [users / the team / another team / the business / later you] | [reach, impact, confidence, effort as you stated them] |
## The call
- Trade-off sentence: I am choosing [A] over [B], which costs [whom] [what], because [reason]; I would revisit if [signal]. Risk accepted: [risk]
- Cut or deferred: [item, by name] | Who is told, and how: [your words] | Who you bring in: [roles] | After the constraint changed to [new constraint]: [what moved, what stayed]
## Notes on the answer
| Rubric row | Status | Your words as evidence |
|---|---|---|
| Constraint and goal restated | [present / thin / missing] | [quote] |
| Costs named with who pays | [status] | [quote] |
| A call made | [status] | [quote] |
| Something cut or deferred, by name | [status] | [quote] |
| People brought in | [status] | [quote] |
| Risk accepted and the signal to revisit | [status] | [quote] |
| Assumptions stated | [status] | [quote] |
| Adjusted when the constraint changed | [status] | [quote] |
## What to practise again
[Date] | [Question] | [The one part redone, and what to repeat next time]
## Decision
You decide whether to repeat this with a different constraint or move to the next round's practice, by [date].
```

## Done When
- The trade-off sentence is complete: what is chosen, over what, who pays, why, and the signal to revisit.
- At least one option is cut or deferred by name, with who is told.
- Every rubric row has a status and a quote, the weakest part is redone, and the log line is written.

## Quality Bar
- The call is stated before its justification, in one sentence someone could repeat. Any RICE figure is labelled as your assumption. A score never stands in for the argument.
- No user segmentation and no metric tree here: the practice is the call, the cut and who pays.
- The rubric is a stand-in built from public guides, not any employer's scoring sheet. Notes describe the answer, with no number and no verdict on you.
- Practice only: the call and its reasons are yours, and Claude is never used during a real interview.

## Next
Run pmjob-app-critique (App Critique) to practise critiquing a live product.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
