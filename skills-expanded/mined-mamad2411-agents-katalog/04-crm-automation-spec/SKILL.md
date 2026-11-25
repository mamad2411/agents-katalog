---
name: 04-crm-automation-spec
description: 04-CRM-AUTOMATION-SPEC
---

# 04-CRM-AUTOMATION-SPEC

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **04-CRM-AUTOMATION-SPEC**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/landing-fable/04-CRM-AUTOMATION-SPEC.md`

## 🧠 Master Agent Prompt & Capabilities

# 04 — CRM AUTOMATION SPECIFICATION
### Pipelines, Tags, Scoring Rubrics & 9 Coordinated Sequences | RJ Funnel OS v1.1
**RJ Business Solutions | Rick Jefferson | 1342 NM 333, Tijeras, NM 87059**

---

## 1. LEAD SCORING RUBRIC

Automated calculation of lead quality based on behavior and fit:

| Behavior / Fit Attribute | Score Weight | Action Trigger |
|---|---|---|
| Authorized Form Completed | +20 | CRM tag: `form_completed` |
| Email Opened | +5 | CRM tag: `email_opened` |
| Link Clicked | +10 | CRM tag: `email_clicked` |
| Video sales letter watched > 10m | +25 | CRM tag: `vsl_fully_watched` |
| Valid Phone Supplied | +15 | CRM tag: `phone_validated` |
| Banned keywords in website/industry | -50 | Move to: `disqualified` |

---

## 2. PIPELINE STAGE ARCHITECTURES

### Local Service & Consulting Default Pipeline:
`New Lead -> Attempting Contact -> Qualified/Discovered -> Proposal Sent -> Negotiation -> Closed Won -> Onboarding -> Active Support`

### Credit & Funding Default Pipeline:
`New Lead -> Application Complete -> Report Uploaded -> Audit Complete -> Agreement Signed -> Client Portal Setup -> Active disputing -> Graduated`

---

## 3. THE 9 ESSENTIAL AUTOMATION SEQUENCES

### Sequence 1: Lead Magnet Delivery (SMS + Email)
- **Trigger:** Form submitted on Squeeze Page.
- **Timing:** Instant (within 60 seconds).
- **Goal:** Deliver value, start engagement.

### Sequence 2: Soap Opera Sequence (Story Arc)
- **Day 1:** Set the stage, hook, open loop.
- **Day 2:** The high drama / brick wall.
- **Day 3:** The epiphany / unique mechanism.
- **Day 4:** Hidden benefits of the system.
- **Day 5:** Real scarcity CTA to book a call.

### Sequence 3: Webinar Show-Up (Registration to Replay)
- **Pre-webinar:** 24h, 3h, 15m reminders to boost show-up.
- **Post-webinar:** Attendee logic (sales pitch) vs No-show logic (replay access).

### Sequence 4: Webinar Sales Close
- **Timing:** Runs for 3 days post-webinar.
- **Goal:** Drive to checkout or booking using objection handling and FAQ.

### Sequence 5: High-Ticket Application Flow
- **Goal:** Complete application form and schedule call.

### Sequence 6: Calendar Booking Confirmations & Reminders
- **Goal:** 0% no-show rate. Reminders at 24h, 2h, and 15m prior, plus SMS.

### Sequence 7: Welcome & Client Onboarding Welcome Sequence
- **Goal:** Immediate setup, client dashboard credentials, onboarding call.

### Sequence 8: Lost Lead Reactivation Loop
- **Trigger:** Inactive for 60+ days.
- **Action:** Simple, direct 9-word email: "Are you still looking to optimize your business systems?"

### Sequence 9: Customer Review & Referral Loop
- **Trigger:** Project completed or 30 days active.
- **Goal:** Compliant positive reviews (no payment in exchange) + partner introductions.

