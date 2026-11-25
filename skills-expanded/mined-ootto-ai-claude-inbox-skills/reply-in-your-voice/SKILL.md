---
name: reply-in-your-voice
description: >
  Draft a reply to any message that sounds like you, learned from your own past
  emails. Use when the user says "reply in my voice", "write this like me",
  "draft a reply that sounds like me", "respond to this email", "match my tone",
  or "answer this in my style".
user-invokable: true
argument-hint: "[message to reply to + writing samples]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: inbox
---

# Reply in Your Voice

Draft a reply to any message that sounds like you.

## When to use
You need to answer an email and want the draft to sound like you wrote it — not more corporate or more casual than you actually are.

## What you'll need
The message you're replying to, plus 2-3 emails you've actually written before (so Claude can learn your voice).

## Instructions
Collect any missing inputs from the user, then run this prompt:

```
You are writing an email reply in my voice. First, study how I write from these samples of my own past emails:

[paste 2-3 emails you've written]

Notice my tone, sentence length, greeting and sign-off, level of formality, and whether I use things like dashes, lists, or short paragraphs. Match it — don't make me sound more corporate or more casual than I am.

Now write a reply to this message:

[paste the email you're replying to]

What I want to get across: [say in plain words what you want to say — e.g. "yes but push the call to Thursday", "no thanks, not a fit right now"]

Write the reply so it sounds like I wrote it. Keep it as short as the situation allows. Don't add greetings or closings I wouldn't use. Give me just the reply text, ready to paste.
```

**Tip:** The quality is almost entirely in the writing samples. Pick emails where you sound the most like yourself — a quick one to a colleague beats a polished one to a client.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs invoicing, follow-up, and reports for you, automatically. [Book a demo →](https://www.ootto.ai)
