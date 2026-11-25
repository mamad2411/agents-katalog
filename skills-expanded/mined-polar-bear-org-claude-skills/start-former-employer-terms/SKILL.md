---
name: start-former-employer-terms
description: Reads your own employment contract and exit papers and lists the clauses that touch your plan, each quoted with its dates, covering non-solicitation of clients and staff, confidentiality, intellectual property, non-compete and notice, with what each may touch and the questions to take to a qualified adviser. Use for "run start-former-employer-terms", "can I contact my old clients", "what does my non compete say", "non solicitation clause", "what does my contract let me do", "check my exit agreement", "can I work with former colleagues", part of the Claude Guide for New Founders Pack by 90n.
---

# Former Employer Terms Check

## When To Use
You want to call the clients and colleagues you worked with, and you do not know what your contract lets you do. Most people signed it years ago and never read it again. This answers: what do my own papers say, in their own words, and what exactly should I ask an adviser before I write to anyone?

## When Not To Use
If you need to know whether a clause can be enforced, or what happens if you ignore it, that is legal advice and this skill does not give it. If your former employer wants to hire you back as a contractor, use Former Employer Engagement Plan for the new arrangement.

## Inputs
- Your own employment contract, and any exit, settlement or separation agreement you signed
- Any policy or handbook pages the contract refers to, if you hold a copy
- Your plan in a few lines: who you want to contact, what you want to offer, what you want to reuse from your old work
If you have none of this, I give you the list of clause types to look for and the questions to ask for a copy of your papers, and mark the output as a first draft.

## Approach
This is a clause inventory and a question list, built from your own documents and nothing else. Restrictive terms differ by contract and by place, and the rules themselves change, so the skill quotes what your papers say and stops there. The failure it prevents is the common one: a warm note to a former client, sent in good faith in week three, by someone who did not know their agreement still named that client. It also prevents the opposite, a founder frozen for months by a clause that, read closely, never mentioned what they feared.

## Workflow
1. Ask at most three questions: which documents you signed and when, the date your employment ended, and what you plan to do in the next six months.
2. Read the documents and find each clause family: non-solicitation of clients, non-solicitation of staff, confidentiality, intellectual property and work product, non-compete, notice and any paid leave period, and anything about announcements or references.
3. Quote each clause word for word with its section number. Nothing is paraphrased into something softer or harder than it says.
4. For each clause, record the dates as written: when it starts, how long it runs, and the end date worked from your leaving date. Where the document gives no period, the cell says "not stated".
5. Record the definitions the clause leans on, as quoted: who counts as a "client", what counts as "confidential", what "solicit" covers, which territory. Where a term is undefined, say so.
6. Map each clause to your plan as "may touch": the people you want to contact, the offer you want to make, the material you want to reuse. This is a pointer for the adviser, never a conclusion.
7. Write the question list, most urgent first, and name what to bring. I give no view on whether any clause applies, is valid or would be enforced.

## Output Format
```markdown
# Former Employer Terms Check
Documents read: [title, date signed] | Employment ended: [date] | Not a legal opinion
## Clauses found
| Clause type | Exact wording (section) | Starts | Runs for | Ends on | Key terms as defined |
|---|---|---|---|---|---|
| [non-solicitation of clients] | "[quote]" ([section]) | [date] | [period or "not stated"] | [date or "unclear"] | [quoted definition, or "undefined"] |
## Clause types not found in these documents
- [type]: not found in [documents read]; ask whether another document applies
## What each may touch in my plan
| Part of my plan | Clause that may touch it | Why I am asking |
|---|---|---|
| [contact former client contacts] | [section] | [wording that seems to cover it] |
## Questions for a qualified adviser
1. [question, with the section it refers to]
## What I do until I have answers
- [action I hold, by my own choice]: until [date]
## Decision
[Your name] takes the questions and the documents to a qualified adviser by [date], and decides what to hold until then.
```

## Done When
- Every clause is quoted word for word with its section.
- Every clause has its dates, or "not stated".
- Clause types that were looked for and not found are listed as not found.
- The question list exists and names the documents to bring.

## Quality Bar
- No sentence says a clause is valid, invalid, enforceable, standard or unusual.
- No general statement about the law of any country or state.
- "Not found in these documents" is never written as "does not apply".
- Client names and confidential terms in your papers stay in this chat.
- Your own documents only; you decide what to hold, and every legal point here is a question: check with a qualified adviser.

## Next
Run start-former-colleagues-list (Former Colleagues List) to write down who saw your work, with any limit from this check beside each name.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
