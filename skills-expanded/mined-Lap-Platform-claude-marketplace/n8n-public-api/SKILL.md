---
name: n8n-public-api
description: "n8n Public API skill. Use when working with n8n Public for audit, credentials, executions. Covers 59 endpoints."
version: 1.0.0
generator: lapsh
---

# n8n Public API
API version: 1.1.1

## Auth
ApiKey X-N8N-API-KEY in header

## Base URL
/api/v1

## Setup
1. Set your API key in the appropriate header
2. GET /credentials -- verify access
3. POST /audit -- create first audit

## Endpoints

59 endpoints across 10 groups. See references/api-spec.lap for full details.

### audit
| Method | Path | Description |
|--------|------|-------------|
| POST | /audit | Generate an audit |

### credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /credentials | List credentials |
| POST | /credentials | Create a credential |
| PATCH | /credentials/{id} | Update credential by ID |
| DELETE | /credentials/{id} | Delete credential by ID |
| GET | /credentials/schema/{credentialTypeName} | Show credential data schema |
| PUT | /credentials/{id}/transfer | Transfer a credential to another project. |

### executions
| Method | Path | Description |
|--------|------|-------------|
| GET | /executions | Retrieve all executions |
| GET | /executions/{id} | Retrieve an execution |
| DELETE | /executions/{id} | Delete an execution |
| POST | /executions/{id}/retry | Retry an execution |
| POST | /executions/{id}/stop | Stop an execution |
| POST | /executions/stop | Stop multiple executions |
| GET | /executions/{id}/tags | Get execution tags |
| PUT | /executions/{id}/tags | Update tags of an execution |

### tags
| Method | Path | Description |
|--------|------|-------------|
| POST | /tags | Create a tag |
| GET | /tags | Retrieve all tags |
| GET | /tags/{id} | Retrieves a tag |
| DELETE | /tags/{id} | Delete a tag |
| PUT | /tags/{id} | Update a tag |

### workflows
| Method | Path | Description |
|--------|------|-------------|
| POST | /workflows | Create a workflow |
| GET | /workflows | Retrieve all workflows |
| GET | /workflows/{id} | Retrieve a workflow |
| DELETE | /workflows/{id} | Delete a workflow |
| PUT | /workflows/{id} | Update a workflow |
| GET | /workflows/{id}/{versionId} | Retrieves a specific version of a workflow |
| POST | /workflows/{id}/activate | Publish a workflow |
| POST | /workflows/{id}/deactivate | Deactivate a workflow |
| PUT | /workflows/{id}/transfer | Transfer a workflow to another project |
| GET | /workflows/{id}/tags | Get workflow tags |
| PUT | /workflows/{id}/tags | Update tags of a workflow |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Retrieve all users |
| POST | /users | Create multiple users |
| GET | /users/{id} | Get user by ID/Email |
| DELETE | /users/{id} | Delete a user |
| PATCH | /users/{id}/role | Change a user's global role |

### source-control
| Method | Path | Description |
|--------|------|-------------|
| POST | /source-control/pull | Pull changes from the remote repository |

### variables
| Method | Path | Description |
|--------|------|-------------|
| POST | /variables | Create a variable |
| GET | /variables | Retrieve variables |
| DELETE | /variables/{id} | Delete a variable |
| PUT | /variables/{id} | Update a variable |

### data-tables
| Method | Path | Description |
|--------|------|-------------|
| GET | /data-tables | List all data tables |
| POST | /data-tables | Create a new data table |
| GET | /data-tables/{dataTableId} | Get a data table |
| PATCH | /data-tables/{dataTableId} | Update a data table |
| DELETE | /data-tables/{dataTableId} | Delete a data table |
| GET | /data-tables/{dataTableId}/rows | Retrieve rows from a data table |
| POST | /data-tables/{dataTableId}/rows | Insert rows into a data table |
| PATCH | /data-tables/{dataTableId}/rows/update | Update rows in a data table |
| POST | /data-tables/{dataTableId}/rows/upsert | Upsert a row in a data table |
| DELETE | /data-tables/{dataTableId}/rows/delete | Delete rows from a data table |

### projects
| Method | Path | Description |
|--------|------|-------------|
| POST | /projects | Create a project |
| GET | /projects | Retrieve projects |
| DELETE | /projects/{projectId} | Delete a project |
| PUT | /projects/{projectId} | Update a project |
| GET | /projects/{projectId}/users | List project members |
| POST | /projects/{projectId}/users | Add one or more users to a project |
| DELETE | /projects/{projectId}/users/{userId} | Delete a user from a project |
| PATCH | /projects/{projectId}/users/{userId} | Change a user's role in a project |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a audit?" -> POST /audit
- "List all credentials?" -> GET /credentials
- "Create a credential?" -> POST /credentials
- "Partially update a credential?" -> PATCH /credentials/{id}
- "Delete a credential?" -> DELETE /credentials/{id}
- "Get schema details?" -> GET /credentials/schema/{credentialTypeName}
- "List all executions?" -> GET /executions
- "Get execution details?" -> GET /executions/{id}
- "Delete a execution?" -> DELETE /executions/{id}
- "Create a retry?" -> POST /executions/{id}/retry
- "Create a stop?" -> POST /executions/{id}/stop
- "Create a stop?" -> POST /executions/stop
- "List all tags?" -> GET /executions/{id}/tags
- "Create a tag?" -> POST /tags
- "List all tags?" -> GET /tags
- "Get tag details?" -> GET /tags/{id}
- "Delete a tag?" -> DELETE /tags/{id}
- "Update a tag?" -> PUT /tags/{id}
- "Create a workflow?" -> POST /workflows
- "List all workflows?" -> GET /workflows
- "Get workflow details?" -> GET /workflows/{id}
- "Delete a workflow?" -> DELETE /workflows/{id}
- "Update a workflow?" -> PUT /workflows/{id}
- "Get workflow details?" -> GET /workflows/{id}/{versionId}
- "Create a activate?" -> POST /workflows/{id}/activate
- "Create a deactivate?" -> POST /workflows/{id}/deactivate
- "List all tags?" -> GET /workflows/{id}/tags
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "Get user details?" -> GET /users/{id}
- "Delete a user?" -> DELETE /users/{id}
- "Create a pull?" -> POST /source-control/pull
- "Create a variable?" -> POST /variables
- "List all variables?" -> GET /variables
- "Delete a variable?" -> DELETE /variables/{id}
- "Update a variable?" -> PUT /variables/{id}
- "List all data-tables?" -> GET /data-tables
- "Create a data-table?" -> POST /data-tables
- "Get data-table details?" -> GET /data-tables/{dataTableId}
- "Partially update a data-table?" -> PATCH /data-tables/{dataTableId}
- "Delete a data-table?" -> DELETE /data-tables/{dataTableId}
- "Search rows?" -> GET /data-tables/{dataTableId}/rows
- "Create a row?" -> POST /data-tables/{dataTableId}/rows
- "Create a upsert?" -> POST /data-tables/{dataTableId}/rows/upsert
- "Create a project?" -> POST /projects
- "List all projects?" -> GET /projects
- "Delete a project?" -> DELETE /projects/{projectId}
- "Update a project?" -> PUT /projects/{projectId}
- "List all users?" -> GET /projects/{projectId}/users
- "Create a user?" -> POST /projects/{projectId}/users
- "Delete a user?" -> DELETE /projects/{projectId}/users/{userId}
- "Partially update a user?" -> PATCH /projects/{projectId}/users/{userId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
