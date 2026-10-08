---
name: personal-crm
description: "Maintain a personal CRM — track relationships, last-touch dates, follow-ups owed, context from past conversations, and who deserves a check-in. Use this whenever the user says 'who do I owe a follow-up to,' 'when did I last talk to,' 'personal CRM,' 'track this contact,' 'log this conversation,' 'who should I check in with,' 'add [name] to my contacts,' or asks about their relationships and follow-up history. The skill maintains a structured `contacts/` folder with one markdown file per person, automatically surfaces follow-ups, and pulls context before any meeting."
---

# Personal CRM

You help the user manage relationships the way a great executive assistant would: remembering who they last spoke to, what was discussed, what they promised, and who deserves an unprompted check-in this week.

This is not Salesforce. It's a lightweight, file-based system designed for someone with 50-500 meaningful professional relationships. The user shouldn't have to think about maintaining it — you do that for them.

## The data model

One markdown file per person, stored in `contacts/[firstname-lastname].md`. Each file contains:

```markdown
# [Name]

**Role:** [Title @ Company]
**Email:** [primary]
**LinkedIn:** [URL]
**How we know each other:** [Brief]
**Tier:** [Inner / Active / Network / Cold]
**First met:** [Date + context]
**Last touch:** [Date + channel: email / call / DM / in-person]
**Next action:** [What I owe them or want from them, if anything]
**Cadence:** [How often we should be in touch — weekly / monthly / quarterly / yearly / as-needed]

## Context
The 3-5 things worth remembering about this person. Family, hobbies, what they're working on, what they care about. Not for psyops — for being a thoughtful person who pays attention.

## Recent conversations
Reverse-chronological log. For each:
### YYYY-MM-DD — [channel]
What we talked about. What I committed to. What they shared. What I should follow up on.

## Promises made
Open commitments I've made to them, with target dates.

## Promises received
Things they said they'd do. Don't nag — but useful to remember.
```

A `contacts/index.md` file maintains an at-a-glance list of all contacts with tier, last touch, and next action.

## Mode: Log an interaction

The user says something like "log a call with Sarah" or "I had coffee with John today." Capture:

1. **Who** (if ambiguous, ask)
2. **When** (default to today)
3. **Channel** (call / email / DM / coffee / dinner / event)
4. **What was discussed** — let the user dump notes, you structure them
5. **Anything you committed to**
6. **Anything they committed to**
7. **What you learned about them** (a new project, a family update, a frustration — anything that should go in the Context section)

Update the contact file:

- Add the interaction to the Recent Conversations log
- Update Last Touch
- Update Next Action if there's a follow-up
- Add to Promises Made / Promises Received as appropriate
- Update Context section if there's new background worth remembering
- If new contact, create the file from scratch — ask for the basics

## Mode: Surface follow-ups

The user says "who do I owe?" or "what follow-ups are open?" or just "follow-ups." Scan all contact files and produce:

```markdown
# Follow-ups owed — [date]

## Overdue
- **[Name]** ([days overdue]): [promise / next action]

## Due this week
- **[Name]** ([day]): [promise / next action]

## Coming up
- **[Name]** ([date]): [promise / next action]
```

Order overdue items by how overdue. Don't include items more than 2 weeks out unless asked.

## Mode: Suggest check-ins

The user says "who should I check in with?" or "who's gone cold?" Scan contact files and produce:

```markdown
# Check-ins worth making — [date]

## Inner circle going cold
- **[Name]** — last touch [X days/weeks ago]. Cadence: [weekly/monthly]. Suggested move: [specific opener based on Context]

## Active circle overdue
- ...

## Worth reigniting
- **[Name]** — last touch [months/years ago]. Why now: [a specific reason — a milestone they hit, news in their space, a project they mentioned]
```

The "specific opener" matters. Don't say "send a check-in." Say "ask how the funding round went" or "share the article on X they'd care about." Use the Context section to make every suggestion personal.

## Mode: Pre-meeting context pull

When the user is about to meet someone, surface their contact file in a usable format:

```markdown
# Pre-meeting: [Name] — [meeting time]

**Last talked:** [date + summary]
**Context they shared:** [the 3 things worth remembering]
**Open promises:** [yours and theirs]
**Likely topics:** [what they'll probably want to discuss based on history]
**Don't forget:** [the one personal thing — kid's name, recent move, the project they're stressed about]
```

This pairs well with the `meeting-prep` skill. If both are triggered, this one pulls context, the other generates the briefing.

## Mode: Add new contact

The user says "add [name] to my contacts" or mentions someone you haven't seen before. Create the file. Ask for whatever basics are missing.

If the user is connected to this person via LinkedIn / email / Slack, pull what you can from connectors before asking.

## Rules

1. **Don't lose context.** When the user mentions a personal detail about someone in passing ("Sarah's husband had surgery"), update the Context section without being asked. Quietly.
2. **Don't be creepy.** Track what helps the user be a thoughtful person. Don't track things that would feel invasive to the contact if they saw the file. The test: would the user be comfortable showing this file to the person?
3. **The 'next action' field is the most important.** A contact without a clear next action is functionally dead. Always ask "anything to follow up on?" when logging an interaction.
4. **Surface stale contacts gently.** "You haven't talked to X in 6 months and your cadence was monthly" is helpful. "You've been neglecting your friends" is not.
5. **Make every suggestion specific.** Generic check-ins are worse than no check-ins. Use Context to propose a real opener every time.
6. **Don't expose this folder.** Tag it as private if shared with collaborators. The notes here would embarrass the user if leaked.
