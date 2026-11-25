---
name: contract-commercial-review
description: "Expert instructions and domain workflows for contract commercial review."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/contract-commercial-review/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Contract Commercial Review

## Purpose

This skill helps the procurement agent review supplier contracts, commercial terms and purchasing conditions from a procurement and business-risk perspective.

The goal is to identify commercial risks, negotiation points, missing clauses and decision-relevant red flags before contract approval or supplier commitment.

This skill does not replace legal review. It supports procurement preparation and highlights commercial issues that should be reviewed by legal, finance, quality, logistics or management where needed.

## When to use

Use this skill when the user asks about:

- supplier contract review,
- obchodní podmínky,
- commercial terms,
- rámcová smlouva,
- kupní smlouva,
- dodavatelská smlouva,
- Incoterms,
- payment terms,
- price validity,
- price indexation,
- SLA,
- penalties,
- liability,
- warranty,
- termination,
- MOQ,
- claims,
- contract red flags,
- negotiation points in contract terms.

## Required inputs

If available, collect:

- supplier name,
- contract type,
- category / material / service,
- contract duration,
- price and currency,
- price validity,
- price adjustment / indexation mechanism,
- Incoterms,
- delivery location,
- lead time,
- MOQ / minimum commitment,
- payment terms,
- warranty terms,
- claim process,
- liability limitation,
- penalties / service credits,
- termination rights,
- exclusivity,
- confidentiality,
- compliance requirements,
- governing law and jurisdiction,
- contract owner,
- business criticality.

## Process

1. Identify the contract type and business context.
2. Separate commercial terms from legal clauses.
3. Review pricing and price-change mechanisms.
4. Review Incoterms, delivery responsibility and logistics risks.
5. Review payment terms and working capital impact.
6. Review MOQ, minimum commitment and volume obligations.
7. Review warranty, claim and quality terms.
8. Review SLA, penalties and escalation process.
9. Review termination rights and contract flexibility.
10. Identify red flags, missing terms and negotiation points.
11. Recommend next steps and responsible stakeholders.

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí
2. Typ smlouvy a kontext
3. Klíčové obchodní podmínky
4. Red flags
5. Chybějící nebo nejasné body
6. Vyjednávací body
7. Doporučení pro nákupčího
8. Body k právní / finanční / kvalitativní kontrole
9. Další kroky

## Commercial review checklist

Review these areas where relevant:

| Area | What to check |
|---|---|
| Price | Unit price, currency, price validity, hidden costs |
| Price adjustment | Indexation, inflation clause, energy surcharge, FX clause |
| Incoterms | Delivery responsibility, risk transfer, included logistics cost |
| Payment terms | Due date, advance payment, cash-flow impact |
| MOQ / volume | Minimum order, minimum annual commitment, take-or-pay |
| Lead time | Standard lead time, emergency delivery, flexibility |
| Quality | Specification, tolerance, inspection, quality documents |
| Claims | Claim deadline, response time, corrective action, credit note |
| Warranty | Warranty duration, scope, exclusions |
| SLA | OTIF target, response times, penalties, escalation |
| Liability | Liability cap, consequential damages, indemnity |
| Termination | Notice period, termination for cause, exit flexibility |
| Exclusivity | Buyer lock-in, supplier exclusivity, restrictions |
| Compliance | SDS, REACH, ESG, certificates, audit rights |
| Confidentiality | Confidential data, drawings, pricing, technical know-how |
| Governing law | Applicable law, jurisdiction, dispute resolution |

## Red flags

Highlight these as potential red flags:

- price can change unilaterally without buyer approval,
- no price validity or no fixed pricing period,
- unclear Incoterms or delivery responsibility,
- buyer accepts high MOQ or take-or-pay without forecast certainty,
- advance payment without protection,
- no clear claim process,
- weak or missing warranty,
- no SLA for critical suppliers,
- no penalty or corrective-action mechanism for repeated failures,
- supplier liability is too limited,
- buyer has weak termination rights,
- exclusivity blocks alternative sourcing,
- missing compliance documentation,
- contract auto-renews without clear notice process,
- mismatch between contract terms and RFQ / offer.

## Recommended risk rating

Use this simple rating where useful:

- Low risk: terms are clear, balanced and commercially acceptable.
- Medium risk: some terms need clarification or negotiation.
- High risk: terms may create significant financial, operational or legal exposure.
- Blocking issue: contract should not be approved before clarification or escalation.

## Rules

- Do not provide legal advice as final legal interpretation.
- Always state that legal clauses should be confirmed by legal counsel where needed.
- Focus on procurement, commercial, operational and business-risk impact.
- Separate confirmed contract terms from assumptions.
- Do not approve a contract; recommend next steps and escalation points.
- Do not ignore small clauses if they create high commercial exposure.
