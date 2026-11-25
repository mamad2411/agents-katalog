---
name: finance-modeling-office-pro
description: Master router for finance, financial modeling, Excel/Office, valuation, market analysis, diligence, and financial deliverable work. Use when the user asks for a broad finance workflow, a new model or deck, an Excel model audit, a research report, a valuation memo, or when you need to choose among the plugin's finance and Office skills.
---

# Finance Modeling Office Pro

Use this skill as the front door for the plugin. It turns broad finance requests into the smallest set of focused skills, files, and checks needed to produce reliable analyst work product.

## Non-Negotiables

- Treat outputs as decision support, not investment, legal, tax, accounting, or compliance advice.
- Current facts must be verified when they matter: market prices, filings, rates, management guidance, laws, regulations, and schedules.
- Prefer deterministic math before narrative. For valuation, dilution, debt schedules, returns, portfolio, and accounting work, calculations come before prose.
- For workbook deliverables, formulas should be live Excel formulas where the user expects a model, not Python-computed static answers.
- Every financial model needs a verification trail: source notes, formula checks, hardcode review, error scan, and a stated recalculation limitation if no spreadsheet engine recalculated cached values.

## Skill Routing

Use focused skills directly when the user request is clear:

| Task | Preferred Skill |
|---|---|
| New DCF workbook | `$dcf-model` or `$officecli-financial-model` |
| 3-statement model | `$3-statement-model` |
| LBO / sponsor returns | `$lbo-model` |
| Trading comps or precedent comps | `$comps-analysis` |
| Public-company valuation from market data | `$market-company-valuation` |
| Existing Excel model QA | `$audit-xls` |
| Messy spreadsheet cleanup | `$clean-data-xls` |
| Headless workbook creation | `$xlsx-author` |
| OfficeCLI workbook/deck authoring | `$officecli-xlsx`, `$officecli-financial-model`, `$officecli-pitch-deck` |
| Initiating coverage / equity research | `$initiating-coverage`, `$equity-research`, `$earnings-analysis` |
| Earnings preview/update | `$earnings-preview`, `$market-earnings-preview`, `$model-update` |
| IB pitch or process material | `$pitch-agent`, `$pitch-deck`, `$teaser`, `$cim-builder` |
| PE memo or diligence | `$ic-memo`, `$dd-checklist`, `$deal-screening`, `$returns-analysis` |
| Portfolio or wealth workflow | `$portfolio-monitoring`, `$client-report`, `$portfolio-rebalance` |
| Fund admin / accounting | `$gl-recon`, `$nav-tieout`, `$roll-forward`, `$variance-commentary` |
| Data analysis / forecasting | `$data-pandas`, `$data-polars`, `$data-statsmodels`, `$data-timesfm-forecasting` |

If a request spans several rows, coordinate the work explicitly: source retrieval, model build, review, narrative/deck, then final verification.

## Default Workflow

1. Define the deliverable: workbook, memo, deck, data pack, dashboard, note, or QA report.
2. Identify data sources and freshness requirements. Ask only if the source cannot be inferred or found.
3. Choose the focused skill(s) and read their instructions before acting.
4. Build calculations with explicit assumptions, source notes, and scenario cases.
5. Run workbook/script checks when files are created or modified.
6. State what was verified, what was not recalculated, and what depends on stale or user-provided inputs.

## Excel Model Standards

Read `references/modeling-standards.md` and `references/excel-delivery-gates.md` for the house modeling rules. In short:

- Inputs, Calc, Outputs, and Checks should be separate zones or clearly separated sections.
- Blue font means hardcoded input; black means same-sheet formula; green means cross-sheet link; red means external link.
- Assumptions live in cells with source notes, not embedded in formulas.
- Calc sheets should not contain unexplained hardcoded numeric cells.
- Use scenario switches and sensitivity grids with live formulas.
- Add balance, tie-out, and sanity checks where the model type calls for them.

## Verification

For any delivered workbook, run at least:

```powershell
python scripts/verify_xlsx.py <workbook.xlsx>
python scripts/verify_financial_model.py <workbook.xlsx>
```

`verify_xlsx.py` checks formula and cached-value error markers. `verify_financial_model.py` adds finance-model QA such as calc hardcodes, formulas with numeric literals, missing Checks sheets, and blank formulas. Both are static checks unless a spreadsheet engine is also used to recalculate the workbook.

## References

- `references/source-inventory.md` records which attached archives contributed to this plugin.
- `references/runtime-spreadsheets.md` defines portable workbook output discipline.
- `references/runtime-documents.md` and `references/runtime-presentations.md` cover memo/deck deliverables.
- `references/connectors.md` names expected connector/data-source behavior.

