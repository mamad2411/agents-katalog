---
name: pre-meeting-context
description: Use this skill before any meeting with a client, partner, prospect, or recurring contact. Triggers on phrases like "prep for [name]", "I have a meeting with [name]", "meeting brief for [company]", or when the user references an upcoming call with a specific person. Produces a one-page briefing with relationship history, open items, and suggested talking points.
---

# Pre-Meeting Context Warmer

## When to use this skill

The user is preparing for a meeting with a specific person or company. They want the same context they would have walking in if they had a chief of staff who had memorized the relationship. Not a smart-sounding agenda. A real briefing.

## Input the user provides

- Name of the person or company they are meeting with
- Optionally: time of meeting, purpose, channel (in-person, video, phone)
- Optionally: pointers to email threads, CRM, notes, or shared docs

If the user only provides a name, ask once for clarifying scope (which company, what context). Do not ask multiple rounds of questions.

## What this skill does

1. Gathers what is available about the relationship:
   - Last 6 months of email exchanges (if accessible)
   - Documented meeting notes from prior calls
   - Open threads, pending asks on either side
   - Concerns or objections this person has named in past conversations
   - Their role, reporting line, and decision-making authority if known

2. Produces a one-page briefing in the structure below.

## Output structure

```
# Meeting Brief: [Name / Company]
*[Date and time of meeting]*

## Relationship Snapshot
- One paragraph on who this person is, what they care about, where this relationship stands
- Last meaningful interaction (when, what, outcome)

## Open Items
- Pending asks from them to us (with status)
- Pending asks from us to them (with status)
- Unresolved questions from the last conversation

## Suggested Talking Points
- 2-4 things worth raising, ordered by importance
- For each, one sentence on why it matters now

## Risks and Things to Avoid
- Topics this person has reacted poorly to in the past
- Commitments we made that we have not yet delivered on (acknowledge upfront)
- Politically sensitive items in their organization
```

## Calibration notes

- Length cap: one page. If the briefing runs longer, cut talking points first, then relationship snapshot.
- Use plain language. The reader is doing this between two other meetings and has 90 seconds to skim.
- Surface the uncomfortable items in "Risks and Things to Avoid" rather than burying them. The hidden veto in a meeting is usually a commitment we forgot we made.
- If data is missing for a section, say so explicitly ("No prior meeting notes available") rather than making things up.

## When NOT to use this skill

- Internal meetings with team members the user works with daily
- Group meetings where the prep is shared, not personal
- First-time introductions where there is no prior context to retrieve

For those, a lighter agenda template is more appropriate.
