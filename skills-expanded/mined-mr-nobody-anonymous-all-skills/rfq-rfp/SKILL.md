---
name: rfq-rfp
description: "Expert instructions and domain workflows for rfq rfp."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/rfq-rfp/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: RFQ / RFP Preparation

## Purpose

Prepare clear, structured and supplier-ready RFQ/RFP communication and response templates.

## When to use

Use this skill when the user needs to:

- create a supplier RFQ,
- prepare a tender package,
- request updated pricing,
- define supplier response requirements,
- collect comparable offers,
- prepare a supplier response matrix.

## Required inputs

If available, collect:

- category or product name,
- item description,
- technical specification,
- quantity / annual volume,
- unit of measure,
- requested delivery location,
- requested Incoterms,
- expected delivery date,
- required validity of offer,
- required documents,
- list of suppliers,
- deadline for supplier response,
- evaluation criteria.

## Process

1. Clarify the RFQ objective.
2. Identify required commercial and technical fields.
3. Make sure supplier answers will be comparable.
4. Request all cost components separately.
5. Request technical deviations explicitly.
6. Define response deadline and validity.
7. Prepare a supplier-friendly email.
8. Prepare a response matrix if needed.
9. Add evaluation criteria.

## Output format

Use Czech by default.

Return:

1. RFQ summary
2. Supplier email draft
3. Required supplier response fields
4. Evaluation criteria
5. Missing inputs / assumptions

## Rules

- Never create an RFQ that asks only for unit price if logistics, currency, validity and technical deviations matter.
- Always ask suppliers to confirm technical compliance or list deviations.
- Always request offer validity.
- If annual volume is unknown, state that the RFQ is indicative.
