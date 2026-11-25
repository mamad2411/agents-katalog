---
name: select-and-act-on-collection-item
description: When an action needs to be performed on one item from a collection, where the selection criteria require detailed information not available in the initial collection listing.
---
## Overview
This skill addresses scenarios where an action must be taken on a single item chosen from a larger collection. The selection process involves first retrieving the entire collection, then enriching each item with detailed data, applying specific criteria (potentially with fallbacks) to identify the best match, and finally executing the desired action using the selected item's identifier.
## When to Apply
- An action needs to be performed on a single item from a collection.
- The initial API for listing items does not provide sufficient detail for selection.
- Selection criteria involve comparing a derived metric of an item against a target value.
- A fallback selection strategy is required if no item perfectly matches the primary criteria.
## Procedure
1. Obtain any necessary target values or criteria from prior steps.
2. Retrieve the full collection of items, handling pagination if the listing API supports it.
3. For each item in the collection, fetch its detailed information using a separate API call, as the initial listing lacks necessary data.
4. From the detailed information of each item, calculate or extract the specific metric required for selection.
5. Apply the primary selection criteria to find a suitable item from the enriched collection.
6. If no item meets the primary criteria, apply a fallback selection strategy to choose the best available item.
7. Perform the final action using the identifier of the selected item.
## Key Patterns
- **Paginated Collection Retrieval:** When an API returns a list of items in pages, a loop is required to fetch all available pages and accumulate the complete collection.
- **Item Enrichment Loop:** If a collection listing API provides only summary information, iterate through each item to make a separate API call to retrieve its full details, which are necessary for selection.
- **Derived Metric Calculation:** Often, the selection criteria depend on a metric that is not directly provided but must be calculated by aggregating or processing sub-components of an item's detailed information.
- **Conditional Selection with Fallback:** Prioritize selecting an item that perfectly matches the primary criteria. If no such item exists, implement a secondary, 'best-effort' selection logic (e.g., choosing the largest, closest, or default item).
- **Unit Normalization:** Ensure all values used for comparison are in consistent units (e.g., converting minutes to seconds) to avoid incorrect evaluations.
## Common Pitfalls
- Not handling pagination, leading to an incomplete collection and potentially missing the optimal item.
- Failing to fetch detailed information for each item when the summary data is insufficient for the selection criteria.
- Incorrectly calculating derived metrics from detailed item information.
- Not implementing a robust fallback selection strategy, which can lead to no item being selected when the primary criteria are not met.
- Ignoring unit conversions, resulting in incorrect comparisons and suboptimal item selection.
