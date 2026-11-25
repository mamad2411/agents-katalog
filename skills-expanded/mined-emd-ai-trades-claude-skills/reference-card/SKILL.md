---
name: reference-card
description: Use this skill after a client build is complete to generate their reference card. Triggers on phrases like "generate reference card", "create the cheat sheet for", "reference card for [business name]", or "make the reference card". Reads the completed skill set from /clients/[business-name]/skills/ and produces a single markdown file the client can keep open while using Claude. Run this after client-build, not before.
---

# Reference Card Generator

Reads a completed client skill set and produces a single, scannable reference document the client can print, pin above their desk, or keep open on their phone alongside Claude. One page. No fluff. Just the five commands and what to type for each one.

## What you need to provide

Either:
- The business name (I'll look up `/clients/[slug]/skills/` automatically)
- A path to the skills folder

## How to generate

### Step 1 — Find the client build
Look up the client folder at `/clients/[slug]/skills/`. Read all 5 SKILL.md files.

### Step 2 — Extract business details
From any skill's "Pre-configured business data" section, extract:
- Business name
- Owner name (if present)
- City/service area (if present)

### Step 3 — Generate the reference card
Use the exact format below. Fill in the business name. For each skill section, use the information from the client's actual configured skill files — not generic examples.

### Step 4 — Save the file
Save to: `/clients/[slug]/[BusinessName]-reference-card.md`

Use PascalCase with no spaces for the filename business name (e.g., "Arctic Air HVAC" → "ArcticAirHVAC-reference-card.md").

## Reference card format

Generate this exact structure, replacing [Business Name] and adapting the example prompts to match the client's trade and services:

```markdown
# [Business Name] — Claude Skills Quick Reference

Keep this open when using Claude. Five commands. That's all you need.

---

## 1. Job Complete Followup

**Type:** `/job-complete-followup`

**When:** Right after you finish a job and want to send a review request.

**What to tell it:**
- Customer first name
- What the job was (e.g. AC install, furnace repair)
- Job address or neighbourhood
- Which tech did the work (optional)
- Anything notable (emergency, repeat customer, warranty)

**What you get back:** SMS review request ready to send, email version, 90-day follow-up reminder, CRM log entry.

**Try this now:**
> Just finished a furnace tune-up for Dave at 45 Elm Street. He was happy with the service.

---

## 2. Estimate Writer

**Type:** `/estimate-writer`

**When:** A customer needs a quote. Your rates, terms, and warranty are already loaded.

**What to tell it:**
- Customer name and address
- What the job is (rough description is fine)
- Parts/materials if you know them
- Any extras (permits, disposal, travel)

**What you get back:** Formatted estimate document, send message, Day 3 and Day 7 follow-ups if they go quiet.

**Try this now:**
> Quote for Lisa at 220 Pine Ave. AC compressor replacement. Parts about $800. Probably 4 hours labour.

---

## 3. Review Responder

**Type:** `/review-responder`

**When:** You have a Google review to respond to — positive, negative, or mixed.

**What to tell it:**
- Paste the review text
- Any context about the job (optional)

**What you get back:** A ready-to-post response under 150 words with your city name included for SEO.

**Try this now:**
> "Great service, arrived on time and fixed the issue quickly. Very professional team."

---

## 4. Missed Call Handler

**Type:** `/missed-call-handler`

**When:** You see a missed call and need to respond fast — within 5 minutes.

**What to tell it:**
- The number or name (if you know it)
- What time the call came in
- Any context (voicemail? existing customer? after hours?)

**What you get back:** SMS to send immediately, callback script for when you ring them back.

**Try this now:**
> Missed call from unknown number at 3:30pm. No voicemail.

---

## 5. Seasonal Campaign

**Type:** `/seasonal-campaign`

**When:** You want to reach out to past customers about an upcoming season or service.

**What to tell it:**
- What campaign (e.g. pre-summer AC tune-up)
- How many customers you're reaching
- Any segment (e.g. all AC customers from last year)
- Any offer or incentive
- How many slots you have available

**What you get back:** Complete 3-touch campaign — SMS + email for each touch, plus a customer tracking template.

**Try this now:**
> Pre-summer AC tune-up campaign. About 50 past customers. $30 off if booked before May 1st. I have 15 slots.

---

*Built for [Business Name] by HVACRanker*
*Skills version: [today's date]*
```

## After generating

Print confirmation:
```
✓ Reference card saved: /clients/[slug]/[BusinessName]-reference-card.md

  The client folder is now ready to deliver:
  /clients/[slug]/
  ├── skills/ (5 configured skills)
  └── [BusinessName]-reference-card.md

  To deliver: ZIP the folder and send with onboarding instructions.
```
