---
name: reach-follow-up-tracker
description: Builds this week's follow-up tracker, with the replies you owe first, one follow-up per silent thread on a date you set with what it could add, the point where each thread closes and first calls to book with free times from your calendar. Use for "run reach-follow-up-tracker", "follow-up tracker", "follow up email", "who do I need to follow up with", "when should I follow up", "track my outreach replies", "replies I owe", "how many times should I follow up", part of the Claude Guide for Outreach Pack by 90n.
---

# Follow-Up Tracker

## When To Use
Good conversations die because nobody wrote back after the first reply. This answers one question for this week: which replies do I owe, which threads get one follow-up, and which do I let go?

## When Not To Use
If you need the lasting record of who you wrote to and what was promised, that is the Outreach Log; this tracker holds only what is due and is rebuilt each week. To understand what one reply is asking, use Reply Triage.

## Inputs
- Your Run of Ten Plan, or the names you wrote to and when.
- Optional: the Gmail connector, used to search and read threads with those people only. It never creates a draft and never sends.
- Optional: the Google Calendar connector, used to read your week for free times. It creates no event; you send the times.
If you have none of this, I start from a list you paste of who you wrote to, when, and whether they answered, and mark the tracker as a first draft.

## Approach
One follow-up, then stop, described generically. A follow-up list is plain practice: what is due from you, what is due from them, and a point where you stop. The judgement is in the stop. One polite follow-up is a courtesy; a third is a sequence. The timing figures quoted online have no primary source, so none appear here, and you set your own dates. The failure it prevents is the quiet one: they answered, you meant to reply, the week moved on.

## Workflow
1. Ask at most three questions: which run or names to check, how long you wait before one follow-up, and whether I may read your inbox and calendar this time.
2. For each person, find the thread and read only who wrote last and when. No message text is copied into the tracker.
3. Replies due from you go first. These are the ones that die: they wrote, and you have not answered.
4. For each silent thread where you wrote last: one follow-up, on a date you set. I note what it could add that is new (a useful link, a simpler question); you write it. If it would add nothing, the thread closes now.
5. After one follow-up with no reply, the thread closes. You may decide otherwise for a reason you write down. No second and third nudges.
6. Where someone agreed to talk, read your calendar and list free times. You send the times and create the event yourself.
7. Hand off: replies go to Reply Triage, and everything said or promised goes to your Outreach Log.

## Output Format
```markdown
# Follow-Up Tracker
Week of: [date] | Run: [number] | Your follow-up wait: [days you set]
## Replies due from you
| Person | They wrote on | What it needs from you | Reply by |
|---|---|---|---|
| [name] | [date] | [your words] | [date you set] |
## One follow-up
| Person | You wrote on | Follow-up on | What it could add |
|---|---|---|---|
| [name] | [date] | [date you set] | [something new, or "nothing: close"] |
## Closed
- [name]: one follow-up, no reply, closed on [date]
## First calls to book
- [name]: free times [from your calendar] · you send them and create the event
## Decision
[Your name] decides by [date] which replies and follow-ups to write and send, and which threads to close.
```

## Done When
- Replies due from you are listed before any follow-up.
- Each silent thread has at most one follow-up, on a date you set.
- Every closed thread shows its close date.
- No message text and no timing statistic appears anywhere.

## Quality Bar
- One follow-up, then stop; never a sequence.
- The tracker is about what is due, never about the person or their silence.
- Inbox and calendar are read for the names in this run only.
- Someone who asked you to stop is never on this tracker.
- Connectors are read only, never used to draft, send or book; you write every follow-up.

## Next
Run reach-reply-triage (Reply Triage) when a reply arrives, to see what it actually asks of you.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
