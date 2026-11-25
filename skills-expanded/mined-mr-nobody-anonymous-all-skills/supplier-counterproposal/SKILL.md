---
name: supplier-counterproposal
description: "Expert instructions and domain workflows for supplier counterproposal."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/supplier-counterproposal/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Supplier Counterproposal

## Purpose

This skill helps the procurement agent prepare a professional counterproposal to a supplier.

The goal is to convert procurement analysis, quotation comparison, contract review or negotiation preparation into a clear supplier-facing response with requested changes, commercial arguments and fallback options.

## When to use

Use this skill when the user asks about:

- supplier counterproposal,
- counteroffer,
- odpověď dodavateli,
- protinávrh,
- vyjednávací e-mail,
- supplier response,
- response to quotation,
- response to commercial terms,
- contract comments to supplier,
- požadované změny podmínek,
- negotiation email,
- price counterproposal,
- commercial counterproposal.

## Required inputs

If available, collect:

- supplier name,
- original supplier offer,
- current price,
- target price,
- competing offer,
- annual volume or spend,
- key objections,
- requested commercial changes,
- contract red flags,
- desired Incoterms,
- desired payment terms,
- desired lead time,
- desired MOQ,
- desired price validity,
- required SLA,
- fallback position,
- negotiation tone,
- deadline for supplier response.

## Process

1. Identify the negotiation objective.
2. Summarize the supplier’s current position.
3. Identify the buyer’s required changes.
4. Separate must-have points from negotiable points.
5. Prepare clear commercial arguments.
6. Avoid emotional or aggressive wording.
7. Propose concrete revised terms.
8. Include a clear response deadline.
9. Keep the tone professional and relationship-aware.
10. Prepare optional soft, standard or firm version if useful.

## Output format

Use Czech by default unless supplier communication should be in English.

Return this structure:

1. Shrnutí cíle
2. Hlavní požadované změny
3. Vyjednávací argumenty
4. Doporučený tón komunikace
5. Návrh e-mailu dodavateli
6. Fallback pozice
7. Další kroky

## Counterproposal structure

A supplier counterproposal should normally include:

- polite opening,
- thanks for the offer,
- confirmation that the offer was reviewed,
- clear list of requested changes,
- commercial reasoning,
- request for revised offer,
- response deadline,
- professional closing.

## Recommended tone levels

Use these tone levels where useful:

### Soft tone

Use when the supplier relationship is strategic, dependency is high, or the buyer wants to preserve flexibility.

### Standard tone

Use as default. Clear, professional, factual and firm without being aggressive.

### Firm tone

Use when the buyer has alternatives, the supplier offer contains significant red flags, or the supplier needs to improve materially.

## Common requested changes

Where relevant, ask for:

- price reduction,
- longer price validity,
- improved payment terms,
- change from EXW to FCA / DAP,
- lower MOQ,
- shorter lead time,
- clearer SLA,
- improved claim process,
- warranty clarification,
- removal or adjustment of auto-renewal,
- better liability balance,
- compliance documentation,
- volume rebate,
- annual price fixation,
- indexation formula clarification.

## Rules

- Do not use false claims or fake competing offers.
- Do not reveal confidential internal targets unless the user explicitly asks.
- Do not make binding commitments on behalf of the buyer.
- Always keep supplier communication professional.
- Clearly separate must-have requirements from negotiation preferences.
- If legal issues are involved, state that final wording should be confirmed by legal.
