---
name: find-extremum-item-and-extract-attribute
description: Identifies an item within a collection based on an extremum condition (min/max value of one of its attributes), and then extracts a different specific attribute from that identified item.
---
## Overview
This pattern addresses tasks where the primary goal is to retrieve a specific piece of information (an attribute) from an item that is identified by an extremum condition (e.g., highest, lowest, most recent) on one of its attributes within a defined collection. The collection itself might be explicitly given or derived from a primary entity.

## When to Apply
- The instruction asks for an attribute of 'the most X' or 'the least Y' of items within a specified collection or related to a primary entity.
- The task involves finding a specific value from a collection based on a comparative criterion.
- The task requires identifying a unique item from a set based on a maximum or minimum value of one of its properties.
- Examples: "Find the [minimum/maximum] [attribute] of a [type of entity].", "Which [entity] has the [highest/lowest] [metric]?", "What is the [property] of the [most/least] [adjective] [entity]?", "What is the name of the employee with the highest salary in department X?".

## Procedure
1. **Identify the target collection of entities.** This collection might be explicitly given, or derived by querying for items associated with an initial entity.
2. For each entity in the collection, identify and read the attribute whose extreme value is sought for comparison.
3. Determine the single entity that possesses the extreme (minimum or maximum) value for that attribute among all candidates.
4. From the identified extremum entity, extract the final requested output attribute.

## Key Patterns
- **Extremum Selection:** A single item is selected from a collection based on a comparative (maximum or minimum) value of one of its properties.
- **Dependent Attribute Retrieval:** The final output is a specific attribute of the item identified by the extremum condition, not the extremum value itself.
- **Collection Derivation (Optional):** The target collection may be a subset of a larger dataset, filtered or associated with a primary entity.

## Common Pitfalls
- Not correctly identifying the scope of the target collection or failing to retrieve all relevant items before attempting to find the extremum.
- Incorrectly identifying the attribute to compare for the extremum condition.
- Returning the extreme value itself instead of the requested *different* attribute of the entity that holds that value.
- Not handling cases where the collection is empty, no related items are found, or the comparison attribute is missing for some entities.