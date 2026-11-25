---
name: email-procurement-analysis
description: "Expert instructions and domain workflows for email procurement analysis."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/email-procurement-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Email Procurement Analysis

## Purpose

This skill helps the procurement agent analyze procurement-related email communication.

The goal is to extract supplier commitments, commercial terms, risks, missing information, negotiation points and recommended next steps from emails or email threads.

This skill is useful for supplier quotations, price changes, delivery confirmations, complaints, contract discussions, RFQ responses and negotiation communication.

## When to use

Use this skill when the user provides or references:

- supplier email,
- RFQ response,
- price offer in email,
- delivery confirmation,
- delay notification,
- complaint communication,
- commercial negotiation,
- contract comments,
- price increase notice,
- payment term discussion,
- supplier escalation,
- meeting follow-up,
- email thread,
- text copied from Outlook or Gmail.

## Required inputs

If available, collect:

- sender,
- recipient,
- date,
- subject,
- supplier name,
- email thread context,
- attachment references,
- offered price,
- currency,
- unit,
- quantity,
- Incoterms,
- delivery date,
- lead time,
- payment terms,
- MOQ,
- validity,
- supplier commitments,
- requested buyer action,
- deadline.

## Process

1. Identify the sender, supplier and communication purpose.
2. Determine whether the email is an offer, response, escalation, confirmation or negotiation message.
3. Extract procurement-relevant facts.
4. Identify commitments made by the supplier.
5. Identify missing or unclear information.
6. Identify commercial, operational or compliance risks.
7. Compare email content with previous RFQ, offer or agreement if available.
8. Recommend the next procurement action.
9. Draft a reply if useful.
10. Separate facts, assumptions and recommended response.

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí e-mailu
2. Typ komunikace
3. Klíčové informace
4. Závazky dodavatele
5. Rizika a nejasnosti
6. Chybějící informace
7. Doporučená reakce
8. Návrh odpovědi dodavateli
9. Další kroky

## Email extraction checklist

Extract where available:

| Area | What to extract |
|---|---|
| Supplier | Name, contact, company, role |
| Offer | Price, currency, unit, quantity, validity |
| Delivery | Lead time, delivery date, partial delivery, delay |
| Incoterms | Delivery condition, delivery place |
| Payment | Payment terms, prepayment, due date |
| MOQ | Minimum order quantity, packaging unit |
| Technical | Specification, deviations, alternatives |
| Quality | Warranty, complaints, replacement, corrective action |
| Compliance | Certificates, SDS, REACH, ESG, missing documents |
| Commitment | What the supplier explicitly confirms |
| Deadline | Date for response, delivery, validity, decision |
| Risk | Ambiguous terms, pressure, missing data, unilateral changes |

## Common email scenarios

### Supplier quotation email

Extract commercial terms and prepare quotation comparison.

### Supplier price increase email

Identify:

- proposed increase,
- effective date,
- reason,
- affected items,
- contract impact,
- negotiation options.

### Delivery delay email

Identify:

- delayed items,
- new delivery date,
- reason,
- impact,
- escalation need.

### Complaint email

Identify:

- complaint topic,
- supplier reaction,
- corrective action,
- deadline,
- claim status.

### Negotiation email

Identify:

- supplier position,
- concessions,
- open points,
- next counterproposal.

## Rules

- Do not treat vague supplier language as a firm commitment.
- Distinguish confirmed facts from implied meaning.
- Always flag missing price, unit, currency, validity, Incoterms or lead time.
- Do not send or draft aggressive replies unless explicitly requested.
- Do not reveal internal targets unless the user asks.
- If the email refers to attachments, state that attachments must be reviewed separately.
- If a reply is needed, use a professional and relationship-aware tone.
