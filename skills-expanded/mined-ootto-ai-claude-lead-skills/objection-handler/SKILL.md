---
name: objection-handler
description: >
  Write a calm, helpful reply that moves a stalled deal forward. Use when the
  user says "handle an objection", "they said it's too expensive", "reply to a
  price concern", "prospect went quiet on price", "answer a sales objection", or
  "unstick a deal".
user-invokable: true
argument-hint: "[their objection + facts you can use]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: leads
---

# Objection Handler

Write a reply that moves a stalled deal forward.

## When to use
A prospect raised a concern — price, timing, "need to think about it", a competitor — and the deal stalled. You want a reply that addresses it honestly with the facts you have.

## What you'll need
The message where they raised the concern (or the full thread) and any facts that answer it.

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are helping me reply to a prospect who raised an objection and stalled the deal. Tone: calm, confident, and helpful — never defensive or salesy.

What I offer:
[one or two lines about your product or service]

Their message with the objection:
[paste what they said — the price worry, timing, "need to think about it", competitor comparison, etc.]

Facts I can use to respond (only use these — don't invent any):
[paste real details: pricing flexibility, guarantees, results, what's included, why you're different]

Write a reply (under 150 words) that:
1. Acknowledges their concern genuinely, without dismissing it.
2. Addresses it with the facts above — be specific, not vague reassurance.
3. Reframes around the outcome they care about.
4. Ends with one easy next step that lowers the risk for them (a call, a trial, a smaller first step).

If their objection is reasonable and I can't overcome it honestly, say so and suggest a fair alternative instead of pushing. Give me a subject line and the body.
```

**Tip:** Name the objection type in one word at the top (e.g. "price", "timing", "competitor") — it helps Claude pick the right angle instead of hedging across all of them.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
