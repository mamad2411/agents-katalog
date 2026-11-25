---
name: job-complete-followup
description: Use this skill immediately after a job is marked complete or closed in your system. Triggers on phrases like "job done", "job complete", "just finished a job", "close out [customer name]", or "mark job complete for [address]". Generates a review request message, schedules a re-engagement follow-up, and logs the customer for future campaigns. Do NOT use before the job is physically finished.
---

# Job Complete Follow-Up

## Pre-configured business data

This skill is configured for **{{BUSINESS_NAME}}** in **{{CITY}}**, serving {{SERVICE_AREA}}.
- Google review link: {{GOOGLE_REVIEW_LINK}}
- Technicians: {{TECHNICIAN_NAMES}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

Use this skill when a job is finished and you want to automatically trigger the post-job sequence:
1. Send a review request to the customer
2. Schedule a seasonal re-engagement in 90 days
3. Log the job to your customer history

## What you need to tell me

Provide as much of the following as you have:
- **Customer name** (first name is enough)
- **Job type** (e.g. AC installation, boiler repair, rewire, pipe burst)
- **Job address or area** (neighbourhood / city is fine — for local keyword use)
- **Technician name** (optional — personalises the message)
- **Any notable detail** (e.g. emergency call-out, warranty job, repeat customer)

## What I'll produce

### 1. Review Request Message (SMS — under 160 characters)
Ready to copy-paste or send via your CRM/SMS tool. Always use {{BUSINESS_NAME}} as the business name and {{GOOGLE_REVIEW_LINK}} as the review link.

### 2. Review Request Email (if you prefer email)
Subject line + 3-paragraph body. Friendly, specific, not generic.

### 3. 90-Day Re-engagement Note
A calendar reminder note with the message to send when 90 days hits — so the customer hears from you before they need someone else.

### 4. Customer Log Entry
A one-line record to paste into your spreadsheet or CRM:
`[Date] | [Name] | [Job type] | [Address] | [Follow-up due date]`

## Example

**You say:**
> Just finished installing a new Carrier AC unit for Sarah at 142 Maple Drive. Jake was the tech. She was really happy with it.

**I produce:**

**SMS (send within 2 hours):**
> Hi Sarah, it's Jake from {{BUSINESS_NAME}}. Really glad the new AC is running well! If you have 60 seconds, a Google review would mean the world to us — {{GOOGLE_REVIEW_LINK}}. Thanks so much!

**Email subject:** Your new AC installation — a quick favour, Sarah

**Re-engagement note (90 days):**
> Send: "Hi Sarah! Hope the AC has been keeping you cool this summer. Just a reminder that we recommend a quick filter check at the 90-day mark — free for our customers. Want us to swing by?"

**Log entry:**
> 2026-02-24 | Sarah | AC Installation | 142 Maple Drive | Follow-up: 2026-05-24

## Tools this works with
- Copy-paste into iMessage, WhatsApp, or any SMS tool
- HouseCall Pro / Jobber / ServiceTitan — paste into the job notes or customer messaging
- Any email client
- Google Sheets — paste the log entry into a running customer tab
