---
name: quotation-comparison
description: "Expert instructions and domain workflows for quotation comparison."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/quotation-comparison/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Supplier Quotation Comparison

## Purpose

Compare supplier quotations in a structured, objective and management-ready way.

## When to use

Use this skill when the user asks to compare:

- supplier offers,
- prices,
- commercial terms,
- delivery terms,
- cost scenarios,
- supplier alternatives.

## Required inputs

If available:

- supplier names,
- offered prices,
- currency,
- unit of measure,
- incoterms,
- logistics cost,
- payment terms,
- lead time,
- MOQ,
- validity of offer,
- technical deviations,
- historical baseline,
- annual volume.

## Process

1. Identify all supplier offers.
2. Normalize units of measure.
3. Normalize currency if exchange rates are provided.
4. Check whether Incoterms are comparable.
5. Separate unit price from landed cost.
6. Check technical comparability.
7. Calculate differences versus best price and baseline.
8. Identify missing data.
9. Highlight risks.
10. Recommend next action.

## Output format

```markdown
## 1. Shrnutí
## 2. Porovnání nabídek
## 3. Finanční dopad
## 4. Rizika a nejasnosti
## 5. Doporučení
## 6. Další kroky
```

## Rules

- Never recommend based only on price if the offers are not technically comparable.
- Always flag missing Incoterms, currency, unit or scope.
- If data is incomplete, provide a conditional recommendation.
- Separate facts from assumptions.
