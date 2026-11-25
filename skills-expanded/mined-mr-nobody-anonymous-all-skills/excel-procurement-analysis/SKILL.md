---
name: excel-procurement-analysis
description: "Expert instructions and domain workflows for excel procurement analysis."
category: procurement
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/gasquet82-code/procurement-agent-skills"
source_repository: "gasquet82-code/procurement-agent-skills"
source_path: "skills/excel-procurement-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Skill: Excel Procurement Analysis

## Purpose

This skill helps the procurement agent analyze Excel-based procurement data.

The goal is to support structured analysis of price lists, RFQ matrices, supplier quotations, spend data, TCO models, supplier scorecards, item lists, order data and invoice data.

This skill focuses on data understanding, cleansing, normalization, comparison and procurement-ready conclusions.

## When to use

Use this skill when the user uploads or references:

- Excel file,
- price list,
- RFQ matrix,
- supplier quotation table,
- spend data,
- supplier list,
- item master,
- purchase order data,
- invoice data,
- TCO calculation,
- supplier scorecard data,
- savings tracker,
- contract coverage table,
- category spend file,
- management dashboard data.

## Required inputs

If available, collect:

- file name,
- sheet names,
- purpose of analysis,
- reporting period,
- category,
- supplier names,
- currency,
- unit of measure,
- quantity,
- price,
- Incoterms,
- lead time,
- payment terms,
- MOQ,
- baseline price,
- target output,
- required management summary.

## Process

1. Identify workbook structure and relevant sheets.
2. Understand column meaning before calculation.
3. Check whether headers, units and currencies are clear.
4. Identify missing, duplicated or inconsistent data.
5. Normalize supplier names, item names, units and currencies where possible.
6. Separate raw data from assumptions.
7. Identify top suppliers, top items, price differences or spend drivers.
8. Check whether comparison is commercially and technically fair.
9. Calculate only where data is sufficient.
10. Prepare procurement-ready conclusions and next steps.

## Output format

Use Czech by default.

Return this structure:

1. Shrnutí
2. Použitý soubor / listy
3. Struktura dat
4. Klíčová zjištění
5. Výpočty / porovnání
6. Datové chyby a nejasnosti
7. Rizika
8. Doporučení
9. Další kroky

## Excel procurement checks

Always check:

| Area | What to check |
|---|---|
| Data scope | Period, category, site, supplier, business unit |
| Headers | Clear column names and meaning |
| Currency | Single or mixed currency, FX assumptions |
| Unit of measure | ks, kg, m2, m, pallet, package, etc. |
| Price | Unit price, total price, net/gross, VAT included/excluded |
| Quantity | Ordered, delivered, invoiced or forecast quantity |
| Supplier names | Duplicate naming, legal entity differences |
| Item names | Duplicate descriptions, unclear specifications |
| Incoterms | EXW, FCA, DAP, DDP, missing delivery basis |
| Logistics | Freight included or excluded |
| Payment terms | Working capital impact |
| MOQ | Minimum order impact |
| Baseline | Whether savings baseline is defined |
| Outliers | Extreme prices, one-off purchases, unusual volumes |
| Missing data | Blank values, inconsistent records |

## Common Excel use cases

### Price list review

Extract:

- supplier,
- item,
- price,
- currency,
- unit,
- validity,
- Incoterms,
- MOQ,
- lead time,
- comments.

### RFQ comparison

Compare:

- supplier prices,
- commercial terms,
- technical deviations,
- delivery terms,
- TCO impact,
- missing data.

### Spend baseline

Analyze:

- spend by supplier,
- spend by category,
- spend by item,
- top suppliers,
- tail spend,
- data quality gaps.

### Supplier scorecard

Analyze:

- OTIF,
- complaints,
- lead time,
- claim value,
- compliance status,
- scorecard ranking.

## Rules

- Do not calculate savings without a clear baseline.
- Do not compare prices without checking unit, currency, Incoterms and technical scope.
- Do not assume that all sheets are relevant.
- Do not modify source data unless the user explicitly asks.
- Always explain assumptions used in calculations.
- Always flag missing or unreliable data.
- If the Excel file contains formulas, preserve the distinction between source values and calculated values.
