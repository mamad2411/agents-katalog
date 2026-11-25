---
name: estimate-writer
description: Use this skill when you need to write a professional estimate or quote for a customer. Triggers on phrases like "write me an estimate", "quote for", "put together a proposal for", "how much should I charge for", or "customer wants a quote for". Produces a complete, professional estimate document plus a follow-up sequence if the customer goes quiet. Do NOT use for invoices — this is pre-job quoting only.
---

# Estimate Writer

## Pre-configured business data

This skill is configured for **{{BUSINESS_NAME}}**.
- Owner: {{OWNER_NAME}}
- Phone: {{PHONE}}
- Email: {{EMAIL}}
- Licence: {{LICENCE_NUMBER}}
- Standard labour rate: {{LABOUR_RATE}}
- Standard call-out fee: {{CALL_OUT_FEE}}
- Payment terms: {{PAYMENT_TERMS}}
- Warranty: {{WARRANTY_TERMS}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

Generates a complete, professional estimate in your business's voice — ready to send to the customer in under 2 minutes.

## What you need to tell me

The following are pre-configured and applied automatically:
- Business name, phone, email, licence number
- Labour rate ({{LABOUR_RATE}}), call-out fee ({{CALL_OUT_FEE}})
- Payment terms ({{PAYMENT_TERMS}})
- Warranty ({{WARRANTY_TERMS}})

You still need to tell me:
- **Customer name and address**
- **Job description** (as rough or detailed as you have it — I'll structure it)
- **Parts/materials needed** (if known — even approximate)
- **Any job-specific extras** (permits, disposal, travel beyond standard)

## What I'll produce

### 1. The Estimate Document
Professional, structured, ready to print or email as a PDF:

```
{{BUSINESS_NAME}}
{{PHONE}} | {{EMAIL}} | {{LICENCE_NUMBER}}

ESTIMATE — [Date]
Prepared for: [Customer Name]
Address: [Job address]
Valid for: 30 days

─────────────────────────────────────────────
SCOPE OF WORK
[Clear description of exactly what's included]

─────────────────────────────────────────────
MATERIALS
[Item]                          $[price]
[Item]                          $[price]

LABOUR
[Task] — [X] hours @ {{LABOUR_RATE}}    $[total]

─────────────────────────────────────────────
SUBTOTAL                         $[amount]
Tax ([X]%)                       $[amount]
TOTAL                            $[amount]

─────────────────────────────────────────────
TERMS
{{PAYMENT_TERMS}}
{{WARRANTY_TERMS}}
[What's NOT included — important for disputes]

Accepted by: _____________ Date: _____________
```

### 2. Send Message (SMS or email)
The message to send alongside the estimate:

> "Hi [Name], estimate attached for the [job type] at [address]. All-in price is $[X]. Happy to answer any questions — just call or text. Valid for 30 days. {{OWNER_NAME}}"

### 3. Follow-Up Sequence (if customer goes quiet)

**Day 3 (if no response):**
> "Hi [Name], just checking you received the estimate I sent for the [job]. Happy to talk through it — no pressure. {{OWNER_NAME}}"

**Day 7 (if still no response):**
> "Hi [Name], last follow-up on the estimate for [job]. If the timing or budget doesn't work right now, no problem at all. If you'd like to revisit later or adjust the scope, just let me know. {{OWNER_NAME}}"

After day 7 — move on. Two follow-ups is professional. Three is annoying.

## Example

**You say:**
> Quote for Tom at 88 River Road. Panel upgrade — 100A to 200A. About 6 hours labour. Parts around $400.

**I produce:** a complete formatted estimate with all figures, the text message to Tom, and a 3-day and 7-day follow-up message ready to copy.

## Tips for better estimates

- **Always list what's NOT included** — this prevents every dispute
- **Include a warranty line** — even "labour guaranteed for 12 months" builds trust
- **Name the specific products** where possible — "Leviton 200A panel" not just "new panel"
- **Round labour to half-hours** — it looks more professional than decimal hours
