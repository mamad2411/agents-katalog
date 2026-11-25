---
name: acct-sales-proposal
description: Writes a customer-first sales proposal, with a summary up front, section titles that carry the message, one to three honest options and an investment section taken only from your price list and marked to validate. Use for "run acct-sales-proposal", "sales proposal", "write a sales proposal", "proposal template", "business proposal for a customer", "commercial proposal", "proposal outline", "respond to a customer request", part of the Claude for Account Executives Pack by 90n.
---

# Sales Proposal

## When To Use
Your proposals describe your company for three pages before they mention the customer. Run this once the brief is approved. It answers: reading only the titles, does the customer understand what you propose, for which result, and what the price rests on?

## When Not To Use
With no sourced facts about the request, start with Proposal Brief. If the customer only expects priced lines, Sales Quote Check is enough. A formal tender with its own response format is outside this skill.

## Inputs
- The Proposal Brief (request, decision, facts, assumptions, angle).
- Your price list, the name of the person who approves prices, and the delivery plan you know you can keep (phases, deliverables, effort).
- A Customer Proof Story the customer has agreed to, if you want to cite one.
If you have none of this, I start from the customer's request in one sentence and your price list, and mark the output as a first draft. It drafts well in Claude Docs, or in Claude Slides when the customer expects a deck.

## Approach
An outline of message titles and honest options, both consulting practice described here generically. Each title is a full sentence that says what to retain, and the titles read alone tell the whole proposal. Each option is a real answer you would gladly deliver; none is a decoy placed to make another look reasonable. The failure it prevents: the customer who skims, lands on "About us" on page two and finds their own problem on page four.

## Workflow
1. I ask at most three questions: document or deck, how many options you would truly deliver, and who approves prices and terms.
2. Titles first. I write every section title as a full sentence, then read them alone from top to bottom. The customer appears by the second section; your company takes a few lines near the end. You approve this thread before I write the body.
3. The summary up front, in three beats: situation, difficulty, answer, in the customer's language from the brief. An assumption from the brief stays marked [ASSUMPTION] in the text.
4. The answer and the plan: phases, deliverables, and what is asked of the customer (availability, access, approvals). No promise of a result.
5. Options: one to three, only if you would deliver each. Test: the customer can say in one sentence what option B does beyond option A. If not, there is one option.
6. Investment: amounts from your price list only, by phase or deliverable, with the assumptions the price depends on. I recompute the totals, set no price and add no discount; each amount reads "[to validate]" until the approver agrees.
7. Terms in plain words (validity, payment), with contract clauses left to your legal team: check with a qualified adviser. Then one dated next step with an owner on each side.

## Output Format
```markdown
# Sales Proposal
**Customer:** [name] · **Version:** [date] · **Amounts:** [to validate by name]
## [Message title of the summary, one sentence]
Situation: [...] · Difficulty: [...] · Answer: [...]
## [Message title: what the customer wants to achieve, in their words, source: brief of date]
## [Message title: what you propose]
| Phase | Deliverables | Asked of the customer | Duration (yours) |
|---|---|---|---|
| [phase] | [deliverables] | [availability, access] | [duration] |
## [Message title: the investment and what it rests on]
| Option | Scope and outcome | Amount (your price list) | Status |
|---|---|---|---|
| [A] | [scope] | [amount from the list] | [to validate] |
Price depends on: [assumptions] · Terms: [validity, payment, in plain words]
## Dated step with owners
| Action | Customer owner (role) | Your owner | Date |
|---|---|---|---|
| [action] | [role] | [name] | [date] |
## Decision
[Approver name] validates prices before sending; [customer role] chooses an option, answer expected by [date].
```

## Done When
- The titles read alone tell the proposal, and the customer appears by the second section.
- Every amount points to a line of your price list and reads "[to validate]".
- Each option passes the one-sentence test, or there is one option.
- The next step has a date and an owner on each side.

## Quality Bar
- No promise of results: you describe what you deliver, not what the customer will surely gain.
- No decoy option, no discount written in by default, no customer proof without that customer's agreement.
- The brief's assumptions stay visible, never dissolved into the text.
- No price or result is invented: every amount comes from your price list and waits for validation, and you send the proposal yourself.

## Next
Run acct-quote-check (Sales Quote Check) to check every line and every total before the quote leaves.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
