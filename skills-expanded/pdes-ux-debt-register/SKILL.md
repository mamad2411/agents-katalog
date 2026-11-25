---
name: pdes-ux-debt-register
description: Builds a UX Debt Register for your product area with one row per issue written as user impact, a value against effort table, the short list to propose for the next planning round and the issues knowingly left. Use for "run pdes-ux-debt-register", "UX debt", "design debt backlog", "prioritise UX fixes", "small UX issues never get fixed", "value vs effort", "UX debt list", "which UX fixes first", part of the Claude for Product Designers Pack by 90n.
---

# UX Debt Register

## When To Use
The broken empty state and the copy nobody rewrote never make the plan, because no single fix is ever important enough. Run it for the product area you design, and keep it going as work ships, so the small issues are seen together when planning comes round. It answers: what hurts users today, how hard is each fix, and which few do you propose next?

## When Not To Use
If the issues come from one round of test sessions and need writing up, use Usability Test Findings; the register is the standing list across sources. One broken flow with a known fix is a ticket, not a register.

## Inputs
- Issues from real sources: test notes, support reports, survey answers, analytics, review notes (names removed)
- Any existing list or tickets, and the journey stages your team uses
- When the next planning round is and who owns the plan, by role
If you have none of this, I start from the issues you can name from memory, mark every row `[evidence needed]` and the output as a first draft.

## Approach
This follows identifying and prioritising UX debt as Kaley describes it for Nielsen Norman Group (2018, nngroup.com/articles/ux-debt/): log each issue from the user's side, where it occurs, how often, who reported it and the effort to fix it, then set user value against effort. The page gives no formula, so there is none here, and it ranks problems in existing features above new ones. The failure it prevents: the content issue that hurts most gets dropped at every planning round, because nobody wrote down how often people hit it.

## Workflow
1. Ask three questions: what evidence you have, which journey stages the team uses, and who in engineering sets effort with you before which planning round.
2. Write one row per issue as user impact ("people cannot tell which plan they are on"), not as a screen fault. Content and accessibility issues count as debt too. Fill the journey stage, the frequency from the evidence or `[unknown]`, the evidence source, and reported by: user, team or stakeholder, never a named person.
3. Set effort with engineering as low, medium or high, covering design and development. Set user value as low, medium or high from the evidence. A row with no evidence is flagged and stays out of the ranking.
4. Place the evidenced rows in the value against effort table. High value with low effort goes first; a medium is placed by you and engineering with the reason written down.
5. Draft the short list to propose, sized to how the team pays debt down (a few items each sprint or every other sprint, or a regular clean-up sprint). Note where a fix sits in code already being changed for technical debt.
6. Put everything else in "knowingly left" with why it waits and the trigger to revisit. Keep the register and update it when a fix ships or new evidence arrives.

## Output Format
```markdown
# UX Debt Register
**Product area:** [area] | **Kept by:** [designer, by role] | **Updated:** [date] | **Planning round:** [date]
## Register
| ID | User impact | Journey stage | Frequency | Evidence source | Reported by | Value | Effort | Flag |
|---|---|---|---|---|---|---|---|---|
| [UXD-1] | [what people experience] | [stage] | [from evidence or unknown] | [test, support, survey, analytics, review] | [user / team / stakeholder] | [L / M / H] | [L / M / H] | [evidence needed / none] |
## Value against effort
| | Low effort | High effort |
|---|---|---|
| High value | [IDs: propose first] | [IDs: propose as planned work] |
| Low value | [IDs: fix when the code nearby is open] | [IDs: leave, with a trigger] |
## Short list to propose
| ID | Why now | Pairs with technical debt | Effort agreed with |
|---|---|---|---|
| [ID] | [reason from the evidence] | [yes, which work / no] | [engineering role] |
## Knowingly left
| ID | Why it waits | Revisit when |
|---|---|---|
| [ID] | [reason] | [trigger or date] |
## Decision
[Product manager] and [engineering lead] decide which short list items go into the plan for [planning round] by [date].
```

## Done When
- Every row names user impact, stage, evidence source and an effort set with engineering, or carries a flag
- Every short list row has evidence behind it, and no flagged row sits in the value against effort table
- Every issue not on the short list sits in "knowingly left" with a reason and a trigger, and the decision line names who owns the plan and a date

## Quality Bar
- Issues describe the product, never who designed or built the part that hurts, and no reporter is named
- Frequencies come from the evidence; I never estimate how many people are affected, and value and effort are words, never a score or a total
- An accessibility issue on the list is not an audit; for legal duties, check with a qualified adviser
- You keep the register and propose the short list; the people who own the plan decide what goes in

## Next
Run pdes-design-review-deck (Design Review Deck) to take the short list to the people who decide.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
