---
name: pricing-analyze
description: Use when calculating or explaining pricing and margin performance, recurring metrics or pricing scenarios.
---

# Pricing analysis

**Before step 1, read the [shared rules](../references/shared-rules.md).**

## 1. Frame the question

- Establish the decision the analysis supports.
- Establish the population, metric and comparison. Handle each requested comparison separately.

## 2. Verify before calculating

- Apply [metric verification](../knowledge/metric-verification.md) before any financial calculation.
- Confirm which field represents each measure.
- Run the data-consistency and eligibility checks on the actual data.
- **Required checks before any line-level calculation.** Run each as a query. Report each one's line count and value, even when it is zero:
  - **Missing values:** lines with no usable price or cost after matching, such as a blank, unmatched or other-currency record. SQL aggregates skip blanks, so a sum or average over them counts that revenue with no cost. Before calculating a measure, define its population once as a view that keeps only the lines where every value the measure needs is present (for example `WHERE unit_cost IS NOT NULL`). Calculate the measure, both parts of a rate included, from that view only. Calculate the left-out lines' count and value from the remaining lines and show them next to the figure (shared rules, section 6).
  - **Implausible values:** lines whose unit price or unit cost is at least five times, or at most a fifth of, the median for the same item in the data you are using.
  - **Unconfirmed definitions:** each choice the result depends on that `.pricing/context.md` does not confirm and the user has not settled, such as which of several price fields is the price, or whether returns count. Calculate the result under each candidate, whatever the column names suggest, and report both.
- If any of these moves the result, it is an unresolved basis (shared rules, section 3): ask the user about it.
- End each requested measure in one of three states:
  - a verified result on an established basis
  - a result delivered on a stated basis with its range and one confirming question, because every candidate treatment gives the same conclusion
  - a held result with side-by-side scenarios and one targeted question, because some candidate treatment changes the conclusion (shared rules, section 3)
- Bound the effect of every unresolved choice and unusable record before holding anything ([metric verification](../knowledge/metric-verification.md), "Bound before holding").

## 3. Calculate

- Compute reported amounts, rates and movements with calculation tools.
- Cross-check totals and displayed values against the actual rating or adjustment mapping.
- Use quantity × unit price or quantity × unit cost only where that mapping is linear and supported.
- Derive movements from unrounded figures. Round only for display.

## 4. Explain

- **Margin movement:** verify both period rates first. Then use [margin drivers](../knowledge/margin-drivers.md) for a reconciled bridge. Keep new and lost items, residuals and unproven commercial causes separate.
- **Results for a group:** before putting a result down to the whole group, look for a cohort inside it that differs. Check how the result moves with when customers or items started, at the finest grain the data supports, and with segment. Where it shifts, find when the shift starts and what else changed then, such as price, offer, channel or spend. Report each cohort that differs, with its size.
- **Comparing periods within a year:** compare with the same period a year earlier, so seasonality is not read as change.
- **Historical price change:** use [price realization](../knowledge/methods/price-realization.md).
- **Proposed price change:** use [price-change economics](../knowledge/methods/price-change-economics.md).
- **Differences between comparable customers or items:** use [peer comparisons](../knowledge/methods/peer-comparisons.md).
- **Price levels and leakage from list to pocket:** use [price waterfall](../knowledge/price-waterfall.md).
- **Retail, channel or order economics:** use [retail economics](../knowledge/retail-economics.md).
- **Recurring revenue, cohort or lifecycle measures:** use [recurring metrics](../knowledge/recurring-metrics.md).
- **Rating recurring or usage schedules:** use [recurring scenarios](../knowledge/methods/recurring-scenarios.md).
- **Experiment or promotion effects:** use [experiments and promotions](../knowledge/methods/experiments-and-promotions.md).
- **Anything else:** pick the card from the [knowledge index](../knowledge/index.md).

## 5. Report

- Show margins as percentages and margin movements in percentage points or basis points.
- Follow the output rules in the shared rules, section 5.
