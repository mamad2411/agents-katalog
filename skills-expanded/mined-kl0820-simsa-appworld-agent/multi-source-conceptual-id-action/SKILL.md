---
name: multi-source-conceptual-id-action
description: Applies an action to entities after resolving their conceptual names to actionable IDs, aggregating specific data from multiple sources, applying exclusionary filters, and passing verbatim parameters.
---
## Overview
This pattern addresses tasks where a primary list of targets and associated data needs to be processed, but requires cross-referencing with other data sources for identity resolution, exclusion criteria, and additional parameters before the final action can be performed.
## When to Apply
- Perform an action on a list of items.
- The items are initially identified by conceptual names.
- The action requires specific contact details or IDs for the items.
- Some items might need to be excluded based on a condition checked in another system.
- The action requires multiple pieces of data for each item, sourced from different places.
## Procedure
1. Identify and resolve the actionable identifiers (e.g., email, ID) for all potential targets from a contact source, based on their conceptual names.
2. Extract the primary data (e.g., amounts, details) for each target from its initial source, applying any initial filtering criteria (e.g., time, category).
3. Query a secondary source to identify any targets that should be excluded from the final action, based on specific conditions (e.g., already completed, specific status).
4. Combine the resolved identifiers, primary data, and exclusion list to perform the final action on the remaining, eligible targets, incorporating any verbatim parameters.
## Key Patterns
- **Identity Resolution Lookup:** Conceptual names from a primary data source must be explicitly resolved to actionable identifiers (e.g., email addresses, API-specific IDs) via a separate lookup against a contact or identity management system before any external action can be taken.
- **Exclusionary Filter:** Before performing the main action, query a separate system or data source to identify and exclude targets that have already met a specific condition or should otherwise not be acted upon.
- **Multi-Source Data Aggregation:** The final action requires combining specific pieces of information (e.g., target identifier, associated value, descriptive text) that originate from distinct data sources.
- **Verbatim Parameter Pass-through:** A specific, fixed string or value provided in the instruction must be passed directly and without modification as a parameter to the final action.
- **Temporal Constraint Application:** Apply time-based filters (e.g., 'since yesterday', 'last week') to data retrieval steps from relevant sources to narrow down the scope of information processed.
## Common Pitfalls
- Attempting to perform an action without first resolving conceptual names to the required actionable identifiers.
- Failing to check for and exclude targets that have already satisfied the task's implicit or explicit conditions.
- Not gathering all necessary data points from their respective sources before attempting the final action.
- Hardcoding or incorrectly interpreting parameters that are meant to be passed verbatim.
- Ignoring or misapplying temporal constraints when retrieving data, leading to incorrect or incomplete datasets.
