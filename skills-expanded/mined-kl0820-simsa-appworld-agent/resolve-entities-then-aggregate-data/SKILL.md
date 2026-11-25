---
name: resolve-entities-then-aggregate-data
description: Aggregates data from a target system for a group of entities whose concrete identifiers must first be resolved from an auxiliary system, often involving cross-system identifier mapping and iterative data collection.
---
## Overview
Many tasks involve calculating a sum or count based on transactions or records for a group of entities. Often, the target entities for these calculations are initially described abstractly (e.g., 'roommates', 'colleagues', 'family') and require a preliminary step to resolve their concrete identifiers from a separate, auxiliary system (e.g., 'contacts', 'directory'). This skill addresses the pattern of translating these abstract definitions into concrete, usable identifiers, then using those identifiers to filter and aggregate data from a transactional or target system. This ensures that the primary data operation uses valid and specific references, bridging information across multiple systems.

## When to Apply
- Aggregating a quantity (e.g., 'how much', 'how many') based on a group of related entities.
- The entities in the group are initially described abstractly or are not directly identifiable in the target system where the aggregation occurs.
- Requires resolving abstract relationships or characteristics into concrete, usable identifiers (e.g., names, phone numbers, user IDs, email addresses) from an auxiliary or primary data source.
- The task involves combining information from multiple systems where one system provides the 'who' (entity definition) and another provides the 'what' (data for aggregation).
- A date, time, direction, or other specific filter constraint is specified for the data retrieval or aggregation.

## Procedure
1.  **Identify Abstract Group/Criteria:** Pinpoint the abstract group of entities or the defining characteristics/relationships mentioned in the instruction.
2.  **Resolve Concrete Identifiers:** Determine the system or source of truth where these abstract entities can be resolved. Translate the abstract definitions into concrete, usable identifiers for each entity. This often involves querying an auxiliary system to map abstract relationships (e.g., "coworkers") to specific identifiers (e.g., email addresses, user IDs) suitable for the target system.
3.  **Retrieve Data with Filters:** Identify the transactional or target system where the data to be aggregated resides. Iterate through the resolved concrete identifiers. For each identifier, query the target system to retrieve relevant data. Apply any specified filters (e.g., date ranges, transaction types, status, directional constraints like 'outgoing' or 'received') during this retrieval phase to ensure accuracy and efficiency.
4.  **Aggregate Data:** Combine the retrieved data across all entities according to the task's requirements (e.g., sum, count, average, list).
5.  **Return Result:** Provide the final aggregated result.

## Key Patterns
-   **Entity Resolution Pre-computation:** The complete set of entities to be processed is determined and resolved into concrete identifiers in a distinct, preceding step before any data collection or processing begins on those entities.
-   **Cross-System Identifier Mapping:** An identifier or characteristic from one system (e.g., a relationship type) is used to derive or map to an identifier suitable for querying or interacting with a different system (e.g., an email address or API key).
-   **Data Dependency Chaining/Sequencing:** The output of an initial identification and resolution step (a list of concrete identifiers) becomes the essential input for a subsequent data retrieval and aggregation step.
-   **Iterative Data Collection and Aggregation:** Data collection and subsequent aggregation often occur in a loop, processing each resolved entity individually or in batches, before combining the results into a final aggregate.
-   **Filter-then-Aggregate:** Apply all necessary filtering conditions (e.g., temporal, directional, identity-based, transaction types) *before* performing the final aggregation to ensure accuracy and efficiency.

## Common Pitfalls
-   **Premature Data Collection/Querying:** Attempting to query the transactional system directly or collect data before the full set of target entities has been unambiguously identified and resolved.
-   **Incorrect Identifier Mapping/Incomplete Resolution:** Failing to correctly map identifiers between different systems, incorrectly identifying the source of truth for entity resolution, or not resolving all necessary identifying information (e.g., only getting names when emails are needed, or missing a required system ID).
-   **Ignoring Data Dependency:** Failing to recognize and properly manage the data dependency between identity resolution and the target system query.
-   **Premature Aggregation/Filtering:** Applying aggregation logic or filters prematurely, before all relevant data has been collected, or not applying all specified filters (e.g., date range, direction) at all, leading to incorrect results.
-   **Missing Data Handling:** Not accounting for potential absence of data in the secondary system for some identified entities, which could lead to errors or incomplete aggregates.