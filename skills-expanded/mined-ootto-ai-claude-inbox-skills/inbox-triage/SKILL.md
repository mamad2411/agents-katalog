---
name: inbox-triage
description: >
  Sort a full inbox into reply-now / later / ignore, with drafts for the urgent
  ones. Use when the user says "triage my inbox", "sort my emails", "inbox
  triage", "what should I reply to", "clear my inbox", or "which emails need a
  response".
user-invokable: true
argument-hint: "[list of unread emails]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: inbox
---

# Inbox Triage

Sort a full inbox into reply-now / later / ignore, with drafts for the urgent ones.

## When to use
Your inbox is full and you need to know what actually needs a response today, what can wait, and what to archive — plus ready-to-send drafts for the urgent ones.

## What you'll need
A list of unread emails (sender, subject, and a line or two of each message — paste as many as you want).

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are my executive assistant triaging my inbox. Below is a list of unread emails, each with sender, subject, and a short preview.

[paste your emails here — one per block, with sender, subject, and preview]

Sort every email into exactly one of three buckets:
1. REPLY NOW — needs a response today (a real person waiting, a deadline, money, or a decision blocked on me)
2. LATER — matters but can wait this week (FYIs I should read, low-urgency requests)
3. IGNORE — newsletters, promos, automated notifications, or anything I can safely archive

For each email give one short line: sender — why it's in that bucket.
Then, for every REPLY NOW email only, write a ready-to-send draft reply: plain, friendly, professional, 2-4 sentences, no filler. If a reply needs information only I have, leave a clearly marked [blank] for me to fill.

Output as three headed sections (Reply Now, Later, Ignore), with the drafts under each Reply Now item.
```

**Tip:** Paste the actual preview text, not just subject lines — the more of each message Claude can see, the better it judges urgency and writes a usable draft.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
