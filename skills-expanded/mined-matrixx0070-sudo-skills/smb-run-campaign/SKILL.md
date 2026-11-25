---
name: smb-run-campaign
version: 1.0.0
description: Run an end-to-end marketing campaign — sales analysis to content brief to assets to CRM send — with an owner-approval gate at every step.
author: matrixx0070
tags: [marketing, campaign, crm, content, sales, gated]
capabilities: []
---

# Run Campaign

## When to use
Run this when the owner wants to launch a promotion, seasonal push, or re-engagement campaign built end to end rather than piece by piece. Every stage is gated: the owner approves before the next begins.

**Not for:** analysis without execution (use smb-sales-brief); sending anything to customers without explicit approval at the send gate — nothing reaches a customer before that click.

## Method
1. **Analyze sales.** Top and bottom sellers, recent trends, customer segments. Recommend a campaign angle and target audience. **Gate: owner approves the angle.**
2. **Content brief.** Offer, message, channel(s), timing, success metric. **Gate: owner approves the brief.**
3. **Assets.** Draft copy, subject lines, captions, image prompts for the approved channels. **Gate: owner reviews and edits.**
4. **Audience.** Pull the recipient segment from the connected CRM; show count and filters. Decision point: if the segment looks unexpectedly large or small, stop and confirm the filters before proceeding. **Gate: owner confirms the list.**
5. **Send.** Schedule or send through the CRM only after final owner approval. **Gate: nothing goes out before that click.**
6. **Report.** Send confirmation and where to watch results.

## Example
Coffee roaster, slow summer. Analyze: cold brew rising, single-origin bags stale; segment = lapsed 90-day buyers. Angle "Summer Cold Brew — 15% off." Owner approves. Brief: email + Instagram, launch Mon, metric = 25 orders. Approved. Assets: subject "Your summer cold brew is here ☕," body draft, IG caption. Owner edits the subject. Audience: 340 lapsed buyers — matches expectation, owner confirms. Send scheduled Mon 8am after final approval. Report: sent, results tracked in the CRM dashboard.

## Pitfalls
- Collapsing the gates — drafting assets or pulling the list before the angle is approved wastes work if direction changes.
- Sending to an unverified segment; a wrong filter can blast the whole list or the wrong people.
- Treating owner edits on assets as optional — the brand voice is theirs.
- Reporting "done" without a success metric or a place to watch results.

## Output format
- **Stage-by-stage output,** each ending with an explicit **"Approve to continue?"** gate.
- **Sequence:** sales analysis → brief → assets → audience count + filters → send confirmation.
- **Approval note:** any step that contacts customers or spends money waits for owner approval.

## Reference

### Campaign timeline (2-week promo, working backward from launch)
| Day | Stage | Gate |
|-----|-------|------|
| −10 | Sales analysis → angle + audience | Owner approves angle |
| −8 | Content brief: offer, channels, timing, metric | Owner approves brief |
| −6 to −4 | Draft assets: copy, subject lines, captions, image prompts | Owner reviews & edits |
| −3 | Pull audience segment from CRM; show count + filters | Owner confirms list |
| −2 | Final review + schedule | Owner clicks send |
| 0 | Launch | — |
| +1 to +14 | Monitor; send reminder/second touch if planned | Owner approves any resend |
| +15 | Report vs. success metric | — |

### Channel benchmark table (typical SMB ranges — treat as sanity checks, not promises)
| Channel | Open / view | Click / engage | Conversion | Notes |
|---------|-------------|----------------|-----------|-------|
| Email (promo) | 20-30% open | 2-4% CTR | 1-3% of sends | Best ROI for existing customers |
| Email (re-engagement) | 10-18% open | 1-3% CTR | 0.5-2% | Expect lower; list is cold |
| SMS | 90%+ open | 8-15% CTR | 2-5% | High intimacy; use sparingly, get consent |
| Instagram organic post | 3-8% reach of followers | 1-3% engagement | Low direct | Awareness, not conversion |
| Instagram/FB paid | — | 0.5-1.5% CTR | 1-2% | CPM $7-15; needs budget approval |
| Google Search ads | — | 3-5% CTR | 3-6% | High intent; CPC varies wildly by niche |
Rule of thumb: a healthy SMB promo email drives orders ≈ (list size × ~1.5%). If a projection assumes 10%+, challenge it.

### Offer-type strengths
- **% off** — simple, good for clearing slow stock; erodes margin (check smb-price-check first).
- **$ off / threshold** ("$10 off $50") — protects margin, lifts average order value.
- **BOGO / bundle** — moves a slow item paired with a winner without a headline discount.
- **Early access / VIP** — re-engages loyal buyers at zero margin cost.
- **Free shipping** — often out-pulls an equivalent % discount psychologically.

### Segment sizing sanity check
Before the send gate, compare the pulled count to expectation. Flags to stop and re-check filters:
- Segment ≈ entire customer list (filter probably didn't apply).
- Segment near zero (filter too narrow or field mismatch).
- Includes unsubscribed / bounced addresses (must be excluded — legal + deliverability).
Always exclude: opted-out, hard-bounced, and staff/test addresses.

### Copy checklist per asset
Subject line (< 50 chars, one clear benefit) · preheader · one primary CTA · offer stated once and clearly · expiry/urgency if real · unsubscribe link (email) · brand voice matches the owner's. Owner edits are mandatory, not optional — the voice is theirs.

### Compliance guardrails
- **Email:** CAN-SPAM — real sender, physical address, working unsubscribe honored within 10 days.
- **SMS:** TCPA — prior express consent; include opt-out ("reply STOP").
- **Discounts/spend:** every offer that costs margin or ad budget waits for owner approval.

### The non-negotiable
Nothing reaches a customer and no budget is spent before the owner's explicit click at each gate. Collapsing gates to "save time" wastes work if direction changes and risks blasting the wrong list.
