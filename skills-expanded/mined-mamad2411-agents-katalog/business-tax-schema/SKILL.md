---
name: business-tax-schema
description: >
  Contains verified revision-to-year mapping tables (4 FL eras R-01-07 through R-01-19,
  2 federal eras pre/post-TCJA), YAML file routing for concept-map and per-year
  expectations, and NOL carryback/carryforward rules with CARES Act exceptions.
  Form 1120, Florida F-1120, Form 5472 line definitions across tax years 2007-2025.
  Consult when looking up which form line a field maps to for a specific tax year,
  checking whether a line number shifted between revisions, finding the FL exemption
  amount for a given year, determining which era governs a tax year, verifying Form 5472
  filing requirements for foreign-owned corps, resolving pre-TCJA vs post-TCJA rules
  (Section 199, graduated rates, AMT), or onboarding a new tax year into the schema.
---

# Business Tax Schema

Structured vocabulary and revision topology for C-corporation tax forms: federal
Form 1120, Florida F-1120, and Form 5472 (foreign-owned corps). This skill provides
the canonical field names, line mappings, and era-routing logic that downstream
preparation skills depend on.

> **State-specific scope:** Federal Form 1120 and Form 5472 content is nationally
> applicable. Florida F-1120 eras, exemption history, and line shifts use **Florida**
> as the reference state jurisdiction. Sections marked (Florida) contain state-specific
> content.

## Era Routing

Every tax year maps to exactly one era for each jurisdiction. Determine the era first,
then apply the era-specific line definitions and rules.

### Federal 1120 Eras

- **Pre-TCJA (2007-2017)** — Graduated rates 15-35%, Section 199 deduction on Line 25, corporate AMT applies, NOL 2-year carryback / 20-year carryforward with 100% usage
- **Post-TCJA (2018+)** — Flat 21% rate, Section 199 repealed, no corporate AMT, NOL indefinite carryforward with 80% usage limit

The TCJA boundary at tax year 2018 is the single most important routing decision in
federal return preparation. When a user asks about any Form 1120 line, rate, or
deduction rule, resolve the era before answering.

### Florida F-1120 Eras (Florida)

Four structural revisions, identified by form revision stamp:

- **R-01-07 (2007-2011)** — Emergency excise tax (EET) present, Schedule VI AMT active, taxpayer election field (E), $5,000 exemption
- **R-01-13 (2012-2014)** — EET dropped, line numbers shift from R-01-07, exemption increases ($25K in 2012, $50K from 2013), Schedule VI still present
- **R-01-16 (2015-2017)** — New credit lines added to Schedule V, email field added to contact section, Schedule VI AMT still active
- **R-01-19 (2018+)** — Schedule VI dropped entirely (mirrors federal AMT repeal), taxpayer election field removed, page 2 letter designators shift

FL corporate tax rate: 5.5% across all eras (2007-2025).

### Florida Exemption History (Florida)

- 2007-2011 — $5,000
- 2012 — $25,000
- 2013-2025 — $50,000

The exemption amount is year-specific and independent of the revision era. Always
look up the exact year, not the era bracket.

## NOL Rules by Era

| Rule | Pre-TCJA (2007-2017) | Post-TCJA (2018+) |
|------|----------------------|-------------------|
| Carryback | 2 years (optional) | Not allowed* |
| Carryforward | 20 years | Indefinite |
| Usage limit | 100% of taxable income | 80% of taxable income |

*CARES Act exception: NOLs arising in 2018-2020 could be carried back 5 years.

The NOL era determines which rules apply to the loss year of origin, not the
utilization year. A pre-TCJA NOL being used in a post-TCJA year retains its
20-year carryforward window but is subject to the 80% limitation in the
utilization year.

## Form 5472

Required every year for C-corps with 25%+ foreign ownership (IRC 6038A).

- Penalty: $25,000 per form for failure to file
- Parts I-VI: reporting entity info, related party details, monetary transactions, nonmonetary transactions, additional information
- Attached to the Form 1120 — not filed separately
- Required even if no reportable transactions occurred during the year

## Concept Mapping

The schema uses a three-layer vocabulary:

1. **Inventory fields** — Internal names from data extraction (e.g., `gross_receipts`, `officer_compensation`)
2. **Form lines** — IRS/state form line identifiers (e.g., `1120.Line_1a`, `F-1120.Line_1`)
3. **Concept names** — Canonical business concepts that bridge inventory to form (e.g., `gross_revenue`, `officer_comp`)

When mapping an inventory field to a form line:
1. Look up the inventory field in the concept map to get the canonical concept name
2. Resolve the tax year to an era
3. Use the era-specific line definitions to get the target form line
4. Validate that the line exists in that era (lines shift between revisions)

