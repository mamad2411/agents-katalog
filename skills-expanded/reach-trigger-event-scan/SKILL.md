---
name: reach-trigger-event-scan
description: Scans for recent public events for one person and their organisation, each with date and link, sorted inside your window or too old, with private events left out, both readings of each event and a pitch-hook test. Use for "run reach-trigger-event-scan", "trigger event scan", "trigger events", "reason to reach out now", "why now", "recent news about this person", "find a hook for outreach", "anything recent to mention", part of the Claude Guide for Outreach Pack by 90n.
---

# Trigger Event Scan

## When To Use
You want a real reason to write now, not "just reaching out". This answers: has something happened for this person or their organisation recently that you could usefully acknowledge, and is it yours to mention?

## When Not To Use
If you need the fuller picture of someone's work, use Person Research Brief. If nothing recent turns up, do not force one: Reason to Write has reasons that need no event, and Buying Signals Watchlist tells you what to wait for.

## Inputs
- The person's name, role and organisation, with your briefs if you have them.
- Your window: how far back an event still counts, in your judgement.
- Any event you already heard about, and from where.
If you have none of this, I start from the name and organisation and mark the scan as a first draft.

## Approach
Trigger events are generic sales practice: a new role, a launch, a talk or an article changes what someone cares about this month. Here the event is a reason to be useful, never a hook. With Claude in Chrome or web search I read public pages only, read only, never LinkedIn. The failure it prevents: "congrats on the new role, we help new leaders with exactly this", which tells the person you were watching them in order to sell.

## Workflow
1. Ask at most three questions: your window, any event you already know of, and whether you have any history with this person at all.
2. Look for these event types, each with a date and a link: new role, launch, talk, article, award, hiring, organisation news. An event with no source is left out.
3. Sort by your window: inside it, or too old to mention. An old event can sit in a brief as background; it is not a reason to write now.
4. Remove anything private: health, family, a departure or a layoff the person did not announce themselves, anything they did not make public. These are excluded with no detail kept, not flagged as openings.
5. For each remaining event, set out both readings in one line each: how mentioning it could be useful to them, and how it could read as watching. From a stranger, a short and specific mention is the only kind that works; you decide.
6. Run the pitch-hook test: if mentioning the event only makes sense next to your offer, flag it as a pitch hook and leave it out.
7. If nothing passes, say "nothing worth mentioning". That result is valid.

## Output Format
```markdown
# Trigger Event Scan
Person: [name], [organisation] | Window: [your window] | Scanned: [date]
## Events inside the window
| Event | Type | Date | Source link | Useful to them | Reads as watching |
|---|---|---|---|---|---|
| [event] | [new role / launch / talk / article / award / hiring / organisation news] | [date] | [link] | [one line] | [one line] |
## Too old to mention
- [event, date, link]
## Left out as private
- [category only, no detail]
## Pitch hooks flagged
- [event, and why it only works next to your offer]
## Decision
[Your name] decides by [date] whether one event is worth mentioning, or to write for another reason, or to wait.
```

## Done When
- Every event has a date and a working link.
- Each event is inside your window or listed as too old.
- Private events are excluded with no detail recorded.
- No event is tied to your offer in any line.

## Quality Bar
- An event the person or their organisation did not make public is never used.
- Organisation news counts only if it plausibly touches this person's role; the line says why.
- Both readings are shown for every event; I never decide it is safe to mention.
- "Nothing worth mentioning" is better than a stretched event.
- An event is a reason to be useful, never a hook; you decide whether to mention it.

## Next
Run reach-reason-to-write (Reason to Write) to choose a reason that serves the other person.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
