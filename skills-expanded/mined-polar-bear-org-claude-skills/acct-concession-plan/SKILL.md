---
name: acct-concession-plan
description: Builds your concession plan with the list of what can be traded, its cost to you and its value to the customer, the order of concessions, the wording "if you, then we" for each and the floor your leadership approved. Use for "run acct-concession-plan", "concession plan", "give-get list", "what can I trade in this negotiation", "the customer wants a discount", "trade-offs for negotiation", "what do I ask for in return", part of the Claude for Account Executives Pack by 90n.
---

# Concession Plan

## When To Use
Every concession is given for nothing and the margin goes in one meeting. You know your limit, but not what you can trade, in which order, or what you ask for in return. Run this before a negotiation. It answers: what can you give, against what, and when?

## When Not To Use
With no approved limit and no alternative worked out, start with Negotiation Plan. Once the deal is agreed and has to be priced on paper, go to Sales Quote Check.

## Inputs
- The floor your leadership approved (price, margin or terms), with the name of the person who approved it.
- What can be traded on your side: timing, volume, contract term, services, payment terms, depending on what you sell.
- For each, its cost to you and its likely value to the customer, which you fill in.
- Your Negotiation Plan, if you made one.
If you have none of this, I start from the standard list of tradables above with the cost and value columns empty, and mark the output as a first draft. The table pastes into any spreadsheet.

## Approach
The four strategies for making concessions described by the Program on Negotiation at Harvard Law School (pon.harvard.edu): label your concessions, ask for and define reciprocity, make concessions contingent, and give in installments. A concession you do not name goes unnoticed and earns you nothing. The failure it prevents: the discount granted up front, then a second one, while the customer has changed nothing on their side.

## Workflow
1. I ask at most three questions: which floor did your leadership approve, what does each tradable really cost your company, and which of the customer's interests are confirmed.
2. I draw the tradables table: item, cost to you, value to the customer, what you ask in return. Cost and value cells stay empty until you fill them.
3. I order the concessions: first what costs you little and is worth a lot to the customer, price last. Each is split into installments and not given in one block.
4. For each I write the contingent wording, "if you [what you ask], then we [concession]", with the ask defined precisely enough to be checked.
5. For each I write the sentence that labels it: what it costs you, said plainly, so it registers as a concession.
6. I check every line against the floor: nothing below it is written down, even as a last resort.
7. I pass on the source's caution: making every concession contingent can undermine trust. You decide whether one or two stay free, as a gesture of good faith.

## Output Format
```markdown
# Concession Plan
Deal: [name] · Floor: [value], approved by [name, job role] on [date]
## Tradables, in order
| Order | Item | Cost to you | Value to the customer | Asked in return | Installments |
|---|---|---|---|---|---|
| 1 | [item] | [you fill] | [you fill] | [ask] | [steps] |
## Wording
| Order | "If you..., then we..." | Sentence that labels the concession |
|---|---|---|
| 1 | [sentence] | [sentence] |
## Free gestures (decided by you)
- [item or "none"]
## Check against the floor
[Every line at or above the floor: yes / line to remove]
## Decision
[Name, job role] confirms the floor and [you] confirm the order by [date], before the meeting.
```

## Done When
- Every line has something asked in return, or is listed as a gesture you chose.
- Price is the last tradable on the list.
- No value goes below the floor, and the floor carries a name and a date.
- Cost and value columns are filled by you, or left empty.

## Quality Bar
- A free concession is the chosen exception, never the habit.
- Each concession is labelled to the customer: they know what it costs you.
- Concessions come in installments, never the whole move at once.
- The table is updated during the negotiation as things are traded; contract and payment terms you trade: check with a qualified adviser.
- Claude invents no price and no discount: costs, values and the floor come from you and your leadership, and you do the negotiating.

## Next
Run acct-mutual-action-plan (Mutual Action Plan) to set with the customer the steps from agreement to signature.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
