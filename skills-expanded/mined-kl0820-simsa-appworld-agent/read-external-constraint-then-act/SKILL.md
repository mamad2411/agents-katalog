---
name: read-external-constraint-then-act
description: Performs an action in one application, using a constraint value that must first be retrieved from a separate, external source, potentially involving selection from a collection.
---
## Overview
This pattern applies when a task involves performing an action in one application, but the criteria or constraint for that action's parameters must first be determined by reading information from a different application or system. The initial step focuses solely on extracting the necessary constraint value, which then informs the subsequent action, potentially involving the selection of specific items from a collection.

## When to Apply
- An action in one application is conditional on a value from another application or system.
- A selection criterion for an item or items needs to be determined from an external data source.
- The instruction specifies a constraint whose value is not immediately available and must be looked up.
- The primary action involves interacting with specific items selected from a collection based on a condition.
- The selection requires comparing a computed property of potential target items against the retrieved constraint.

## Procedure
1. **Retrieve the Constraint Value:** Identify the constraint or criterion required for the primary action and its source (another application, system, or document). Create a milestone to read and extract this specific value.
2. **Identify Potential Targets (if selection is involved):** If the action requires selecting items from a collection, identify all potential target items within the target application.
3. **Compute Target Properties (if selection is involved):** For each potential target item, compute the property relevant to the constraint that will be used for comparison. This may involve iterating through sub-components or attributes.
4. **Filter or Select Targets (if selection is involved):** Filter or select the target item(s) that satisfy the retrieved constraint, based on their computed properties.
5. **Perform Primary Action:** Create a subsequent milestone to perform the primary action in its target application, using the extracted constraint value to filter, select, or parameterize the action on the identified or selected target item(s).

## Key Patterns
- **Constraint Value Pre-computation:** A value that acts as a constraint or filter for a subsequent action is always retrieved and established in a dedicated preceding step, even if it means interacting with a different application or system.
- **Cross-Application/System Data Dependency:** Information required for an action in one application is sourced from a distinct, separate application or system, necessitating an explicit read step in the source before the action in the target.
- **Candidate Metric Computation:** For each potential target item (when selection is involved), a specific metric or property is computed to allow comparison against the constraint.
- **Separation of Read and Act:** Reading/gathering information (constraint, candidates, metrics) is separated into distinct milestones from the final action milestone.

## Common Pitfalls
- Attempting to perform the action or selection without first fully establishing the constraint value.
- Embedding the constraint value retrieval or candidate evaluation within the final action step, leading to complex or unmanageable single milestones.
- Not computing the necessary metrics for candidate items before attempting comparison (when selection is involved).
- Failing to retrieve all potential candidates before selection (when selection is involved).
- Ignoring the explicit instruction to use an external source for a constraint, and instead guessing or using a default.