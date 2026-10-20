# Skill: Excel Workbook (XLSX) with real formulas

## Purpose

Render a **multi-sheet Excel workbook with real, editable formulas** using the shipped `make_xlsx.py` renderer. Unlike the other renderers (which consume Markdown), this one consumes a **JSON `--spec`**. Use it for cost models, IP-capacity plans, throughput/sizing calculators — anything where the user should change an input and see results recompute.

**The policy is REAL formulas** (`=SUM`, `=IF`, `=NPV`, `=FV`, `=PMT`, `=2^(...)`) — never hard-coded computed values — so a user can edit one `Inputs` cell and watch `Summary`/`Scenarios` update.

## Locate the renderer

`make_xlsx.py` ships inside this extension's `renderers/` directory. Resolve its path (first that exists wins):

1. `./extensions/network-desk/renderers/make_xlsx.py`  *(repo checkout)*
2. `./.github/extensions/network-desk/renderers/make_xlsx.py`  *(project install)*
3. `$HOME/.copilot/extensions/network-desk/renderers/make_xlsx.py`  *(user install — `%USERPROFILE%` on Windows)*

## Dependencies

```bash
pip install openpyxl
```

## The `--spec` JSON contract (pin this down — invalid specs are rejected)

Required top-level fields: **`title`**, **`specialist`**, **`sheets`**. Rules:

- Every sheet has a **unique `name` ≤ 31 chars** (Excel limit).
- A sheet uses **either** `headers` + `rows` (a simple table) **or** explicit `cells` (positioned values/formulas) — or both intentionally.
- A **formula** goes in `"formula": "=..."` — **never** put a formula string in `"value"` (it would render as text, not compute).
- **Declare `named_ranges`** for every input that a computed cell depends on, and reference inputs **by name** in formulas. Do **not** point formulas at brittle `A1` coordinates — an off-by-one ref silently ships a wrong number. `named_ranges[].ref` must target a sheet that exists.
- Put assumptions/inputs on an **`Inputs`** sheet; put results on **`Summary`** / **`Scenarios`**.
- **Cost models — live rates only:** when the `Inputs` sheet contains cloud pricing rates, those rates MUST be fetched from a live pricing API (Azure → Azure Retail Prices API via the Pricing Analyst's `retail-prices-api` skill; AWS → AWS Price List Query API; GCP → Cloud Billing Catalog API) — never hard-coded or model-recalled. Add a **`Source`** column to the `Inputs` sheet recording, per rate, the `armSkuName`/SKU id, region, `meterName`, currency, and `effectiveStartDate` (or retrieval date). Use a placeholder rate **only** when the API was unreachable, and flag it explicitly (e.g. `INDICATIVE — API unreachable`) in the `Source` column.
- Only use Excel functions you can verify exist in desktop Excel.

### Minimal valid example

```json
{
  "title": "IP Capacity Plan - 2026-05-28",
  "specialist": "capacity-planner",
  "named_ranges": [
    {"name": "vnet_prefix_bits",   "ref": "Inputs!$B$2"},
    {"name": "subnet_prefix_bits", "ref": "Inputs!$B$3"}
  ],
  "sheets": [
    {
      "name": "Summary",
      "cells": [
        {"ref": "A1", "value": "IP Capacity Plan", "style": "h1"},
        {"ref": "A3", "value": "Usable hosts / subnet"},
        {"ref": "B3", "formula": "=2^(32-subnet_prefix_bits)-5", "number_format": "#,##0"},
        {"ref": "A4", "value": "Subnets in VNet"},
        {"ref": "B4", "formula": "=2^(subnet_prefix_bits-vnet_prefix_bits)", "number_format": "#,##0"}
      ]
    },
    {
      "name": "Inputs",
      "headers": ["Parameter", "Value"],
      "rows": [["VNet prefix (/n)", 16], ["Subnet prefix (/n)", 24]]
    }
  ]
}
```

## Invocation

```bash
python "$RENDERERS/make_xlsx.py" \
  --spec model.json \
  --specialist capacity-planner
# --output OPTIONAL → network-desk/capacity-planner/reports/model.xlsx
```

- Pass the specialist **directory** name (kebab-case) as `--specialist` for the default path, or set `--output` explicitly. `--outdir` overrides the base folder.
- Keep the `model.json` `--spec` next to the `.xlsx` so the workbook can be regenerated.

## Graceful failure

- **`ModuleNotFoundError: openpyxl`** → `pip install openpyxl` and retry.
- **Validation error** (bad named range, missing sheet, duplicate name, formula in `value`) → the renderer rejects the spec with a message; fix the spec per the contract above and retry. Save the `.json` so the user can inspect it.

## References

- openpyxl: https://openpyxl.readthedocs.io/

**Analysis only — verify against vendor documentation before applying.**
