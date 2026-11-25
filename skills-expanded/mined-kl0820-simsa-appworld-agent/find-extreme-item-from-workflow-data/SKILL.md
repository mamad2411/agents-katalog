---
name: find-extreme-item-from-workflow-data
description: Identifies an item with an extreme value from a collection provided by a previous workflow step or direct input, then extracts a specific field from that item.
---
## Overview
This skill addresses scenarios where the goal is to select a single item from a dataset based on an extreme value (minimum or maximum) of one of its attributes. It involves retrieving data from a prior execution step or direct input, iterating or filtering to find the item with the extreme value, and then extracting a specific field or a different attribute from the identified item.

## When to Apply
- Instruction asks to find the 'least', 'lowest', 'most', or 'highest' of something.
- The required data is available from a previous milestone's output or as a direct input collection.
- The task involves identifying a single item based on an extreme attribute value (max or min).
- The final output is a specific property or a different attribute of that extreme-valued item.

## Procedure
1. Obtain the collection of structured items from a prior step or direct input.
2. Check if the collection is empty. If it is, handle the empty case (e.g., return a default empty value like null or an empty string) and terminate.
3. Iterate through the collection to identify the item that has the maximum or minimum value for the designated comparison attribute.
4. From the identified item, extract the value of the target output attribute or required output field.
5. Construct the final result using the extracted field.

## Key Patterns
- **Prior Data Dependency:** The operation can rely on data produced by a preceding milestone, eliminating the need for new API calls, or accept direct input.
- **Extreme Value Selection:** Use a min/max function or equivalent logic on the collection, specifying the attribute key for comparison.
- **Attribute Extraction:** Once the target item is identified, access a different attribute or a specific field of that same item to fulfill the output requirement.
- **Empty Collection Guard:** Always include a check for an empty input collection to prevent errors and provide a graceful fallback.

## Common Pitfalls
- Attempting to make new API calls when the necessary data is already available from a prior step.
- Forgetting to handle the case where the input collection is empty, leading to runtime errors.
- Incorrectly specifying the attribute key for comparison when finding the minimum/maximum value.
- Extracting the comparison attribute instead of the required output attribute/field from the identified item.
- Inefficiently iterating through the collection multiple times when a single pass or optimized function could suffice.