---
name: openrouter-api
description: "OpenRouter API skill. Use when working with OpenRouter for responses, messages, activity. Covers 36 endpoints."
version: 1.0.0
generator: lapsh
---

# OpenRouter API
API version: 1.0.0

## Auth
Bearer bearer | Bearer bearer

## Base URL
https://openrouter.ai/api/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /activity -- verify access
3. POST /responses -- create first responses

## Endpoints

36 endpoints across 14 groups. See references/api-spec.lap for full details.

### responses
| Method | Path | Description |
|--------|------|-------------|
| POST | /responses | Create a response |

### messages
| Method | Path | Description |
|--------|------|-------------|
| POST | /messages | Create a message |

### activity
| Method | Path | Description |
|--------|------|-------------|
| GET | /activity | Get user activity grouped by endpoint |

### chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat/completions | Create a chat completion |

### credits
| Method | Path | Description |
|--------|------|-------------|
| GET | /credits | Get remaining credits |
| POST | /credits/coinbase | Create a Coinbase charge for crypto payment |

### embeddings
| Method | Path | Description |
|--------|------|-------------|
| POST | /embeddings | Submit an embedding request |
| GET | /embeddings/models | List all embeddings models |

### generation
| Method | Path | Description |
|--------|------|-------------|
| GET | /generation | Get request & usage metadata for a generation |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /models/count | Get total count of available models |
| GET | /models | List all models and their properties |
| GET | /models/user | List models filtered by user provider preferences, privacy settings, and guardrails |
| GET | /models/{author}/{slug}/endpoints | List all endpoints for a model |

### endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /endpoints/zdr | Preview the impact of ZDR on the available endpoints |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers | List all providers |

### keys
| Method | Path | Description |
|--------|------|-------------|
| GET | /keys | List API keys |
| POST | /keys | Create a new API key |
| PATCH | /keys/{hash} | Update an API key |
| DELETE | /keys/{hash} | Delete an API key |
| GET | /keys/{hash} | Get a single API key |

### guardrails
| Method | Path | Description |
|--------|------|-------------|
| GET | /guardrails | List guardrails |
| POST | /guardrails | Create a guardrail |
| GET | /guardrails/{id} | Get a guardrail |
| PATCH | /guardrails/{id} | Update a guardrail |
| DELETE | /guardrails/{id} | Delete a guardrail |
| GET | /guardrails/assignments/keys | List all key assignments |
| GET | /guardrails/assignments/members | List all member assignments |
| GET | /guardrails/{id}/assignments/keys | List key assignments for a guardrail |
| POST | /guardrails/{id}/assignments/keys | Bulk assign keys to a guardrail |
| GET | /guardrails/{id}/assignments/members | List member assignments for a guardrail |
| POST | /guardrails/{id}/assignments/members | Bulk assign members to a guardrail |
| POST | /guardrails/{id}/assignments/keys/remove | Bulk unassign keys from a guardrail |
| POST | /guardrails/{id}/assignments/members/remove | Bulk unassign members from a guardrail |

### key
| Method | Path | Description |
|--------|------|-------------|
| GET | /key | Get current API key |

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/keys | Exchange authorization code for API key |
| POST | /auth/keys/code | Create authorization code |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a response?" -> POST /responses
- "Create a message?" -> POST /messages
- "List all activity?" -> GET /activity
- "Create a completion?" -> POST /chat/completions
- "List all credits?" -> GET /credits
- "Create a coinbase?" -> POST /credits/coinbase
- "Create a embedding?" -> POST /embeddings
- "List all models?" -> GET /embeddings/models
- "List all generation?" -> GET /generation
- "List all count?" -> GET /models/count
- "List all models?" -> GET /models
- "List all user?" -> GET /models/user
- "List all endpoints?" -> GET /models/{author}/{slug}/endpoints
- "List all zdr?" -> GET /endpoints/zdr
- "List all providers?" -> GET /providers
- "List all keys?" -> GET /keys
- "Create a key?" -> POST /keys
- "Partially update a key?" -> PATCH /keys/{hash}
- "Delete a key?" -> DELETE /keys/{hash}
- "Get key details?" -> GET /keys/{hash}
- "List all guardrails?" -> GET /guardrails
- "Create a guardrail?" -> POST /guardrails
- "Get guardrail details?" -> GET /guardrails/{id}
- "Partially update a guardrail?" -> PATCH /guardrails/{id}
- "Delete a guardrail?" -> DELETE /guardrails/{id}
- "List all keys?" -> GET /guardrails/assignments/keys
- "List all members?" -> GET /guardrails/assignments/members
- "List all keys?" -> GET /guardrails/{id}/assignments/keys
- "Create a key?" -> POST /guardrails/{id}/assignments/keys
- "List all members?" -> GET /guardrails/{id}/assignments/members
- "Create a member?" -> POST /guardrails/{id}/assignments/members
- "Create a remove?" -> POST /guardrails/{id}/assignments/keys/remove
- "Create a remove?" -> POST /guardrails/{id}/assignments/members/remove
- "List all key?" -> GET /key
- "Create a key?" -> POST /auth/keys
- "Create a code?" -> POST /auth/keys/code
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
