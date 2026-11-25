---
name: resolve-recipients-calculate-and-distribute
description: When a task requires distributing a calculated amount among a set of identified recipients, and the source amount and recipients need to be retrieved from different systems.
---
## Overview
This pattern addresses tasks where a primary action involves distributing a value. It prioritizes resolving all necessary inputs: identifying the target recipients and their required identifiers, and extracting the source value from its location. A calculation step then derives the distributed amount per recipient, followed by the final action.
## When to Apply
- Distribute a value among multiple entities.
- Identify recipients from a contact list or directory.
- Extract a numerical value from a document or record.
- Perform a calculation based on multiple retrieved values.
- Execute an action for each identified recipient.
## Procedure
1. Identify the target entities and their required identifiers from a contact source.
2. Locate and extract the primary numerical value from its source document/system, applying any necessary filtering criteria.
3. Calculate the individual share or distributed amount based on the primary numerical value and the count of identified entities (plus any additional participants).
4. For each identified entity, perform the specified action using their identifier and the calculated individual share, along with any required static parameters.
## Key Patterns
- **Recipient Resolution First:** Identifiers for target entities must be resolved and retrieved before any actions can be performed on those entities. This ensures the action has valid targets.
- **Source Value Extraction:** The primary numerical value to be distributed must be extracted from its specific source, often requiring filtering or selection criteria, before it can be used in calculations.
- **Pre-computation of Distributed Value:** All values required for a calculation (source amount, number of participants) must be retrieved before the calculation itself. The calculation is a distinct step that produces a derived value.
- **Iterative Action on Resolved Targets:** The final action is performed iteratively for each resolved target, using the pre-calculated individual amount and their specific identifier.
## Common Pitfalls
- Attempting to perform an action on recipients before their identifiers are fully resolved.
- Trying to calculate the distributed amount before all necessary input values (total amount, number of participants) are available.
- Failing to correctly identify or filter the source document for the primary numerical value.
- Incorrectly counting participants for the distribution calculation.
- Not separating the data retrieval steps from the calculation and action steps, leading to data dependencies issues.
