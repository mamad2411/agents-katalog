---
name: customer-support-inbox
description: Triages customer support messages by severity, drafts on-brand replies, escalates refunds/legal/angry cases to a human, and captures repeat questions into an FAQ file. Use when the user says "work the support inbox", "answer these customer messages", "triage support", or support requests are piling up. Don't use for the user's own general email — use email-triage — or for mining happy customers for quotes — use testimonial-harvester.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Support, Customers, Triage]
    related_skills: [email-triage, testimonial-harvester, weekly-revenue-report]
---

# Customer Support Inbox

Works a batch of customer messages the way a good support lead would: severity first, empathy always, drafts for everything, and a hard human-escalation line for money, law, and anger. Every reply is a **draft the user approves before it goes out**, and every repeat question feeds an FAQ file so the inbox shrinks over time instead of just cycling.

## When to Use

- A batch of support messages needs triage and replies (email, DMs, form submissions the user pastes or points to).
- User asks "handle support", "what do these customers need", "draft replies to these".
- Building or updating the product FAQ from real questions.
- **Not for:** the user's personal/general inbox — use `email-triage`. Not for soliciting reviews or quotes — use `testimonial-harvester`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Load the batch | `read_file` the export, or pull via the connected email tool (read-only) |
| Severity buckets | P1 broken/can't-use · P2 blocked-but-working · P3 question · P4 feedback/praise |
| Escalation test | Refund/chargeback, legal words, or angry tone → **human**, no drafted resolution |
| FAQ file | `faq.md` in the product folder — `grep -i "keyword" faq.md` before drafting from scratch |
| Log the run | append one summary line to `support-log.md` (date, counts, escalations) |
| Spot repeat questions | `grep -c -i "password reset" faq.md` and eyeball the batch for twins |
| Trend check | `tail -5 support-log.md` — is P1 volume rising week over week? |

## Procedure

1. **Precheck** — confirm the message source (file export or connected tool) and locate `faq.md` and the brand-tone notes if they exist (`ls`, then `read_file`). No tone notes? Default: warm, direct, first-person, no corporate filler — and ask the user once to confirm.
2. **Triage pass** — read every message before answering any. Tag each P1–P4. Within a bucket, oldest first. P1s surface to the user immediately, even before drafting the rest.
3. **Escalation gate (before drafting)** — flag for human handling, with a one-line summary and NO drafted resolution, anything that involves: refund or chargeback requests, legal threats or lawyer language, data/privacy incidents, or clearly angry customers (profanity, "scam", threats to post publicly). For these you may draft only a holding line: "Thanks for flagging this — {Name} is looking at it personally and will reply today." The user decides everything else.
4. **Draft replies** — for the rest, check `faq.md` first (grep the topic) and reuse the canonical answer; otherwise write fresh. Every draft: acknowledge the specific issue in the first line, give the answer or the exact next step, one question max back to the customer. Match brand tone. **Never send** — save all replies as drafts labeled with the customer name.
5. **FAQ capture loop** — any question asked twice-or-more in this batch (or once here plus once in `faq.md` history) gets its best-drafted answer appended to `faq.md` under a `## {Question}` heading. This is how next week's batch gets smaller.
6. **Deliver** — output the template: escalations first, then drafts by severity, then FAQ updates, then the log line. Remind the user: drafts only, nothing sent.

## Output Template

```
# Support Batch — {Date} ({N} messages)

## 🚨 Escalated to you ({n})
- {Customer} — {refund/legal/angry} — {one-line summary} — holding draft ready: yes/no

## Reply drafts ({n})
### P1 — {Customer}: {issue}
> {draft reply}
### P2/P3 ...

## FAQ updated
- Added: "{question}" (asked {n}x)

## Numbers
P1 {n} · P2 {n} · P3 {n} · P4 {n} · escalated {n} · FAQ +{n}
Nothing has been sent — review drafts and fire when ready.
```

## Pitfalls

- **Agent resolves a refund itself** ("I've processed your refund") — money moved, or worse, a promise the business can't keep. Recovery: money is always human territory; strip any commitment language from drafts and route to the escalation list.
- **Tone whiplash** — templated corporate boilerplate to a customer who wrote casually, or breezy jokes to a furious one. Recovery: mirror the customer's register; re-read their message before finalizing each draft.
- **Answering messages in arrival order** — a P1 outage waits behind six P4 thank-yous. Recovery: triage the whole batch before drafting anything; the template forces severity order.
- **FAQ never updated** — the same "how do I reset my password" gets hand-drafted forever. Recovery: step 5 is not optional; if a question repeats and `faq.md` didn't grow, the run isn't done.
- **Draft sent by accident via a connected tool** — recovery: only ever use draft-creation calls, never send calls; if the tool lacks a draft mode, output replies as text for the user to paste.

## Verification

- [ ] Every message in the batch appears exactly once (escalated or drafted) — counts add up
- [ ] All refund/legal/angry messages are in the escalation list with no resolution promised
- [ ] Zero messages were sent; all replies exist as drafts or paste-ready text
- [ ] Repeat questions appended to `faq.md` (diff shows the additions)
- [ ] Summary line appended to `support-log.md`
- [ ] Each draft's first line acknowledges the customer's specific issue (no generic openers)
