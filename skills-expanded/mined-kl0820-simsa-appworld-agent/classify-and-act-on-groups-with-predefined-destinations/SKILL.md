---
name: classify-and-act-on-groups-with-predefined-destinations
description: Categorize items based on attributes, then act on them into distinct, pre-created destinations, including handling for default or unclassified items.
---
## Overview
This skill addresses tasks requiring items to be grouped by specific criteria, then moved or processed into distinct, pre-defined target locations. It ensures that all classification logic is resolved upfront, all necessary destination structures are prepared, and provides for handling items that don't fit explicit categories.

## When to Apply
- Instructions involve categorizing multiple items based on their attributes.
- The categorized items need to be moved or processed into distinct, named destinations.
- The destinations themselves need to be created or ensured to exist before items are moved.
- A 'catch-all' or default destination is specified for items not matching explicit criteria.

## Procedure
1.  **Read and Classify Items:** Retrieve all relevant items from the source, extracting the attributes necessary for classification. Store this as a structured collection (e.g., list of dictionaries) where each entry represents an item and includes its unique identifier, its relevant attributes for classification, and its determined classification category/destination. Identify necessary attributes by consulting API documentation for item listing and metadata retrieval, then apply the task's classification rules to assign a category. If an attribute's value (e.g., a date) requires interpretation relative to the current time or other dynamic context, ensure this context is established or retrieved before classification.
2.  **Identify and Prepare Destinations:** Based on the determined classification categories from the previous step, identify all unique target destination names. This includes any explicitly defined categories and the designated default target location for unclassified items. Create or ensure the existence of each identified target destination. This involves extracting unique category names, mapping them to specific destination names as per task rules, and then using appropriate API calls to create these destinations if they do not already exist.
3.  **Act on Classified Items:** For each item in the structured collection from the first step, use its unique identifier and its determined target destination to perform the required action (e.g., move, copy, update) into that destination, preserving original item properties as specified. This step iterates through the pre-classified items and leverages the pre-created destinations. Any items not matching explicit criteria should be moved to the designated default target location.

## Key Patterns
-   **Pre-classification:** All items are classified based on their attributes in a preliminary step, generating an intermediate data structure that maps each item to its intended category/destination, before any actions are performed.
-   **Destination Pre-creation:** All target destinations (including default ones) are created or verified to exist as a distinct step before any items are moved or processed into them, ensuring atomicity and preventing 'destination not found' errors during the main action phase.
-   **Iterative Action on Classified Groups:** The final action involves iterating through the pre-classified items and performing the specified operation (e.g., move, copy) for each item into its designated, pre-created target, leveraging the results of the classification step.
-   **Default Category Handling:** Explicitly plan for a final 'catch-all' action to handle items that do not fit into any specific, predefined categories, ensuring comprehensive processing.
-   **Contextual Attribute Interpretation:** If an attribute's value requires interpretation relative to the current time or other dynamic context, ensure this context is established or retrieved before classification.

## Common Pitfalls
-   Attempting to create destinations on-the-fly for each item, leading to redundant operations or race conditions.
-   Performing actions on items before their classification is fully determined, resulting in incorrect assignments.
-   Not ensuring all required attributes for classification are read in the initial step.
-   Failing to create all necessary target destinations before attempting to move items into them.
-   Overlooking a 'default' or 'catch-all' category, leaving some items unprocessed.
-   Not considering external context (e.g., current date) when interpreting relative classification criteria.