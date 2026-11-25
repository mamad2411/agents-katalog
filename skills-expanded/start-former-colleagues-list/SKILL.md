---
name: start-former-colleagues-list
description: Builds a Former Colleagues List from your own memory and records, per past employer, with the colleagues, managers, clients and suppliers who saw your work, where each is now from linked public work sources, last contact, any limit from your terms check, one useful reason to write, and a first run of 5 to 10 names you pick. Use for "run start-former-colleagues-list", "list my former colleagues", "who already knows my work", "reconnect with past clients", "where do first clients come from", "people from my old job who moved on", "who should hear I am on my own", part of the Claude Guide for New Founders Pack by 90n.
---

# Former Colleagues List

## When To Use
Your first clients will most likely be people who already know your work, and that list exists only in your head. In your head it holds the six people you had lunch with. On paper it holds everyone who watched you solve a problem. This answers: who saw my work, where are they now, and who do I write to first?

## When Not To Use
To read your whole LinkedIn network against a brief, including people who never worked with you, use Warm Network Map. If you know the one person and need the words, go to Reconnect Message.

## Inputs
- Your past employers and roles, and the names you can recall for each, in any order
- Your own records: a personal address book, messages in your own accounts, your Career Proof Inventory. With the Gmail connector on a personal account, I can search and read for last contact dates; I never draft or send.
- Your Former Employer Terms Check, if you ran it
If you have none of this, I start from the names you can recall in ten minutes and mark the output as a first draft.

## Approach
Dormant ties, as Levin, Walter and Murnighan describe them in Organization Science (2011): people you once worked closely with and lost touch with. Reconnecting can bring back the trust you built, together with news you would not hear from people you see every week. The list is built from your memory and your own records, never from a former employer's customer system, client list or org chart. The failure it prevents is the list that turns into a round of "do you have any work for me?", which spends the trust it was meant to revive.

## Workflow
1. Ask at most three questions: which employers and years to cover, whether any relationship ended badly (those stay off unless you decide otherwise), and whether you ran the terms check.
2. Prompt your memory by group, per employer: colleagues and peers, managers and sponsors, clients and customers you served, suppliers and partners. For each name: their role then, and what they saw you do, tied to an inventory row where one fits.
3. Find where each is now from public work sources you point me to or I search: current role and organisation, one link per fact. People who moved get their new role; that move is often the warmest door. Nothing from personal life. Unknown stays "unknown".
4. Add last contact from your own records, or "not found". Never a guess.
5. Add the limit column from your terms check: "none noted", "may be covered by [section]: ask adviser first", or "terms not checked". I do not decide whether a limit applies.
6. Propose one reason to write from five useful ones: share something relevant, catch up, congratulate, introduce them to someone, suggest a conversation. Each rests on a fact in the row. "Checking whether you need help" is never a reason.
7. Show the list in the order you gave it, with no ordering by seniority, value or likelihood to buy. You pick a first run of 5 to 10.

## Output Format
```markdown
# Former Colleagues List
Employers covered: [employers, years] | Prepared: [date] | Left off by my choice: [count or none]
## The list
| Name | Group | Role then, and what they saw | Where now (linked) | Last contact | Limit from terms check | Reason to write |
|---|---|---|---|---|---|---|
| [name] | [colleague / manager / client / supplier] | [role; inventory row] | [role, organisation] ([link]) or unknown | [date or not found] | [none noted / ask adviser first / not checked] | [share / catch up / congratulate / introduce / suggest a conversation]: [one line] |
## My first run (I pick 5 to 10)
1. [name]: [reason to write] | write by [date]
## Held until I have an answer
- [name]: [which clause, which question]
## Decision
[Your name] chooses the first run and the date each message goes, by [date]; names marked "ask adviser first" wait.
```

## Done When
- Every "where now" fact has a link, and every gap says "unknown" or "not found".
- Every reason to write rests on a fact in the same row.
- Every row has a limit mark, even if it is "not checked".
- The first run holds 5 to 10 names, all picked by you.

## Quality Bar
- Public, work-related facts only; no personal life, no inferred traits.
- No column for seniority, budget, value or how likely someone is to buy.
- A reason to write is useful to them first; an ask for work never appears here.
- Whether a clause covers a person is a legal question: check with a qualified adviser.
- Your memory and your own records, never a former employer's files; you choose who to write to.

## Next
Run start-linkedin-data-export (LinkedIn Data Export Guide) to get the rest of your network into one private file.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
