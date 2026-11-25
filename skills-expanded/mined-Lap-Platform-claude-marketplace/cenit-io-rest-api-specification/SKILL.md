---
name: cenit-io-rest-api-specification
description: "Cenit IO - REST API Specification API skill. Use when working with Cenit IO - REST API Specification for setup. Covers 40 endpoints."
version: 1.0.0
generator: lapsh
---

# Cenit IO - REST API Specification
API version: v1

## Auth
ApiKey X-User-Access-Key in header | ApiKey X-User-Access-Token in header

## Base URL
https://cenit.io/api/v1

## Setup
1. Set your API key in the appropriate header
2. GET /setup/connection -- verify access
3. POST /setup/connection -- create first connection

## Endpoints

40 endpoints across 1 groups. See references/api-spec.lap for full details.

### setup
| Method | Path | Description |
|--------|------|-------------|
| GET | /setup/connection/{id} | Retrieve an existing connection |
| DELETE | /setup/connection/{id} | Delete a connection |
| GET | /setup/connection | Returns a list of connections |
| POST | /setup/connection | Create or update a connection |
| GET | /setup/connection_role/{id} | Return a connection role |
| DELETE | /setup/connection_role/{id} | Delete a connection role. |
| GET | /setup/connection_role | Returns a list of connection roles |
| POST | /setup/connection_role | Create or update a connection role |
| GET | /setup/data_type/ | Returns a list of data types |
| POST | /setup/data_type/ | Create or update a data type |
| GET | /setup/data_type/{id} | Retrieve a data type |
| DELETE | /setup/data_type/{id} | Delete a data type |
| GET | /setup/observer/ | Returns a list of events |
| POST | /setup/observer/ | Create or update an event |
| GET | /setup/observer/{id} | Retrieve an existing event |
| DELETE | /setup/observer/{id} | Delete an event |
| GET | /setup/scheduler/ | Returns a list of schedulers |
| POST | /setup/scheduler/ | Create or update an scheduler |
| GET | /setup/scheduler/{id} | Retrieve an existing schedule |
| DELETE | /setup/scheduler/{id} | Delete an schedule |
| GET | /setup/flow/ | Returns a list of flows |
| POST | /setup/flow/ | Create or update a flow |
| GET | /setup/flow/{id} | Retrieve an existing flow |
| DELETE | /setup/flow/{id} | Delete a flow. |
| GET | /setup/schema/ | Returns a list of schemas |
| POST | /setup/schema/ | Create or update an schema |
| GET | /setup/schema/{id} | Retrieve an existing schema |
| DELETE | /setup/schema/{id} | Delete an schema. |
| GET | /setup/translator/ | Returns a list of translators |
| POST | /setup/translator/ | Create or update a translator |
| GET | /setup/translator/{id} | Retrieve an existing translator |
| DELETE | /setup/translator/{id} | Delete a translator |
| GET | /setup/webhook/ | Returns a list of webhooks |
| POST | /setup/webhook/ | Create or update a webhook |
| GET | /setup/webhook/{id} | Retrieve an existing webhook |
| DELETE | /setup/webhook/{id} | Delete a webhook |
| GET | /setup/namespace/ | Returns a list of namespaces |
| POST | /setup/namespace/ | Create or update a namespace |
| GET | /setup/namespace/{id} | Retrieve an existing namespace |
| DELETE | /setup/namespace/{id} | Delete a namespace |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get connection details?" -> GET /setup/connection/{id}
- "Delete a connection?" -> DELETE /setup/connection/{id}
- "List all connection?" -> GET /setup/connection
- "Create a connection?" -> POST /setup/connection
- "Get connection_role details?" -> GET /setup/connection_role/{id}
- "Delete a connection_role?" -> DELETE /setup/connection_role/{id}
- "List all connection_role?" -> GET /setup/connection_role
- "Create a connection_role?" -> POST /setup/connection_role
- "List all data_type?" -> GET /setup/data_type/
- "Create a data_type?" -> POST /setup/data_type/
- "Get data_type details?" -> GET /setup/data_type/{id}
- "Delete a data_type?" -> DELETE /setup/data_type/{id}
- "List all observer?" -> GET /setup/observer/
- "Create a observer?" -> POST /setup/observer/
- "Get observer details?" -> GET /setup/observer/{id}
- "Delete a observer?" -> DELETE /setup/observer/{id}
- "List all scheduler?" -> GET /setup/scheduler/
- "Create a scheduler?" -> POST /setup/scheduler/
- "Get scheduler details?" -> GET /setup/scheduler/{id}
- "Delete a scheduler?" -> DELETE /setup/scheduler/{id}
- "List all flow?" -> GET /setup/flow/
- "Create a flow?" -> POST /setup/flow/
- "Get flow details?" -> GET /setup/flow/{id}
- "Delete a flow?" -> DELETE /setup/flow/{id}
- "List all schema?" -> GET /setup/schema/
- "Create a schema?" -> POST /setup/schema/
- "Get schema details?" -> GET /setup/schema/{id}
- "Delete a schema?" -> DELETE /setup/schema/{id}
- "List all translator?" -> GET /setup/translator/
- "Create a translator?" -> POST /setup/translator/
- "Get translator details?" -> GET /setup/translator/{id}
- "Delete a translator?" -> DELETE /setup/translator/{id}
- "List all webhook?" -> GET /setup/webhook/
- "Create a webhook?" -> POST /setup/webhook/
- "Get webhook details?" -> GET /setup/webhook/{id}
- "Delete a webhook?" -> DELETE /setup/webhook/{id}
- "List all namespace?" -> GET /setup/namespace/
- "Create a namespace?" -> POST /setup/namespace/
- "Get namespace details?" -> GET /setup/namespace/{id}
- "Delete a namespace?" -> DELETE /setup/namespace/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
