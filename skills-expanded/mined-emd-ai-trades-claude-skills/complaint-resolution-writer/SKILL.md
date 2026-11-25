---
name: complaint-resolution-writer
description: Use this skill when you need to respond to a customer complaint — email, phone, BBB, or in-person dispute. Triggers on phrases like "customer is complaining about", "got a complaint about", "BBB complaint", "customer wants a refund", "dispute about the work", "angry customer email", or "how do I respond to this complaint". Produces a professional response letter plus an internal incident log. Do NOT use for public Google reviews — use review-responder for those. This is for private dispute resolution.
---

# Complaint Resolution Writer

## Pre-configured business data

This skill is configured for **{{BUSINESS_NAME}}**.
- Owner: {{OWNER_NAME}}
- Phone: {{PHONE}}
- Email: {{EMAIL}}
- Trade: {{TRADE}}
- Licence: {{LICENCE_NUMBER}}
- Standard warranty: {{WARRANTY_TERMS}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

**An unresolved complaint costs you 10+ referrals.** A well-handled one can turn into your most loyal customer.

This skill produces professional response letters for any customer dispute — billing, quality, scheduling, warranty claims, or scope disagreements.

## The difference from review-responder

| | Review Responder | Complaint Resolution Writer |
|---|---|---|
| **Where** | Public (Google, Yelp) | Private (email, phone, BBB) |
| **Length** | Under 150 words | As long as needed |
| **Goal** | Look good to other readers | Resolve the issue and protect yourself |

## What you need to tell me

The following are pre-configured:
- Business name, phone, email, licence
- Standard warranty terms ({{WARRANTY_TERMS}})

You still need to tell me:
- **Customer name**
- **What happened** (their complaint + your side)
- **The original scope/price**
- **What you're willing to offer** as resolution

## What I'll produce

### 1. Response Letter

```
{{BUSINESS_NAME}}
{{PHONE}} | {{EMAIL}} | {{LICENCE_NUMBER}}
[Date]

RE: Service at [address] — [Job type]

Dear [Customer Name],

Thank you for bringing this to our attention. We take every
concern seriously, and I want to address your [issue] directly.

WHAT WAS AGREED:
[Summary of original scope, price, and terms]

WHAT HAPPENED:
[Factual timeline]

OUR POSITION:
[Your side — professional, not defensive]

PROPOSED RESOLUTION:
[Specific offer]

We'd like to resolve this within [X] business days. Please
reply to this email or call us at {{PHONE}}.

Respectfully,
{{OWNER_NAME}}
{{BUSINESS_NAME}}
{{PHONE}} | {{EMAIL}} | {{LICENCE_NUMBER}}
```

### 2. BBB Complaint Response (if applicable)

```
BBB RESPONSE — Complaint #[number]

Business: {{BUSINESS_NAME}}
Customer: [Name]
Date of service: [Date]

RESPONSE:
[Concise, factual account — under 500 words]
[Resolution status]

Contact: {{OWNER_NAME}}, {{PHONE}}, {{EMAIL}}
```

### 3. Internal Incident Log

```
INCIDENT LOG — [Date]

Customer: [Name]
Job: [Type] at [Address]
Original price: $[Amount]
Contract on file: [Yes/No]

COMPLAINT SUMMARY:
[What the customer claims]

FACTUAL TIMELINE:
[Date] — [What happened]

RESOLUTION OFFERED:
[Specific offer]

RESOLUTION STATUS:
[ ] Accepted  [ ] Rejected  [ ] Pending  [ ] Escalated

Logged by: {{OWNER_NAME}}
```

### 4. Follow-Up After Resolution

> "Hi [Name], I'm glad we were able to work this out. We genuinely appreciate your patience, and the feedback you gave us has led to [specific change]. If you ever need anything, don't hesitate to reach out. — {{OWNER_NAME}}, {{BUSINESS_NAME}}"

### 5. Escalation Letter (if they reject your resolution)

```
{{BUSINESS_NAME}}
[Date]

RE: Final Response — Service at [address]

Dear [Customer Name],

Further to our correspondence regarding the [job type]
completed on [date], we have made the following good-faith
effort to resolve your concerns:

[Summary of offers made]

As the work was completed in accordance with the agreed
scope of work, and our resolution offer remains available,
we consider this matter addressed from our end.

Should you wish to accept our offer, please contact us
by [date].

Respectfully,
{{OWNER_NAME}}
{{BUSINESS_NAME}}
{{PHONE}} | {{EMAIL}} | {{LICENCE_NUMBER}}
```

## Common complaint types

| Complaint | Key principle |
|-----------|--------------|
| **"Work was done wrong"** | Offer to inspect and re-do if warranted |
| **"Price was higher than quoted"** | Reference the original estimate/contract |
| **"You damaged my property"** | Inspect, photograph, involve insurance if needed |
| **"You missed the appointment"** | Apologise directly, offer priority rescheduling |
| **"It broke again"** | Warranty callback — inspect at no charge |
| **"Your tech was rude"** | Apologise without qualifying, offer a different tech |