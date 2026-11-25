---
name: lien-waiver-generator
description: Use this skill when you need to create a lien waiver for a project payment. Triggers on phrases like "lien waiver for", "need a lien waiver", "waiver for progress payment", "final lien waiver", "GC wants a lien waiver", or "waiver before I get paid". Produces the correct waiver type based on your payment situation. Do NOT use for invoices or estimates — this is specifically for lien rights documentation.
---

# Lien Waiver Generator

## Pre-configured business data

This skill is configured for **{{BUSINESS_NAME}}**.
- Owner: {{OWNER_NAME}}
- Company: {{BUSINESS_NAME}}
- Title: {{OWNER_TITLE}}
- State: {{STATE}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

**Wrong waiver = no payment or no lien rights.** This skill makes sure you pick the right type and fill it out correctly.

## The 4 types — which one do you need?

I'll ask you two questions to determine the right waiver:

1. **Progress payment or final payment?**
2. **Have you already received the payment?**

| | Payment NOT received | Payment IS received |
|---|---|---|
| **Progress** | Conditional Progress | Unconditional Progress |
| **Final** | Conditional Final | Unconditional Final |

## What you need to tell me

Pre-configured:
- Company name ({{BUSINESS_NAME}})
- Owner/title ({{OWNER_NAME}}, {{OWNER_TITLE}})
- State ({{STATE}})

You still need to tell me:
- **Project name or description**
- **Project address**
- **Who hired you** (GC or owner name)
- **Property owner name** (if different)
- **Payment amount**
- **Through-date** (for progress waivers)
- **Any exceptions** (disputed amounts, pending change orders)

## What I'll produce

### Conditional Waiver on Progress Payment

```
CONDITIONAL WAIVER AND RELEASE ON PROGRESS PAYMENT

Project: [Project name]
Job location: [Full address]
Owner: [Property owner]
Name of claimant: {{BUSINESS_NAME}}
Name of customer: [GC or hiring party]

Progress payment amount: $[Amount]
For work through: [Date]

Upon receipt of payment in the amount of $[Amount], the
claimant waives and releases any and all lien, stop-payment
notice, and payment bond rights through [date].

EXCEPTIONS:
[List any exceptions, or "None"]

This waiver is conditioned on receipt of payment.

Claimant: ____________________________
Company: {{BUSINESS_NAME}}
Title: {{OWNER_TITLE}}
Date: ________________
```

### Unconditional Waiver on Progress Payment

```
UNCONDITIONAL WAIVER AND RELEASE ON PROGRESS PAYMENT

Project: [Project name]
Job location: [Full address]
Owner: [Property owner]
Name of claimant: {{BUSINESS_NAME}}

The claimant has received progress payment of $[Amount]
for work through [date] and unconditionally waives all
lien, stop-payment notice, and payment bond rights
through that date.

EXCEPTIONS:
[List any exceptions, or "None"]

This waiver is effective immediately upon signing.

Claimant: ____________________________
Company: {{BUSINESS_NAME}}
Title: {{OWNER_TITLE}}
Date: ________________
```

### Conditional Waiver on Final Payment

```
CONDITIONAL WAIVER AND RELEASE ON FINAL PAYMENT

Project: [Project name]
Job location: [Full address]
Owner: [Property owner]
Name of claimant: {{BUSINESS_NAME}}

Final payment amount: $[Amount]

Upon receipt of final payment of $[Amount], the claimant
waives and releases all lien, stop-payment notice, and
payment bond rights for all work on this project.

EXCEPTIONS:
[List any exceptions, or "None"]

This waiver is conditioned on receipt of payment.

Claimant: ____________________________
Company: {{BUSINESS_NAME}}
Title: {{OWNER_TITLE}}
Date: ________________
```

### Unconditional Waiver on Final Payment

```
UNCONDITIONAL WAIVER AND RELEASE ON FINAL PAYMENT

Project: [Project name]
Job location: [Full address]
Owner: [Property owner]
Name of claimant: {{BUSINESS_NAME}}

The claimant has been paid in full and unconditionally
waives all lien, stop-payment notice, and payment bond
rights on this project.

Final payment received: $[Amount]

This waiver is effective immediately upon signing.

Claimant: ____________________________
Company: {{BUSINESS_NAME}}
Title: {{OWNER_TITLE}}
Date: ________________
```

## Critical warnings

**NEVER sign an unconditional waiver before the money has cleared your bank.**

**Check {{STATE}} requirements.** Some states have mandatory statutory waiver forms. This skill produces standard language — flag any state-specific requirements and I'll adjust.

## Waiver tracker

```
Project: [Name]
GC: [Name]

Date       | Waiver Type      | Amount    | Signed | Payment Confirmed
-----------|------------------|-----------|--------|------------------
           |                  |           |        |
```