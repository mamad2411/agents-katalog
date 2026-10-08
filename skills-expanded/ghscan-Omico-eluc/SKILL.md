---
name: money-review
description: Review cart pricing changes against the project's discount and integer-cent rules.
---

# Money review

Read [pricing rules](references/pricing.md) before assessing changes to cart totals. Compare the implementation with these rules, including values immediately below, at and above the discount boundary.

For each confirmed violation of these rules, prefix the finding title with `[金额规则]`. Include the triggering subtotal, expected total and actual total in the body. Use the run's normal finding locations and coverage format. If no violation is established, report no finding.
