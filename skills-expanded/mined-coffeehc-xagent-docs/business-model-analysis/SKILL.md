---
name: business-model-analysis
description: Use when analyzing, comparing, or designing a business model, revenue model, monetization path, unit economics, customer segment, value proposition, go-to-market logic, competitive moat, market entry, or venture/business idea. Prefer this Skill when the task needs commercial viability, assumptions, risks, validation plan, or business model report. Do not use for detailed financial statement analysis, personalized investment advice, or unsupported revenue guarantees.
meta:
  version: 2
  display_name: 商业模式分析
---

# Business Model Analysis

## Purpose

Evaluate whether a business idea can create, deliver, and capture value with a realistic customer, channel, cost, revenue, and validation path.

## Use When

Use for:

- business idea evaluation
- SaaS or service business model design
- revenue model comparison
- unit economics reasoning
- competitive moat review
- go-to-market assumptions
- market entry thinking

## Material Gate

Identify:

- target customer, pain, current alternative, buyer, user, and payer
- offer, pricing idea, channel, delivery model, and cost drivers
- evidence for demand, willingness to pay, competition, and feasibility
- desired output: quick critique, model canvas, report, or validation plan

If data is weak, label the model as hypothesis, not proven opportunity.
If the analysis depends on market size, competitor claims, current examples, pricing benchmarks, or customer willingness-to-pay evidence, use `skills_find` / `skills_load` for `market-research`, `research-synthesis`, or an equivalent evidence Skill when available before treating the conclusion as source-backed.
If the expected output is a final report or investor-style brief, treat report packaging as a separate capability. Use `skills_find` / `skills_load` for `html-report-builder` or an equivalent visual report Skill when available.

## Workflow

1. State the customer problem and why current alternatives are insufficient.
2. Map value proposition, buyer, user, payer, channel, and delivery.
3. Identify revenue streams, cost structure, gross margin logic, and unit economics assumptions.
4. Compare defensibility: switching cost, data, workflow lock-in, brand, network, distribution, or operational expertise.
5. Surface key risks and invalidating assumptions.
6. Propose validation tests before scaling.
7. Use evidence Skills for source-backed demand, competition, pricing, or case claims when those facts are not already provided.
8. Use `html-report-builder` for business model reports or investor-style briefs when available, with Markdown limited to notes, assumptions, validation logs, or supporting drafts unless explicitly requested as final format.

## Checks

- Customer and payer are explicit.
- Revenue and cost logic are separated.
- Competition includes non-consumption and manual alternatives.
- Risks are testable.
- Recommendation is scenario-based, not guaranteed.
- External demand, competition, pricing, or benchmark claims are source-backed or explicitly labeled as assumptions.
- Final report deliverables expose assumptions, validation evidence, risks, and unverified items.

## Outputs

- business model analysis
- business model canvas
- unit economics assumptions
- moat and risk summary
- validation plan
- market entry brief

## Boundary

This Skill owns business model reasoning, viability framing, and validation planning. It does not own accounting advice, investment advice, fundraising claims, legal/tax approval, or revenue guarantees.

It must not run shell, Python, Node, npm, curl, MCP, market-data, CRM, ads, payment, spreadsheet, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
