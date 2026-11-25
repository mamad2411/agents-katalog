---
name: multi-touch-sequence
description: >
  Draft a short, low-pressure follow-up series for a lead that went quiet. Use
  when the user says "follow-up sequence", "nudge a quiet lead", "lead went
  cold", "chase a prospect", "draft follow-up emails", or "no reply follow-up".
user-invokable: true
argument-hint: "[last message/thread + the action you want]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: leads
---

# Multi-Touch Follow-Up Sequence

Draft a short follow-up series for a lead that went quiet.

## When to use
A lead stopped replying and you want a 3-email series spread over about two weeks that nudges them without being pushy or guilt-trippy.

## What you'll need
The last thing you said to them (or the full thread) and what you're trying to get them to do next.

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are writing a short follow-up sequence for a lead who went quiet. Tone: friendly, low-pressure, never pushy or guilt-trippy.

What I offer:
[one line about your product or service]

The conversation so far:
[paste the last message I sent, or the full thread]

The action I want them to take:
[e.g. book a call, reply with a yes/no, confirm a quote]

Write 3 follow-up emails to send over about two weeks:
- Email 1 (a few days later): a light nudge that adds something useful — a relevant tip, link, or quick reminder of the value.
- Email 2 (about a week later): a different angle, e.g. ask if the timing is wrong or the need has changed.
- Email 3 (final): a short, graceful "I'll stop here unless you'd like to pick this back up" close.

Each email under 90 words, with a subject line. Reference the real context from the thread — no generic filler, no fake urgency or made-up discounts.
```

**Tip:** Tell Claude the gap between emails you prefer (e.g. "space them 3, 5, and 7 days apart") so the sequence fits your sales cycle.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
