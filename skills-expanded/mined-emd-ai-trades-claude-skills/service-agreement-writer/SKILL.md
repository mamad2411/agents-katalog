---
name: service-agreement-writer
description: Use this skill when you need to create a maintenance plan, service agreement, or membership contract for a customer. Triggers on phrases like "write a service agreement", "create a maintenance plan", "membership contract", "recurring service plan", "annual maintenance agreement", or "how should I structure my maintenance plans". Produces a complete tiered agreement document plus a sales pitch script. Do NOT use for one-time job contracts — this is for recurring service relationships only.
---

# Service Agreement Writer

## Pre-configured business data

This skill is configured for **{{BUSINESS_NAME}}**.
- Owner: {{OWNER_NAME}}
- Phone: {{PHONE}}
- Email: {{EMAIL}}
- Trade: {{TRADE}}
- Licence: {{LICENCE_NUMBER}}
- Service area: {{SERVICE_AREA}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

### Agreement details
- Visit checklist: {{VISIT_CHECKLIST}}
- Bronze tier: {{BRONZE_VISITS}} visits/year — ${{BRONZE_PRICE_ANNUAL}}/year or ${{BRONZE_PRICE_MONTHLY}}/month
- Silver tier: {{SILVER_VISITS}} visits/year — ${{SILVER_PRICE_ANNUAL}}/year or ${{SILVER_PRICE_MONTHLY}}/month
- Gold tier: {{GOLD_VISITS}} visits/year — ${{GOLD_PRICE_ANNUAL}}/year or ${{GOLD_PRICE_MONTHLY}}/month
- Parts discount: {{PARTS_DISCOUNT}}
- Labour discount: {{LABOUR_DISCOUNT}}
- Priority scheduling: {{PRIORITY_SCHEDULING}}
- Emergency response: {{EMERGENCY_RESPONSE}}

**Maintenance agreements are 55% of trades industry revenue.** If you don't offer them, you're leaving your most profitable revenue stream on the table.

## What you need to tell me

The following are pre-configured and applied automatically:
- Business name, phone, email, trade
- Tier pricing and visit counts
- Discount percentages
- Priority/emergency response terms

You still need to tell me:
- **Customer name and address**
- **Which tier they're interested in** (or "show them all three")
- **Any system-specific notes** (e.g. "they have a 15-year-old furnace" — I'll tailor the pitch)

## What I'll produce

### 1. The Agreement Document

```
{{BUSINESS_NAME}}
SERVICE AGREEMENT
{{PHONE}} | {{EMAIL}} | {{LICENCE_NUMBER}}

─────────────────────────────────────────────

BRONZE — ESSENTIAL CARE
${{BRONZE_PRICE_ANNUAL}}/year or ${{BRONZE_PRICE_MONTHLY}}/month
• {{BRONZE_VISITS}} scheduled maintenance visit(s) per year
• {{VISIT_CHECKLIST}}
• {{PARTS_DISCOUNT}} discount on parts
• Standard scheduling

SILVER — PRIORITY CARE (MOST POPULAR)
${{SILVER_PRICE_ANNUAL}}/year or ${{SILVER_PRICE_MONTHLY}}/month
• {{SILVER_VISITS}} scheduled maintenance visits per year
• Everything in Bronze, plus:
• {{PARTS_DISCOUNT}} discount on parts AND {{LABOUR_DISCOUNT}} on labour
• {{PRIORITY_SCHEDULING}}
• No diagnostic fee on service calls

GOLD — COMPLETE PROTECTION
${{GOLD_PRICE_ANNUAL}}/year or ${{GOLD_PRICE_MONTHLY}}/month
• {{GOLD_VISITS}} scheduled maintenance visits per year
• Everything in Silver, plus:
• {{EMERGENCY_RESPONSE}}
• No overtime charges
• Annual system report with recommendations

─────────────────────────────────────────────

WHAT'S INCLUDED IN EVERY VISIT:
{{VISIT_CHECKLIST}}

WHAT'S NOT INCLUDED:
• Replacement parts and equipment (discounted per tier)
• Code upgrades or system modifications
• Damage from misuse, neglect, or third-party work
• New system installations

TERMS:
• Agreement term: 12 months, auto-renews annually
• Cancellation: 30 days written notice, prorated refund
• Visits scheduled during normal business hours (Mon–Fri 8am–5pm)

─────────────────────────────────────────────

AGREED BY:
Customer: _________________ Date: _________
Address: _________________________________
Phone: _______________ Email: ______________

{{BUSINESS_NAME}}: ____________ Date: _________
```

### 2. Sales Script (for technicians on-site)

```
AFTER THE JOB — NATURAL TRANSITION:

"Everything's running great now. One thing I'd recommend —
[specific to their system] — is getting it checked
[once / twice] a year so small issues don't turn into
big repairs.

We have a maintenance plan that covers that — starts at
${{BRONZE_PRICE_MONTHLY}} a month. You get [key benefit]
plus {{PARTS_DISCOUNT}} off any parts if something comes up.

Want me to send you the details?"
```

### 3. Email — Send After the Pitch

**Subject:** Your maintenance plan details — {{BUSINESS_NAME}}

> Hi [Name],
>
> Thanks again for having us out today — glad we got [the issue] sorted.
>
> As I mentioned, here are the maintenance plan options. Most of our residential customers go with Silver — it covers {{SILVER_VISITS}} visits a year plus {{PRIORITY_SCHEDULING}}.
>
> [Attach or paste the agreement tiers]
>
> Happy to answer any questions. You can sign up by replying to this email or calling us at {{PHONE}}.
>
> {{OWNER_NAME}}
> {{BUSINESS_NAME}}

### 4. Follow-Up (7 days later)

> "Hi [Name], just following up on the maintenance plan info I sent last week. No pressure — just wanted to make sure it didn't get buried in your inbox. — {{OWNER_NAME}}"

### 5. Renewal Reminder (30 days before expiry)

> "Hi [Name], your maintenance agreement with {{BUSINESS_NAME}} renews on [date]. Your next scheduled visit is [month]. Everything auto-renews — no action needed. If you'd like to upgrade your plan or make changes, just reply here. Thanks for being a valued customer! — {{OWNER_NAME}}"