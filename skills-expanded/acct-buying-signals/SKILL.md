---
name: acct-buying-signals
description: Builds a buying signals brief for one named account or a short list, with dated public events, a link for each, what each might mean marked as an inference, the question it lets you ask and the signals looked for and not found. Use for "run acct-buying-signals", "buying signals", "trigger events for this account", "why now for this account", "what changed at this customer", "find a reason to call this account", "account news scan", "sales intelligence on my accounts", part of the Claude for Account Executives Pack by 90n.
---

# Buying Signals Brief

## When To Use
You want to call an account you own and "just checking in" is all you have. Run this for one account, or for a short list from your territory, before a call block. It answers: what has publicly changed at this account, when, and what does that let you ask?

## When Not To Use
Before a booked meeting you need the whole picture: run Account Research Brief. If you already hold a signal and want to work out what to say to one person, run Reason to Call. This is not a way to find new companies; it stays inside accounts you already own.

## Inputs
- The account names (ten at most per run) and their websites.
- What you sell them or could, in one line, so I know which changes matter.
- How far back a signal still counts for you (you set the window).
If you have none of this beyond a name, I start from the company's own newsroom and mark the output as a first draft. With Claude in Chrome I read the public pages myself; otherwise paste them.

## Approach
Trigger events read from public sources, with a source for every signal and unknowns stated: common practice, described here generically. A signal is a reason to ask a question, never proof of a need. The failure it prevents is the confident opener built on a guess ("I see you are investing heavily in...") that the customer corrects in the first ten seconds. A quiet account gets a short brief that says so.

## Workflow
1. I ask at most three questions: which accounts, what kind of change makes your offer relevant, and how old a signal may be.
2. I read only public sources the company controls or files: its newsroom and announcements, its public filings, the public company register of its country, its own job page. No purchased intent data, no private profiles, no automated collection from social networks.
3. I look for six signal types, in this order: a leadership change in a relevant role, an announcement (funding, acquisition, new site, partnership), a filing, a new role posted, a product or service launch, a goal stated in public.
4. Each signal gets one row: what happened, the link, the date of the event and the date I read it. No link, no row.
5. Beside each I write what it might mean, marked "inference", and the open question it lets you ask. The question never assumes the inference is true.
6. I list what I looked for and did not find, per signal type, so you know a blank is a checked blank and not a gap in the search.
7. Signals older than your window move to a dated "older context" line. I do not rank the accounts or score the signals; you choose which ones earn a call.

## Output Format
```markdown
# Buying Signals Brief
Accounts: [names] · Window: [set by you] · Sources read: [list] · Research checked [date]
## Signals found
| Account | Signal type | What happened | Link | Event date | Might mean (inference) | Question it lets you ask |
|---|---|---|---|---|---|---|
| [account] | [leadership / announcement / filing / role posted / launch / stated goal] | [fact] | [link] | [date] | [inference] | [open question] |
## Looked for and not found
| Account | Signal types with nothing found | Sources checked |
|---|---|---|
| [account] | [types] | [pages] |
## Older context
- [account]: [fact], [date], [link]
## Decision
[You] choose which signals earn a call this week, by [date], and verify each link before you use it.
```

## Done When
- Every signal has a working link and an event date.
- Every "might mean" is marked as an inference and has a question beside it.
- The not-found table is filled for every account.
- Nothing in the brief comes from outside public sources and your own notes.

## Quality Bar
- One signal, one link, one date; a signal I cannot link is left out.
- People appear only through a public change of job role; nothing personal.
- No score, no ranking of accounts, no "intent" label.
- A thin footprint gives a short brief; I never pad it.
- No signal is invented: each comes from a public source with its date and link, and you decide who to call.

## Next
Run acct-call-list (Weekly Call List) to choose the 10 to 20 contacts these signals give you a true reason to call.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
