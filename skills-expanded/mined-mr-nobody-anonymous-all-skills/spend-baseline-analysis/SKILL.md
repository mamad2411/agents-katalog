---
name: spend-baseline-analysis
description: "Expert instructions and domain workflows for spend baseline analysis."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/spend-baseline-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Spend Baseline Analysis

## Purpose

This skill helps the procurement agent create, validate and explain a purchasing spend baseline for a category, supplier group, plant, business unit or reporting period.

A spend baseline is the foundation for category strategy, RFQ prioritization, savings tracking, supplier consolidation and management reporting.

## When to use

Use this skill when the user asks about:

- spend baseline,
- annual spend,
- supplier spend,
- category spend,
- purchasing data analysis,
- savings baseline,
- procurement transparency,
- category diagnostic,
- top suppliers,
- top items,
- unmanaged spend,
- spend by plant, site or business unit.

## Required inputs

If available, collect:

- reporting period,
- supplier name,
- category,
- item / material description,
- quantity,
- unit of measure,
- price,
- currency,
- invoice value,
- order value,
- plant / location,
- cost center,
- buyer / owner,
- contract status,
- purchase order date,
- invoice date.

## Process

1. Define the scope of the baseline.
2. Identify the time period.
3. Group spend by category, supplier, item and site.
4. Clean obvious duplicates or inconsistent naming.
5. Normalize currencies if FX rates are available.
6. Check whether prices and quantities use comparable units.
7. Identify top suppliers and top items.
8. Identify unmanaged or fragmented spend.
9. Highlight missing or unreliable data.
10. Prepare management-ready conclusions.

## Output format

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí
2. Rozsah baseline
3. Hlavní zjištění
4. Spend podle dodavatelů
5. Spend podle kategorií / položek
6. Datové mezery a rizika
7. Příležitosti
8. Doporučené další kroky

## Key checks

Always check:

- whether the reporting period is clear,
- whether spend includes or excludes VAT,
- whether currencies are mixed,
- whether supplier names are duplicated,
- whether units are consistent,
- whether one-off purchases distort the baseline,
- whether spend is linked to a category,
- whether there is a contract owner.

## Rules

- Do not claim savings without a defined baseline.
- Do not mix invoice value and order value without stating it.
- Do not compare spend across currencies without FX assumptions.
- Always mark incomplete or unreliable data.
- Always distinguish spend visibility from confirmed savings opportunity.
