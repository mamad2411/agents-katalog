---
name: faq-responder
description: >
  Draft answers to your most common inbound questions, using only the facts about
  your business. Use when the user says "answer this customer question", "draft an
  FAQ reply", "respond to this inquiry", "write answers to common questions",
  "reply to this customer", or "build a reply library".
user-invokable: true
argument-hint: "[business facts + incoming question(s)]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: inbox
---

# FAQ Responder

Draft answers to your most common inbound questions.

## When to use
You get the same questions over and over — pricing, hours, turnaround, policies — and you want accurate, ready-to-send answers built only from your real business facts.

## What you'll need
The question someone sent you (or a list of the questions you get asked most), plus a few facts about your business.

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are drafting answers to questions people email my business. Here is what you should know about us, so every answer is accurate:

[paste the facts: what you sell, pricing, hours, turnaround times, refund/cancellation policy, how to book or buy, anything else you get asked about]

Here is the question (or list of questions) I need answered:

[paste the incoming question, or a list of your most common questions]

For each question, write a short, friendly answer I can send as-is. Rules:
- Only use the facts I gave you. If a question can't be answered from those facts, don't make something up — instead write the answer with a clearly marked [blank] where the missing info goes.
- Keep each answer to a few sentences, warm but professional.
- Where it helps, end with a simple next step (e.g. "Want me to send the booking link?").

Give me each answer ready to paste, labeled with its question.
```

**Tip:** Build this once into a reusable reply library — paste your top 10 questions at the same time and save the answers as templates you tweak per person.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
