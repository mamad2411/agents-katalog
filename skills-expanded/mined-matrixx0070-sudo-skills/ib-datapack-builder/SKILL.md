---
name: ib-datapack-builder
version: 1.0.0
description: Extract and normalize a target's financials into an IC-ready workbook with a documented, auditable assumptions layer that every downstream deal model ties back to.
author: matrixx0070
tags: [investment-banking, m&a, financial-analysis, datapack, normalization]
capabilities: []
---

## When to use
Use this when you have raw financials — audited statements, management accounts, a trial balance — and need a single clean workbook that the CIM, the valuation, and the merger model all draw from. The datapack is the source of truth: it normalizes reported numbers, isolates one-off and non-recurring items, and records every assumption so the analysis is auditable and defensible in diligence.

**Not for:** the buyer-facing narrative (use ib-cim-builder), the accretion/dilution mechanics (use ib-merger-model), or pipeline tracking (use ib-deal-tracker). If the source financials are unreconciled or of unknown provenance, resolve that before building.

## Method
1. Inventory sources and lock provenance: which statement, which period, audited vs. management, and the FX and fiscal-year convention. One tab lists every source and its status.
2. Lay out the historical financials on a consistent basis — P&L, balance sheet, cash flow — for 3-5 years, with a single sign and units convention across the book.
3. Normalize EBITDA: strip out non-recurring, one-off, and owner-related items (litigation, restructuring, above-market owner comp, related-party rent) into a transparent quality-of-earnings bridge from reported to adjusted.
   **Decision point:** for any adjustment above the materiality threshold, require a documented source and rationale; if it cannot be evidenced, leave it out and flag it.
4. Separate hard inputs (cells you type from source) from calculations (formulas) and assumptions (drivers you choose) — color/label them distinctly so a reviewer can audit at a glance.
5. Build the assumptions tab: every growth rate, margin, and driver in one place, each with a stated basis, so downstream models point to it rather than hard-coding.
6. Tie out: the datapack totals must reconcile to the audited statements; document any bridging difference.
7. Version and date the workbook; downstream models reference this version, not scattered copies.

## Example
> Datapack for a sell-side services business. Reported EBITDA $9.2M normalized to $11.0M via a QoE bridge: +$1.1M above-market owner salary, +$0.4M one-time litigation, +$0.3M related-party rent to market. Each add-back cited to payroll records or the lease. Inputs blue, formulas black, assumptions on a dedicated green tab. Historicals tied to audited FY statements within $2k (rounding). CIM and merger model both referenced datapack v3.

## Pitfalls
- Hard-coding numbers into formulas so no one can trace where a figure came from — every input traces to a source, every driver to the assumptions tab.
- Aggressive or undocumented EBITDA add-backs that inflate adjusted earnings and collapse under buyer QoE diligence.
- Mixing units, signs, or FX conventions across tabs so totals silently fail to tie.
- Letting multiple uncontrolled copies circulate; downstream work must reference one dated version.

## Output format
```
DATAPACK — PROJECT <codename> — v<n> — <date>

TAB: Sources        <statement | period | audited/mgmt | FX | status>
TAB: P&L            <FY-4 ... FY0, consistent basis, units stated>
TAB: Balance Sheet  <FY-4 ... FY0>
TAB: Cash Flow      <FY-4 ... FY0>
TAB: EBITDA Bridge  Reported EBITDA           <->
                    + non-recurring items     <-> (source)
                    + owner/related-party adj <-> (source)
                    = Adjusted EBITDA         <->
TAB: Assumptions    <driver | value | basis/source>
TAB: Tie-out        <datapack total vs audited | difference | explanation>

Legend: INPUT (from source) | CALC (formula) | ASSUMPTION (driver)
Downstream models must reference: datapack v<n>
```

## Reference
- Adjusted (normalized) EBITDA = reported EBITDA +/- non-recurring, one-off, and owner/related-party items; the reported-to-adjusted "quality of earnings" bridge is the most scrutinized exhibit in buy-side diligence.
- Model hygiene: separate inputs, calculations, and assumptions; never hard-code an assumption inside a formula; a single dated source of truth feeds the CIM, valuation, and merger model.
- Common normalizations: above/below-market owner compensation, related-party rent, one-time legal/restructuring, discontinued operations, non-recurring gains/losses, and run-rate adjustments for recent hires or contracts.
- Every add-back needs evidence; unsupported adjustments are the fastest way to lose credibility in confirmatory diligence.
