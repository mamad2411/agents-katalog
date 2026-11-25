---
name: process-prior-data-find-min-and-transform
description: This skill applies when the goal is to process data obtained from a previous step, specifically to find a minimum value based on a key, and then apply a transformation to that value.
---
## Overview
This pattern addresses scenarios where the current milestone's primary function is to perform calculations or aggregations on data already prepared by a preceding milestone, without requiring new API calls. It involves identifying an extreme value (e.g., minimum or maximum) within a collection and then applying a series of transformations to that value to produce the final result.
## When to Apply
- Compute a value based on previously fetched data.
- Identify the smallest/largest item based on a specific attribute.
- Perform arithmetic operations (e.g., conversion, rounding) on a derived value.
- No new API calls are required for this milestone.
## Procedure
1. Read the structured data passed from the prior milestone.
2. Identify the item within the data collection that has the minimum (or maximum) value for a specified attribute.
3. Extract the relevant attribute's value from the identified item.
4. Apply the required arithmetic transformations (e.g., division, multiplication, rounding) to this extracted value.
5. Return the final transformed scalar value.
## Key Patterns
- **Prior Data Consumption:** The milestone exclusively uses data from a previous step, indicating a processing-only stage where no new external API calls are needed.
- **Min/Max Aggregation:** Finding the minimum or maximum value of a specific field across a collection of items is a common aggregation pattern.
- **Scalar Transformation:** Applying a sequence of mathematical operations (e.g., division, rounding) to a single numerical value to derive the final answer.
## Common Pitfalls
- Forgetting to handle cases where the input data from the prior milestone might be empty, leading to errors during aggregation.
- Incorrectly applying rounding or conversion rules (e.g., using integer division instead of float division, or choosing the wrong rounding method).
- Attempting to make new API calls when all necessary data is already available from a preceding milestone, leading to redundant operations.
