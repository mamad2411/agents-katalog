---
name: seasonal-campaign
description: Use this skill to generate a seasonal re-engagement campaign targeting past customers. Triggers on phrases like "write a campaign for spring tune-ups", "reach out to past AC customers", "pre-winter furnace campaign", "I want to contact past customers about", or "seasonal campaign for". Produces a complete multi-touch campaign (SMS + email) ready to send. Do NOT use for new leads — this is for customers who have already used your business.
---

# Seasonal Campaign Generator

## Pre-configured business data

This skill is configured for **{{OWNER_NAME}}** at **{{BUSINESS_NAME}}**, serving {{SERVICE_AREA}}.
- Trade/services: {{PRIMARY_SERVICES}}
- Phone: {{PHONE}}
- Booking link: {{BOOKING_LINK}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

Your past customers are your most profitable source of new revenue. They already trust you. They already know your work. They just need a reason to call.

This skill turns your customer history into a complete outreach campaign — timed to the seasons when they'll need you most.

## The seasonal calendar for trades businesses

| Trade | Season | Campaign timing | Hook |
|-------|--------|----------------|------|
| HVAC | Spring | March–April | AC tune-up before summer heat |
| HVAC | Fall | September–October | Furnace check before winter |
| Plumbing | Fall | October–November | Pipe insulation before freeze |
| Plumbing | Spring | March | Post-winter pipe inspection |
| Electrical | Pre-summer | April–May | Panel check, outdoor circuits, EV charger |
| Electrical | Pre-winter | October | Heating loads, safe harbour check |
| Roofing | Post-storm | After major weather events | Free inspection offer |
| Roofing | Spring | March–April | Winter damage inspection |
| General | Any | 90 days after job | Satisfaction check + referral ask |

## What you need to tell me

The following are pre-configured and applied automatically:
- Business name ({{BUSINESS_NAME}})
- Trade/services ({{PRIMARY_SERVICES}})
- Service area ({{SERVICE_AREA}})

You still need to tell me:
- **The campaign type** (which season/service you're promoting)
- **How many customers** you're reaching out to (gives me the right scale)
- **Any customer segments** you want to target (e.g. "everyone who had AC work last summer", "all furnace customers from 2024")
- **Any offer or incentive** (e.g. "$30 off tune-up booked before May 1st" — or nothing, just a reminder)
- **Your available slots** (e.g. "booking out 3 weeks, can take 15 more tune-ups")

## What I'll produce

### 1. Campaign SMS — Touch 1 (Week 1)

> "Hi [Name], it's {{BUSINESS_NAME}} — we serviced your [unit/system] last [season]. With [hot weather/cold season] coming, now's the best time to book a tune-up before our schedule fills up. Replying 'YES' gets you first pick of slots. — {{OWNER_NAME}}"

### 2. Campaign Email — Touch 1 (same week, different channel)

**Subject:** Your [AC/furnace/system] before [season] — a quick note from {{BUSINESS_NAME}}

> Hi [Name],
>
> It's {{OWNER_NAME}} from {{BUSINESS_NAME}} — we took care of your [job type] back in [month/year].
>
> [Season] is just around the corner, and the last thing you want is [specific problem that happens when equipment isn't maintained — e.g. your AC failing on the hottest day of the year / your boiler packing in when temperatures drop].
>
> We're offering [service] for $[price or range] through [date], and I wanted to give past customers first access before we open it up publicly.
>
> Book here: {{BOOKING_LINK}} or just reply to this email.
>
> {{OWNER_NAME}}
> {{BUSINESS_NAME}} | {{PHONE}}

### 3. Touch 2 — Nudge (10 days later, to non-responders only)

**SMS:**
> "Hi [Name], just checking you got my message about the [service] — we're about half-booked now. Happy to answer any questions. — {{BUSINESS_NAME}}"

**Email subject:** Still a few spots left — {{BUSINESS_NAME}}

> Just a quick follow-up on the [service] offer. We're filling up faster than expected — if you'd like to lock in a slot before summer, just reply here or call {{PHONE}}. No pressure either way. — {{OWNER_NAME}}

### 4. Touch 3 — Final call (7 days after touch 2)

**SMS:**
> "Last spots for [service] this [season]. After this we're fully booked until [month]. If you'd like to get in, text back and I'll hold a slot. — {{BUSINESS_NAME}}"

This is the last message. Three touches is the limit. Anyone who hasn't responded after touch 3 goes into a 6-month dormant list.

### 5. Customer List Template

A simple format for running this manually if you don't have a CRM:

```
Name | Phone | Email | Last job | Last job date | Campaign sent | Response | Booked?
-----|-------|-------|----------|---------------|--------------|---------|--------
     |       |       |          |               |              |         |
```

Copy this into Google Sheets. Filter by "Last job date" to find the right customers for each campaign.

## The referral add-on (include in any campaign)

Add this postscript to Touch 1 for existing customers who are likely happy:

> P.S. If you know anyone who needs [service], we'd love the introduction. We'll take $[X] off your next service for every referral that books.

This is the highest ROI line in any campaign. Past happy customers are your best salespeople.

## What "good" looks like

A campaign to 50 past customers with 3 touches typically produces:
- 8–15% booking rate (4–7 jobs) from the campaign alone
- 1–3 referrals from satisfied responders
- Zero ad spend

That's the value sitting in your customer list right now.
