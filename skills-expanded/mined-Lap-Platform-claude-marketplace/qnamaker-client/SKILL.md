---
name: qnamaker-client
description: "QnAMaker Client API skill. Use when working with QnAMaker Client for endpointSettings, endpointkeys, alterations. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# QnAMaker Client
API version: 4.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /endpointSettings -- verify access
3. POST /knowledgebases/{kbId} -- create first knowledgebases

## Endpoints

15 endpoints across 5 groups. See references/api-spec.lap for full details.

### endpointSettings
| Method | Path | Description |
|--------|------|-------------|
| GET | /endpointSettings | Gets endpoint settings for an endpoint. |
| PATCH | /endpointSettings | Updates endpoint settings for an endpoint. |

### endpointkeys
| Method | Path | Description |
|--------|------|-------------|
| GET | /endpointkeys | Gets endpoint keys for an endpoint |
| PATCH | /endpointkeys/{keyType} | Re-generates an endpoint key. |

### alterations
| Method | Path | Description |
|--------|------|-------------|
| GET | /alterations | Download alterations from runtime. |
| PUT | /alterations | Replace alterations data. |

### knowledgebases
| Method | Path | Description |
|--------|------|-------------|
| GET | /knowledgebases | Gets all knowledgebases for a user. |
| GET | /knowledgebases/{kbId} | Gets details of a specific knowledgebase. |
| DELETE | /knowledgebases/{kbId} | Deletes the knowledgebase and all its data. |
| POST | /knowledgebases/{kbId} | Publishes all changes in test index of a knowledgebase to its prod index. |
| PUT | /knowledgebases/{kbId} | Replace knowledgebase contents. |
| PATCH | /knowledgebases/{kbId} | Asynchronous operation to modify a knowledgebase. |
| POST | /knowledgebases/create | Asynchronous operation to create a new knowledgebase. |
| GET | /knowledgebases/{kbId}/{environment}/qna | Download the knowledgebase. |

### operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /operations/{operationId} | Gets details of a specific long running operation. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all endpointSettings?" -> GET /endpointSettings
- "List all endpointkeys?" -> GET /endpointkeys
- "Partially update a endpointkey?" -> PATCH /endpointkeys/{keyType}
- "List all alterations?" -> GET /alterations
- "List all knowledgebases?" -> GET /knowledgebases
- "Get operation details?" -> GET /operations/{operationId}
- "Get knowledgebase details?" -> GET /knowledgebases/{kbId}
- "Delete a knowledgebase?" -> DELETE /knowledgebases/{kbId}
- "Update a knowledgebase?" -> PUT /knowledgebases/{kbId}
- "Partially update a knowledgebase?" -> PATCH /knowledgebases/{kbId}
- "Create a create?" -> POST /knowledgebases/create
- "List all qna?" -> GET /knowledgebases/{kbId}/{environment}/qna
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
