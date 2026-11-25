---
name: firm-problem-statement
description: Writes the client's problem as a point of view in their words (who, needs, because) together with the decision it serves (the question, who decides, by when, what is fixed, what can be reversed), success in their measures, impact in their figures, constraints, out of scope, one How Might We question and the rival test. Use for "run firm-problem-statement", "write the problem statement", "what is their real problem", "which decision is this work for", "my proposals describe me not them", "frame the client's problem", "how might we question for this client", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Problem Statement

## When To Use
You can describe your approach in your sleep and still could not write, in the client's words, what is wrong and what they have to decide about it. Run this after the call and the playback, before any option or price. It answers two questions together: what is the problem as they would sign it, and which decision, taken by whom and by when, is the work meant to serve?

## When Not To Use
To lay out causes or show where an answer could be wrong, use Issue Tree after this. With no call yet, a statement built from the brief alone is a guess; prepare Discovery Call Questions first.

## Inputs
- Your call record (verbatim lines, facts, figures) and the client's reply to your playback, if any
- Your cost of waiting sheet for the impact lines, and their brief for constraints
- What you know about who decides and by when
If you have none of this, I start from your own summary of the call, leave impact blank and mark the statement as a first draft to test with the client.

## Approach
Three ideas are combined. A point of view statement and a How Might We question, common in design practice and described generically: a group, its need, and an insight, then a question that opens routes. The problem definition fields of hypothesis-led consulting (a practitioner guide to problem solving): the question, context, success criteria, scope and constraints. And one decider per decision, the D in Bain's RAPID roles (bain.com/insights/rapid-decision-making). The failure it prevents is a well-put problem with no owner, so the work answers a question nobody has to decide.

## Workflow
1. Ask, in one go: which role or group at the client feels this most? Who decides, and by when? Has the client confirmed or corrected your playback?
2. Set the point of view out in three parts: [who] needs [need, as a verb] because [insight]. Who is a role or group at the client, never your service. The need is a verb such as "to choose" or "to stop losing". The insight comes from a verbatim line or a fact, with its reference.
3. Write the decision frame. The question as a real choice built around an outcome, not around a preferred answer. One decider by role, who must agree, the deadline and what waiting costs. What is already fixed, and which steps could be undone later and which could not. If nobody can name the decider, that becomes the first question for the client, ahead of everything else.
4. Write success in their measures and impact in their figures, copied from the sheet with who gave each. Blanks stay blank with the question beside them.
5. Add constraints and out of scope, each tied to a line in your notes or their brief. Out of scope holds what they said they do not want and what you will not cover.
6. Write one How Might We question that opens several routes and names none of yours, then run the rival test: could this page sit unchanged in another consultant's proposal? If yes, add their words and constraints until it could not.

## Output Format
```markdown
# Problem and Decision Statement
Client: [role or team] · Call: [date] · Playback confirmed: [yes / corrected / no reply]
## Point of view
[Who] needs [need, as a verb] because [insight]. · Source: [verbatim line or fact]
## The decision this serves
| Question | Decides (role) | Must agree | By when | Already fixed | Reversible later? |
|---|---|---|---|---|---|
| [the choice, as an outcome] | [role] | [roles] | [date] | [what is settled] | [which steps yes, which no] |
## Success and impact
| Measure or consequence (theirs) | Figure and unit | Period | Said by (role) |
|---|---|---|---|
| [measure] | [figure, or blank with question] | [period] | [role] |
## Constraints and out of scope
- Constraint: [budget, people, time, systems] · Source: [line]
- Out of scope: [what they do not want / what you will not cover]
## How might we
How might we [question that opens routes]? · Rival test: [passes / fails, and what was changed]
## Decision
[You] decide by [date] whether this goes to [client decider role] to confirm as written, or back with one more question.
```

## Done When
- The "because" traces to a specific line in the call record
- One decider is named by role with a date, or the gap is the first question to the client
- Every figure is the client's with who said it, and blanks are blank
- The page passes the rival test, or says what was changed until it did

## Quality Bar
- "Who" is a role or group, never a comment on a named person's ability
- The decision question does not smuggle in the answer you would like to sell
- Words the client used, not your vocabulary; one page, or it is still two problems
- Their words, their figures and their decider; I invent nothing to make the problem larger, and you decide when it is ready to show them.

## Next
Run firm-issue-tree (Issue Tree) to split the question into parts and see which rest on evidence.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
