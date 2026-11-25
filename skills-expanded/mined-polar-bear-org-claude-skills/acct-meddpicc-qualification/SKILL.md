---
name: acct-meddpicc-qualification
description: Checks one deal letter by letter with MEDDPICC, giving for each letter the written proof with its source, what is assumed and what is unknown, the champion role tested by dated actions, the gaps turned into questions and a pursue or walk away choice for you. Use for "run acct-meddpicc-qualification", "MEDDPICC", "MEDDIC", "MEDDICC", "qualify this deal", "is this deal real", "my champion is not a champion", "deal qualification checklist", "what do I still not know about this deal", part of the Claude for Account Executives Pack by 90n.
---

# MEDDPICC Qualification

## When To Use
Your "champion" has never introduced you to the person who signs. The deal feels good and you cannot say why it should close. Run this on one deal that matters. It answers: letter by letter, what is proven in writing, what do you only assume, and what must you ask next?

## When Not To Use
For a small, short deal the method is overkill: use a four-question check (budget, authority, need, timing) and keep in mind that a budget rarely exists before the need has taken shape. To see every deal at once, run Pipeline Review. To map who holds which role, run Stakeholder Map.

## Inputs
- Everything written on the deal: call notes, emails, the customer's documents, your proposal. With Salesforce in Claude (beta) I can read the opportunity; any CRM works by copy and paste.
- Your Stakeholder Map, if you have one.
- Your own threshold: which letters must be proven before you commit more time.
If you have none of this, I start from one paragraph on the deal and mark the output as a first draft, with most letters reading "unknown".

## Approach
MEDDIC was created inside PTC in 1996, and MEDDPICC is its extended form (meddicc.com): metrics, economic buyer, decision criteria, decision process, paper process, pain, champion, competition. Here it judges the deal, never a person. The honest default for every letter is "unknown". The same source shows a champion by what the person does, and notes that a friendly host is likely not one; so the champion letter holds dated actions, not a label. The failure it prevents: the warm deal that sits in your forecast for two quarters.

## Workflow
1. I ask at most three questions: which deal and what is at stake, which letters must be proven for you to keep investing, and what the customer has said so far and in which conversation.
2. I sort every fact you pasted under one letter. Metrics: the quantified value the customer expects. Economic buyer: the role with overall authority in the decision. Decision criteria. Decision process. Paper process: the steps from decision to signature. Pain, in their terms. Champion. Competition: any other vendor, initiative, in-house option or doing nothing.
3. Each letter gets three cells: written proof with its source and date, assumed, unknown. A fact with no source moves to "assumed". Your hopes are not proof, and I will say so kindly.
4. Champion is tested by dated actions only: gave you access to the economic buyer, told you the decision criteria, debriefed you after an internal meeting. No action seen means the role is unproven on this deal. It says nothing about the person.
5. Each gap becomes one question, in the order you would ask them, in the customer's language.
6. I check the letters against your threshold and show which are met. I give no score and no total.
7. I write the note and stop. You choose: pursue, pursue once the questions are answered, or walk away.

## Output Format
```markdown
# MEDDPICC Qualification Note
Deal: [name] · Stage: [stage] · Date: [date] · Your threshold: [letters that must be proven]
## Letters
| Letter | Written proof (source, date) | Assumed | Unknown | Question to close the gap |
|---|---|---|---|---|
| Metrics | [fact] ([call of date]) | [assumption] | [gap] | [question] |
| Economic buyer | [role, proof] | [assumption] | [gap] | [question] |
| Decision criteria / Decision process / Paper process / Pain / Competition | [fact] | [assumption] | [gap] | [question] |
## Champion role: dated actions
| Action | Seen on (date, source) |
|---|---|
| Access to the economic buyer / criteria shared / debrief given | [date, notes] or "not seen" |
## Against your threshold
[Letters met: ...] · [Letters not met: ...]
## Questions, in order
1. [question]
## Decision
[Your name] decides by [date]: pursue, pursue after the questions are answered, or walk away, because [one line].
```

## Done When
- Every letter has a row, and every proof carries a source and a date.
- The champion table lists dated actions or "not seen".
- Each gap has one question, and the list fits one screen.
- The Decision names you, a date and a reason.

## Quality Bar
- Unknown stays unknown; I never guess a budget, a signer or a deadline.
- No number per letter and no total; the threshold is yours.
- Doing nothing and doing it in house are listed under competition whenever they could apply.
- The note judges the deal, never a person: "champion" is a role tested by dated actions, and nothing rates a buyer.

## Next
Run acct-deal-review (Deal Review Brief) to turn this note into the pre-read for your review with your manager.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
