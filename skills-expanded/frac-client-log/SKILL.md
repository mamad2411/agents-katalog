---
name: frac-client-log
description: Keeps one running log per client for a fractional leader, with decisions, commitments made and received, open asks, scope asks as they arrive and days used, plus a "where we left off" page that reloads the context before each session, with one client per workspace and never mixed. Use for "run frac-client-log", "start a client log", "where did we leave off with this client", "what did I promise whom", "log this week's decisions and commitments", "reload my context for this client", "per-client notebook", part of the Claude for Fractional Leaders Pack by 90n.
---

# Client Log

## When To Use
Every Tuesday starts with twenty minutes of remembering what you promised whom. Notes sit in three tools, a decision was made in a corridor, and the "can you also" from last Thursday is in a chat you cannot find. Use it at the end of every client session to log, and at the start of the next to reload.

## When Not To Use
If one decision needs its full reasoning, options and dissent, run Decision Record and link it from the log. If you want to compare your clients side by side, run Weekly Review Across Clients; the log itself never holds more than one client.

## Inputs
- Today's notes for this one client: meeting notes, messages, what was decided, asked and promised
- The existing log for this client, if there is one
- Days or half-days worked for this client since the last entry
If you have none of this, I start from what you remember of the last session, mark those entries "from memory" and mark the log as a first draft.

## Approach
A per-client notebook with a decision log, a practitioner convention; a fractional marketplace's guidance on knowledge transfer makes the same point from the other end: document from day one, because the handover is built from what you logged. The judgment is to log little and always: six entry types, each dated, each with its source. The rule that matters most is separation. Keep one Project per client where you have Projects (beta), or one chat and one folder per client. If something pasted here belongs to another client, I stop and say so.

## Workflow
1. Ask at most three questions: which client is this; what happened since the last entry; how many days or half-days did you work for them?
2. Sort what you paste into six entry types: decision, commitment I made, commitment made to me, open ask, scope ask, days used. Each entry gets a date, who was involved by role, and its source. Nothing is added that is not in your notes.
3. Flag every scope ask the day it arrives, with the line of the statement of work or charter it touches if you can name it. Absorbing the first one silently is what makes the third one hard to price.
4. Close what is done: mark commitments kept, late or dropped, with the date. A late commitment of yours is shown first, not hidden.
5. Total the days used this month against the days agreed.
6. Rebuild the "where we left off" page: the last decisions, what you owe and by when, what you are owed, open asks, and the first thing to do when you sit down.

## Output Format
```markdown
# Client Log
Client: [one client only] · Workspace: [Project or folder for this client] · Updated: [date]
## Where we left off
- Last decisions: [decision, date]
- I owe: [commitment] to [role] by [date]
- I am owed: [commitment] from [role] by [date]
- First thing next session: [action]
## Log
| Date | Type | Entry | Who (role) | Source | Status |
|---|---|---|---|---|---|
| [date] | [decision / I committed / committed to me / open ask / scope ask / days used] | [as in your notes] | [role] | [meeting, message] | [open / kept / late / dropped] |
## Scope asks waiting
| Date | Ask | Baseline line it touches | Raised with the CEO? |
|---|---|---|---|
| [date] | [ask] | [statement of work or charter line, or unclear] | [yes, date / not yet] |
## Days
Used this month: [n] · Agreed: [n] · Difference: [n]
## Decision
[You] decide before the next session which scope asks to raise with [CEO], and by when.
```

## Done When
- Every entry has a date, a type and a source
- Scope asks are listed separately with the baseline line they touch
- Days used are totalled against days agreed
- "Where we left off" can be read in two minutes

## Quality Bar
- Entries record what was said and done, never a judgment of the person
- Nothing is tidied into a decision that was only discussed; it is logged as an open ask
- "From memory" entries stay marked until confirmed
- Late or dropped commitments of your own are logged as plainly as anyone else's
- One client per log and per workspace; nothing is invented, and if a note belongs to another client I stop and leave it out

## Next
Run frac-weekly-review (Weekly Review Across Clients) to compare, for your eyes only, where the week's days went.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
