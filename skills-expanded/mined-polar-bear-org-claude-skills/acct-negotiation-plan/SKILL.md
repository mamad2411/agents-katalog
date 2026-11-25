---
name: acct-negotiation-plan
description: Prepares a negotiation plan with your target and the limit your leadership approved, your best alternative and the buyer's supposed one, the possible zone of agreement marked as an estimate, the interests behind stated positions and the questions to ask. Use for "run acct-negotiation-plan", "negotiation plan", "negotiation prep", "the buyer wants a discount", "prepare my price negotiation", "what is my walk-away", "BATNA", "procurement is pushing on price", part of the Claude for Account Executives Pack by 90n.
---

# Negotiation Plan

## When To Use
The buyer asks for a lower price and all you prepared is your price. You walk in without knowing what you will do if there is no deal, or what the buyer wants behind the request. Run this before the meeting. It answers: how far can you go, and what must you learn before you give anything?

## When Not To Use
If the customer has not raised price and still doubts the offer, run Objection Handling first. If this plan is done and you need what to trade and in which order, go to Concession Plan.

## Inputs
- The buyer's request in their words, with its date (email, call notes).
- Your target and your limit, the limit set by your leadership: the price, margin or terms below which you do not sign.
- What you know about the customer: deadlines, alternatives they mentioned, internal constraints.
If you have none of this, I start from the buyer's request and mark the output as a first draft, with the limit left as "[to be set by your leadership]".

## Approach
BATNA, your best alternative to a negotiated agreement, and the split between positions and interests both come from the Program on Negotiation at Harvard Law School (pon.harvard.edu): keep the alternative realistic, compare like for like, reassess as facts change, and look for the need behind the demand. Your strength in the room comes from what you will do without this deal, not from the list price. The failure it prevents: giving way at the first ask for lack of a written limit, or bluffing an alternative you do not have.

## Workflow
1. I ask at most three questions: which limit did your leadership approve and until when, what do you do if there is no deal, and what did the buyer say, word for word, and when.
2. Your BATNA: the concrete thing you do without a deal (another opportunity, another customer, waiting). If it is weak I write it weak, and you plan with that; it is never bluffed in the room.
3. The buyer's alternatives as far as you know them (a named competitor, doing it in house, doing nothing), each marked "hypothesis" with what would confirm it.
4. Target and limit: the limit comes from your leadership with the approver's name, the target from you; I propose neither. The possible zone of agreement is the overlap between your limit and the buyer's supposed limit, always labelled "estimate".
5. Positions and interests: for each position you heard, the possible interest behind it (this year's budget, a comparison with another offer, a need to justify the choice internally), marked "confirmed" with its source or "to verify".
6. The open questions to ask in the meeting to test those interests and alternatives, starting with "what would have to be true for the current price to work?".
7. The list of what is not negotiable, each with the plain sentence you use to say it calmly. If a fact changed since the proposal, the plan is updated before you speak.

## Output Format
```markdown
# Negotiation Plan
Deal: [name] · Meeting: [date] · Prepared by: [you]
## Target and limit
| Element | Value | Source |
|---|---|---|
| Target | [your target] | you |
| Limit | [limit] | [name, job role], approved on [date] |
| Possible zone of agreement | [overlap or "no zone visible"] | estimate |
## Alternatives
| Side | Alternative if there is no deal | Strength | What would confirm it |
|---|---|---|---|
| You (BATNA) | [alternative] | [strong / weak] | [fact] |
| Buyer (hypothesis) | [alternative] | estimate | [question to ask] |
## Positions and interests
| Position heard (date) | Possible interest | Status |
|---|---|---|
| "[buyer's words]" | [interest] | confirmed ([source]) / to verify |
## Questions to ask and what is not negotiable
- [open question] / [item not negotiable] · said as: [plain sentence]
## Decision
[Name, job role] confirms the limit and [you] confirm the target by [date], before the meeting.
```

## Done When
- The limit carries the name of the person who approved it, or reads "[to be set by your leadership]".
- Everything about the buyer is marked "hypothesis" or "estimate", or carries its source.
- Each position heard is quoted with its date, a possible interest and a question to verify it.

## Quality Bar
- A weak BATNA is written weak; the plan does not teach you to bluff.
- No tactic aimed at the other person's psychology, no false deadline, no profile of the buyer: their interests and alternatives, never their character.
- Contract or payment terms you are unsure of: check with a qualified adviser.
- I invent no price, discount or limit; the buyer's limit is only ever an estimate, and you hold the conversation yourself.

## Next
Run acct-concession-plan (Concession Plan) to decide what to trade, against what and in which order.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
