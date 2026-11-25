---
name: multi-step-transaction-action
description: This skill applies when a task requires identifying a contact, finding a related financial transaction, and then performing a subsequent financial action based on that transaction.
---
## Overview
This structural pattern addresses tasks that involve chaining information from multiple sources (e.g., contacts, financial records) to perform a specific action. It requires careful identification of the target contact, filtering and selecting the correct transaction, and then using that extracted information to execute a new transaction.
## When to Apply
- Tasks involving finding a specific contact's details.
- Tasks requiring retrieval and filtering of financial transactions.
- Tasks that involve performing a financial action (e.g., sending money, refunding) based on previously identified transactions.
- Tasks that explicitly mention 'returning' or 'sending back' money related to a prior payment.
## Procedure
1. Acquire Target Contact Identifier: Search for a contact using a provided query. Accumulate all results, handling pagination. From the accumulated results, identify the precise target contact using a specific field (e.g., first name, case-insensitive match). If an exact match is not found, apply a fallback heuristic (e.g., select the first plausible match). Extract a unique identifier (e.g., email address) for this contact to be used in subsequent steps.
2. Acquire Service Authentication Token: Obtain an authentication token for the financial service. This involves a comprehensive strategy: first, check for a pre-existing token (e.g., environment variable or sandbox-provided); if not found, attempt to retrieve credentials from a secure source (e.g., supervisor API) and perform a login using various available identifiers (e.g., email, username) until a token is successfully acquired.
3. Retrieve and Filter Related Transactions: Using the acquired service authentication token and the target contact identifier, fetch all relevant transactions from the financial service. Ensure all pages of results are retrieved and accumulated. Filter these transactions based on specified criteria (e.g., status, direction).
4. Select Specific Transaction: From the filtered list of transactions, identify and select the single most relevant transaction based on a specific ordering criterion (e.g., the latest by creation timestamp). If no matching transaction is found, report this condition.
5. Extract Transaction Details: From the selected transaction, extract all necessary details required for the subsequent action, such as the transaction amount, the receiver's identifier, and any relevant transaction IDs.
6. Perform Financial Action: Using the extracted transaction details and the service authentication token, execute the required financial action (e.g., create a new payment or refund). Include any specified descriptive notes or messages.
7. Confirm Action Outcome: Capture any confirmation details (e.g., new transaction ID) from the financial action and confirm its successful execution.
## Key Patterns
- **Robust Authentication Token Acquisition:** When an API requires an authentication token, implement a multi-tiered acquisition strategy: first check for pre-existing tokens (e.g., environment variables), then attempt to retrieve credentials from a secure source (e.g., supervisor API) and perform login using various available identifiers (e.g., email, username) until a token is successfully acquired.
- **Paginated Data Accumulation:** When an API returns paginated results, iterate through all pages, incrementing the page index until an empty list or specific termination condition is met, accumulating all results into a single collection for subsequent processing.
- **Multi-Stage Data Filtering and Selection:** After initial data retrieval, apply successive filtering steps based on different criteria (e.g., exact string match, status, relationship) to narrow down to the precise target. When multiple matches remain, apply a deterministic selection rule (e.g., latest by timestamp, first in list) to choose a single item.
- **Cross-Step Identifier Chaining:** Extract critical identifiers (e.g., email, ID) from the output of one step to serve as precise input parameters for subsequent API calls or filtering operations in later steps, ensuring data consistency and accuracy across the procedural flow.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval.
- Not implementing a robust authentication strategy, causing API calls to fail due to missing tokens.
- Using a generic search result directly without further filtering to precisely identify the target, leading to incorrect data association.
- Not providing a fallback mechanism when an exact match for a contact or transaction is not found, causing the process to halt prematurely.
- Hardcoding values instead of extracting them dynamically from prior steps or API responses.
- Ignoring the specific description or note requirements for financial transactions.
