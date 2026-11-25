---
name: inbox-triage
description: Processes a batch of emails — categorizes them, drafts responses where appropriate, and tells the user which ones need a human decision. Use when the user asks to triage the inbox, clear email, batch-process email, or prep email responses. Best run once or twice a day, not continuously.
---

# Inbox Triage

Turn a full inbox into three stacks: handled, drafts-for-your-review, and flagged-for-a-decision. Don't send anything without explicit approval.

## Before starting

1. Read `context/about-me.md` — who is the user, who are their priority contacts
2. Read `context/voice.md` — any draft reply must sound like them
3. Read `context/preferences.md` — their rules on what to auto-reply vs. escalate
4. Read `memory.md` if it exists — prior corrections to triage logic

## What to produce

A markdown file saved to `/output/inbox-triage-{YYYY-MM-DD-HHmm}.md` with four sections:

1. **Archived / filed (no action needed)** — count + one-line summary. The newsletters, receipts, notifications, FYI-cc'd threads. Just counts, not individual items.
2. **Drafted replies for your review** — threads where a standard response is appropriate and you've drafted it. Each item: sender, subject, one-line context, draft reply.
3. **Flagged for your decision** — threads that need the user's judgment before anyone replies. Each item: sender, subject, one-line context, the specific decision needed.
4. **Summary** — total emails processed, how many in each bucket, any patterns worth noting.

Do not actually send, archive, or label anything unless the user has explicitly approved auto-actions in their preferences file.

## Inputs

- Gmail or equivalent connector (required)
- The window to triage (default: since last triage run, or last 12 hours)
- Priority contacts list from `about-me.md` or `preferences.md`

## How it works

1. Pull emails from the window (unread + recently-read)
2. For each email, categorize:
   - **Archive-worthy?** Newsletters, receipts, automated notifications, CC threads where user isn't the primary recipient, confirmations that don't require action
   - **Draftable?** Clear request with an obvious standard answer — meeting confirmations, simple scheduling, "thanks" replies, known-answer FAQs
   - **Needs decision?** Everything else that isn't obvious
3. For draftable items, write a reply in the user's voice. Under 80 words unless the situation needs more.
4. For decision items, name the specific decision needed ("accept/decline," "yes/no/renegotiate," etc.)
5. Save the triage file, tell the user what to look at first

## What not to do

- Do not send anything without approval. This is a triage, not an autoresponder.
- Do not draft replies for anything that involves: money, a commitment, a promise, a new relationship, or legal language. Flag those.
- Do not apply labels, move to folders, or archive without explicit prior permission in `preferences.md`.
- Do not hallucinate context from email threads. If a thread is ambiguous, flag it — don't guess.

## Example output structure

```markdown
# Inbox Triage — 2026-04-18 10:42 AM

## Summary
- 47 emails processed since 2026-04-18 07:00
- 31 archive-worthy (newsletters, receipts, notifications)
- 9 drafted replies for your review
- 7 flagged for your decision

**Look at first:** Sarah Chen's reply about the SOW — she's asking a pricing question I can't answer.

---

## Archived / filed (31, no action needed)
- 12 newsletters
- 8 automated notifications (calendar, Slack digest, GitHub)
- 6 CC'd threads where you weren't the primary recipient
- 5 receipts / order confirmations

## Drafted replies for your review (9)

### 1. Morgan — "Tuesday 1:1 — reschedule?"
Context: Morgan needs to move the 1:1 from 9am to 11am Tuesday
Draft reply:
> Morgan — 11am works. Same agenda. See you then.

### 2. Conference organizer — "Confirming your speaker slot"
Context: Routine confirmation for a talk you already agreed to
Draft reply:
> Confirmed. I'll send the slide deck by 2026-04-26 as requested. Let me know if the tech check window changes.

[...7 more...]

## Flagged for your decision (7)

### 1. Sarah Chen (Northwind) — "Quick question on pricing"
Context: Sarah is asking for a 15% discount in exchange for a multi-year commitment. This is a pricing decision I can't make for you.
Decision needed: accept / counter / decline with alternative

### 2. Taylor (vendor) — "Contract renewal — new terms attached"
Context: New contract has a 12% price increase and changed liability terms.
Decision needed: review and send back, or route to legal

[...5 more...]
```

## Customization notes

- **For EAs.** You're likely triaging both your inbox and a principal's inbox. Ask which inbox, and tune the "priority contacts" list accordingly.
- **For high-volume inboxes.** Set the triage window to 4–6 hours instead of 12. Run it more often.
- **For founders.** Be more conservative on "drafted replies" — when in doubt, flag for decision. The risk of a wrong-voice email going out is higher than the time saved.
- **If the drafts are bad.** Save feedback to `memory.md`. The next run will be better. This skill improves fast with correction.
