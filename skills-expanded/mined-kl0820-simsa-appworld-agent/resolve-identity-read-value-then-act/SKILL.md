---
name: resolve-identity-read-value-then-act
description: Resolves a named entity to a system identifier, retrieves a specific parameter value from historical data using filtering, and then performs an action.
---
## Overview
This pattern addresses tasks where an action needs to be performed on a named entity with a specific parameter. It outlines the preparatory steps to correctly identify the target and retrieve the parameter value from historical data before executing the action, ensuring data dependencies are met and the action is performed with the correct context and accurate, context-aware values.

## When to Apply
- An action needs to be performed on a named entity or person.
- A required parameter for the action is not explicitly provided but must be derived from specific historical transactions, records, or system state.
- The named entity needs to be resolved to a canonical or system-specific identifier.
- The main action involves a specific application or service.

## Procedure
1. **Identify the named entity** mentioned in the instruction.
2. **Resolve the named entity to its canonical or system-specific identifier(s)**. This often involves using a general contact management tool to ensure the correct target for subsequent app-specific actions.
3. **Identify the specific parameter value** required for the main action that is not directly provided in the instruction.
4. **Retrieve this specific value from the relevant application's historical data or records**. Apply all necessary filtering criteria (e.g., 'last', 'most recent', 'sent to X', 'received from Y') to precisely identify the correct record, using the resolved identifier if applicable.
5. **Execute the main action** using the resolved target identifier and the retrieved parameter value.

## Key Patterns
- **Identity Resolution First:** Always resolve the named entity to a canonical or system-specific identifier (e.g., contact ID, email, phone number) *before* attempting to use it in subsequent steps or interacting with app-specific tools that require an identifier. This prevents ambiguity and ensures correct targeting.
- **Data Dependency Ordering & Pre-computation:** All necessary parameters and identifiers must be read, derived, and confirmed *before* attempting the final action. Milestones are strictly ordered based on data dependencies, where outputs of earlier steps (resolved identifiers, retrieved values) become inputs for subsequent steps.
- **Filtered Value Extraction:** When a value is needed from a set of records, apply all filtering criteria to precisely identify the correct record before extracting the required value.

## Common Pitfalls
- Attempting to perform an action without a fully resolved target identifier, or using an incorrect/ambiguous identifier.
- Executing the main action without first retrieving the necessary, context-dependent parameter from historical data.
- Using an incorrect parameter value (e.g., not the 'last' one, or from the wrong direction/context).
- Assuming the required value is a default or can be inferred without explicit retrieval.
- Not passing the resolved identifier consistently across all dependent steps.