---
name: meeting-notes-to-action-items
description: >
  Turn raw meeting notes into owners, deadlines, and follow-up emails. Use when
  the user says "turn my notes into action items", "meeting follow-up", "who owns
  what from this meeting", "action items from these notes", "send meeting
  follow-ups", or "what did we decide".
user-invokable: true
argument-hint: "[raw meeting notes + attendees]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: inbox
---

# Meeting Notes to Action Items

Turn raw notes into owners, deadlines, and follow-up emails.

## When to use
A meeting just ended and you have messy notes — you need a clean list of who owns what by when, the decisions made, and a ready-to-send follow-up for each person.

## What you'll need
Your raw meeting notes (messy is fine), and the names of who was in the room.

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are turning my raw meeting notes into a clean set of action items and follow-ups. Here are the notes:

[paste your raw notes — bullet points, fragments, whatever you have]

People in the meeting: [list names]

Do three things:

1. ACTION ITEMS — a table with three columns: Task | Owner | Deadline. Pull every commitment or next step from the notes. Assign the owner named in the notes; if no owner was given, put "[unassigned]". If a deadline was mentioned use it, otherwise put "[no date]". Don't invent tasks that aren't in the notes.

2. DECISIONS — a short list of anything the group actually decided.

3. FOLLOW-UP EMAILS — for each person who owns an action item, write a short, friendly email reminding them of just their items and deadlines. Keep each one to a few sentences, ready to send.

Flag anything ambiguous instead of guessing.
```

**Tip:** Don't clean up your notes first — paste them raw. Claude is good at making sense of shorthand, and over-editing risks dropping a commitment you'd want captured.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
