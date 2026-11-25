---
name: grant-budget
description: >
  Build the grant budget workbook and budget narrative. This skill should be
  used when the user says "build the budget", "create the budget justification",
  "budget narrative", "we need the budget forms", or when the requirements
  matrix for an active grant includes budget deliverables.
version: 0.1.0
---

# Grant Budget

Produce a budget the program officer can defend and an auditor cannot
puncture: an Excel workbook plus a narrative where every number in the
narrative matches the workbook exactly.

## Inputs

Read the requirements matrix for: award ceiling/floor, match or cost-share
percentage, indirect cost rules (de minimis 10% MTDC vs. negotiated rate),
allowable/unallowable costs, budget period(s), and required forms (e.g.,
SF-424A). Read the project description draft so the budget funds exactly
the activities the narrative promises — reviewers cross-check.

Gather from the user what the profile does not contain: salaries or salary
bands for named roles, fringe rate, and real vendor quotes for major
purchases. Never invent compensation figures.

## Workbook (`final/budget.xlsx`)

Build with the spreadsheet toolchain, one budget period per sheet plus a
summary sheet for multi-year awards. Standard categories (adapt to the
funder's own form when one is prescribed):

Personnel (role, annual salary, FTE%, months, request), Fringe (rate
applied to personnel), Travel (trips × people × cost basis), Equipment
(per-unit ≥ the funder's capitalization threshold, usually $5,000),
Supplies, Contractual (each consultant with day rate and days), Other,
Total Direct, Indirect (show base and rate), Total, and Match columns
where required.

Rules: every line computes from visible unit assumptions (formulas, not
typed totals); match column shows source of match and whether cash or
in-kind; indirect base excludes items the rate agreement excludes;
grand total lands within the award range. Round to whole dollars.

## Narrative (`drafts/budget-narrative.md` → docx)

One paragraph per line item, in the funder's category order: what it is,
how the cost was computed (unit × rate × time, quote, or salary basis),
and why it is necessary for the project — tie each item to an activity in
the project narrative. Apply the house style; budget narratives are prose,
not tables restated.

## Verification pass

Before delivery: recompute every category subtotal and the grand total
independently and compare to the workbook; check narrative-to-workbook
agreement line by line; check personnel in the budget appear in the
narrative and vice versa; confirm no unallowable costs; confirm match math
meets the required percentage. Report the checks performed.
