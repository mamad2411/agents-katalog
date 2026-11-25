---
name: sales-call-summary
version: 1.0.0
description: Turn raw call notes or a transcript into a clean recap, CRM-ready fields, owned action items, and a ready-to-send follow-up email.
author: matrixx0070
tags: [sales, call-notes, follow-up, crm, meddic]
capabilities: []
---

# Sales Call Summary

## When to use
Use this right after a sales call when you have messy notes or a transcript and need a clean recap, CRM-ready fields, owned action items, and a follow-up email you can send in one edit.

**Not for:** prepping before the call (use sales-call-prep); building the next outreach sequence (use sales-draft-outreach); generating a formal proposal or one-pager (use sales-create-asset).

## Method
1. **Read for signal.** Extract what was decided, what changed about the deal, and what was promised — ignore small talk.
2. **Capture BANT/MEDDIC facts.** Pull budget, authority, need, timeline, metrics, decision criteria, and champion signals as they surfaced. Mark what is still unknown.
3. **List action items.** Every commitment becomes an item with an owner (you or them) and a due date. Do not lose their promises. **Decision point:** an item with no owner or date is not done — assign a default owner and flag it.
4. **Note risks and objections.** Record anything that could stall the deal, with its current status.
5. **Set next step.** Identify the concrete next milestone and whether it is scheduled. **Decision point:** no next step agreed on the call → make securing one the top follow-up action.
6. **Draft the follow-up email.** Mirror their language, confirm shared understanding, restate their action items and yours, and propose the next step with a specific time.
7. **Flag inference.** Anything you inferred rather than heard gets marked, not stated as fact.

## Example
From rough notes "CFO liked ROI, wants security review, Priya sending SOC2, decide by month-end": Recap = positive economic-buyer call, one gate remaining (security). Action items: you → send SOC2 report by Wed; them → Priya routes to InfoSec by Fri. Risk: security review timeline vs. month-end deadline. Next step: decision call booked for the 28th. Email confirms all four in six lines.

## Pitfalls
- **Transcribing, not summarizing.** A wall of everything said buries the three things that matter.
- **Orphan action items.** Commitments with no owner evaporate; theirs especially.
- **Stating inference as fact.** "They have budget" when they only implied it poisons the CRM.
- **Vague next step.** "Circle back soon" is not a milestone; name a date.

## Output format
```
Recap: <3-4 sentences>
Key facts (BANT/MEDDIC):
  - Budget: <> | Authority: <> | Need: <> | Timeline: <> | Metrics: <> | unknown: <>
Action items:
  - <you/them> — <task> — due <date>
Risks/objections:
  - <risk> — status: <>
Next step: <what> — <when / unscheduled>
Follow-up email:
  Subject: <>
  <body, ready to send>
```
