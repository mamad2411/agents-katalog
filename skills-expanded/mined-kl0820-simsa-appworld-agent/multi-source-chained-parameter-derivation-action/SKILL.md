---
name: multi-source-chained-parameter-derivation-action
description: Sequentially retrieves and processes data from multiple sources to derive a list of entities, each with its own specific action parameters, then performs an iterative action for each entity using its uniquely derived parameters.
---
## Overview
This pattern addresses tasks where the final action or output depends on data that is not immediately available from a single source. It involves a sequence of data retrieval, processing, and aggregation steps, where the output of one step serves as input for the next, culminating in a final, often iterative, action.
## When to Apply
- Instruction implies combining information from multiple distinct sources (e.g., 'read X from Y' then 'read A from B' then 'do C with X and A').
- A final action needs to be performed iteratively for each item in a list, where both the list and the parameters for the action are derived from previous steps.
- A calculation or transformation requires input values obtained from different prior data retrieval or processing steps.
- The task involves a clear sequence of data acquisition, transformation, and then a final interaction with a service.
## Procedure
1. Retrieve primary data from the first required source.
2. Extract or process key information from the primary data.
3. Retrieve secondary data from another source, potentially using information extracted in the previous step.
4. Process or filter the secondary data to obtain a relevant collection of entities.
5. Combine the extracted key information and the processed secondary data to calculate any necessary derived values.
6. Iterate over the collection of entities obtained from the secondary data, performing the final action for each entity using the derived values and other relevant information.
## Key Patterns
- **Data Dependency Chain:** The output of an earlier data retrieval or processing step directly informs the parameters or scope of subsequent steps, creating a sequential dependency chain where each milestone builds upon the previous one.
- **Iterative Action on Derived List:** A common final step involves iterating over a collection of entities (e.g., contacts, items) retrieved in an earlier stage, performing a uniform action for each, parameterized by a value calculated from aggregated data.
- **Variable Preservation Across Milestones:** Intermediate results and processed data from earlier milestones are explicitly stored and retrieved using a mechanism like `prior_variable_values` to ensure continuity and avoid redundant API calls or re-computation in later steps.
- **Multi-source Data Aggregation:** The task requires synthesizing information from distinct API categories or data sources (e.g., file system, contacts, payment services) to form a complete set of inputs for the final operation.
- **Implicit 'Self' Inclusion in Calculations:** When a task specifies sharing or splitting among a group, explicitly account for the user (the agent's principal) as one of the participants in the calculation, even if not explicitly listed in retrieved data.
- **Robust Data Extraction/Parsing:** When extracting specific values from unstructured text (e.g., file content), employ robust parsing techniques like regular expressions with appropriate flags (e.g., `re.IGNORECASE`) to handle variations in formatting and ensure accurate data capture.
- **Pagination Handling:** For APIs that support pagination, implement a loop to fetch all available pages until an empty or partial page is returned, ensuring complete data retrieval.
## Common Pitfalls
- Forgetting to include the user (the agent's principal) in calculations when the task implies a group share or split.
- Failing to handle pagination for APIs that return results in chunks, leading to incomplete data retrieval.
- Not correctly passing intermediate results or processed data from one milestone to the next, requiring re-computation or re-retrieval.
- Hardcoding values that should be dynamically derived from prior steps or API responses.
- Assuming a single API call will provide all necessary data, overlooking the need for multiple distinct data sources.
- Incomplete or brittle parsing of unstructured text (e.g., file content), leading to failure if the format varies slightly.
- Not validating the structure of API responses (e.g., checking if a response is an error dictionary or an expected list) before attempting to access specific keys or iterate.
