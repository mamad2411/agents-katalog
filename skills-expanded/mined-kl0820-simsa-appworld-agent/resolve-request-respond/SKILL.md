---
name: resolve-request-respond
description: This skill applies when a task requires responding to an incoming request by first resolving the sender's identity, then understanding the request's content, and finally generating a data-driven response.
---
## Overview
Many tasks involve responding to an external request. This pattern addresses the common challenge of accurately identifying the requestor, fully comprehending their specific needs or constraints, and then synthesizing information from various sources to formulate an appropriate and channel-specific reply.
## When to Apply
- Responding to an external communication.
- Generating a response based on specific criteria from an incoming message.
- An implicit or explicit incoming request from a named entity.
- Retrieving information from a specific data source to fulfill a request.
## Procedure
1. Resolve the identity of the requestor to a concrete communication address or identifier.
2. Read the full content of the incoming request using the resolved identity to understand specific criteria or constraints.
3. Retrieve and process relevant data from the specified source(s) based on the criteria identified in the request.
4. Format the processed data according to the requirements of the response channel.
5. Send the formatted response to the requestor using their resolved communication address or identifier.
## Key Patterns
- **Identity Resolution First:** Before any communication action (reading or sending), resolve any named or abstract identity to a concrete, actionable address or identifier for the communication channel. This ensures subsequent steps operate on a valid target.
- **Request-Driven Data Filtering:** The content of an incoming request often contains implicit or explicit criteria that must be applied when retrieving or processing data from a separate source. The request must be fully parsed *before* data retrieval.
- **Read-Before-Act:** All necessary information gathering (identity resolution, request parsing, data retrieval) should be completed and stored as intermediate results *before* initiating the final action (e.g., sending a response). This minimizes errors and allows for comprehensive processing.
## Common Pitfalls
- Attempting to communicate with a named entity without first resolving their concrete address or identifier for the specific communication channel.
- Generating a response without fully parsing the incoming request for specific constraints or filtering criteria.
- Sending a response before all necessary data has been retrieved and processed according to the request.
- Failing to format the response appropriately for the target communication channel.
