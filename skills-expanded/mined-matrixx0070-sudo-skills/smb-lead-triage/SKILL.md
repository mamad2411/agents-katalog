---
name: smb-lead-triage
version: 1.0.0
description: Score raw inbound leads into a "call these 5 today" list on fit/intent/value/freshness, with tailored openings and follow-up timing — outreach owner-approved.
author: matrixx0070
tags: [small-business, sales, leads, triage, lead-scoring, pipeline]
capabilities: []
---

# Lead Triage

## When to use
Use this when inbound leads are piling up and the owner or a small sales team needs to know exactly who to contact first today — instead of working the list in random order or letting hot leads go cold.

**Not for:** building a call list from existing CRM deals with history (use smb-call-list) or CRM data hygiene (use smb-crm-cleanup). This triages fresh, un-worked inbound.

## Method
1. **Gather the leads.** List new and open inbound leads with source, date received, stated need, budget signal, and any prior contact.
2. **Score each lead.** Rate on fit (matches ideal customer), intent (urgency and buying signals), value (estimated deal size), and freshness (newer and un-contacted ranks higher). Decision point: combine into one score, but let strong intent override a mediocre fit — an urgent buyer beats a perfect-profile tire-kicker.
3. **Rank and cut to five.** Surface the top 5 to call today; hold the rest in a warm queue.
4. **Draft the approach.** For each of the five, write a one-line context brief and a suggested opening (call or message) referencing their stated need.
5. **Set follow-ups.** Recommend next-touch timing for leads not reached and for the warm queue.
6. **Flag mismatches.** Note leads that are poor fit or spam to deprioritize.

Present outreach drafts for the owner to approve before sending; customer contact is owner-approved.

## Example
18 new leads. Top pick: "Marisol, form fill 2 hrs ago, needs a catered event for 60 next month, budget noted" — score 9/10 (high intent + fresh + fits). Opening: "Hi Marisol, saw you need catering for 60 next month — happy to lock a date; what's the day?" Warm queue: a good-fit lead with no urgency → next touch in 3 days. Deprioritized: a "free samples?" message with no event → spam-ish, hold.

## Pitfalls
- **Scoring fit over intent.** A ready-to-buy lead who's slightly off-profile still outranks a perfect fit with no urgency.
- **Working the list oldest-first.** Freshness matters — a 2-hour-old inbound converts far better than a week-old one.
- **Generic openings.** Reference the lead's stated need, not "just following up."
- **Sending unapproved.** Draft the outreach; the owner approves before any message goes out.

## Output format
```
Leads reviewed: <n> | new: <n>
Call these 5 today:
  1. <name> — source <..> — score <n>/10 — need <..>
     Opening: "<suggested>"
Warm queue (ranked): <lead> — next touch <when>
Follow-up schedule: <not-reached leads — timing>
Deprioritized / spam: <lead — why>
```

## Reference

### Scoring rubric (weighted, 100-point scale)
Score each lead on four dimensions, multiply by the weight, and sum. Fit and intent carry the most weight because they predict conversion; freshness is a tiebreaker and a decay multiplier, not the whole score.

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| Fit | 30 | Match to ideal customer profile — industry, size, geography, use case |
| Intent | 35 | Buying signals — explicit need, timeline, "how much / how soon", demo request |
| Value | 20 | Estimated deal size and margin |
| Freshness | 15 | How recently they came in and whether un-contacted |

**Fit anchors (0-30):** 30 = squarely in ICP; 20 = adjacent, workable; 10 = edge case; 0 = out of market.
**Intent anchors (0-35):** 35 = asked to buy / booked a call / stated a deadline; 25 = requested pricing or a demo; 15 = downloaded/asked a question; 5 = passive browse; 0 = no signal.
**Value anchors (0-20):** scale to your own average order value — 20 = well above AOV, 12 = around AOV, 5 = below, 0 = unknown/tiny.
**Freshness anchors (0-15):** 15 = < 1 hour and un-contacted; 12 = same day; 8 = 1-3 days; 4 = 4-7 days; 0 = > 7 days or already worked.

### Score bands and SLA
| Band | Score | Action | Response SLA |
|------|-------|--------|--------------|
| A — Hot | 75-100 | Call today, personally | < 1 hour if possible; same day mandatory |
| B — Warm | 50-74 | Call within 24-48h; nurture sequence | 1 business day |
| C — Cool | 25-49 | Automated nurture; revisit weekly | 3-5 days |
| D — Disqualify | < 25 or spam | Archive with reason | none |

The **5-minute rule** matters: contacting a web lead within 5 minutes vs 30 minutes can raise the odds of a real conversation by roughly an order of magnitude, and drops sharply after the first hour. This is why a fresh B-lead often outranks a day-old A on *who to call first this second*.

### Override rules
- **Intent trumps fit.** A ready-to-buy lead slightly off-profile (high intent, mid fit) still ranks above a perfect-fit tire-kicker with no urgency.
- **Freshness as a decay multiplier.** For time-sensitive businesses, multiply the intent+value subtotal by 0.9 per day un-contacted after day one — a hot lead going cold should visibly fall.
- **Hard disqualifiers** (auto-D regardless of score): no budget authority, out of service area, competitor recon, obvious spam, or explicitly "just researching, no timeline."

### Opening-line framework
Reference the stated need, propose a concrete next step, keep it one or two sentences. Structure: **{recognize their need} → {credible one-line proof/answer} → {specific ask with a date}.** Avoid "just following up" and "touching base." Example spine: "Hi {name}, saw you need {stated need} by {their timeline} — we do exactly that; would {day/time} work for a quick call to lock it in?"

### Follow-up cadence for un-reached leads
A persistent, multi-touch cadence recovers far more than one-and-done. Suggested sequence across ~2-3 weeks: Day 0 (call + email), Day 1 (call at a different time of day), Day 3 (email with a specific value point), Day 5 (call), Day 8 (short "still interested?" email), Day 14 (break-up email — "should I close your file?"). Vary channel and time of day; most connects happen on attempts 2-6, not attempt 1. Move to the warm/nurture queue only after the cadence is exhausted.

### Metrics
Track speed-to-first-contact (median minutes), contact rate (reached ÷ attempted), lead-to-opportunity conversion by band (validate that A > B > C — if not, the rubric weights need recalibration), and time-to-first-touch vs conversion to prove the freshness effect in your own data.
