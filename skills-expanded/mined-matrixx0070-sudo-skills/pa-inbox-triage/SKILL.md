---
name: pa-inbox-triage
version: 1.0.0
description: Triage a personal inbox into act, defer, delegate, or archive and draft replies for the owner to send.
author: matrixx0070
tags: [inbox, email, triage, productivity, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner hands you a personal inbox (or a screenshot/paste of messages) and wants it sorted into a clear action plan with reply drafts ready to go. Good for morning inbox zero, post-vacation backlog, or a "what needs me today" sweep across email, DMs, and texts.

**Not for:** work-project task breakdowns (that is a project-management job), spam-filter tuning, or actually sending mail on your own. You draft; the owner sends.

## Method

1. Pull the raw list. Ask for the messages if not provided; accept paste, forward, or a connected mailbox read.
2. Bucket each item into exactly one of: **ACT** (needs a reply/action from the owner today), **DEFER** (matters but not today — attach a date), **DELEGATE** (someone else should own it), **ARCHIVE** (FYI/done/no action).
3. Decision point — is the sender a person expecting a human reply, or an automated/bulk message? Automated → ARCHIVE or DEFER; person → ACT or DELEGATE.
4. Decision point — does an ACT item need info you do not have? If yes, mark it BLOCKED and note the missing input instead of guessing.
5. For each ACT and DELEGATE item, draft a reply in the owner's voice. Keep it short, match the relationship's formality.
6. Rank ACT items by urgency x importance so the owner works top-down.
7. Present the plan. Confirm before sending anything or messaging any person — never auto-send a draft.

## Example

Input: 4 messages. Output:
- ACT: "Landlord — lease renewal by Fri." Draft: "Hi Sam, happy to renew for another year at the current terms. Can you send the paperwork? Thanks, [Owner]."
- DEFER (Sat): "Friend — dinner sometime?" Draft parked.
- DELEGATE: "Accountant — needs last receipt." Suggest forwarding to bookkeeper.
- ARCHIVE: "Newsletter digest."

## Pitfalls

- Auto-sending drafts. Always stop and confirm; a wrong send to a person is not reversible.
- Over-drafting essays. Personal replies are 2-4 sentences; long drafts get rewritten anyway.
- Two buckets for one item. Force a single primary bucket so nothing is ambiguous.
- Guessing missing facts (dates, amounts, names) to complete a draft. Mark BLOCKED instead.

## Output format

```
INBOX TRIAGE — [date] — [N] items

ACT ([n])
1. [sender] — [subject] — due [when]
   DRAFT: "[reply text]"
DEFER ([n])
- [sender] — [subject] — revisit [date]
DELEGATE ([n])
- [sender] — [subject] — to [who] — DRAFT: "[text]"
ARCHIVE ([n])
- [sender] — [subject]
BLOCKED
- [item] — needs: [missing input]

Next: reply YES to send ACT/DELEGATE drafts, or edit any first.
```
