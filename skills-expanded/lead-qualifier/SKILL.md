---
name: lead-qualifier
description: >
  Score an inbound enquiry on fit and intent and suggest the next action. Use
  when the user says "qualify this lead", "score this lead", "is this lead hot
  or cold", "rate this enquiry", "should I follow up", or "qualify inbound".
user-invokable: true
argument-hint: "[the inbound message + what you sell]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: leads
---

# Lead Qualifier

Score an inbound enquiry and suggest the next action.

## When to use
A new enquiry lands and you want to know how good it is — fit, intent, what's missing, and whether to reply now, book a call, send pricing, or nurture later.

## What you'll need
The inbound message (email, form submission, or DM) and a one-line description of what you sell and your typical deal size.

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are a sales qualifier for my business. Here is what I sell and my typical deal size:
[describe your offer and price range]

Here is a new inbound enquiry:
[paste the full message, including any name, company, and contact details]

Do the following:
1. Score this lead from 1 to 10 on fit and intent, and say in one sentence why.
2. Label it Hot, Warm, or Cold.
3. List what you can infer about them: budget signals, timeline, decision-maker or not, and the specific problem they want solved.
4. Flag anything missing that I'd need before I can quote (max 3 items).
5. Recommend the single best next action (reply now, book a call, send pricing, or nurture later) and why.

Only use facts from the message. If something is unknown, say "unknown" — do not guess. Keep the whole response under 200 words, plain text, no preamble.
```

**Tip:** Paste a couple of past deals that closed (and a couple that didn't) above the enquiry so it learns what a good lead looks like for you specifically.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
