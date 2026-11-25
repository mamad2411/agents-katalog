---
name: identify-and-process-specific-record
description: This skill applies when the task requires identifying a specific record from a list based on criteria and then performing an action using its details.
---
## Overview
This pattern addresses tasks that involve locating a particular entity or record within a collection, often requiring filtering, sorting, and potentially pagination. Once the target record is identified, its specific attributes are extracted and used as input for a subsequent action or to fulfill the milestone's output requirement.
## When to Apply
- Find X for Y
- Identify the Z that matches A
- Retrieve the most recent B
- Perform action C using details from D
## Procedure
1. Identify the initial search/list API and the criteria for finding the target record.
2. Call the search/list API, applying any initial filters provided by the API.
3. Implement a pagination loop to ensure all relevant records are retrieved and accumulated.
4. Filter the accumulated records based on specific criteria (e.g., exact string match, status).
5. If multiple records match, apply a sorting rule (e.g., by timestamp for 'most recent') and select the single desired record.
6. Extract specific attributes from the selected record that are needed for subsequent steps or the milestone's output.
7. Handle cases where no matching record is found, typically by setting the result to null or an empty structure.
8. If a subsequent action is required, use the extracted attributes from the selected record as parameters for another API call.
9. Capture the result of the action or the extracted attributes as the milestone's output.
## Key Patterns
- **Pagination Loop:** When an API returns a paginated list, iterate through pages until an empty list or a list smaller than the page limit is returned, accumulating all results.
- **Data Chaining:** Information (e.g., an identifier or specific attribute) extracted from a record in an earlier milestone is used as input for an API call in a subsequent milestone.
- **Filtering and Selection:** After retrieving a list of records, apply programmatic filters (e.g., attribute comparison) to narrow down to the specific target record, and then select it.
- **Most Recent Selection:** To find the 'last' or 'most recent' item, parse relevant timestamp fields (e.g., 'created_at') into comparable date/time objects and select the record with the maximum value.
- **Case-Insensitive Matching:** When comparing string attributes (e.g., names, emails), convert both values to a consistent case (e.g., lowercase) to ensure robust matching.
- **Read-Milestone Empty Handling:** For milestones that retrieve data, explicitly check if no matching record was found and set the output variable to null or an empty structure, allowing downstream milestones to gracefully handle the absence of data.
## Common Pitfalls
- Failing to implement pagination, leading to incomplete search results and potentially missing the target record.
- Incorrectly filtering or selecting the wrong record due to imprecise matching criteria or improper sorting.
- Not handling the 'no record found' scenario, which can cause errors in subsequent steps that expect data.
- Failing to correctly pass and retrieve necessary data (identifiers, attributes) from one milestone's output to the next.
- Ignoring case sensitivity when comparing string fields, leading to missed matches.
- Not accumulating results from paginated API calls, only processing the last page.
