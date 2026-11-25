---
name: respond-to-request-with-filtered-data
description: When a request is received via a communication channel, requiring a response with filtered data from a separate source.
---
## Overview
This skill addresses tasks where an agent receives a request from a specific contact through a communication medium. It involves identifying the contact, extracting the specific criteria from their message, querying an external data source based on these criteria, and then formatting and sending the results back to the original contact via the same communication channel.
## When to Apply
- An instruction to respond to a specific contact.
- A request received via a communication channel (e.g., message, email).
- The response requires data from an external application or source.
- The data needs to be filtered or selected based on the content of the request.
- A specific output format for the response is specified.
## Procedure
1. Resolve the identifier for the requesting entity.
2. Read the incoming communication from the requesting entity to extract the specific request or filtering criteria.
3. Retrieve relevant data from the designated data source, applying the extracted criteria.
4. Format the retrieved data as specified.
5. Send the formatted data as a response to the requesting entity via the original communication channel.
## Key Patterns
- **Identity Resolution First:** Always resolve the target entity's identifier before attempting any communication or interaction with them.
- **Request-Driven Filtering:** Extract specific constraints or keywords from the incoming request before querying the data source.
- **Data Dependency Ordering:** Ensure that steps that produce necessary inputs (like an identifier or filtering criteria) are completed before steps that consume them.
- **Separate Read and Act:** Reading information (contact, message, data) is distinct from acting on it (sending a reply).
## Common Pitfalls
- Attempting to interact with a named entity without first resolving their unique identifier.
- Querying the data source before fully understanding the specific filtering criteria from the request.
- Failing to format the output according to the specified requirements before sending the response.
- Not using the correct communication channel or recipient for the reply.
