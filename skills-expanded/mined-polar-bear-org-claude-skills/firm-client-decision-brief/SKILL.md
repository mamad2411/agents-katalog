---
name: firm-client-decision-brief
description: Builds a neutral one-page decision brief your client contact owns and can use inside their company, with the decision framed around their outcome, every way to proceed including doing nothing and doing it in house with their own AI, consequences on their criteria in their figures, what would make each option the right one and the open facts with whom to ask, recommending nothing. Use for "run firm-client-decision-brief", "help my contact make the case internally", "neutral decision brief for the client", "one page for their leadership meeting", "my sponsor has to convince the board", "options including doing nothing", "a fair comparison they can forward", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Client Decision Brief

## When To Use
Your contact wants this to happen. The people who must agree, a budget holder, a leadership meeting, a colleague sure it can be done with AI, will never speak to you. Sending your contact in with your sales document makes them your salesperson. Run this to give them a fair page of their own, which sets out the choice their company faces.

## When Not To Use
To state your own advice, use Recommendation Memo; that page is signed by you and takes a side. To summarise your proposal for its signer, use Proposal Executive Summary. To compare your quote with a cheaper one, use Like-for-Like Quote Comparison.

## Inputs
- What the client says they are deciding, by when, and who decides
- The criteria they have named, in their words and units, and your proposal's options
- What they have said about doing nothing, and about doing it themselves or with their own AI
If you have none of this, I start from your proposal and call record and mark every criterion as an assumption for your contact to correct. Claude Docs suits a page your contact will edit.

## Approach
This is a decision frame with options and consequences, the basic form of decision analysis, described generically: state the decision, then compare what each route leads to on criteria the client owns, in plain words and with no invented score. The whole value is neutrality. A page that leans your way is spotted at once and costs your contact their standing in the room. Doing nothing and doing it in house with their own AI are real options with real strengths, and those strengths are written first.

## Workflow
1. Ask, in one go: what does the client believe they are deciding, and by when? Which criteria have they named? What have they said about doing it themselves?
2. Frame the decision in one sentence around an outcome and not around hiring you: "how [client team] will [outcome] by [date]". Add who decides, who must approve, the deadline and what is already settled.
3. List every way to proceed: do nothing, do it in house with their own AI, your option or options, any other route they mentioned. Write each so that its keenest supporter would say "yes, that is my case".
4. Compare consequences on the client's criteria only, in their units: cost in their figures, time to a result, risk, effort from their people. An unknown reads "unknown: ask [role]". No weighted score. Where AI makes the in-house route quicker or cheaper, that goes down first.
5. Write "what would make this the right choice" for each option: the facts under which it wins. In an argument you are not present for, this is the most useful section.
6. Read it as a sceptical colleague of your contact would. Any sentence that sells, any adjective standing in for evidence, any option drawn feebly on purpose is rewritten. Then hand it over as theirs to change.

## Output Format
```markdown
# Client Decision Brief
Prepared for [contact role] to use and edit · [date] · This page recommends nothing.
## The decision
[One sentence, as an outcome] · Decide by [date] · Decides: [role] · Approves: [roles] · Already settled: [what]
## Ways to proceed, compared
| Criterion (the client's, their units) | Do nothing | In house with own AI | [Option A] | [Other route] |
|---|---|---|---|---|
| [cost, in their figures] | [consequence or unknown] | [consequence] | [consequence] | [consequence] |
| [time to a result] | [consequence] | [consequence] | [consequence] | [consequence] |
## What would make each the right choice
- [Option]: right if [fact]
## Open facts
- [Unknown]: ask [role]
## Decision
[Client decider role] chooses among these routes by [date]; [contact role] owns this page and may change any line of it.
```

## Done When
- The decision is framed around the client's outcome, not around engaging you
- Doing nothing and the in-house route each have a fair column
- Each consequence is stated on the client's criteria and in their figures, or marked "unknown"
- A sceptical reader could not tell which option is yours

## Quality Bar
- No option is drawn weak to flatter another
- The strengths of the in-house route come before its limits
- Blanks stay blank; no figure, fee or result is supplied to fill one
- Roles are named; nobody on the client side is judged
- Neutral, in the client's words and figures, with nothing invented and no recommendation; your contact owns it and you only hand it over.

## Next
Run firm-mutual-action-plan (Mutual Action Plan) to map the steps from their yes to the first day of work.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
