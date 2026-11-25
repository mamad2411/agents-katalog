---
name: negotiation-brief
description: "Expert instructions and domain workflows for negotiation brief."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/negotiation-brief/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Supplier Negotiation Brief

## Purpose

Prepare a practical supplier negotiation strategy, including arguments, target outcomes and fallback options.

## When to use

Use this skill when the user needs:

- negotiation arguments,
- price reduction strategy,
- supplier meeting preparation,
- counteroffer,
- contract negotiation,
- BATNA,
- email before or after negotiation.

## Required inputs

If available:

- supplier name,
- current price,
- target price,
- competing offer,
- annual spend,
- supplier performance,
- contract status,
- market context,
- technical dependency,
- alternative suppliers,
- urgency,
- relationship importance.

## Process

1. Define negotiation objective.
2. Establish factual baseline.
3. Identify buyer leverage.
4. Identify supplier leverage.
5. Prepare financial arguments.
6. Prepare non-price arguments.
7. Define target, acceptable range and walk-away point.
8. Define BATNA.
9. Prepare talking points.
10. Prepare follow-up email if needed.

## Output format

```markdown
## Vyjednávací brief

### 1. Cíl
### 2. Výchozí pozice
### 3. Argumenty pro jednání
### 4. Možné ústupky
### 5. BATNA
### 6. Doporučená taktika
### 7. Talking points
### 8. Návrh e-mailu
```

## Rules

- Do not recommend aggressive negotiation if supplier dependency is high and alternatives are weak.
- Do not use false claims.
- Keep tone professional and relationship-aware.
- Always separate hard facts from negotiation positioning.
