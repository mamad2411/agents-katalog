---
name: tco-analysis
description: "Expert instructions and domain workflows for tco analysis."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/tco-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Total Cost of Ownership Analysis

## Purpose

Calculate and explain the full economic impact of a supplier, category or sourcing decision.

## When to use

Use this skill when the user mentions:

- TCO,
- total cost,
- landed cost,
- logistics,
- currency impact,
- payment terms,
- inventory,
- switching cost,
- multi-supplier scenario,
- annual spend impact.

## Required inputs

If available:

- unit price,
- currency,
- annual volume,
- unit of measure,
- logistics cost,
- customs / duties,
- packaging cost,
- payment terms,
- lead time,
- inventory impact,
- quality cost,
- complaint cost,
- switching cost,
- baseline supplier / price,
- FX rate.

## Process

1. Define the baseline.
2. Identify all cost elements.
3. Normalize prices to the same unit.
4. Convert currency if FX rate is available.
5. Calculate landed cost.
6. Add operational costs if available.
7. Calculate annualized impact.
8. Create scenarios if assumptions vary.
9. Identify cost drivers.
10. Provide recommendation.

## Output format

```markdown
## 1. TCO shrnutí
## 2. Vstupní data a předpoklady
## 3. Výpočet
## 4. Scénáře
## 5. Hlavní cost drivers
## 6. Rizika
## 7. Doporučení
```

## Rules

- Do not invent FX rates unless the user explicitly allows estimates.
- Do not hide assumptions.
- Always show whether logistics and payment terms are included.
- If full TCO cannot be calculated, provide a partial landed cost analysis.
