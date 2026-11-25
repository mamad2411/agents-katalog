---
name: adopt-ai-adoption-brief
description: Turns "get everyone using AI" into an adoption brief with one observable work change per role, what stops as well as starts, and the sponsor and decision owner. Use for "run adopt-ai-adoption-brief", "AI adoption brief", "we need everyone using AI", "define the AI rollout", "what should people do differently with AI", "scope an AI adoption programme", "AI adoption plan first step", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Adoption Brief

## When To Use
The instruction is "get everyone using AI" and nobody has said what anyone should do differently on Monday. You have a tool, a sponsor and a deadline, and no sentence that a person in a role could read and recognise as their own work. This skill answers one question: what exactly changes, for which role, and who decides.

## When Not To Use
Not when people still cannot name a task AI would help with: run AI Use Case Map first, then come back and pick one change per role from it. Not for designing the test of a change either: that is AI Pilot Plan, which carries the measures and the stop rule this brief leaves out.

## Inputs
- The instruction as it was given to you, word for word, and who gave it.
- The roles in scope, with one or two tasks per role where the problem shows (a real example, sanitised), and who can approve the change.
- What was observed of the problem and by whom, what is only assumed, and any existing rule that makes part of this mandatory.
If you have none of this, I start from the instruction and one role, and mark the output as a first draft.

## Approach
The brief specifies the target behaviour before anything else is planned, as the Behaviour Change Wheel does (Michie, van Stralen and West, 2011, an open access article in Implementation Science), and frames it with the three questions of the Model for Improvement from the Institute for Healthcare Improvement. The judgment is in refusing the slogan: "be AI-first" cannot be trained, supported or checked, while "the analyst drafts the first version of [report] with AI and checks every figure against [source] before sending" can. The failure this prevents is the programme that reports a licence count for a year because nobody ever wrote down what the work was supposed to look like.

## Workflow
1. Ask up to three questions: what problem is this meant to fix and what has been observed of it, which roles are in scope and which are out, and who sponsors the change and who decides. If the user has already answered, do not ask again.
2. Separate the problem from the preferred answer. Write what was observed, with its source and date, apart from what is assumed. If the only evidence is "we bought the tool", say so in the brief: that is a reason to check, not a problem statement.
3. Write one behaviour statement per role: who (the role), does what (the action), on which task, when (the trigger), where or in which tool, and how often. Test each one: would two people reading it recognise the same behaviour? If not, rewrite it. One change per role; a second change waits for a second brief.
4. For each change, write what stops as well as what starts. If the old step stays, people now do both, and the change will be dropped the first busy week.
5. Answer the three questions: what are we trying to accomplish, how will we know that a change is an improvement, what change can we make that will result in improvement. Write the expected benefit as a hypothesis, and beside it what would show the change is unnecessary or harmful.
6. Separate what is mandatory (an existing rule, quoted with its source) from what is proposed. Set scope and exclusions, including tasks and material where AI is not to be used. Name the sponsor and the decision owner; where they are unknown, write "to confirm" and mark what depends on it as pending.
7. Close with one baseline observation someone can make this week, and a date to check the brief with people who do the work. They can change the wording, the task and the frequency, and the brief records what they changed.

## Output Format
```markdown
# AI Adoption Brief
Status: [first draft / checked with people in the role on [date]] · Prepared for: [sponsor role]
## The problem and its evidence
- Observed: [observation], from [source, date]
- Assumed, not yet checked: [assumption]
## The three questions
- What are we trying to accomplish: [one sentence]
- How will we know that a change is an improvement: [what would be seen in the work, at team level]
- What change can we make that will result in improvement: [the changes below]. Hypothesis: [expected benefit]. Unnecessary or harmful if: [what would show it]
## One work change per role
| Role | Action | Task | Trigger | Where or in which tool | How often | What stops |
|---|---|---|---|---|---|---|
| [role] | [checkable action] | [task] | [when] | [place or tool] | [frequency] | [the old step that ends] |

## Scope, exclusions and what is mandatory
- In scope: [roles, tasks]. Out of scope: [roles, tasks, material where AI is not used, and why]
- Mandatory: [existing rule and its source]. Proposed: [item], to be approved by [role]
## First check with the people affected
- Baseline observation: [what, by whom, when]
- Check with [roles who do the work] on [date], led by [name]. What they changed: [to fill in after the check]
## Decision
[Sponsor name] decides by [date] whether the brief goes ahead as written, is changed, or stops, after [decision owner name] has checked it with people in each role.
```

## Done When
- Every role in scope has exactly one behaviour statement, with all six parts filled or marked "to confirm" and a "what stops" entry, even if that entry is "nothing stops, and here is the cost of that".
- The benefit is written as a hypothesis, with what would disprove it.
- Sponsor, decision owner and the date of the check with people in the role are named.

## Quality Bar
- No slogan survives: "use AI more" and "be AI-first" are replaced by an action on a task, written per role and never per named person, with no target expressed as a share of people to be counted.
- Nothing is invented: no figure, benefit, quote or view of the people affected that the user did not supply. Gaps are bracketed.
- Mandatory and proposed are never mixed, and a rule is quoted from its source. Any legal, data protection or employment point: check with a qualified adviser.
- One page, with no measures table and no stop rule: those belong to the pilot.
- The brief names a work change, never a usage target per person; the sponsor decides and people affected check it first.

## Next
Run adopt-ai-starting-point-survey (AI Starting Point Survey) to ask the people affected where they are before planning anything for them.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
