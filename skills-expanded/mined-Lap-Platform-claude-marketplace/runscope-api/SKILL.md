---
name: runscope-api
description: "Runscope API skill. Use when working with Runscope for account, teams, buckets. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# Runscope API
API version: 1.0.0

## Auth
OAuth2

## Base URL
https://api.runscope.com/

## Setup
1. Configure auth: OAuth2
2. GET /account -- verify access
3. POST /buckets -- create first buckets

## Endpoints

29 endpoints across 3 groups. See references/api-spec.lap for full details.

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Account Resource |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/{teamId}/people | Teams Resource |
| GET | /teams/{teamId}/integrations | Team integrations list |
| GET | /teams/{teamId}/agents | Team agents list |

### buckets
| Method | Path | Description |
|--------|------|-------------|
| GET | /buckets | Returns a list of buckets. |
| POST | /buckets | Create a new bucket |
| GET | /buckets/{bucketKey} | Returns a single bucket resource. |
| DELETE | /buckets/{bucketKey} | Delete a single bucket resource. |
| GET | /buckets/{bucketKey}/messages | Retrieve a list of messages in a bucket |
| DELETE | /buckets/{bucketKey}/messages | Clear a bucket (remove all messages). |
| POST | /buckets/{bucketKey}/messages | Create a message |
| GET | /buckets/{bucketKey}/errors | Retrieve a list of error messages in a bucket |
| GET | /buckets/{bucketKey}/messages/{messageId} | Retrieve the details for a single message. |
| GET | /buckets/{bucketKey}/tests | Returns a list of tests. |
| POST | /buckets/{bucketKey}/tests | Create a test. |
| GET | /buckets/{bucketKey}/tests/{testId} | Retrieve the details of a given test by ID. |
| PUT | /buckets/{bucketKey}/tests/{testId} | Modify a test's name, description, default environment and its steps. To modify other individual properties of a test, make requests to the steps, environments, and schedules subresources of the test. |
| DELETE | /buckets/{bucketKey}/tests/{testId} | Delete a test, including all steps, schedules, test-specific environments and results. |
| GET | /buckets/{bucketKey}/tests/{testId}/steps | List test steps for a test. |
| POST | /buckets/{bucketKey}/tests/{testId}/steps | Add new test step. |
| PUT | /buckets/{bucketKey}/tests/{testId}/steps/{stepId} | Update the details of a single test step. |
| DELETE | /buckets/{bucketKey}/tests/{testId}/steps/{stepId} | Delete a step from a test. |
| GET | /buckets/{bucketKey}/tests/{testId}/environments | Return details of the test's environments (only those that belong to the specified test) |
| POST | /buckets/{bucketKey}/tests/{testId}/environments | Create new test environment. |
| PUT | /buckets/{bucketKey}/tests/{testId}/environments/{environmentId} | Update the details of a test environment. |
| GET | /buckets/{bucketKey}/tests/{testId}/metrics | Return details of the test metrics for the specified timeframe. |
| GET | /buckets/{bucketKey}/environments | Returns list of shared environments for a specified bucket. |
| POST | /buckets/{bucketKey}/environments | Create new shared environment. |
| PUT | /buckets/{bucketKey}/environments/{environmentId} | Update the details of a shared environment. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all account?" -> GET /account
- "List all people?" -> GET /teams/{teamId}/people
- "List all integrations?" -> GET /teams/{teamId}/integrations
- "List all agents?" -> GET /teams/{teamId}/agents
- "List all buckets?" -> GET /buckets
- "Create a bucket?" -> POST /buckets
- "Get bucket details?" -> GET /buckets/{bucketKey}
- "Delete a bucket?" -> DELETE /buckets/{bucketKey}
- "List all messages?" -> GET /buckets/{bucketKey}/messages
- "Create a message?" -> POST /buckets/{bucketKey}/messages
- "List all errors?" -> GET /buckets/{bucketKey}/errors
- "Get message details?" -> GET /buckets/{bucketKey}/messages/{messageId}
- "List all tests?" -> GET /buckets/{bucketKey}/tests
- "Create a test?" -> POST /buckets/{bucketKey}/tests
- "Get test details?" -> GET /buckets/{bucketKey}/tests/{testId}
- "Update a test?" -> PUT /buckets/{bucketKey}/tests/{testId}
- "Delete a test?" -> DELETE /buckets/{bucketKey}/tests/{testId}
- "List all steps?" -> GET /buckets/{bucketKey}/tests/{testId}/steps
- "Create a step?" -> POST /buckets/{bucketKey}/tests/{testId}/steps
- "Update a step?" -> PUT /buckets/{bucketKey}/tests/{testId}/steps/{stepId}
- "Delete a step?" -> DELETE /buckets/{bucketKey}/tests/{testId}/steps/{stepId}
- "List all environments?" -> GET /buckets/{bucketKey}/tests/{testId}/environments
- "Create a environment?" -> POST /buckets/{bucketKey}/tests/{testId}/environments
- "Update a environment?" -> PUT /buckets/{bucketKey}/tests/{testId}/environments/{environmentId}
- "List all metrics?" -> GET /buckets/{bucketKey}/tests/{testId}/metrics
- "List all environments?" -> GET /buckets/{bucketKey}/environments
- "Create a environment?" -> POST /buckets/{bucketKey}/environments
- "Update a environment?" -> PUT /buckets/{bucketKey}/environments/{environmentId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
