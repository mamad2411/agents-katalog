---
name: acct-stakeholder-map
description: Maps the roles in one buying decision, with who holds each role or unknown, what each has said with date and source, the roles you have not met and the next contact per role. Use for "run acct-stakeholder-map", "stakeholder map", "map the buying committee", "who decides on this deal", "decision maker map", "I only talk to one person at this account", "who signs", "multithread this deal", part of the Claude for Account Executives Pack by 90n.
---

# Stakeholder Map

## When To Use
The cycle is getting longer, more people are in the decision and you are talking to one of them. Run this when a single friendly contact is your only window into the deal. It answers: which roles weigh on this decision, which are empty on your map, and who do you ask to meet next?

## When Not To Use
To learn about the company itself, run Account Research Brief. To test whether the deal is real letter by letter, run MEDDPICC Qualification. Objectives and actions for the year belong in Account Plan, which reuses this map as it is.

## Inputs
- The deal in one sentence and its stage.
- The people you know on the customer side, with their job roles.
- Your dated call notes: what each person said, and when. With Salesforce in Claude (beta) I can read the contacts on the account; any CRM export works too.
If you have none of this, I start from your contact's job role and the deal, and mark the output as a first draft full of questions.

## Approach
Buying decisions are made by a set of roles, not one person, as organizational buying research has long described; the economic buyer and champion definitions come from the MEDDPICC method (meddicc.com). One person can hold several roles and roles shift during a deal. The map records roles, dated words and dated actions, never characters. The failure it prevents: learning in the last week that a buyer or a signer you never met is holding the deal.

## Workflow
1. I ask at most three questions: what decision does the customer have to make, who has spoken to you so far, and who do you believe signs.
2. I set the rows as roles: signs (the economic buyer, the role with overall authority in the decision), funds, uses the result, checks (technical, security, legal), buys (procurement), and champion as a role. A role can be empty; a person can hold two.
3. Per role I record who holds it (name and job role, or "unknown"), what they said with date and source, what they need from this decision, and your last contact.
4. I keep "said" (in your notes, sourced) apart from "assumed" (your guess, to verify). An assumption never moves into the said column, and a job title alone never proves who signs.
5. The champion row holds dated actions only: introduced you to the signer, shared the decision criteria, debriefed you after an internal meeting. With no such action the row reads "no action yet", which is a finding about the deal, not about the person.
6. Empty and unmet roles are the real result. For each I write how to reach it through your contact: the question to ask or the introduction to request. Never around them.
7. I propose one next contact per role, with an owner and a date you set. If you ask for a personality profile, a buyer type or an influence or power rating of a person, I refuse and return to roles and dated words.

## Output Format
```markdown
# Stakeholder Map
Deal: [name] · Stage: [stage] · Updated: [date]
## Roles in the decision
| Role | Who (name, job role) | Said (date, source) | Assumed (to verify) | Needs from this decision | Last contact |
|---|---|---|---|---|---|
| Signs (economic buyer) | [name or unknown] | ["...", call of date] | [assumption] | [need] | [date] |
| Funds / Uses / Checks / Buys | [name or unknown] | [words, source] | [assumption] | [need] | [date] |
## Champion role: dated actions
| Action seen | Date | Source |
|---|---|---|
| [introduced you to the signer / shared criteria / debriefed you] or "no action yet" | [date] | [your notes] |
## Unmet roles
| Role | How to reach it through your contact | Owner |
|---|---|---|
| [role] | [introduction to request from contact] | [you] |
## Contact plan
| Role | Action | Owner | Date |
|---|---|---|---|
| [role] | [action] | [name] | [date] |
## Decision
[You] decide which unmet role to cover first, through whom, by [date].
```

## Done When
- Every role has a name or "unknown", and every reported word has a date and a source.
- Said and assumed are in separate columns.
- Each unmet role has a route through your contact, and each role has a dated next contact.

## Quality Bar
- The map describes the decision, not the people: job role and role in the decision, nothing on character or mood.
- Quotation marks only for words that are in your notes.
- Personal data is limited to name, job role and work exchanges; if in doubt, check with a qualified adviser.
- "Champion" is a role shown by dated actions, never a label or a verdict on a person.
- Roles and dated words only: no profile, no rating of a buyer, and you make every contact yourself.

## Next
Run acct-account-plan (Account Plan) to set objectives and dated actions on this account using the map.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
