---
name: find-extreme-item-with-attribute-normalization
description: Finds an item with an extreme value in a collection, specifically handling and normalizing the comparison attribute's data type for accurate evaluation before extracting a result field.
---
## Overview
This skill addresses the common need to find a single item from a list based on an extreme value of one of its properties. It involves iterating through a collection, potentially transforming the comparison attribute for consistent evaluation, and then selecting the item that holds the minimum or maximum value for that attribute. The skill also handles cases where the input collection might be empty.
## When to Apply
- When the task requires identifying a single item from a collection based on the minimum or maximum value of one of its attributes.
- When the comparison attribute might need type conversion or parsing before comparison.
- When the final output is a specific field from the identified extreme item.
## Procedure
1. Receive a collection of structured items as input.
2. Check if the input collection is empty; if so, return a predefined null or empty result.
3. For each item in the collection, identify the attribute to be used for comparison.
4. If necessary, transform or parse the comparison attribute into a consistent, comparable data type (e.g., string to datetime, string to number).
5. Iterate through the collection to find the item that possesses the extreme (minimum or maximum) value for the designated comparison attribute.
6. From the identified extreme item, extract the specific attribute required as the final output.
7. Return the extracted attribute value.
## Key Patterns
- **Extreme Value Selection:** To find an item with an extreme value (min/max) in a collection, iterate through the items, apply a consistent comparison logic to a designated attribute, and keep track of the item that currently holds the extreme value.
- **Attribute Normalization for Comparison:** Before comparing attributes across items, ensure they are all in a consistent, comparable data type. This often involves parsing strings into native types (e.g., dates, numbers) or handling mixed types gracefully.
- **Handling Empty Collections:** Always check if the input collection is empty at the beginning of the process to prevent errors and provide a graceful, expected null or empty result.
## Common Pitfalls
- Not handling empty input collections, leading to errors.
- Comparing attributes of inconsistent data types (e.g., comparing date strings directly without parsing, leading to lexicographical comparison instead of chronological).
- Incorrectly identifying the comparison attribute or the desired output attribute.
- Assuming the comparison attribute is always present or valid for every item without error handling.
