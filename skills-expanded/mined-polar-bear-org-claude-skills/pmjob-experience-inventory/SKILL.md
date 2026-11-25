---
name: pmjob-experience-inventory
description: Interviews you role by role, one question at a time, and writes your Career Evidence Inventory with one evidence row per piece of work, strengths backed by two rows and a do-not-claim list. Use for "run pmjob-experience-inventory", "interview me about my career", "I cannot remember what I did in that role", "list what I have really done", "build my evidence rows", "what did I decide in that job", "career inventory before interviews", "find proof for my resume", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Career Evidence Inventory

## When To Use
Fifteen years of work and you cannot remember what you did in the role before last. The launches come back; the decisions, the project you stopped and the team you unblocked do not. Run this before any story, resume line or profile claim, to answer one question: what did I do, what did I decide, and how would I show it?

## When Not To Use
If the rows exist and you need spoken answers, run Interview Story Bank. If you need lines for the page, run Product Resume Bullets. This skill records and does not polish.

## Inputs
- Your resume or a rough list of roles with dates, newest first
- Anything that shows a result and that you may keep: a launch note, a review deck, a research report, an email, your own record
- The roles you are aiming at, if you know them
If you have none of this, I start from your current role and the last piece of work you remember, and mark the output as a first draft.

## Approach
The section list comes from the brag document described on jvns.ca (June 2019), and the questions from The STAR method guide of the National Careers Service: Situation, Task, Action, Result. The brag document's point is that hard-to-quantify work is the work most likely to go unnoticed, so I ask for it on purpose. Two columns are added for experienced people: scope and the decision. The failure this prevents: an inventory written from memory in one evening, which keeps five launches and loses the judgement behind them.

## Workflow
1. Ask up to three questions: which roles to cover and how far back to go in detail, which roles you are aiming at (fine if unsure), and what is under a confidentiality duty and stays out.
2. Walk the roles newest first, one question at a time, with one follow-up before moving on. Older roles get one or two rows; you set the depth.
3. In each role, prompt through six sections: goals you were given; projects and launches; collaboration and mentoring; design and documentation (specs, strategy docs, design system work, research); team and company building (hiring, process, rituals); what you learned. Ask directly for the quiet work: a team unblocked, a project stopped, a decision not to build.
4. For each piece of work, ask STAR as questions: the situation, the task that was yours, the action you personally took, the result and what you gained. Then ask for scope (team, users or surface affected, in words unless sourced) and the decision (the call you made or shaped, and who made the final call).
5. Write one evidence row per piece of work. "How you know" is a source you could show or "memory only". No number goes in a row without a source. A result the team produced is written as the team's, with your part beside it.
6. Name a strength only where two or more rows show it, with the row IDs. One row gives "possible", nothing more.
7. Build the do-not-claim list: team results, decisions made by others, numbers with no source, anything confidential. Your own words stay verbatim in the notes.

## Output Format
```markdown
# Career Evidence Inventory
Updated: [date] · Roles covered: [list] · Status: [first draft / full]
## Interview notes
[Role, piece of work]: [your words, verbatim, short]
## Evidence rows
| ID | What | When | Your part | Scope | The decision | What changed | How you know |
|---|---|---|---|---|---|---|---|
| E1 | [piece of work] | [dates] | [what you did, "I"] | [team, users or surface, in words unless sourced] | [the call, and who made the final call] | [change, the team's result named as the team's] | [source you could show / memory only] |
## Strengths
| Strength | Rows that show it | Status |
|---|---|---|
| [strength] | [E1, E4] | [backed / possible] |
## Do-not-claim list
- [team result, someone else's decision, unsourced number or confidential item] · [why it is not yours to claim]
## Decision
You decide which "memory only" rows to find a source for and which rows go forward to the story bank, by [date].
```

## Done When
- Every role you chose has been asked about across all six sections, even where the answer was "nothing"
- Every row has a scope, a decision and a "how you know" entry
- Every figure has a source, or the result is in words
- Each named strength lists at least two row IDs, and the do-not-claim list is written

## Quality Bar
- One question at a time; no questionnaire in one message.
- "I" for your part, the team by role for theirs. Colleagues, managers and customers appear by role and nobody's contribution is judged.
- No rounding, no estimating, no upgrading a title or a scope.
- No employer confidential detail. A Project can keep the inventory as the file later skills read; pasting it into a chat works too.
- Only what you did and can describe in an interview; no row, result or number is added for you.

## Next
Run pmjob-story-bank (Interview Story Bank) to turn the rows into stories you can tell.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