### source_ref Notation

Data lineage in schema files uses `source_ref` to trace values back to extraction:

```yaml
source_ref: "extracted_values[field=gross_receipts]"
```

## Revision Topology

Line numbers are not stable across revisions. When working with historical returns
or multi-year comparisons, always verify line definitions against the correct era.

### Federal Line Shifts (TCJA Boundary)

Key changes at the 2017-2018 boundary:
- Line 25 (Section 199 domestic production deduction) — present pre-TCJA, removed post-TCJA
- Line 29a/29b (NOL deduction) — carryback election line removed post-TCJA
- Schedule C (DRD) — computation unchanged but AMT interaction removed
- Tax rate schedule — graduated table replaced by flat 21% on Line 31

### Florida Line Shifts (Florida)

Cross-revision changes to watch:
- **R-01-07 to R-01-13**: EET lines removed, line numbers renumber from that point down; exemption amount field changes
- **R-01-13 to R-01-16**: Credit lines added to Schedule V (insertion, not renumber); email field added to contact block
- **R-01-16 to R-01-19**: Schedule VI AMT dropped entirely; taxpayer election field (E) removed; page 2 letter designators shift

## Adding a New Tax Year

1. Create expectations file using the prior year as template
2. Verify the FL revision era — if a new revision stamp appears, update the era file or create a new one
3. Check for federal law changes requiring a revision update (rate changes, new deductions, new schedules)
4. Run assess-year validation against the new expectations

## Historical Form Sourcing

Each tax year requires year-specific source forms. Current-year forms do not document
historical line structures.

- **IRS Prior Archive (2007-2024)** — `irs.gov/pub/irs-prior/i1120--{year}.pdf`
- **TaxFormFinder FL (2011-2024)** — `taxformfinder.org/forms/{year}/{year}-florida-form-f-1120.pdf`
- **eformrs.com FL (2007-2010)** — `eformrs.com/Forms{yy}/States{yy}/FL/FL1120.pdf`

Use the IRS prior archive as authoritative for federal line definitions. Use
TaxFormFinder or eformrs for Florida forms depending on the year range.

## Validation Sources

External references for verifying schema accuracy:

- IRS Section 199 Repeal — `irc.bloombergtax.com/public/uscode/doc/irc/section_199`
- FL Statutes 220.14 (corporate income tax) — `flsenate.gov/Laws/Statutes/2024/0220.14`
- FL DOR Corporate Income Tax — `floridarevenue.com/taxes/taxesfees/Pages/corporate.aspx`

## Supporting References

Read these for field-level detail and structured data:

- `references/business-tax-schema.md` — Full schema source with concept vocabulary, file routing table for YAML data files (concept-map, core form definitions, revision-era files, per-year expectations), revision-to-year mapping tables, NOL rules, FL exemption history, Form 5472 overview, historical form sourcing URLs, and new-year onboarding procedure. Read when you need the YAML file routing table, the source_ref notation spec, or the canonical era-to-year mapping.

## Cross-Plugin References

For GL account structure that feeds tax line mapping:
- Invoke `accounting-foundation:chart-of-accounts` for account numbering, Form 1120 tax-line mapping at the GL level, and book-tax difference classification

For entity context affecting form selection:
- Invoke `accounting-foundation:entity-profile` for corporate entity type, ownership structure (triggers Form 5472), fiscal year, and state nexus

For financial data flowing into tax forms:
- Invoke `accounting-foundation:financial-statements` for income statement and balance sheet presentation that maps to Form 1120 schedules
- Invoke `bookkeeping:monthly-close` for period-end financials that feed return preparation

For platform-level field extraction:
- Invoke `qbo-integration:qbo-reporting` for QBO report data that maps to schema inventory fields
- Invoke `qbo-integration:qbo-audit` for QBO tax data extraction and audit trail

## Cross-Plugin Consumers

Skills that depend on this schema for form structure and line definitions:

- `tax-prep:form-1120-prep` — federal Form 1120 line definitions, era routing, and field-to-line mapping for return assembly
- `tax-prep:state-returns` — Florida F-1120 revision topology, era-specific line numbers, and exemption amounts
- `tax-prep:tax-forms` — supporting schedule structure and line vocabulary across form types
- `tax-prep:nol-tracking` — NOL era rules (carryback/carryforward windows, usage limits) and CARES Act exceptions
- `tax-prep:tax-compliance` — filing requirement rules that depend on form revision and era
- `tax-prep:e-filing` — form field identifiers for electronic filing package assembly
- `tax-prep:tax-planning` — era-specific rate tables and deduction availability for planning scenarios
- `financial-planning:tax-provision` — federal and state rate tables, TCJA boundary logic for ASC 740 provision computation
