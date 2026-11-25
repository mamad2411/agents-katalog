---
name: acct-call-list
description: Builds a weekly call list of 10 to 20 contacts in accounts you already own, each with the account, the job role, the signal or history behind the call and its source, the accounts left off and a check of the calling and email rules that apply. Use for "run acct-call-list", "call list", "who should I call this week", "weekly call list", "build my call block", "target list from my accounts", "which accounts to call first", "prospecting inside my accounts", part of the Claude for Account Executives Pack by 90n.
---

# Weekly Call List

## When To Use
Your call block arrives and you start from the top of the CRM alphabet. Run this once a week before the block. It answers: in the accounts you own, who is it useful to call this week, and what is the true reason for each call?

## When Not To Use
To develop the reason for one person, run Reason to Call: here each line carries one possible reason only. To prepare a meeting that is already booked, run Account Research Brief. This list never reaches outside your named accounts.

## Inputs
- Your accounts and contacts (CRM export, or read through Salesforce in Claude, beta), with the last contact date.
- Your Buying Signals Brief, or recent history per account from your notes.
- What your offer does and for which job role.
If you have none of this, I start from a list of accounts you type and your offer in two sentences, and mark the output as a first draft.

## Approach
Fit of each account to a written brief, accounts and not people, one short list at a time: common practice, described here generically. You write down first who a call would be useful to and why, then each account is checked against that. Rules on business calls and email differ by country; the UK Information Commissioner's Office and the US Federal Trade Commission both publish guidance, and neither replaces advice. The failure it prevents: forty identical calls to whoever comes first, and a week of voicemails.

## Workflow
1. I ask at most three questions: which problem your offer answers and for which role, which signs show an account has that problem this quarter, and how many calls your block can hold.
2. I write the brief in four lines: the problem, the role concerned, signs an account has it, signs it does not. You correct it before I look at one account.
3. I check each account against each sign: yes, no or unknown, with the source. No score and no rank: three plain columns.
4. I propose; you choose 10 to 20 contacts. One list for one week, no bulk import, nothing carried over without a fresh reason.
5. Each chosen line gets the reason for the call, taken from a dated signal or from your history with them, with its source. An account with no true reason is left off and listed apart, so you can see why.
6. For each contact I keep the name, the job role and the source, nothing else.
7. I add the rules check: the country of each contact, whether your company screens numbers against the do-not-call lists that apply there, and whether anyone on the list has asked not to be contacted. I list points to verify; I do not state what the law allows. Check with a qualified adviser.

## Output Format
```markdown
# Weekly Call List
Week of [date] · Owner: [name] · Block size: [number set by you]
## Brief
- Problem: [problem] · Role concerned: [role]
- Signs an account has it: [signs] · Signs it does not: [signs]
## Calls this week (10 to 20, chosen by you)
| Account | Contact (name, job role) | Sign 1 | Sign 2 | Reason for the call (signal or history) | Source and date |
|---|---|---|---|---|---|
| [account] | [name, role] | [yes / no / unknown] | [yes / no / unknown] | [reason] | [link or notes of date] |
## Left off this week
| Account | Why (no true reason, wrong time, asked not to be contacted) |
|---|---|
| [account] | [why] |
## Rules to verify before calling or emailing
- [country]: [do-not-call screening in place? opt-outs honoured? points to verify] Check with a qualified adviser.
## Decision
[You] confirm the list and the day of the call block by [date]; [name] confirms the screening points.
```

## Done When
- The brief was corrected by you before any account was checked.
- The list holds 10 to 20 contacts, all in accounts you already own, chosen by you.
- Every line has a sourced reason, and every account left off has a why.
- The rules section lists points to verify and ends with the adviser line.

## Quality Bar
- "Unknown" beats a guess written as a fact.
- No score on an account and nothing at all on a person beyond name and job role.
- Anyone who asked not to be contacted stays off the list.
- You choose who to call, in small numbers, inside your own accounts; no contact or reason is invented and Claude calls no one.

## Next
Run acct-reason-to-call (Reason to Call) to work out, person by person, what is true and useful to say.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
