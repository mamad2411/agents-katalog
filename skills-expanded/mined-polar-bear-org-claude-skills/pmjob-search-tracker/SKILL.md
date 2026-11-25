---
name: pmjob-search-tracker
description: Sets up a Job Search Tracker with one row per process (company, role, stage, next step, date, who you know, AI rule), runs a twenty minute weekly review that picks this week's actions, allows one nudge for a silent process and then a close, and reminds you to delete contact details when the search ends. Use for "run pmjob-search-tracker", "track my job search", "job search tracker", "weekly job search review", "which processes need a follow-up", "the recruiter went silent", "how many times do I chase", "organise my interview processes", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Job Search Tracker

## When To Use
Five processes at five stages and you just missed a follow-up. Use this once to set the table up, then for twenty minutes each week to decide what you do next and what you let go. It answers: across everything open, what are my moves this week?

## When Not To Use
This holds one row per process. The rounds inside one process belong in Interview Loop Map, and companies you have not approached yet belong in Target Company List. What you learned in a round goes in Interview Round Debrief, not in the notes column.

## Inputs
- Your open processes, however rough: company, role, where it stands, the last contact and its date
- Any date an employer gave you for hearing back, and the AI rule per process if you have a Candidate AI Use Plan
- Last week's tracker, if this is a review
If you have none of this, I start from the processes you can list from memory and mark the output as a first draft.

## Approach
A light pipeline log with a weekly review: the habit you already use for a roadmap, pointed at your own search. Three rules do the work. Every open row has a next step, an owner and a date. Silence gets one nudge, then a close. The table shows actions and dates, never a tally that judges you. The failure it prevents is the fourth polite chaser to a process that ended three weeks ago, sent on the day a live one needed your prep.

## Workflow
1. Ask at most three questions: which processes are open and at what stage; for each, whose move it is and since when; and how long a silence you allow before a nudge where the employer gave no date.
2. Build the rows: Company, Role, Stage, Last contact, Next step, Whose move, Due, Who I know, AI rule, Notes. Stages are in your words; a simple default is listed, applied, recruiter screen, loop, offer, closed. "Who I know" is a name and a role, with no contact details.
3. Repair first: any open row without a next step, an owner (me or them) and a date is fixed before anything else. A row you cannot give a next step is usually a row to close.
4. Run the weekly review in fixed order, twenty minutes: update stages; rows where it is my move; rows gone silent; pick three to five actions for the week; one line on what to stop doing.
5. Apply the silence rule: one polite nudge once the date the employer gave has passed, or after the gap you set. Then the row closes as "no reply" and you move on. A closed row can reopen if they come back. You write and send the nudge yourself.
6. Close out when the search ends: delete the contact details of recruiters and contacts you no longer need, wherever you kept them. Keeping other people's personal data raises data protection questions, so check with a qualified adviser.
7. Keep it somewhere you will open weekly. In the desktop app with Google Drive connected, the table can become a Google Sheet created from the chat; a Project can hold it between reviews; pasting last week's table back works too.

## Output Format
```markdown
# Job Search Tracker
**Review date:** [date] · **Silence gap you set:** [your number of days] · **Open processes:** [count from your rows]
## Processes
| Company | Role | Stage | Last contact | Next step | Whose move | Due | Who I know | AI rule | Notes |
|---|---|---|---|---|---|---|---|---|---|
| [company] | [role] | [stage] | [date, what] | [next step] | [me / them] | [date] | [name, role, or nobody yet] | [rule and where written, or not asked yet] | [ ] |
## This week
| # | Action | Process | By |
|---|---|---|---|
| 1 | [action] | [company, role] | [date] |
**Stop doing:** [one line]
## Silent processes
| Process | Date they gave, or your gap | Nudge sent on | Outcome |
|---|---|---|---|
| [company, role] | [date] | [date, or not yet] | [replied / closed as no reply on [date], reopens if they come back] |
## End of search
- [ ] Contact details of recruiters and contacts no longer needed are deleted, on [date]
## Decision
You decide this week's three to five actions and which silent rows to close, by [date].
```

## Done When
- Every open row has a next step, an owner and a date
- This week holds three to five actions, each tied to a row, and each silent row shows one nudge at most or a close
- The AI rule column is filled or reads "not asked yet"

## Quality Bar
- Dates and actions only: no count that rates your progress and no comparison with any average search length
- One nudge, never a second or third chaser; names and roles only in the table, with no contact details saved to memory
- The end-of-search delete step is on the page from the first version
- The tracker logs your real processes; you send every nudge yourself and nothing is applied to or sent for you.

## Next
Run pmjob-offer-comparison (Offer Comparison) when a process reaches an offer.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
