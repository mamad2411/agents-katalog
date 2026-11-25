---
name: pdes-design-sameness-check
description: Builds a Design Sameness Check for one design, with an inventory of its default choices (typeface, colour and gradients, backgrounds, layout pattern, radius and shadow, iconography, motion, phrasing), each marked by you as chosen on purpose or inherited from a default, up to three places for a real decision, and a list of what stays standard because users expect it. Use for "run pdes-design-sameness-check", "my design looks like every other product", "why does this look generic", "which of these choices are defaults", "everything generated looks the same", "make this recognisable as ours", "check for the default look", part of the Claude for Product Designers Pack by 90n.
---

# Design Sameness Check

## When To Use
The screen looks fine and could belong to any product, and three other teams' generated designs look just like it. Nothing is wrong enough to fix, which is the problem. It answers: which visible choices on this screen did anyone ever decide, and where would a real decision make the product recognisable?

## When Not To Use
If nothing written says what the product stands for, write Design Principles first, because there is nothing to check a choice against. If you want to know whether the design works, use Design Self-Critique. This check says nothing about quality.

## Inputs
- One screen or flow, as a frame list, exported styles or a plain description of what is on it
- Where it came from: a tool's starter file, a template, a generated draft, the design system, or a blank canvas
- The product's principles and brand lines, pasted, if they exist
If you have none of this, I start from your description of the screen and mark the output as a first draft.

## Approach
Anthropic's account of why model output converges on a default look and how direction changes it (Improving frontend design through skills, 12 November 2025), with the point in Nielsen Norman Group's State of UX 2026 that producing interface screens is now cheap. That article is about code output, and it names four directions: typography, colour, motion and backgrounds. The eight rows and the chosen or inherited marks are this skill's own design, not the article's. I list and ask; I never call a choice good, bad, generic or tasteful. The failure it prevents is the redesign that swaps one default typeface for another and calls it a point of view.

## Workflow
1. Ask three questions: which screen or flow, where did its starting point come from, and what do the principles and the brand say (paste them)?
2. Fill the inventory in eight fixed rows: typeface; colour and gradients; backgrounds; layout pattern (cards, hero); radius and shadow; iconography; motion; phrasing. Each row states what is on the screen in neutral words: the value, the pattern, the sentence.
3. For each row I ask one question: did you decide this, or did it arrive with the tool, the template or the draft? You give one of two marks, chosen on purpose or inherited from a default. If you cannot name the reason, the row is inherited; that is information, not a fault.
4. For every chosen row, write the reason and the principle or brand line it rests on. Where the reason cites neither, the cell reads "[no principle cited]" and stays that way.
5. You pick at most three inherited rows where a real decision would make the product recognisable. For each I write the question to answer and the principle it should answer to, never the answer.
6. Write the "stays standard" list: the conventions users expect (where navigation sits, how forms behave), kept on purpose. Being different is not the goal; a decided default is still a decision.

## Output Format
```markdown
# Design Sameness Check
**Screen or flow:** [name] | **Starting point:** [tool default, template, generated draft, design system, blank canvas] | **Date:** [date]
## Inventory
| Row | What is on the screen | Mark (designer) | Reason, with principle or brand line | Where it came from |
|---|---|---|---|---|
| Typeface | [what is used] | [chosen on purpose or inherited from a default] | [reason, or "[no principle cited]"] | [source] |
| Colour and gradients | [what is used] | [mark] | [reason] | [source] |
| Backgrounds, layout pattern, radius and shadow, iconography, motion, phrasing | [one row each] | [mark] | [reason] | [source] |
## Where a real decision would show (three at most)
| Row | The question to answer | Principle or brand line it answers to | Who is asked |
|---|---|---|---|
| [row] | [question] | [principle] | [role] |
## Stays standard, on purpose
- [convention users expect, and why it stays]
## Decision
[Designer] decides by [date] which of the picked rows change and answers the question for each; where a row touches the brand or the design system, [brand owner or system owner] confirms by [date].
```

## Done When
- All eight rows are filled, each with a mark you gave, not one I assumed
- Every chosen row has a reason, and missing principles show as "[no principle cited]"
- No more than three rows are picked for a real decision, each with a question and not an answer
- The "stays standard" list exists and names at least the navigation and form conventions

## Quality Bar
- Neutral description only: what is there, never whether it is good
- No comparison with another designer's or another team's work by name
- An inherited row is not a failure, and a chosen row is not a compliment
- Any change that follows still has to meet contrast and readability checks and be seen by real users
- Claude lists and asks, and gives no taste verdict; you decide what to change

## Next
Run pdes-critique-session-brief (Critique Session Brief) to take the work to peers.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
