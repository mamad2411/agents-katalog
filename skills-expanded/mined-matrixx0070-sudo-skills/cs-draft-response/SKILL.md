---
name: cs-draft-response
version: 1.0.0
description: Draft a professional, empathetic customer reply matched to sentiment and outcome — acknowledge, answer, next steps — with a shorter chat variant.
author: matrixx0070
tags: [customer-support, writing, empathy, tone, communication, de-escalation]
capabilities: []
---

## When to use

Use this to write a customer-facing reply: answering a question, delivering bad news, apologizing for an outage, declining a request, or following up. The output is ready to send — clear, human, and on-brand.

**Not for:** finding the facts to say (cs-research first), sorting or prioritizing the ticket (cs-ticket-triage), or handing off internally (cs-escalation). Never draft over facts you have not verified.

## Method

1. Read for the real ask and the emotional state (frustrated, confused, urgent, calm). **Decision point:** if upset, lead with acknowledgment; if neutral, lead with the answer.
2. Decide the outcome you can actually deliver: full fix, partial fix + timeline, workaround, or a reasoned "no" with an alternative. Never over-promise.
3. Structure: acknowledge → answer/action → next steps → invite follow-up. Put the most important line first for scanners.
4. Be specific — reference their account, name the exact steps, give real dates. Replace "we're looking into it" with what and when.
5. For bad news or a decline: apologize once and sincerely, explain briefly, then pivot to what you *can* do. No blame, jargon, or defensiveness.
6. Close by making the next move easy and setting a response-time expectation.

## Example

> **Situation:** Angry customer, export broken 2 days, no reply yet.
> **Subject:** Your export issue — fixed, and what happened
> Hi Sam — I'm sorry this has blocked you for two days; that's on us. The export bug was fixed this morning, and I've re-run your Q2 report — it's in your dashboard now. As a thank-you for your patience I've added a one-month credit. If anything still looks off, reply here and it comes straight to me. — Alex

## Pitfalls

- Leading with the answer when the customer is angry — they need to feel heard first.
- Over-apologizing (three "sorry"s) — it reads as weakness; apologize once, then act.
- Vague reassurance with no date or step — erodes trust faster than bad news.
- Hedging a clear "no" — a kind, direct decline with an alternative beats false hope.

## Output format

```
Subject: <if email>
Tone read: <detected sentiment + chosen register>
Draft response:
<ready to send>

Short variant (chat/quick reply):
<1-3 sentences>

Notes: <verify or personalize before sending>
```
