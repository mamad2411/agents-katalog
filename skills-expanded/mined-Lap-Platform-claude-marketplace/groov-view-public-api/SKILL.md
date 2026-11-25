---
name: groov-view-public-api
description: "groov View Public API skill. Use when working with groov View Public for info, whoami, data-store. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# groov View Public API
API version: R4.2a

## Auth
ApiKey api_key in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /info -- verify access
3. POST /v1/data-store/read -- create first read

## Endpoints

10 endpoints across 4 groups. See references/api-spec.lap for full details.

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Get information about groov View. No authorization required. |

### whoami
| Method | Path | Description |
|--------|------|-------------|
| GET | /whoami | Get information about the user you are authenticated as. Authorized for admins, editors, operators, and kiosk. |

### data-store
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/data-store/devices | List devices available in the data store. Authorized for admins and editors. |
| GET | /v1/data-store/devices/{id}/tags | List tags of the given device. Authorized for admins and editors. |
| GET | /v1/data-store/tags | List all data store tags defined in the project. Authorized for admins and editors. |
| POST | /v1/data-store/read | Read selected tags from the data store. Authorized for admins and editors. |
| GET | /v1/data-store/read/{id} | Read the current value of a single tag. Authorized for admins and editors. |
| POST | /v1/data-store/write/{id} | Writes a new value to the given tag. Authorized for admins and editors. |

### logging
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/logging/groovLogs.txt | Downloads the complete groov View log. Added in groov View R4.2a. |
| GET | /v1/logging/groovLogs.json | Downloads the complete groov View log in JSON format. Added in groov View R4.2a. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all info?" -> GET /info
- "List all whoami?" -> GET /whoami
- "List all devices?" -> GET /v1/data-store/devices
- "List all tags?" -> GET /v1/data-store/devices/{id}/tags
- "List all tags?" -> GET /v1/data-store/tags
- "Create a read?" -> POST /v1/data-store/read
- "Get read details?" -> GET /v1/data-store/read/{id}
- "List all groovLogs.txt?" -> GET /v1/logging/groovLogs.txt
- "List all groovLogs.json?" -> GET /v1/logging/groovLogs.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
