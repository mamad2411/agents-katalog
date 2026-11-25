---
name: skill
description: "Imported from gasquet82-code/procurement-agent-skills"
category: general
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/supplier-scorecard/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Skill: Supplier Scorecard

## Purpose

This skill helps the procurement agent evaluate supplier performance using a structured scorecard.

The goal is to support supplier review meetings, sourcing decisions, supplier development, risk management and management reporting.

## When to use

Use this skill when the user asks about:

- supplier scorecard,
- supplier evaluation,
- supplier performance,
- supplier rating,
- supplier KPI,
- supplier review,
- vendor evaluation,
- OTIF,
- complaints,
- lead time,
- quality performance,
- supplier ranking,
- preferred supplier decision.

## Required inputs

If available, collect:

- supplier name,
- category,
- reporting period,
- annual spend,
- delivered volume,
- number of deliveries,
- OTIF performance,
- lead time,
- quality complaints,
- claim value,
- price competitiveness,
- payment terms,
- responsiveness,
- technical support,
- compliance documentation,
- contract status,
- risk level,
- dependency level,
- business criticality.

## Process

1. Define the scorecard purpose.
2. Define the reporting period.
3. Select relevant KPI categories.
4. Assign weights to KPI categories.
5. Score each supplier consistently.
6. Highlight performance gaps.
7. Identify critical risks.
8. Recommend supplier status.
9. Propose corrective actions.
10. Prepare a management-ready summary.

## Recommended scorecard categories

Use these categories as default:

| Category | Suggested weight | What to evaluate |
|---|---:|---|
| Price / commercial competitiveness | 25 % | Price level, savings, payment terms, price stability |
| Delivery performance | 20 % | OTIF, lead time, flexibility, delivery reliability |
| Quality performance | 20 % | Complaints, defect rate, claim handling, technical consistency |
| Service and communication | 10 % | Responsiveness, escalation handling, cooperation |
| Compliance and documentation | 10 % | SDS, REACH, certificates, contract documents, ESG documents |
| Strategic fit / risk | 15 % | Dependency, alternatives, capacity, business criticality |

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí
2. Vstupní data a předpoklady
3. Scorecard tabulka
4. Hodnocení podle KPI
5. Hlavní rizika
6. Doporučený supplier status
7. Nápravná opatření / akční plán
8. Doporučení pro management

## Supplier status logic

Use these supplier statuses where useful:

- Preferred supplier: strong performance, strategic fit, low or manageable risk.
- Approved supplier: acceptable performance, can be used under standard conditions.
- Conditional supplier: usable, but requires corrective action or closer monitoring.
- Development supplier: potential exists, but performance must improve.
- Risk supplier: high risk, weak performance or serious dependency issue.
- Phase-out candidate: supplier should be replaced or reduced if alternatives exist.

## Key checks

Always check:

- whether scoring data is available or estimated,
- whether all suppliers are evaluated using the same criteria,
- whether performance issues are recurring or one-off,
- whether quality and delivery issues have financial impact,
- whether low price hides operational risk,
- whether dependency risk changes the recommendation,
- whether corrective actions have clear owners and deadlines.

## Rules

- Do not rank suppliers if data is not comparable.
- Do not overvalue price if delivery or quality performance is weak.
- Always separate measured KPI data from subjective assessment.
- Always show assumptions when exact KPI data is missing.
- Do not recommend phase-out without considering business continuity and alternatives.
