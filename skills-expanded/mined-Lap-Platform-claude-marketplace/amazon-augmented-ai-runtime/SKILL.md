---
name: amazon-augmented-ai-runtime
description: "Amazon Augmented AI Runtime API skill. Use when working with Amazon Augmented AI Runtime for human-loops. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Augmented AI Runtime
API version: 2019-11-07

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /human-loops -- verify access
3. POST /human-loops -- create first human-loops

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### human-loops
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /human-loops/{HumanLoopName} | Deletes the specified human loop for a flow definition. If the human loop was deleted, this operation will return a ResourceNotFoundException. |
| GET | /human-loops/{HumanLoopName} | Returns information about the specified human loop. If the human loop was deleted, this operation will return a ResourceNotFoundException error. |
| GET | /human-loops | Returns information about human loops, given the specified parameters. If a human loop was deleted, it will not be included. |
| POST | /human-loops | Starts a human loop, provided that at least one activation condition is met. |
| POST | /human-loops/stop | Stops the specified human loop. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a human-loop?" -> DELETE /human-loops/{HumanLoopName}
- "Get human-loop details?" -> GET /human-loops/{HumanLoopName}
- "List all human-loops?" -> GET /human-loops
- "Create a human-loop?" -> POST /human-loops
- "Create a stop?" -> POST /human-loops/stop
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
