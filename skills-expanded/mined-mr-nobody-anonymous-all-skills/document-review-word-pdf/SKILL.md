---
name: document-review-word-pdf
description: "Expert instructions and domain workflows for document review word pdf."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/document-review-word-pdf/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Document Review Word PDF

## Purpose

This skill helps the procurement agent review Word, PDF and text-based procurement documents.

The goal is to extract key procurement information, identify commercial and operational risks, compare document content with RFQ or supplier expectations, and prepare a structured summary for the buyer, category manager or management.

This skill is used for document understanding. If the document contains contract or commercial terms, combine this skill with Contract Commercial Review. If the document requires a supplier response, combine it with Supplier Counterproposal.

## When to use

Use this skill when the user uploads or references:

- Word document,
- PDF document,
- supplier offer,
- commercial terms,
- technical specification,
- contract draft,
- framework agreement,
- supplier presentation,
- product datasheet,
- certificate,
- SDS document,
- REACH declaration,
- quality document,
- ESG document,
- audit document,
- tender document,
- RFQ response document.

## Required inputs

If available, collect:

- document name,
- document type,
- supplier name,
- category / material / service,
- purpose of review,
- expected decision,
- related RFQ or baseline,
- required output format,
- deadline,
- specific concerns from the user.

## Process

1. Identify document type and purpose.
2. Extract key procurement-relevant information.
3. Separate commercial, technical, quality, compliance and operational content.
4. Identify missing or unclear information.
5. Identify red flags and risks.
6. Compare document terms against RFQ or expected requirements if available.
7. Highlight assumptions and limitations.
8. Recommend next steps.
9. Suggest which additional skills should be used if needed.
10. Prepare a structured buyer-ready or management-ready output.

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí dokumentu
2. Typ dokumentu a účel
3. Klíčové informace
4. Obchodní podmínky
5. Technické / kvalitativní informace
6. Compliance / dokumentace
7. Red flags a rizika
8. Chybějící nebo nejasné body
9. Doporučení
10. Další kroky

## Procurement extraction checklist

When reviewing a document, extract where available:

| Area | What to extract |
|---|---|
| Supplier | Name, entity, contact, location |
| Scope | Product, service, material, category |
| Price | Unit price, currency, price validity, hidden costs |
| Quantity | MOQ, annual volume, order batch, packaging unit |
| Incoterms | Delivery term, delivery place, risk transfer |
| Delivery | Lead time, partial delivery, urgent delivery |
| Payment | Payment terms, advance payment, invoice conditions |
| Validity | Offer validity, contract duration, price fixation |
| Quality | Specifications, tolerance, inspection, warranty |
| Claims | Claim process, deadlines, corrective actions |
| Compliance | SDS, REACH, certificates, ESG, audit rights |
| Contract | Termination, liability, penalties, auto-renewal |
| Risk | Dependency, operational risk, missing data |

## Document risk levels

Use this simple rating where useful:

- Low risk: document is clear, complete and aligned with procurement requirements.
- Medium risk: some terms or data need clarification.
- High risk: document contains significant commercial, operational or compliance risk.
- Blocking issue: document should not be accepted before clarification, correction or escalation.

## Common red flags

Highlight these where relevant:

- unclear price or missing currency,
- price validity missing or too short,
- unclear unit of measure,
- hidden costs,
- EXW or unclear Incoterms without logistics cost,
- advance payment without protection,
- high MOQ without forecast certainty,
- missing technical specification,
- missing compliance documentation,
- unclear warranty,
- short claim period,
- missing SLA,
- unilateral price change,
- automatic contract renewal,
- weak termination rights,
- mismatch between offer and RFQ,
- scanned PDF or unclear source document.

## Rules

- Do not assume missing document content.
- Do not invent values that are not in the document.
- Always separate extracted facts from assumptions.
- If the document is scanned, incomplete or hard to read, state this limitation.
- If legal interpretation is needed, recommend legal review.
- If commercial terms are included, recommend using Contract Commercial Review.
- If a supplier response is needed, recommend using Supplier Counterproposal.
