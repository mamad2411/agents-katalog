---
name: reach-buying-signals-watchlist
description: Builds a buying signals watchlist for the accounts on your list, with the one or two public signs worth watching per account, the page where each would appear, how often you look, the alert words, what you will do when a sign appears and the accounts to stop watching. Use for "run reach-buying-signals-watchlist", "buying signals watchlist", "buying signals", "what should I watch for", "account watchlist", "set up alerts for my accounts", "nothing has happened there yet", "when should I reach out", part of the Claude Guide for Outreach Pack by 90n.
---

# Buying Signals Watchlist

## When To Use
The account fits and nothing has happened there yet. Writing now would be writing for no reason. This answers: what would have to happen for a message to make sense, where would I see it, and how much of my week does watching cost?

## When Not To Use
If you want to know what has already happened, run Trigger Event Scan; this skill looks ahead. If you do not yet know which moments start a need for your work, build the Buying Situations Map first.

## Inputs
- Your Target Account List, with the accounts marked "none yet" for a reason to write.
- Your Buying Situations Map, or the two or three moments that usually start a need for your work.
- How much time a week you will give to watching.
If you have none of this, I start from three accounts and one situation you describe, and mark the watchlist as a first draft.

## Approach
Watching public pages and news alerts by hand. For each account you pick one or two signs from your own buying situations and the single page where each would show, then look on a rhythm you can keep. A news alert, as Google Search Help describes under "Create an alert", can bring new results for words you choose to your inbox. No bought intent data, no tracking of people, nothing behind a login, and any browsing is read only and never on LinkedIn. The failure it prevents: checking forty websites every morning for a week, then never again.

## Workflow
1. Ask at most three questions: which accounts are waiting, which situations matter most, and how much time a week you will spend watching.
2. For each account, pick one or two signs from your map, written as something public that either has or has not happened: a named role advertised, a new leader in the role you serve, an announced project.
3. Name the one page where each sign would appear (the careers page, the news page, the leadership page, a regulator's register) and link it.
4. Write alert words for a news alert: the organisation's name plus the words of the sign. Say what an alert will miss, such as pages that are not indexed, and expect noise for common names.
5. Set the rhythm: how often you look, and on which day. Watching is about organisations and public roles; no person's activity is followed.
6. Write what you will do when a sign appears: run the Trigger Event Scan, then decide. A sign is a reason to look, not yet a reason to write.
7. Set the stop: the date after which an account with no sign leaves the watchlist.

## Output Format
```markdown
# Buying Signals Watchlist
Accounts watched: [number] | Time per week: [your limit] | Look on: [day] | Started: [date]
## Signs per account
| Account | Sign to watch (public, yes or no) | Page where it would appear | Alert words | Seen? (date, link) |
|---|---|---|---|---|
| [organisation] | [sign from your situations map] | [link] | [organisation name + words] | [no / yes, date, link] |
## When a sign appears
[What you do next, in one line.]
## Stop watching
| Account | Leaves the list on | Reason |
|---|---|---|
| [organisation] | [date you set] | [no sign / no longer fits] |
## Decision
[Your name] decides by [date] which accounts stay on the watchlist and which sign, once seen, is worth a scan.
```

## Done When
- Each account has at most two signs, each one public and answerable yes or no.
- Each sign has one linked page.
- A rhythm and a weekly time limit are written down.
- Every account has a date on which it leaves the list.

## Quality Bar
- Signs come from your own buying situations, not a generic list of "intent signals".
- Organisations and public roles are watched; individuals are not followed.
- No purchased data, no tracking pixels, no tools that monitor people.
- A sign that appeared is recorded with its date and link, like any other fact.
- Claude helps you decide what to watch; you look, and you decide whether a sign is a reason to write.

## Next
Run reach-trigger-event-scan (Trigger Event Scan) when a sign appears, to check it before you write.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
