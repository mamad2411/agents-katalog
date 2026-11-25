---
name: qakka
description: "Qakka API skill. Use when working with Qakka for queues, status. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Qakka
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /queues -- verify access
3. POST /queues -- create first queues

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### queues
| Method | Path | Description |
|--------|------|-------------|
| GET | /queues | Get list of all Queues. |
| POST | /queues | Create new queue. |
| DELETE | /queues/{queueName} | Delete Queue. |
| GET | /queues/{queueName}/config | Get Queue config. |
| PUT | /queues/{queueName}/config | Update Queue configuration. |
| GET | /queues/{queueName}/data/{queueMessageId} | Get data associated with a Queue Message. |
| GET | /queues/{queueName}/messages | Get next Queue Messages from a Queue |
| POST | /queues/{queueName}/messages | Send Queue Message with a binary data (blob) payload. |
| DELETE | /queues/{queueName}/messages/{queueMessageId} | Acknowledge that Queue Message has been processed. |

### status
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Status of webapp. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all queues?" -> GET /queues
- "Create a queue?" -> POST /queues
- "Delete a queue?" -> DELETE /queues/{queueName}
- "List all config?" -> GET /queues/{queueName}/config
- "Get data details?" -> GET /queues/{queueName}/data/{queueMessageId}
- "List all messages?" -> GET /queues/{queueName}/messages
- "Create a message?" -> POST /queues/{queueName}/messages
- "Delete a message?" -> DELETE /queues/{queueName}/messages/{queueMessageId}
- "List all status?" -> GET /status

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
