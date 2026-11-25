---
name: acct-account-plan
description: Writes the account plan for one key account, with the customer's goals in their own words, a whitespace map, objectives, dated actions with owners, relationship gaps by role, risks and review dates. Use for "run acct-account-plan", "account plan", "key account plan", "strategic account plan", "write my account plan", "grow this account", "whitespace map", "account planning template", part of the Claude for Account Executives Pack by 90n.
---

# Account Plan

## When To Use
Leadership wants a written plan for every key account and the last one is a year old. Run this at the start of a planning period or before an account review. It answers: where does this account stand with us, what is the customer trying to do, and who does what by when?

## When Not To Use
For your whole book over a quarter, run Territory Plan. For a small account the method is too heavy: an Account Research Brief and one dated next step are enough.

## Inputs
- Your Stakeholder Map and your latest call notes on this account.
- What the account buys from you today and your own figures for it (CRM export), if you want them in the plan; I add none.
- The objectives your leadership set for this account, and the next renewal or budget date if you know it.
If you have none of this, I start from the account name and your memory of the last three conversations, and mark the output as a first draft. Works well in Projects (beta), one Project per account, or as a page in Claude Docs.

## Approach
Strategic account planning treated as planning done with the customer, the stance the Strategic Account Management Association takes in its public resources (strategicaccounts.org), with the split between positions and interests from the Program on Negotiation at Harvard Law School (pon.harvard.edu). The plan starts from what the customer is trying to achieve, in their words, before anything you want to sell. The failure it prevents: a plan that lists your products and is stale within a quarter because the customer never saw it.

## Workflow
1. I ask at most three questions: what objective did leadership set for this account, what are the two or three things the customer told you about their goals, and on which dates will the plan be reviewed.
2. Where the account stands with you: what is in place, what went well, what went wrong, each line resting on a dated fact or marked as a hypothesis.
3. The customer's goals in their words, each with source and date, marked stated or inferred. An inferred goal becomes a question for your next meeting. Beside each: the interest behind the position, on their side and on yours.
4. The whitespace map: for each customer unit or need, one of four states (in place, in progress, possible, not relevant). You fill it; I do not guess a cell. "Possible" must name the customer goal it serves, or it is parked.
5. Objectives from your own figures, each with a result you want and an activity you control. Then actions with an owner and a date, five at most for the next 90 days.
6. Relationship gaps by role, taken from the Stakeholder Map as it is: none, single thread, or not met. A gap that threatens an objective gets an action.
7. Risks with an owner each, the review dates you set, and a short version of the goals section you can show the customer and ask them to correct.

## Output Format
```markdown
# Account Plan
Account: [name] · Owner: [name] · Period: [from, to] · Renewal or budget date: [date or unknown] · Version: [date]
## Where the account stands
| In place | Went well | Went wrong | Source and date |
|---|---|---|---|
| [fact] | [fact] | [fact or hypothesis] | [source] |
## Customer goals, in their words
| Goal | Source and date | Stated or inferred | Interest behind it | Our interest and limits |
|---|---|---|---|---|
| [goal] | [call notes of date] | [stated / inferred] | [interest or unknown] | [yours] |
## Whitespace map
| Unit or need | In place, in progress, possible, not relevant | Customer goal it serves |
|---|---|---|
| [unit] | [state] | [goal or parked] |
## Objectives and actions
| Objective (result and activity) | Action | Owner | Date |
|---|---|---|---|
| [objective] | [action] | [name] | [date] |
## Relationship gaps, risks and review dates
- [role]: [none / single thread / not met] · action or risk owner: [name] · Reviews: [dates you set]
## Decision
[Manager name] approves the objectives and the first actions at the review of [date]; [you] share the goals section with [customer role] by [date].
```

## Done When
- Every customer goal has a source and a date, or is marked inferred with its question.
- Every "possible" cell names the customer goal it serves.
- Every action and risk has an owner and a date, and the review dates are set.

## Quality Bar
- The customer's words come first; your product list never sets the goals.
- Figures are yours or marked "to quantify"; no number about the account is invented.
- People appear by their role in the decision, never by character; no power or influence ratings.
- The customer's goals carry their source, unknown stays unknown, and you have the planning conversation with the customer yourself.

## Next
Run acct-territory-plan (Territory Plan) to place this account in your whole book for the quarter.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
