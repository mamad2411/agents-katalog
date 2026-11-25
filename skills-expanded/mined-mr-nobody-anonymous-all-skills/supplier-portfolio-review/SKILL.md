---
name: supplier-portfolio-review
description: "Expert instructions and domain workflows for supplier portfolio review."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/supplier-portfolio-review/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Supplier Portfolio Review

## Purpose

This skill helps the procurement agent review, structure and optimize a supplier portfolio for a category, plant, business unit or company.

The goal is to understand supplier dependency, fragmentation, consolidation potential, risk exposure and the recommended future supplier model.

## When to use

Use this skill when the user asks about:

- supplier portfolio,
- supplier base,
- supplier mix,
- supplier consolidation,
- dual sourcing,
- single sourcing,
- supplier dependency,
- supplier segmentation,
- supplier map,
- supplier risk,
- strategic supplier review,
- local vs central suppliers.

## Required inputs

If available, collect:

- supplier names,
- category / subcategory,
- annual spend by supplier,
- number of active suppliers,
- supplier location,
- supplied items / services,
- contract status,
- lead time,
- quality performance,
- OTIF / delivery performance,
- complaint history,
- dependency level,
- technical uniqueness,
- switching difficulty,
- alternative suppliers,
- business criticality.

## Process

1. Define the scope of the supplier review.
2. Map all active suppliers.
3. Group suppliers by category, site, spend and criticality.
4. Identify top suppliers by spend.
5. Identify fragmented tail spend.
6. Identify single-source and high-dependency risks.
7. Review supplier performance if data is available.
8. Assess consolidation potential.
9. Decide where dual sourcing is needed.
10. Recommend target supplier portfolio.

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí
2. Současný dodavatelský model
3. Supplier map
4. Rizika dodavatelského portfolia
5. Konsolidační příležitosti
6. Doporučený cílový supplier model
7. Quick wins
8. Další kroky

## Supplier segmentation logic

Use these segments where useful:

- Strategic supplier: high spend, high business impact, long-term importance.
- Critical supplier: operationally important, difficult to replace.
- Leverage supplier: competitive market, negotiation potential.
- Bottleneck supplier: low spend but high risk or limited alternatives.
- Tail supplier: low spend, fragmented or transactional purchases.

## Key checks

Always check:

- whether supplier count is justified by business need,
- whether single-source dependency exists,
- whether supplier consolidation could create risk,
- whether local suppliers provide flexibility,
- whether global or regional suppliers could improve leverage,
- whether suppliers have comparable scope,
- whether performance data supports the recommendation.

## Rules

- Do not recommend supplier consolidation blindly.
- Do not assume fewer suppliers always means lower risk.
- Keep dual sourcing for critical or high-risk items where justified.
- Separate commercial opportunity from operational risk.
- Always explain the trade-off between consolidation, flexibility and resilience.
- 
