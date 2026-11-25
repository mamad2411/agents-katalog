---
name: deepgram-api-specification
description: "Deepgram API Specification API skill. Use when working with Deepgram API Specification for agent, auth, listen. Covers 39 endpoints."
version: 1.0.0
generator: lapsh
---

# Deepgram API Specification
API version: 1.0.0

## Auth
ApiKey Authorization in header | Bearer bearer

## Base URL
https://api.deepgram.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/agent/settings/think/models -- verify access
3. POST /v1/auth/grant -- create first grant

## Endpoints

39 endpoints across 7 groups. See references/api-spec.lap for full details.

### agent
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/agent/settings/think/models | List Agent Think Models |

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/auth/grant | Token-based Authentication |

### listen
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/listen | Transcribe and analyze pre-recorded audio and video |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/models | List Models |
| GET | /v1/models/{model_id} | Get a specific Model |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/projects | List Projects |
| GET | /v1/projects/{project_id} | Get a Project |
| PATCH | /v1/projects/{project_id} | Update a Project |
| DELETE | /v1/projects/{project_id} | Delete a Project |
| GET | /v1/projects/{project_id}/balances | Get Project Balances |
| GET | /v1/projects/{project_id}/balances/{balance_id} | Get a Project Balance |
| GET | /v1/projects/{project_id}/billing/breakdown | Get Project Billing Breakdown |
| GET | /v1/projects/{project_id}/billing/fields | List Project Billing Fields |
| GET | /v1/projects/{project_id}/invites | List Project Invites |
| POST | /v1/projects/{project_id}/invites | Create a Project Invite |
| DELETE | /v1/projects/{project_id}/invites/{email} | Delete a Project Invite |
| GET | /v1/projects/{project_id}/keys | List Project Keys |
| POST | /v1/projects/{project_id}/keys | Create a Project Key |
| GET | /v1/projects/{project_id}/keys/{key_id} | Get a Project Key |
| DELETE | /v1/projects/{project_id}/keys/{key_id} | Delete a Project Key |
| DELETE | /v1/projects/{project_id}/leave | Leave a Project |
| GET | /v1/projects/{project_id}/members | List Project Members |
| DELETE | /v1/projects/{project_id}/members/{member_id} | Delete a Project Member |
| GET | /v1/projects/{project_id}/members/{member_id}/scopes | List Project Member Scopes |
| PUT | /v1/projects/{project_id}/members/{member_id}/scopes | Update Project Member Scopes |
| GET | /v1/projects/{project_id}/models | List Project Models |
| GET | /v1/projects/{project_id}/models/{model_id} | Get a Project Model |
| GET | /v1/projects/{project_id}/purchases | List Project Purchases |
| GET | /v1/projects/{project_id}/requests | List Project Requests |
| GET | /v1/projects/{project_id}/requests/{request_id} | Get a Project Request |
| GET | /v1/projects/{project_id}/self-hosted/distribution/credentials | List Project Self-Hosted Distribution Credentials |
| POST | /v1/projects/{project_id}/self-hosted/distribution/credentials | Create a Project Self-Hosted Distribution Credential |
| GET | /v1/projects/{project_id}/self-hosted/distribution/credentials/{distribution_credentials_id} | Get a Project Self-Hosted Distribution Credential |
| DELETE | /v1/projects/{project_id}/self-hosted/distribution/credentials/{distribution_credentials_id} | Delete a Project Self-Hosted Distribution Credential |
| GET | /v1/projects/{project_id}/usage | Get Project Usage |
| GET | /v1/projects/{project_id}/usage/breakdown | Get Project Usage Breakdown |
| GET | /v1/projects/{project_id}/usage/fields | List Project Usage Fields |

### read
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/read | Analyze text content |

### speak
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/speak | Text to Speech transformation |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all models?" -> GET /v1/agent/settings/think/models
- "Create a grant?" -> POST /v1/auth/grant
- "Create a listen?" -> POST /v1/listen
- "List all models?" -> GET /v1/models
- "Get model details?" -> GET /v1/models/{model_id}
- "List all projects?" -> GET /v1/projects
- "Get project details?" -> GET /v1/projects/{project_id}
- "Partially update a project?" -> PATCH /v1/projects/{project_id}
- "Delete a project?" -> DELETE /v1/projects/{project_id}
- "List all balances?" -> GET /v1/projects/{project_id}/balances
- "Get balance details?" -> GET /v1/projects/{project_id}/balances/{balance_id}
- "List all breakdown?" -> GET /v1/projects/{project_id}/billing/breakdown
- "List all fields?" -> GET /v1/projects/{project_id}/billing/fields
- "List all invites?" -> GET /v1/projects/{project_id}/invites
- "Create a invite?" -> POST /v1/projects/{project_id}/invites
- "Delete a invite?" -> DELETE /v1/projects/{project_id}/invites/{email}
- "List all keys?" -> GET /v1/projects/{project_id}/keys
- "Create a key?" -> POST /v1/projects/{project_id}/keys
- "Get key details?" -> GET /v1/projects/{project_id}/keys/{key_id}
- "Delete a key?" -> DELETE /v1/projects/{project_id}/keys/{key_id}
- "List all members?" -> GET /v1/projects/{project_id}/members
- "Delete a member?" -> DELETE /v1/projects/{project_id}/members/{member_id}
- "List all scopes?" -> GET /v1/projects/{project_id}/members/{member_id}/scopes
- "List all models?" -> GET /v1/projects/{project_id}/models
- "Get model details?" -> GET /v1/projects/{project_id}/models/{model_id}
- "List all purchases?" -> GET /v1/projects/{project_id}/purchases
- "List all requests?" -> GET /v1/projects/{project_id}/requests
- "Get request details?" -> GET /v1/projects/{project_id}/requests/{request_id}
- "List all credentials?" -> GET /v1/projects/{project_id}/self-hosted/distribution/credentials
- "Create a credential?" -> POST /v1/projects/{project_id}/self-hosted/distribution/credentials
- "Get credential details?" -> GET /v1/projects/{project_id}/self-hosted/distribution/credentials/{distribution_credentials_id}
- "Delete a credential?" -> DELETE /v1/projects/{project_id}/self-hosted/distribution/credentials/{distribution_credentials_id}
- "Search usage?" -> GET /v1/projects/{project_id}/usage
- "Search breakdown?" -> GET /v1/projects/{project_id}/usage/breakdown
- "List all fields?" -> GET /v1/projects/{project_id}/usage/fields
- "Create a read?" -> POST /v1/read
- "Create a speak?" -> POST /v1/speak
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
