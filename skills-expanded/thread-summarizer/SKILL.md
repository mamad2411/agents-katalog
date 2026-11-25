---
name: thread-summarizer
description: >
  Turn a long email thread into key points and the decision needed. Use when the
  user says "summarize this thread", "catch me up on this email", "what's this
  thread about", "TL;DR this thread", "what do I need to do here", or "summarize
  this email chain".
user-invokable: true
argument-hint: "[full email thread]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: inbox
---

# Thread Summarizer

Turn a long email thread into key points and the decision needed.

## When to use
A long back-and-forth has piled up and you need to catch up in 30 seconds — what it's about, what's been decided, what's open, and what's waiting on you.

## What you'll need
A long email thread (paste the whole thing, oldest to newest).

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are summarizing a long email thread for me so I can catch up in 30 seconds. Here is the full thread:

[paste the entire thread, oldest message first]

Give me:
1. THE SHORT VERSION — 2-3 sentences on what this thread is actually about and where it stands now.
2. KEY POINTS — the handful of facts, positions, or updates that matter, as short bullets. Note who said what when it's important (e.g. "Sam wants to delay to Q3").
3. DECISIONS ALREADY MADE — anything the group has agreed on.
4. OPEN QUESTIONS — what's still unresolved.
5. WHAT I NEED TO DO — the specific decision or action waiting on me, if any. If nothing is waiting on me, say so plainly.

Be accurate and neutral — don't invent agreement that isn't there. Keep the whole thing tight; skip the pleasantries in the emails.
```

**Tip:** Paste the thread oldest-message-first so the story reads in order. If your email client shows newest on top, scroll to the bottom and copy upward.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
