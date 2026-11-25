---
name: cost-check
description: "Produce an order-of-magnitude construction cost check (per m2 or per ft2, elemental or whole-building) with the rate source, its date, its location, and the inflation and location adjustments always stated, plus a low/likely/high sensitivity range. Refuses to quote a rate from memory as fact: rates come from the architect, a cost consultant, or a cited published source. Use when the architect wants \"a rough cost\", \"cost per square metre\", \"is this within budget\", \"budget check\", \"order of magnitude cost\", \"how much would this cost to build\", or \"compare the cost of two options\". Takes areas from area-check or programme-schedule; hands to value-engineering when the scheme is over budget and to fee-proposal when cost drives the fee."
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Cost check

Architects need to know early whether a scheme is roughly affordable. A cost check answers that with arithmetic anyone can audit: area times a sourced rate, adjusted openly, with a range. It is not a cost plan, and it says so.

## When to use

- Feasibility: does the brief fit the budget?
- Comparing options where cost is one of the criteria.
- A sense-check of a contractor's or cost consultant's number.
- Before a client meeting where "how much?" will be the first question.

## Input

- **Areas**, with the measurement basis (GIA / GFA / NIA, and the standard if known, e.g. IPMS, RICS, BOMA). From `area-check` or `programme-schedule`.
- **Rates.** One of:
  - From the architect or their cost consultant.
  - A published source (a cost guide, a national construction statistics index, recent tender returns), with **publisher, edition, date, location, and what the rate includes**.
  - If none is available: stop and ask. Offer what to look for. Don't fill the gap.
- Location, building type, specification level, and procurement route (they move rates).
- The budget, and what it includes (construction only, or with fees, VAT/sales tax, contingency, FF&E, land).

## Process

1. **Line up the bases.** Is the budget construction-only or all-in? Is the rate per GIA or GFA? Does it include external works, demolition, preliminaries, contingency, tax? Mismatched inclusions are the main source of false comfort. List the inclusions and exclusions side by side.
2. **Adjust openly**, if the rate is from another year or place:
   - Inflation: rate x (index now / index at rate date), with the index named and both values shown. If no index is available, don't adjust. Report the rate's date instead.
   - Location: a published location factor, named. Otherwise none.
3. **Compute.** Area x adjusted rate, per element or whole building. Show the arithmetic line by line.
4. **Add the allowances the rate excludes**, each as a stated percentage chosen by the architect or consultant, e.g. contingency or design development risk. Ask; don't pick the percentage for them.
5. **Give a range.** Low / likely / high, from the rate source's own range, or ±% agreed with the architect. Early-stage estimates are wide. Say so.
6. **Compare to budget**, on matching inclusions only.

## Domain knowledge

- **Elemental breakdowns** follow a standard such as NRM 1 (UK, RICS), UniFormat (US), or the ICMS (International Construction Measurement Standards) framework. Use the one the cost consultant uses.
- **What moves cost most at concept:** wall-to-floor ratio (envelope area per floor area), storey count and basements, structural spans, envelope specification, and services intensity. Name the driver when two options differ.
- **Rates go stale fast** in volatile markets. A rate more than a year old without an index adjustment should be flagged prominently.
- **Units:** convert ft2 to m2 at 1 ft2 = 0.092903 m2 (exact definition: 1 ft = 0.3048 m). Show the conversion.

## Output format

```
## Cost check: [project / option]

**Area:** [x m2 GIA] ([source, measurement basis])
**Rate source:** [publisher, edition/date, location, inclusions]
**Adjustments:** [inflation: index name, values, factor] · [location: factor, source] · [none]

| Item | Area / qty | Rate (adjusted) | Basis | Cost |
|---|---|---|---|---|

**Allowances (architect / consultant set):** [contingency x%, ...]
**Range:** low [ ] · likely [ ] · high [ ]  ([basis for the range])
**Against budget:** [budget, inclusions] -> [within / over by / under by], [like-for-like / not comparable because ...]
**Main cost driver:** [one line]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't quote a construction rate from memory as fact. A rate needs a source, date, and location, or it doesn't go in the table.
- Don't choose the contingency or risk percentage for the architect. Ask.
- Don't compare to a budget with different inclusions without saying so.
- Don't call this a cost plan or a pre-tender estimate. Recommend a cost consultant for anything the client will rely on.
