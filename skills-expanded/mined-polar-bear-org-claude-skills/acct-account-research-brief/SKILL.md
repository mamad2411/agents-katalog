---
name: acct-account-research-brief
description: Builds a one-page account research brief before a meeting, with every fact sourced and dated, unknowns written as unknown, two or three hypotheses to test and three questions to ask. Use for "run acct-account-research-brief", "account research", "research this account before my meeting", "pre-call research", "company research before a sales call", "what do we know about this account", "prep me on this customer", "I have a meeting tomorrow", part of the Claude for Account Executives Pack by 90n.
---

# Account Research Brief

## When To Use
You have a meeting tomorrow and all you know about the account is its website. Run this the day before. It answers one question: what do we really know about this account, where does each fact come from, and what is left to learn in the room?

## When Not To Use
If you only need a dated reason to call an account you own, run Buying Signals Brief. If the question is who takes part in the decision, run Stakeholder Map. For a written plan over the year, run Account Plan: this brief is a one-page snapshot before one meeting.

## Inputs
- The company name and the pages you want read: its site, newsroom, public filings or register entry.
- Your history with the account: CRM export, past proposals, your notes, what it buys from you today.
- The purpose of the meeting and the job role of the person you are meeting.
If you have none of this, I start from the company name and its own home page and mark the output as a first draft. With Claude in Chrome I read the public pages myself; with Projects (beta) you can keep one Project per account.

## Approach
Sourced research and hypothesis-led preparation, both common practice and described here generically: one fact, one source, one date, and a point of view to test, not a list of facts the customer already knows. The failure it prevents is opening with a "recent news" item you misread or a figure from nowhere, and losing the customer's trust in the first minute. A thin public footprint gives a short brief; I do not fill cells to look thorough.

## Workflow
1. I ask at most three questions: what is the meeting for, what has already happened between you and this account, and which unknown worries you most.
2. I record facts in three columns: the fact, its source (a link, or "your notes of [date]") and the date of the source. A fact with no source is deleted or moved to the hypotheses. If I recall something I cannot link, it stays out.
3. I fill four rows first: what the company does, recent events, what it buys from you, history with you. "Unknown" is a valid cell, and an old figure is dated as old.
4. I name the likely "why now" in one line, marked as an inference, with the fact it rests on.
5. I write two or three hypotheses, each one sentence the customer could disagree with, each with the question that tests it and the answer that would kill it. Three is the ceiling; beyond that you are guessing, not preparing.
6. For people I write the name and job role only, from the company's own pages or your notes. No private life, no social profile research, no reading of character.
7. I turn the biggest unknowns into three questions to ask, then cut to one page: a line that would not change what you ask or listen for goes.

## Output Format
```markdown
# Account Research Brief
Account: [name] · Meeting: [date, purpose] · Meeting with: [job role] · Research checked [date]
## Facts
| Topic | Fact | Source | Source date |
|---|---|---|---|
| What they do | [fact] | [link] | [date] |
| Recent events | [fact or unknown] | [link] | [date] |
| What they buy from you | [fact or unknown] | [CRM, your notes of date] | [date] |
| History with you | [fact] | [CRM, proposal of date] | [date] |
## Why now (inference)
[One line] Rests on: [fact above]
## Hypotheses to test
| Hypothesis | Question that tests it | Answer that would kill it |
|---|---|---|
| [one sentence] | [question] | [answer] |
## People
- [name or unknown] · [job role] · [source]
## Three questions to ask
1. [question drawn from an unknown]
## Decision
[You] choose the hypothesis to lead with and what to verify before [meeting date].
```

## Done When
- Every fact row has a source and a date, or reads "unknown".
- The "why now" and every hypothesis are marked as inference or untested, each with its question.
- The three questions come from the biggest unknowns, and the brief fits one page.

## Quality Bar
- No figure about the account without a dated source; nothing beyond what the source page prints.
- Hypotheses stay apart from facts and are never written as findings.
- People appear by name and job role only; no judgment of anyone.
- No fact about the customer is invented: each line has its source or is marked unknown, and you have the conversation.

## Next
Run acct-stakeholder-map (Stakeholder Map) to see which roles take part in the decision and which you have not met.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
